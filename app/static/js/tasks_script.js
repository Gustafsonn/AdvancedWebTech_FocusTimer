document.getElementById("taskListSelect").addEventListener("change", async function () {
	const taskListId = this.value;
	const taskListContainer = document.getElementById("taskList");
	const taskListTitle = document.getElementById("taskListTitle");

	taskListContainer.innerHTML = "";
	taskListTitle.textContent = "Tasks";

	if (!taskListId) {
		return;
	}

	try {
		const response = await fetch(`/tasks/api/get_tasks/${taskListId}`, {
			method: 'POST',
		});

		if (!response.ok) {
			throw new Error("failed to set task list");
		}

		const data = await response.json();
		console.log(data.message);
	} catch (error) {
		console.error(error);
	}
});


window.onload = async function() {
	const taskListContainer = document.getElementById("taskListContainer");
	const currentTaskListId = taskListContainer.dataset.currentTaskListId;

	if (currentTaskListId) {
		const taskListContainer = document.getElementById("taskList");
		const taskListTitle = document.getElementById("taskListTitle");

		taskListContainer.innerHTML = "";
		taskListTitle.textContent = "Tasks";

		try {
			const response = await fetch(`/tasks/api/get_tasks/${currentTaskListId}`);
			if (!response.ok) {
				throw new Error("failed to fetch tasks");
			}

			const data = await response.json();

			if (data.error) {
				taskListContainer.innerHTML = `<li>${data.error}</li>`;
				return;
			}

			taskListTitle.textContent = `Tasks for: ${data.title}`;

			data.tasks.forEach(task => {
				const li = document.createElement("li");
				li.textContent = task.task;

				if (task.completed) {
					li.style.textDecoration = "line-through";
				}

				taskListContainer.appendChild(li);
			});
		} catch (error) {
			taskListContainer.innerHTML = '<li>Error loading tasks</li>';
			console.error(error);
		}
	}
};

const showTaskInfo = document.getElementById('showtaskInfoButton');

showTaskInfo.assEventListener('click', () => {
	location.reload();
});
