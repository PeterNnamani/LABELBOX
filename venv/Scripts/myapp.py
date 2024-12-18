from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB setup
client = MongoClient("your_mongodb_connection_string_here")
db = client["labelbox_db"]
tasks_collection = db["tasks"]

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    task = tasks_collection.find_one({"task_id": task_id})
    if task:
        return jsonify(task), 200
    return jsonify({"error": "Task not found"}), 404

@app.route('/save-annotation', methods=['POST'])
def save_annotation():
    data = request.get_json()
    task_id = data.get('task_id')
    annotations = data.get('annotations')
    if task_id and annotations:
        tasks_collection.update_one(
            {"task_id": task_id},
            {"$set": {"annotations": annotations}},
            upsert=True
        )
        return jsonify({"message": "Annotations saved successfully"}), 200
    return jsonify({"error": "Invalid data"}), 400

if __name__ == '_main_':
    app.run(debug=True)