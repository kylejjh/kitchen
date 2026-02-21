import { useEffect, useState } from "react";

const API = "http://127.0.0.1:5000";  // IMPORTANT: not localhost

function App() {
  const [one, setOne] = useState(null);
  const [two, setTwo] = useState(null);
  const [three, setThree] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      fetch(`${API}/demo/one`).then(res => res.json()),
      fetch(`${API}/demo/two`).then(res => res.json()),
      fetch(`${API}/demo/three`).then(res => res.json()),
    ])
      .then(([a, b, c]) => {
        setOne(a);
        setTwo(b);
        setThree(c);
      })
      .catch(err => setError(err.toString()));
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Kitchen API Demo (3 endpoints)</h1>

      {error && <p style={{ color: "red" }}>{error}</p>}

      <h2>/demo/one</h2>
      <pre>{JSON.stringify(one, null, 2)}</pre>

      <h2>/demo/two</h2>
      <pre>{JSON.stringify(two, null, 2)}</pre>

      <h2>/demo/three</h2>
      <pre>{JSON.stringify(three, null, 2)}</pre>
    </div>
  );
}

export default App;
