import { useEffect, useState } from "react";
import { advancedSearch, fetchMovies, simpleSearch } from "./api/movies.js";
import MovieList from "./components/MovieList.jsx";

const FIELDS = [
  { value: "all", label: "All fields" },
  { value: "title", label: "Title" },
  { value: "director", label: "Director" },
  { value: "description", label: "Description" },
  { value: "cast", label: "Cast" },
];

export default function App() {
  const [mode, setMode] = useState("simple");
  const [movies, setMovies] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [q, setQ] = useState("");
  const [field, setField] = useState("all");

  const [adv, setAdv] = useState({
    title: "",
    director: "",
    description: "",
    cast: "",
    genre: "",
    year: "",
  });

  useEffect(() => {
    fetchMovies()
      .then(setMovies)
      .catch((e) => setError(e.message));
  }, []);

  async function onSimple(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      setMovies(await simpleSearch(q, field));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  async function onAdvanced(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const payload = { ...adv };
      if (payload.year === "") delete payload.year;
      setMovies(await advancedSearch(payload));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header>
        <h1>Cinema Finder</h1>
        <p className="tagline">
          Practice assessment — simple &amp; advanced movie search
        </p>
      </header>

      <div className="tabs">
        <button
          className={mode === "simple" ? "active" : ""}
          onClick={() => setMode("simple")}
          type="button"
        >
          Simple Search
        </button>
        <button
          className={mode === "advanced" ? "active" : ""}
          onClick={() => setMode("advanced")}
          type="button"
        >
          Advanced Search
        </button>
      </div>

      {mode === "simple" ? (
        <form className="panel" onSubmit={onSimple}>
          <label>
            Search in
            <select value={field} onChange={(e) => setField(e.target.value)}>
              {FIELDS.map((f) => (
                <option key={f.value} value={f.value}>
                  {f.label}
                </option>
              ))}
            </select>
          </label>
          <label>
            Query
            <input
              value={q}
              onChange={(e) => setQ(e.target.value)}
              placeholder="e.g. Nolan, dream, Keanu"
              required
            />
          </label>
          <button type="submit" disabled={loading}>
            Search
          </button>
        </form>
      ) : (
        <form className="panel grid" onSubmit={onAdvanced}>
          {["title", "director", "description", "cast", "genre"].map((key) => (
            <label key={key}>
              {key}
              <input
                value={adv[key]}
                onChange={(e) => setAdv({ ...adv, [key]: e.target.value })}
              />
            </label>
          ))}
          <label>
            year
            <input
              type="number"
              value={adv.year}
              onChange={(e) => setAdv({ ...adv, year: e.target.value })}
            />
          </label>
          <button type="submit" disabled={loading}>
            Apply filters (AND)
          </button>
        </form>
      )}

      {error && <p className="error">{error}</p>}
      <MovieList movies={movies} />
    </div>
  );
}
