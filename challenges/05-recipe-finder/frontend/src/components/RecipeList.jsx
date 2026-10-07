export default function RecipeList({ recipes }) {
  if (!recipes.length) {
    return <p className="empty">No recipes match your search.</p>;
  }

  return (
    <ul className="recipe-list">
      {recipes.map((r) => (
        <li key={r.id} className="recipe-card">
          <h3>
            {r.name}{" "}
            <span className="meta">
              ({r.cook_time_minutes} min · {r.diet})
            </span>
          </h3>
          <p>
            <strong>Cuisine:</strong> {r.cuisine}
          </p>
          <p>
            <strong>Ingredients:</strong> {r.ingredients}
          </p>
        </li>
      ))}
    </ul>
  );
}
