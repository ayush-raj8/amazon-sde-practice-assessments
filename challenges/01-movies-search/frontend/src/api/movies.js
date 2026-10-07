const API = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000/api";

export async function fetchMovies() {
  const res = await fetch(`${API}/movies/`);
  if (!res.ok) throw new Error("Failed to load movies");
  return res.json();
}

export async function simpleSearch(q, field) {
  const params = new URLSearchParams({ q, field });
  const res = await fetch(`${API}/movies/search/?${params}`);
  if (!res.ok) throw new Error("Simple search failed");
  return res.json();
}

export async function advancedSearch(filters) {
  const res = await fetch(`${API}/movies/advanced-search/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(filters),
  });
  if (!res.ok) throw new Error("Advanced search failed");
  return res.json();
}
