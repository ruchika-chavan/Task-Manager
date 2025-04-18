from datetime import datetime
from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize Database
def init_db():
    try:
        conn = sqlite3.connect("tasks.db")
    except sqlite3.Error as e:
        print(f"Database error during initialization: {e}")
        raise  # Optionally, raise the error or handle it as needed
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
    try:
        conn = sqlite3.connect("tasks.db")
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
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

    try:
        conn = sqlite3.connect("tasks.db")
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
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
    try:
        conn = sqlite3.connect("tasks.db")
    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {e}"}), 500
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
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(debug=True)
