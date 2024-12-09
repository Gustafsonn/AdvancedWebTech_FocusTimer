let taskCount = 1;

function addTask() {
	taskCount++;
	const taskDiv = document.createElement('div');
	taskDiv.classList.add('task-item');
	taskDiv.innerHTML = `
		<label for="task_${taskCount}">Task Description:</label>
		<input type="text" id="task_${taskCount}" name="tasks[]" required><br><br>
	`;
	document.getElementById('tasks').appendChild(taskDiv);
}
