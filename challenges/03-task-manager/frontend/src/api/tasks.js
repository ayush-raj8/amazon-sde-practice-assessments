const API = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8002/api";

export async function fetchTasks(filters = {}) {
  const params = new URLSearchParams();
  if (filters.status) params.set("status", filters.status);
  if (filters.priority) params.set("priority", filters.priority);
  if (filters.due_before) params.set("due_before", filters.due_before);
  const qs = params.toString();
  const res = await fetch(`${API}/tasks/${qs ? `?${qs}` : ""}`);
  if (!res.ok) throw new Error("Failed to load tasks");
  return res.json();
}

export async function createTask(payload) {
  const res = await fetch(`${API}/tasks/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to create task");
  return res.json();
}

export async function updateTask(id, payload) {
  const res = await fetch(`${API}/tasks/${id}/`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to update task");
  return res.json();
}

export async function markComplete(id) {
  const res = await fetch(`${API}/tasks/${id}/complete/`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to mark complete");
  return res.json();
}

export async function deleteTask(id) {
  const res = await fetch(`${API}/tasks/${id}/`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to delete task");
}
