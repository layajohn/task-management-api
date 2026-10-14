
from flask import Flask, jsonify, request
import sqlite3
from contextlib import contextmanager

app = Flask(__name__)

DATABASE = "tasks.db"


# Connect to the database and close the connection safely
@contextmanager
def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


# Create the tasks table if it does not exist
def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'pending'
            )
        """)


# Home endpoint
@app.route("/")
def home():
    return jsonify({
        "message": "My Task Management API is running!"
    })


# Get all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    with get_db() as db:
        rows = db.execute(
            "SELECT * FROM tasks ORDER BY id"
        ).fetchall()

    return jsonify([dict(row) for row in rows])


# Create a new task
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Send a valid JSON object"}), 400

    title = data.get("title")
    description = data.get("description", "")

    if not isinstance(title, str) or not title.strip():
        return jsonify({"error": "A non-empty title is required"}), 400

    if not isinstance(description, str):
        return jsonify({"error": "Description must be text"}), 400

    with get_db() as db:
        cursor = db.execute(
            "INSERT INTO tasks (title, description) VALUES (?, ?)",
            (title.strip(), description.strip())
        )

        task_id = cursor.lastrowid

        row = db.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

    return jsonify(dict(row)), 201


# Get one task by ID
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    with get_db() as db:
        row = db.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

    if row is None:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(dict(row))


# Update an existing task
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({"error": "Send a valid JSON object"}), 400

    allowed_fields = {"title", "description", "status"}

    if not set(data).issubset(allowed_fields):
        return jsonify({"error": "Invalid task fields"}), 400

    with get_db() as db:
        row = db.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

        if row is None:
            return jsonify({"error": "Task not found"}), 404

        title = data.get("title", row["title"])
        description = data.get("description", row["description"])
        status = data.get("status", row["status"])

        if not isinstance(title, str) or not title.strip():
            return jsonify({"error": "Title cannot be empty"}), 400

        if not isinstance(description, str):
            return jsonify({"error": "Description must be text"}), 400

        if status not in ("pending", "in_progress", "completed"):
            return jsonify({"error": "Invalid status"}), 400

        db.execute(
            """
            UPDATE tasks
            SET title = ?, description = ?, status = ?
            WHERE id = ?
            """,
            (title.strip(), description.strip(), status, task_id)
        )

        updated_row = db.execute(
            "SELECT * FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

    return jsonify(dict(updated_row))


# Delete a task by ID
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with get_db() as db:
        cursor = db.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,)
        )

        if cursor.rowcount == 0:
            return jsonify({"error": "Task not found"}), 404

    return jsonify({
        "message": "Task deleted successfully"
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
