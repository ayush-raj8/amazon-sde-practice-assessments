# Django Tutorial — Campus Club Desk

**Goal:** understand how one HTTP request becomes a JSON response in Django.

This is a learning scaffold, not an assessment. There are **no tests**. One Django **project**, two **apps**, a couple of endpoints.

---

## Project map

```
backend/
  manage.py              ← process entry (sets DJANGO_SETTINGS_MODULE)
  config/                ← the Django *project*
    settings.py          ← INSTALLED_APPS, ROOT_URLCONF, DATABASES
    urls.py              ← root urlpatterns (includes each app)
  clubs/                 ← App 1
    urls.py → views.py   ← club list endpoint
  events/                ← App 2
    urls.py → views.py   ← event list endpoint
```

| Piece | What it is |
|-------|------------|
| **Project** (`config`) | Shared settings + root URL router |
| **App** (`clubs`, `events`) | Feature slice: models + urls + views |

---

## Request → response cycle

Follow this for every call. Example: **`GET /api/clubs/`**

```
Browser / curl
    │  GET http://127.0.0.1:8005/api/clubs/
    ▼
manage.py
    │  loads config.settings  (DJANGO_SETTINGS_MODULE)
    ▼
config/settings.py
    │  ROOT_URLCONF = "config.urls"
    │  INSTALLED_APPS includes "clubs", "events"
    ▼
config/urls.py
    │  path("api/", include("clubs.urls"))
    │  strips the "api/" prefix → remaining path: "clubs/"
    ▼
clubs/urls.py
    │  path("clubs/", views.list_clubs)
    ▼
clubs/views.py → list_clubs(request)
    │  Club.objects.all()  →  serialize  →  Response(JSON)
    ▼
HTTP 200  [{ "id": 1, "name": "Robotics", ... }, ...]
```

Same chain for events: `config/urls.py` → `include("events.urls")` → `events/urls.py` → `events/views.py`.

### What each hop answers

| Question | File |
|----------|------|
| Which settings module? | `manage.py` → `DJANGO_SETTINGS_MODULE` |
| Are my apps loaded? | `settings.py` → `INSTALLED_APPS` |
| Where do URLs start? | `settings.py` → `ROOT_URLCONF` |
| Who owns `/api/...`? | `config/urls.py` → `include(...)` |
| Which function runs? | app `urls.py` → `path(..., views.fn)` |
| What JSON comes back? | that function in `views.py` |

If you get **404**: stop at the URLConf hop — path pattern or `include` is wrong.  
If you get **500**: the view ran; read the traceback (usually model/serializer).  
If you get **200 with wrong data**: the view ran; read the queryset / serializer.

---

## Endpoints (only these)

| Method | URL | App | View |
|--------|-----|-----|------|
| `GET` | `/api/health/` | clubs | `health` |
| `GET` | `/api/clubs/` | clubs | `list_clubs` |
| `GET` | `/api/events/` | events | `list_events` |

Optional query on events: `?club=<id>` filters by club foreign key.

Try them yourself:

```bash
curl http://127.0.0.1:8005/api/health/
curl http://127.0.0.1:8005/api/clubs/
curl http://127.0.0.1:8005/api/events/
curl "http://127.0.0.1:8005/api/events/?club=1"
```

---

## Run

```bash
./run.sh            # API + React UI
./run.sh --backend  # API only
./run.sh --agent    # coach — explain settings / URL tracing / this cycle
```

- UI: http://127.0.0.1:5178  
- API: http://127.0.0.1:8005/api/health/

---

## Practice drill

1. Start `./run.sh`, open the UI, click a club or load events.
2. In DevTools → Network, copy the request URL.
3. Walk the cycle above with that URL until you land on the view function.
4. Change a field name in the serializer or add a `print()` in the view; refresh and observe the response.
5. Ask the coach (`./run.sh --agent`) to quiz you on any hop you cannot explain yet.
