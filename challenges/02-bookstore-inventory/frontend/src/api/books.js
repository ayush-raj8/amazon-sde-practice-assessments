const API = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8001/api";

export async function fetchBooks({ category = "", q = "" } = {}) {
  const params = new URLSearchParams();
  if (category) params.set("category", category);
  if (q) params.set("q", q);
  const qs = params.toString();
  const res = await fetch(`${API}/books/${qs ? `?${qs}` : ""}`);
  if (!res.ok) throw new Error("Failed to load books");
  return res.json();
}

export async function createBook(payload) {
  const res = await fetch(`${API}/books/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to create book");
  return res.json();
}

export async function updateBook(id, payload) {
  const res = await fetch(`${API}/books/${id}/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to update book");
  return res.json();
}

export async function deleteBook(id) {
  const res = await fetch(`${API}/books/${id}/`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to delete book");
}
