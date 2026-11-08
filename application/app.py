
from flask import Flask, request, jsonify

app = Flask(__name__)

# Temporary task storage
tasks = []
task_id_counter = 1


# Homepage
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "application": "DevOps Automation Platform",
        "message": "Task Management API is running",
        "status": "success"
    }), 200


# Health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    }), 200


# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


# Create a new task
@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_counter

    data = request.get_json(silent=True)

    if not data or not isinstance(data.get("title"), str) or not data["title"].strip():
        return jsonify({"error": "Valid task title is required"}), 400

    task = {
        "id": task_id_counter,
        "title": data["title"].strip(),
        "completed": False
    }

    tasks.append(task)
    task_id_counter += 1

    return jsonify(task), 201


# Update an existing task
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "JSON body is required"}), 400

    for task in tasks:
        if task["id"] == task_id:
            if "title" in data:
                if not isinstance(data["title"], str) or not data["title"].strip():
                    return jsonify({"error": "Valid title is required"}), 400
                task["title"] = data["title"].strip()

            if "completed" in data:
                if not isinstance(data["completed"], bool):
                    return jsonify({"error": "completed must be a boolean"}), 400
                task["completed"] = data["completed"]

            return jsonify(task), 200

    return jsonify({"error": "Task not found"}), 404


# Delete a task
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return jsonify({"message": "Task deleted"}), 200

    return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
