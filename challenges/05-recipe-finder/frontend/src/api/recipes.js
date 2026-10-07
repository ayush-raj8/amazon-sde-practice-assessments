const API = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8004/api";

export async function fetchRecipes() {
  const res = await fetch(`${API}/recipes/`);
  if (!res.ok) throw new Error("Failed to load recipes");
  return res.json();
}

export async function searchRecipes(filters) {
  const res = await fetch(`${API}/recipes/search/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(filters),
  });
  if (!res.ok) throw new Error("Recipe search failed");
  return res.json();
}
