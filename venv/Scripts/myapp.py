from flask import Flask, jsonify, request
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017")  # Replace with your connection string if needed
db = client["labelbox_db"]
collection = db["tasks"]

# Sample project data
project_data = {
    "project_name": "LabelBox Project",
    "description": "This project is a LabelBox Project.",
    "language": "Python",
    "created_at": "2024-12-19"
}

# API endpoint to retrieve a task by its task ID
@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = collection.find_one({"task_id": task_id})
    if task:
        # Convert MongoDB ObjectId to string for JSON serialization
        task["_id"] = str(task["_id"])
        return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404

# API endpoint to save annotations for a task
@app.route('/save-annotation', methods=['POST'])
def save_annotation():
    data = request.get_json()
    task_id = data.get('task_id')
    annotations = data.get('annotations')
    
    if task_id and annotations:
        # Update or insert annotations for the specified task
        collection.update_one(
            {"task_id": task_id},
            {"$set": {"annotations": annotations}},
            upsert=True
        )
        return jsonify({"message": "Annotations saved successfully"}), 200
    
    return jsonify({"error": "Invalid data"}), 400

if __name__ == '__main__':
    # Insert sample project data into MongoDB (if not already present)
    existing_project = collection.find_one({"project_name": project_data["project_name"]})
    if not existing_project:
        result = collection.insert_one(project_data)
        print(f"Sample data inserted with ID: {result.inserted_id}")
    else:
        print("Sample data already exists in the database.")
    
    # Run the Flask app
    app.run(debug=True)
