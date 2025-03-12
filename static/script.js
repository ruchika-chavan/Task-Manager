document.addEventListener("DOMContentLoaded", fetchTasks);

function fetchTasks() {
    fetch("/tasks")
        .then(response => response.json())
        .then(tasks => {
            const taskList = document.getElementById("taskList");
            taskList.innerHTML = "";

            const today = new Date().toISOString().split("T")[0]; // Get today's date in YYYY-MM-DD format

            tasks.forEach(task => {
                const row = document.createElement("tr");

                // Check if the deadline is past
                const isPastDeadline = task.deadline < today;

                row.innerHTML = `
                    <td>${task.task}</td>
                    <td>${task.deadline}</td>
                    <td>${task.importance}</td>
                    <td><button class="btn btn-danger" onclick="deleteTask(${task.id})">Delete</button></td>
                `;

                // if (task.importance == "High") {
                //     row.style.backgroundColor = "#e57b7b"; // Light Red
                //     row.classList.add("high-imp");
                // }
                // else if (task.importance == "Moderate") {
                //     row.style.backgroundColor = "#e5e37b"; // Light Yellow
                //     row.classList.add("mod-imp");
                // }
                // else if (task.importance == "Low") {
                //     row.style.backgroundColor = "#aee57b"; // Light Green
                //     row.classList.add("low-imp");
                // }

                // Apply class if the deadline has passed
                if (isPastDeadline) {
                    row.classList.add("past-deadline");
                }

                console.log(`Task: ${task.task}, Deadline: ${task.deadline}, Is Past Deadline: ${isPastDeadline}`);

                taskList.appendChild(row);
            });
        });
}

function addTask() {
    const taskInput = document.getElementById("taskInput").value.trim();
    const deadlineInput = document.getElementById("deadlineInput").value;
    const importanceInput = document.getElementById("importanceInput").value;

    if (taskInput === "" || deadlineInput === "") {
        alert("Please enter a task and deadline!");
        return;
    }

    // Get today's date in YYYY-MM-DD format
    const today = new Date().toISOString().split("T")[0];

    if (deadlineInput < today) {
        alert("Deadline cannot be in the past!");
        return;
    }

    fetch("/tasks", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task: taskInput, deadline: deadlineInput, importance: importanceInput })
    })
    .then(response => response.json())
    .then(() => {
        document.getElementById("taskInput").value = "";
        document.getElementById("deadlineInput").value = "";
        importanceInput.value = "Moderate";  // Reset importance dropdown to default
        fetchTasks();
    });
}

function deleteTask(taskId) {
    fetch(`/tasks/${taskId}`, { method: "DELETE" })
    .then(response => response.json())
    .then(() => fetchTasks());
}

function deleteAllTasks() {
    if (!confirm("Are you sure you want to delete all tasks?")) return;

    fetch("/tasks", { method: "DELETE" })
        .then(response => response.json())
        .then(() => fetchTasks());
}