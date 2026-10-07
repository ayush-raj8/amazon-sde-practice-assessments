import { useEffect, useState } from "react";
import { fetchRecipes, searchRecipes } from "./api/recipes.js";
import RecipeList from "./components/RecipeList.jsx";

const DIETS = [
  { value: "any", label: "Any diet" },
  { value: "vegetarian", label: "Vegetarian (includes vegan)" },
  { value: "vegan", label: "Vegan" },
];

function parseIngredients(raw) {
  return raw
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}

export default function App() {
  const [recipes, setRecipes] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const [ingredientInput, setIngredientInput] = useState("");
  const [chips, setChips] = useState([]);
  const [cuisine, setCuisine] = useState("");
  const [diet, setDiet] = useState("any");
  const [maxCookTime, setMaxCookTime] = useState("");

  useEffect(() => {
    fetchRecipes()
      .then(setRecipes)
      .catch((e) => setError(e.message));
  }, []);

  function commitIngredients(raw) {
    const next = parseIngredients(raw);
    if (!next.length) return;
    setChips((prev) => {
      const seen = new Set(prev.map((c) => c.toLowerCase()));
      const merged = [...prev];
      for (const term of next) {
        if (!seen.has(term.toLowerCase())) {
          seen.add(term.toLowerCase());
          merged.push(term);
        }
      }
      return merged;
    });
    setIngredientInput("");
  }

  function onIngredientKeyDown(e) {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      commitIngredients(ingredientInput + (e.key === "," ? "," : ""));
    } else if (e.key === "Backspace" && !ingredientInput && chips.length) {
      setChips((prev) => prev.slice(0, -1));
    }
  }

  function removeChip(index) {
    setChips((prev) => prev.filter((_, i) => i !== index));
  }

  async function onSearch(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const pending = parseIngredients(ingredientInput);
      const ingredients = [...chips];
      for (const term of pending) {
        if (!ingredients.map((c) => c.toLowerCase()).includes(term.toLowerCase())) {
          ingredients.push(term);
        }
      }
      if (pending.length) {
        setChips(ingredients);
        setIngredientInput("");
      }

      const payload = {};
      if (ingredients.length) payload.ingredients = ingredients;
      if (cuisine.trim()) payload.cuisine = cuisine.trim();
      if (diet && diet !== "any") payload.diet = diet;
      if (maxCookTime !== "") payload.max_cook_time = Number(maxCookTime);

      setRecipes(await searchRecipes(payload));
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header>
        <h1>Recipe Finder</h1>
        <p className="tagline">
          Practice assessment — filter recipes by ingredients, cuisine, diet &amp;
          cook time
        </p>
      </header>

      <form className="panel" onSubmit={onSearch}>
        <label className="ingredients-label">
          Ingredients (comma or Enter to add chips)
          <div className="chip-input">
            {chips.map((chip, i) => (
              <button
                key={`${chip}-${i}`}
                type="button"
                className="chip"
                onClick={() => removeChip(i)}
                title="Remove"
              >
                {chip} ×
              </button>
            ))}
            <input
              value={ingredientInput}
              onChange={(e) => {
                const v = e.target.value;
                if (v.includes(",")) {
                  commitIngredients(v);
                } else {
                  setIngredientInput(v);
                }
              }}
              onKeyDown={onIngredientKeyDown}
              onBlur={() => {
                if (ingredientInput.trim()) commitIngredients(ingredientInput);
              }}
              placeholder="e.g. tomato, basil"
            />
          </div>
        </label>

        <label>
          Cuisine
          <input
            value={cuisine}
            onChange={(e) => setCuisine(e.target.value)}
            placeholder="e.g. Italian"
          />
        </label>

        <label>
          Diet
          <select value={diet} onChange={(e) => setDiet(e.target.value)}>
            {DIETS.map((d) => (
              <option key={d.value} value={d.value}>
                {d.label}
              </option>
            ))}
          </select>
        </label>

        <label>
          Max cook time (minutes)
          <input
            type="number"
            min="1"
            value={maxCookTime}
            onChange={(e) => setMaxCookTime(e.target.value)}
            placeholder="e.g. 30"
          />
        </label>

        <button type="submit" disabled={loading}>
          Search
        </button>
      </form>

      {error && <p className="error">{error}</p>}
      <RecipeList recipes={recipes} />
    </div>
  );
}
