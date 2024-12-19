import React, { useState, useEffect } from "react";
import "./App.css"; // Import CSS file

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Example fetch to get datasets (replace with your API logic)
  useEffect(() => {
    fetch("https://api.labelbox.com/graphql", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_API_KEY", // Make sure to replace with your actual key
      },
      body: JSON.stringify({
        query: `
          query {
            datasets {
              id
              name
            }
          }
        `,
      }),
    })
      .then((response) => response.json())
      .then((result) => {
        setData(result.data.datasets); // Update state with API data
        setLoading(false); // Stop loading
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setLoading(false); // Stop loading on error
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Welcome to Labelbox App</h1>
        {loading ? (
          <p>Loading datasets...</p>
        ) : (
          <div>
            <h2>Datasets:</h2>
            <ul>
              {data && data.length > 0 ? (
                data.map((dataset) => (
                  <li key={dataset.id}>{dataset.name}</li>
                ))
              ) : (
                <li>No datasets found.</li>
              )}
            </ul>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
