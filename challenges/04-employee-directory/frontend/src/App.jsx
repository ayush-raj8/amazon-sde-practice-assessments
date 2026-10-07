import { useEffect, useState } from "react";
import { fetchEmployees } from "./api/employees.js";
import EmployeeList from "./components/EmployeeList.jsx";

const DEPARTMENTS = [
  { value: "", label: "All departments" },
  { value: "Engineering", label: "Engineering" },
  { value: "Product", label: "Product" },
  { value: "Sales", label: "Sales" },
  { value: "HR", label: "HR" },
  { value: "Marketing", label: "Marketing" },
];

const SORTS = [
  { value: "name", label: "Name" },
  { value: "department", label: "Department" },
];

export default function App() {
  const [employees, setEmployees] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [q, setQ] = useState("");
  const [department, setDepartment] = useState("");
  const [sort, setSort] = useState("name");

  async function load(filters) {
    setLoading(true);
    setError("");
    try {
      setEmployees(await fetchEmployees(filters));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load({ sort: "name" });
  }, []);

  function onSubmit(e) {
    e.preventDefault();
    load({ q, department, sort });
  }

  return (
    <div className="page">
      <header>
        <h1>People Directory</h1>
        <p className="tagline">
          Practice assessment — search and filter employees
        </p>
      </header>

      <form className="panel" onSubmit={onSubmit}>
        <label>
          Name search
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="e.g. Ali, Patel"
          />
        </label>
        <label>
          Department
          <select
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
          >
            {DEPARTMENTS.map((d) => (
              <option key={d.value || "all"} value={d.value}>
                {d.label}
              </option>
            ))}
          </select>
        </label>
        <label>
          Sort by
          <select value={sort} onChange={(e) => setSort(e.target.value)}>
            {SORTS.map((s) => (
              <option key={s.value} value={s.value}>
                {s.label}
              </option>
            ))}
          </select>
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Loading…" : "Search"}
        </button>
      </form>

      {error && <p className="error">{error}</p>}
      <EmployeeList employees={employees} />
    </div>
  );
}
