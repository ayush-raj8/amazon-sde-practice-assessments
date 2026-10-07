export default function MovieList({ movies }) {
  if (!movies.length) {
    return <p className="empty">No movies match your search.</p>;
  }

  return (
    <ul className="movie-list">
      {movies.map((m) => (
        <li key={m.id} className="movie-card">
          <h3>
            {m.title} <span className="year">({m.year})</span>
          </h3>
          <p>
            <strong>Director:</strong> {m.director}
          </p>
          <p>
            <strong>Genre:</strong> {m.genre}
          </p>
          <p>
            <strong>Cast:</strong> {m.cast}
          </p>
          <p className="desc">{m.description}</p>
        </li>
      ))}
    </ul>
  );
}
