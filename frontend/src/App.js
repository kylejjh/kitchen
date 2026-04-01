import { useEffect, useState } from "react";

const API = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:5000";

function App() {
  const [cuisines, setCuisines] = useState([]);
  const [ingredients, setIngredients] = useState([]);

  const [selectedCuisine, setSelectedCuisine] = useState("");
  const [selectedIngredient, setSelectedIngredient] = useState("");

  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      fetch(`${API}/cuisines`).then((res) => {
        if (!res.ok) {
          throw new Error("Failed to load cuisines");
        }
        return res.json();
      }),
      fetch(`${API}/ingredients`).then((res) => {
        if (!res.ok) {
          throw new Error("Failed to load ingredients");
        }
        return res.json();
      }),
    ])
      .then(([cuisineData, ingredientData]) => {
        setCuisines(cuisineData.cuisines || []);
        setIngredients(Array.isArray(ingredientData) ? ingredientData : []);
      })
      .catch((err) => setError(err.toString()));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Kitchen Form</h1>
      <p>Dropdown options are loaded from backend endpoints.</p>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <div style={{ marginBottom: 20 }}>
        <label htmlFor="cuisine-select"><strong>Choose a cuisine:</strong></label>
        <br />
        <select
          id="cuisine-select"
          value={selectedCuisine}
          onChange={(e) => setSelectedCuisine(e.target.value)}
          style={{ marginTop: 8, padding: 6, minWidth: 220 }}
        >
          <option value="">-- Select a cuisine --</option>
          {cuisines.map((cuisine) => (
            <option key={cuisine._id || cuisine.id || cuisine.slug} value={cuisine.slug}>
              {cuisine.name}
            </option>
          ))}
        </select>
      </div>

      <div style={{ marginBottom: 20 }}>
        <label htmlFor="ingredient-select"><strong>Choose an ingredient:</strong></label>
        <br />
        <select
          id="ingredient-select"
          value={selectedIngredient}
          onChange={(e) => setSelectedIngredient(e.target.value)}
          style={{ marginTop: 8, padding: 6, minWidth: 220 }}
        >
          <option value="">-- Select an ingredient --</option>
          {ingredients.map((ingredient) => (
            <option key={ingredient.id} value={ingredient.name}>
              {ingredient.name}
            </option>
          ))}
        </select>
      </div>

      <h2>Selected Values</h2>
      <pre>
        {JSON.stringify(
          {
            cuisine: selectedCuisine,
            ingredient: selectedIngredient,
          },
          null,
          2
        )}
      </pre>
    </div>
  );
}

export default App;
