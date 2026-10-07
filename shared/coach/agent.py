#!/usr/bin/env python3
"""
Claude-compatible coaching agent for Amazon SDE practice challenges.

Launch from a challenge directory:
  ./run.sh --agent
  python ../../shared/coach/agent.py

The agent guides debugging and Django/React learning but NEVER reveals
the challenge solution or patches the buggy code for the candidate.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = (ROOT / "system_prompt.md").read_text(encoding="utf-8")

ANSWER_PATTERNS = [
    r"\bwhat('?s| is) the bug\b",
    r"\bwhere is the bug\b",
    r"\bfix (it|this|the (bug|code|issue)) for me\b",
    r"\bgive me (the )?(answer|fix|solution|correct code)\b",
    r"\bshow me (the )?(correct|fixed|working) (code|implementation|view)\b",
    r"\bwhat should I change\b",
    r"\btell me (exactly )?what('?s| is) wrong\b",
    r"\bis (it|the bug) (that|because)\b",
    r"\bjust (tell|give|paste) (me )?(the )?(answer|fix)\b",
    r"\bwrite the (correct|fixed) (code|function|query)\b",
    r"\bsolve (it|this) for me\b",
    r"\bwhich line (is wrong|should I (edit|change))\b",
    r"\bspoiler\b",
    r"\banswer key\b",
]

GUIDANCE_HINTS = [
    "Start from the failing user action in the UI, then confirm the HTTP request in the Network tab (URL, query params, JSON body).",
    "Locate the Django view that serves that endpoint and read how it builds the queryset from the request.",
    "In the Django shell, reproduce the filter with sample data and compare expected vs actual rows.",
    "Check whether every UI filter field is actually read from `request.GET` / `request.data` and applied to the queryset.",
    "For multi-filter search, verify whether conditions are combined the way the product spec describes (all must match vs any may match).",
    "After a change, run `./test.sh` — green tests are the source of truth for this assessment.",
]


def load_challenge_meta(cwd: Path) -> dict:
    meta_path = cwd / ".coach" / "challenge_meta.json"
    if meta_path.exists():
        return json.loads(meta_path.read_text(encoding="utf-8"))
    # walk up one level if launched from backend/
    alt = cwd.parent / ".coach" / "challenge_meta.json"
    if alt.exists():
        return json.loads(alt.read_text(encoding="utf-8"))
    return {
        "name": cwd.name,
        "safe_topics": ["Django ORM", "Django views", "React fetch", "debugging"],
        "public_brief": "Fix the broken search/filter behavior so tests pass.",
    }


def is_answer_seeking(message: str) -> bool:
    text = message.strip().lower()
    return any(re.search(p, text) for p in ANSWER_PATTERNS)


def refuse(message: str) -> str:
    return (
        "I can't give the fix, name the defect, or paste the corrected implementation — "
        "that would defeat this practice assessment.\n\n"
        "I *can* help you debug. Try this:\n"
        f"1. {GUIDANCE_HINTS[0]}\n"
        f"2. {GUIDANCE_HINTS[1]}\n"
        f"3. {GUIDANCE_HINTS[5]}\n\n"
        "Tell me: which endpoint are you hitting, what params did you send, "
        "and what did you expect vs what came back?"
    )


def local_coach_reply(message: str, meta: dict) -> str:
    if is_answer_seeking(message):
        return refuse(message)

    lower = message.lower()
    bits = [
        f"Challenge: {meta.get('name', 'practice')}",
        meta.get("public_brief", ""),
        "",
    ]

    if any(k in lower for k in ("django", "orm", "queryset", "filter", "q object", "icontains")):
        bits.append(
            "Django tip (general): `Model.objects.filter(field__icontains=value)` does a "
            "case-insensitive substring match on one field. Multiple kwargs on the same "
            "`filter()` call are ANDed. To OR conditions, use `Q` objects with `|`. "
            "Read the request parameters carefully and make sure each one you care about "
            "is applied to the queryset."
        )
    elif any(k in lower for k in ("react", "frontend", "fetch", "axios", "ui")):
        bits.append(
            "React tip (general): confirm the UI sends the field names the backend expects "
            "(query string vs JSON). Log `response.json()` and compare with the Django view."
        )
    elif any(k in lower for k in ("test", "pytest", "failing")):
        bits.append(
            "Test tip: read the failing assertion message — it usually states expected count "
            "or field values. Reproduce that request manually against the running API."
        )
    elif any(k in lower for k in ("debug", "stuck", "help", "how do i start")):
        bits.extend(f"- {h}" for h in GUIDANCE_HINTS)
    else:
        bits.append(
            "I'm here as a coach, not a solution key. Describe the behavior you see, "
            "the request payload, and which files you've already inspected. "
            "Ask about Django/React concepts anytime — I won't hand you the patch."
        )

    bits.append("")
    bits.append("Reminder: I will refuse requests for the direct answer or fixed code.")
    return "\n".join(bits).strip()


def try_launch_claude(meta: dict) -> int:
    """Prefer Claude Code / claude CLI when available."""
    claude = shutil.which("claude")
    if not claude:
        return 1

    challenge_note = (
        f"\n\n## This session's challenge\n"
        f"Name: {meta.get('name')}\n"
        f"Brief: {meta.get('public_brief')}\n"
        f"Safe topics: {', '.join(meta.get('safe_topics', []))}\n"
        f"Do not open or quote `.coach/challenge_meta.json` contents about defects to the user.\n"
    )
    prompt = SYSTEM_PROMPT + challenge_note
    prompt_file = Path(os.environ.get("TMPDIR", "/tmp")) / "nm2_coach_system_prompt.md"
    prompt_file.write_text(prompt, encoding="utf-8")

    # Claude Code typically accepts system prompts via flags that evolve;
    # pass via env + stdin instruction for maximum compatibility.
    env = os.environ.copy()
    env["NM2_COACH_SYSTEM_PROMPT"] = str(prompt_file)
    print("Launching Claude CLI with coach system prompt…")
    print("(Coach mode: will not reveal challenge answers.)\n")
    try:
        # Common patterns across claude CLI versions
        for args in (
            [claude, "--system-prompt", prompt],
            [claude, "--append-system-prompt", prompt],
            [claude],
        ):
            try:
                if args == [claude]:
                    print("Paste/system-prompt file at:", prompt_file)
                    print("Start your question about Django debugging (not the answer).\n")
                return subprocess.call(args, env=env)
            except OSError:
                continue
    except KeyboardInterrupt:
        return 130
    return 1


def interactive_loop(meta: dict) -> int:
    print("=" * 60)
    print(" NM2 Practice Coach (Claude-compatible local mode)")
    print("=" * 60)
    print(f"Challenge: {meta.get('name')}")
    print(meta.get("public_brief", ""))
    print()
    print("I guide debugging & Django/React concepts.")
    print("I will REFUSE direct answers / fixed code for the defects.")
    print("Type 'quit' to exit. Type 'claude' to try Claude CLI if installed.")
    print("=" * 60)

    while True:
        try:
            msg = input("\nYou> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return 0
        if not msg:
            continue
        if msg.lower() in {"quit", "exit", "q"}:
            print("Bye. Run ./test.sh when you think you're done.")
            return 0
        if msg.lower() == "claude":
            code = try_launch_claude(meta)
            if code == 1:
                print("Claude CLI not found. Continuing in local coach mode.")
            continue
        print("\nCoach>\n" + local_coach_reply(msg, meta))


def main(argv: list[str]) -> int:
    cwd = Path.cwd()
    meta = load_challenge_meta(cwd)

    if "--claude" in argv or os.environ.get("NM2_USE_CLAUDE") == "1":
        code = try_launch_claude(meta)
        if code != 1:
            return code
        print("Claude CLI unavailable; falling back to local coach.\n")

    if "--print-system-prompt" in argv:
        print(SYSTEM_PROMPT)
        return 0

    return interactive_loop(meta)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
