import { useCallback, useEffect, useState } from "react";
import {
  createTask,
  fetchTasks,
  markComplete,
  updateTask,
} from "./api/tasks.js";
import TaskList from "./components/TaskList.jsx";

const EMPTY_FORM = {
  title: "",
  description: "",
  status: "todo",
  priority: "medium",
  due_date: "",
};

export default function App() {
  const [tasks, setTasks] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    status: "",
    priority: "",
    due_before: "",
  });
  const [form, setForm] = useState(EMPTY_FORM);

  const load = useCallback(async (nextFilters = filters) => {
    setLoading(true);
    setError("");
    try {
      setTasks(await fetchTasks(nextFilters));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    load();
  }, [load]);

  async function onFilter(e) {
    e.preventDefault();
    await load(filters);
  }

  async function onCreate(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const payload = { ...form };
      if (!payload.due_date) payload.due_date = null;
      await createTask(payload);
      setForm(EMPTY_FORM);
      await load();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function onComplete(id) {
    setError("");
    try {
      await markComplete(id);
      await load();
    } catch (err) {
      setError(err.message);
    }
  }

  async function onPriorityChange(id, priority) {
    setError("");
    try {
      await updateTask(id, { priority });
      await load();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="page">
      <header>
        <h1>Task Board</h1>
        <p className="tagline">
          Practice assessment — filter, create, and complete tasks
        </p>
      </header>

      <form className="panel" onSubmit={onFilter}>
        <label>
          Status
          <select
            value={filters.status}
            onChange={(e) => setFilters({ ...filters, status: e.target.value })}
          >
            <option value="">Any</option>
            <option value="todo">todo</option>
            <option value="doing">doing</option>
            <option value="done">done</option>
          </select>
        </label>
        <label>
          Priority
          <select
            value={filters.priority}
            onChange={(e) =>
              setFilters({ ...filters, priority: e.target.value })
            }
          >
            <option value="">Any</option>
            <option value="low">low</option>
            <option value="medium">medium</option>
            <option value="high">high</option>
          </select>
        </label>
        <label>
          Due on or before
          <input
            type="date"
            value={filters.due_before}
            onChange={(e) =>
              setFilters({ ...filters, due_before: e.target.value })
            }
          />
        </label>
        <button type="submit" disabled={loading}>
          Apply filters
        </button>
      </form>

      <form className="panel grid" onSubmit={onCreate}>
        <label>
          Title
          <input
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
            required
          />
        </label>
        <label>
          Description
          <input
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
          />
        </label>
        <label>
          Status
          <select
            value={form.status}
            onChange={(e) => setForm({ ...form, status: e.target.value })}
          >
            <option value="todo">todo</option>
            <option value="doing">doing</option>
            <option value="done">done</option>
          </select>
        </label>
        <label>
          Priority
          <select
            value={form.priority}
            onChange={(e) => setForm({ ...form, priority: e.target.value })}
          >
            <option value="low">low</option>
            <option value="medium">medium</option>
            <option value="high">high</option>
          </select>
        </label>
        <label>
          Due date
          <input
            type="date"
            value={form.due_date}
            onChange={(e) => setForm({ ...form, due_date: e.target.value })}
          />
        </label>
        <button type="submit" disabled={loading}>
          Create task
        </button>
      </form>

      {error && <p className="error">{error}</p>}
      <TaskList
        tasks={tasks}
        onComplete={onComplete}
        onPriorityChange={onPriorityChange}
      />
    </div>
  );
}
