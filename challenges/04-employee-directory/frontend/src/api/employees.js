const API = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8003/api";

export async function fetchEmployees({ q = "", department = "", sort = "name" } = {}) {
  const params = new URLSearchParams();
  if (q) params.set("q", q);
  if (department) params.set("department", department);
  if (sort) params.set("sort", sort);
  const qs = params.toString();
  const res = await fetch(`${API}/employees/${qs ? `?${qs}` : ""}`);
  if (!res.ok) throw new Error("Failed to load employees");
  return res.json();
}
