const API = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8005/api";

export async function fetchClubs({ category = "" } = {}) {
  const params = new URLSearchParams();
  if (category) params.set("category", category);
  const qs = params.toString();
  const res = await fetch(`${API}/clubs/${qs ? `?${qs}` : ""}`);
  if (!res.ok) throw new Error("Failed to load clubs");
  return res.json();
}

export async function createClub(payload) {
  const res = await fetch(`${API}/clubs/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to create club");
  return res.json();
}

export async function updateClub(id, payload) {
  const res = await fetch(`${API}/clubs/${id}/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to update club");
  return res.json();
}

export async function deleteClub(id) {
  const res = await fetch(`${API}/clubs/${id}/`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to delete club");
}

export async function fetchEvents({ club = "", status = "" } = {}) {
  const params = new URLSearchParams();
  if (club) params.set("club", club);
  if (status) params.set("status", status);
  const qs = params.toString();
  const res = await fetch(`${API}/events/${qs ? `?${qs}` : ""}`);
  if (!res.ok) throw new Error("Failed to load events");
  return res.json();
}

export async function createEvent(payload) {
  const res = await fetch(`${API}/events/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to create event");
  return res.json();
}

export async function cancelEvent(id) {
  const res = await fetch(`${API}/events/${id}/cancel/`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to cancel event");
  return res.json();
}

export async function deleteEvent(id) {
  const res = await fetch(`${API}/events/${id}/`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to delete event");
}
