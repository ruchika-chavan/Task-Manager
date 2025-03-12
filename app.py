from datetime import datetime
from flask import Flask, render_template, request, jsonify
import sqlite3

from __init__ import app  # Only import app, no db import here!


# Initialize Database
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            deadline TEXT NOT NULL,
            importance TEXT CHECK(importance IN ('High', 'Moderate', 'Low')) NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


init_db()  # Run the database initialization


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, task, deadline, importance 
        FROM tasks 
        ORDER BY deadline ASC, 
            CASE importance 
                WHEN 'High' THEN 1 
                WHEN 'Moderate' THEN 2 
                WHEN 'Low' THEN 3 
            END ASC
        """
    )
    tasks = [
        {"id": row[0], "task": row[1], "deadline": row[2], "importance": row[3]}
        for row in cursor.fetchall()
    ]
    conn.close()
    return jsonify(tasks)


@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    task = data.get("task")
    deadline = data.get("deadline")
    importance = data.get("importance")

    if not task or not deadline or not importance:
        return jsonify({"error": "Missing fields"}), 400

    # Check if deadline is before today
    today = datetime.today().date()
    task_deadline = datetime.strptime(deadline, "%Y-%m-%d").date()

    if task_deadline < today:
        return jsonify({"error": "Deadline cannot be in the past!"}), 400

    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (task, deadline, importance) VALUES (?, ?, ?)",
        (task, deadline, importance),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Task added successfully"}), 201


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task deleted successfully"}), 200


@app.route("/tasks", methods=["DELETE"])
def delete_all_tasks():
    with sqlite3.connect("tasks.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks")  # Clears all tasks
        conn.commit()
    return jsonify({"message": "All tasks deleted"}), 200


if __name__ == "__main__":
    app.run(debug=True)
