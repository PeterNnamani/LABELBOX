import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [task, setTask] = useState(null);
  const [annotations, setAnnotations] = useState('');

  useEffect(() => {
    // Fetch task data from Flask backend
    axios.get('http://127.0.0.1:5000/tasks/task_1')
      .then(response => {
        setTask(response.data);
      })
      .catch(error => {
        console.error("There was an error fetching the task!", error);
      });
  }, []);

  const handleSaveAnnotation = () => {
    // Save annotation to database
    axios.post('http://127.0.0.1:5000/save-annotation', {
      task_id: task.task_id,
      annotations: annotations
    })
      .then(response => {
        alert(response.data.message);
      })
      .catch(error => {
        console.error("Error saving annotations", error);
      });
  };

  return (
    <div className="App">
      <h1>Labelbox Demo</h1>
      {task && (
        <div>
          <img src={task.image_url} alt="Task" width="300" />
          <textarea
            value={annotations}
            onChange={(e) => setAnnotations(e.target.value)}
            placeholder="Enter your annotations here"
          />
          <button onClick={handleSaveAnnotation}>Save Annotations</button>
        </div>
      )}
    </div>
  );
}

export default App;