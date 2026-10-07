export default function EmployeeList({ employees }) {
  if (!employees.length) {
    return <p className="empty">No employees match your filters.</p>;
  }

  return (
    <ul className="employee-list">
      {employees.map((e) => (
        <li key={e.id} className="employee-card">
          <h3>{e.name}</h3>
          <p>
            <strong>Title:</strong> {e.job_title}
          </p>
          <p>
            <strong>Department:</strong> {e.department}
          </p>
          <p>
            <strong>Location:</strong> {e.location}
          </p>
          <p className="email">{e.email}</p>
        </li>
      ))}
    </ul>
  );
}
