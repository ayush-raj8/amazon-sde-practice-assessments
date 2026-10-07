import { useCallback, useEffect, useState } from "react";
import {
  cancelEvent,
  createClub,
  createEvent,
  deleteClub,
  deleteEvent,
  fetchClubs,
  fetchEvents,
  updateClub,
} from "./api/desk.js";

const EMPTY_CLUB = { name: "", campus: "", category: "", member_count: "0" };
const EMPTY_EVENT = {
  title: "",
  club: "",
  event_date: "",
  location: "",
  capacity: "20",
};

export default function App() {
  const [tab, setTab] = useState("clubs");
  const [clubs, setClubs] = useState([]);
  const [events, setEvents] = useState([]);
  const [category, setCategory] = useState("");
  const [clubFilter, setClubFilter] = useState("");
  const [clubForm, setClubForm] = useState(EMPTY_CLUB);
  const [eventForm, setEventForm] = useState(EMPTY_EVENT);
  const [editCampus, setEditCampus] = useState({});
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const loadClubs = useCallback(async (filters = { category }) => {
    setClubs(await fetchClubs(filters));
  }, [category]);

  const loadEvents = useCallback(async (filters = { club: clubFilter }) => {
    setEvents(await fetchEvents(filters));
  }, [clubFilter]);

  useEffect(() => {
    (async () => {
      setLoading(true);
      setError("");
      try {
        await loadClubs({ category: "" });
        await loadEvents({ club: "" });
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  async function wrap(fn) {
    setLoading(true);
    setError("");
    try {
      await fn();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header>
        <h1>Campus Club Desk</h1>
        <p className="tagline">
          Tutorial challenge — one Django project, two apps (<code>clubs</code> +{" "}
          <code>events</code>)
        </p>
      </header>

      <div className="trace">
        Debug tip: start at <code>config/settings.py</code> →{" "}
        <code>ROOT_URLCONF</code> → <code>config/urls.py</code> includes → app{" "}
        <code>urls.py</code> → view function. Confirm the path you hit in the Network
        tab matches the view you are reading.
      </div>

      <div className="tabs">
        <button
          type="button"
          className={tab === "clubs" ? "active" : ""}
          onClick={() => setTab("clubs")}
        >
          Clubs
        </button>
        <button
          type="button"
          className={tab === "events" ? "active" : ""}
          onClick={() => setTab("events")}
        >
          Events
        </button>
      </div>

      {error && <p className="error">{error}</p>}
      {loading && <p className="muted">Loading…</p>}

      {tab === "clubs" ? (
        <>
          <form
            className="panel"
            onSubmit={(e) => {
              e.preventDefault();
              wrap(() => loadClubs({ category }));
            }}
          >
            <label>
              Category filter
              <input
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                placeholder="e.g. STEM"
              />
            </label>
            <button type="submit" disabled={loading}>
              Apply
            </button>
          </form>

          <form
            className="panel grid"
            onSubmit={(e) => {
              e.preventDefault();
              wrap(async () => {
                await createClub({
                  ...clubForm,
                  member_count: Number(clubForm.member_count),
                });
                setClubForm(EMPTY_CLUB);
                await loadClubs({ category });
              });
            }}
          >
            <h2 className="form-title">Add club</h2>
            {["name", "campus", "category"].map((key) => (
              <label key={key}>
                {key}
                <input
                  value={clubForm[key]}
                  onChange={(e) => setClubForm({ ...clubForm, [key]: e.target.value })}
                  required
                />
              </label>
            ))}
            <label>
              members
              <input
                type="number"
                min="0"
                value={clubForm.member_count}
                onChange={(e) =>
                  setClubForm({ ...clubForm, member_count: e.target.value })
                }
                required
              />
            </label>
            <button type="submit" disabled={loading}>
              Create
            </button>
          </form>

          <ul className="list">
            {clubs.map((club) => (
              <li className="card" key={club.id}>
                <div>
                  <h3>
                    {club.name}
                    <span className="badge">{club.category}</span>
                  </h3>
                  <p>
                    Campus: {club.campus} · Members: {club.member_count}
                  </p>
                </div>
                <div className="actions">
                  <input
                    placeholder="new campus"
                    value={editCampus[club.id] ?? ""}
                    onChange={(e) =>
                      setEditCampus({ ...editCampus, [club.id]: e.target.value })
                    }
                  />
                  <button
                    type="button"
                    className="ghost"
                    disabled={loading || !(editCampus[club.id] || "").trim()}
                    onClick={() =>
                      wrap(async () => {
                        await updateClub(club.id, {
                          campus: editCampus[club.id].trim(),
                        });
                        setEditCampus({ ...editCampus, [club.id]: "" });
                        await loadClubs({ category });
                      })
                    }
                  >
                    Save campus
                  </button>
                  <button
                    type="button"
                    className="danger"
                    disabled={loading}
                    onClick={() =>
                      wrap(async () => {
                        await deleteClub(club.id);
                        await loadClubs({ category });
                        await loadEvents({ club: clubFilter });
                      })
                    }
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </>
      ) : (
        <>
          <form
            className="panel"
            onSubmit={(e) => {
              e.preventDefault();
              wrap(() => loadEvents({ club: clubFilter }));
            }}
          >
            <label>
              Club filter
              <select
                value={clubFilter}
                onChange={(e) => setClubFilter(e.target.value)}
              >
                <option value="">All clubs</option>
                {clubs.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </label>
            <button type="submit" disabled={loading}>
              Apply
            </button>
          </form>

          <form
            className="panel grid"
            onSubmit={(e) => {
              e.preventDefault();
              wrap(async () => {
                await createEvent({
                  ...eventForm,
                  club: Number(eventForm.club),
                  capacity: Number(eventForm.capacity),
                  status: "scheduled",
                });
                setEventForm(EMPTY_EVENT);
                await loadEvents({ club: clubFilter });
              });
            }}
          >
            <h2 className="form-title">Add event</h2>
            <label>
              title
              <input
                value={eventForm.title}
                onChange={(e) => setEventForm({ ...eventForm, title: e.target.value })}
                required
              />
            </label>
            <label>
              club
              <select
                value={eventForm.club}
                onChange={(e) => setEventForm({ ...eventForm, club: e.target.value })}
                required
              >
                <option value="">Select…</option>
                {clubs.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name}
                  </option>
                ))}
              </select>
            </label>
            <label>
              date
              <input
                type="date"
                value={eventForm.event_date}
                onChange={(e) =>
                  setEventForm({ ...eventForm, event_date: e.target.value })
                }
                required
              />
            </label>
            <label>
              location
              <input
                value={eventForm.location}
                onChange={(e) =>
                  setEventForm({ ...eventForm, location: e.target.value })
                }
                required
              />
            </label>
            <label>
              capacity
              <input
                type="number"
                min="1"
                value={eventForm.capacity}
                onChange={(e) =>
                  setEventForm({ ...eventForm, capacity: e.target.value })
                }
                required
              />
            </label>
            <button type="submit" disabled={loading}>
              Create
            </button>
          </form>

          <ul className="list">
            {events.map((event) => (
              <li className="card" key={event.id}>
                <div>
                  <h3>
                    {event.title}
                    <span
                      className={`badge ${event.status === "cancelled" ? "cancelled" : ""}`}
                    >
                      {event.status}
                    </span>
                  </h3>
                  <p>
                    {event.club_name} · {event.event_date} · {event.location} · cap{" "}
                    {event.capacity}
                  </p>
                </div>
                <div className="actions">
                  {event.status !== "cancelled" && (
                    <button
                      type="button"
                      className="ghost"
                      disabled={loading}
                      onClick={() =>
                        wrap(async () => {
                          await cancelEvent(event.id);
                          await loadEvents({ club: clubFilter });
                        })
                      }
                    >
                      Cancel event
                    </button>
                  )}
                  <button
                    type="button"
                    className="danger"
                    disabled={loading}
                    onClick={() =>
                      wrap(async () => {
                        await deleteEvent(event.id);
                        await loadEvents({ club: clubFilter });
                      })
                    }
                  >
                    Delete
                  </button>
                </div>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
}
