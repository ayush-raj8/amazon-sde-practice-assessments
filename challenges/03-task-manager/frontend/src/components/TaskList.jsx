export default function TaskList({ tasks, onComplete, onPriorityChange }) {
  if (!tasks.length) {
    return <p className="empty">No tasks match your filters.</p>;
  }

  return (
    <ul className="task-list">
      {tasks.map((t) => (
        <li key={t.id} className={`task-card status-${t.status}`}>
          <div className="task-head">
            <h3>{t.title}</h3>
            <span className={`badge status`}>{t.status}</span>
          </div>
          <p className="desc">{t.description || "No description"}</p>
          <div className="meta">
            <label>
              Priority
              <select
                value={t.priority}
                onChange={(e) => onPriorityChange(t.id, e.target.value)}
              >
                <option value="low">low</option>
                <option value="medium">medium</option>
                <option value="high">high</option>
              </select>
            </label>
            <span>Due: {t.due_date || "—"}</span>
          </div>
          <div className="actions">
            {t.status !== "done" && (
              <button type="button" onClick={() => onComplete(t.id)}>
                Mark complete
              </button>
            )}
          </div>
        </li>
      ))}
    </ul>
  );
}
