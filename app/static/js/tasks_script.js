const dropdownIcon = document.getElementById('dropdownIcon');
const dropdownContent = document.getElementById('dropdownContent');
const taskListSelect = document.getElementById('taskListSelect');
const footer = document.querySelector('footer h1');
if (dropdownIcon) {
	dropdownIcon.addEventListener('click', () => {
		dropdownContent.classList.toggle('active');
	});
}

if  (taskListSelect) {
	taskListSelect.addEventListener("change", async function () {
		const taskListId = this.value;
		console.log("User selected task:", taskListId);
		if(taskListId) {
			sessionStorage.setItem('current_task_list_id', taskListId);

			await fetch('/tasks/update_task_list', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ task_list_id: taskListId }),
			});

			console.log("session updated to:", taskListId)
			await displayTasks(taskListId);
			await displayNextTask(taskListId);
		}
	});
}

document.getElementById('taskCompleted').addEventListener("click", async function () {
	const footer = document.querySelector("footer h1");
	const currentTask = footer.textContent.replace("CurrentFocus: ", "");

	if (!currentTask || currentTask === "select a task") {
		alert("No task selected to mark as complete.");
		return;
	}

	try {
		const response = await fetch('/tasks/api/complete_task', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ task: currentTask })
		});

		const data = await response.json();

		if (response.ok) {
			alert(data.message);

			const currentTaskListId = sessionStorage.getItem('current_task_list_id');
			if (currentTaskListId) {
				await displayTasks(currentTaskListId);
				await displayNextTask(currentTaskListId);
			}
		} else {
			alert(data.error || "Failed to complete task.");
		}
	} catch (error) {
		console.error("Error completing task:", error);
		alert("An error occurred while completing the taskk.");
	}
});


async function displayTasks(taskListId) {
	const sections = document.querySelectorAll('[data-section]');

	sections.forEach(section => {
		const taskListToDo = section.querySelector(".taskListToDo");
		const taskListDone = section.querySelector(".taskListDone");
		const taskListTitle = section.querySelector("h2");

		taskListToDo.innerHTML = "";
		taskListDone.innerHTML = "";
		taskListTitle.textContent = "Tasks";
	});

	if (!taskListId) {
		sections.forEach(section => {
			const taskListTitle = section.querySelector(".taskListTitle");
			if (taskListTitle) taskListTitle.textContent = "No task list selected";
		});
		return;
	}

	try {
		const response = await fetch(`/tasks/api/get_tasks/${taskListId}`);

		if (!response.ok) {
			throw new Error("Failed to fetch tasks");
		}

		const data = await response.json();

		if (data.error) {
			sections.forEach(section => {
				taskListToDo = section.querySelector("h2");
				if (taskListToDo) taskListToDo.innerHTML = `<li>${data.error}</li>`;
			});
			return;
		}

		sections.forEach(section => {
			const taskListToDo = section.querySelector(".taskListToDo");
			const taskListDone = section.querySelector(".taskListDone");
			const taskListTitle = section.querySelector("h2");

			if (taskListTitle) taskListTitle.textContent = `Tasks for: ${data.title}`;
	

			data.tasks.forEach(task => {
				const li = document.createElement("li");
				li.textContent = task.task;

				if (task.completed) {
					li.style.textDecoration = "line-through";
					if (taskListDone) taskListDone.appendChild(li);
				} else {
					if (taskListToDo) taskListToDo.appendChild(li);
				}
			});
		});
	} catch (error) {
		console.error("Error loading tasks:", error);
	}
}

async function displayNextTask(taskListId) {

	if (!taskListId) {
		footer.textContent = "Please select a task list from Tasks";
		return;
	}

	try {
		const response = await fetch(`/tasks/api/get_first_incomplete_task?task_list_id=${taskListId}`);

		if (!response.ok) {
			throw new Error("Failed to fetch the next task");
		}

		const data = await response.json();

		footer.innerHTML = "";

		if (data.task) {
			footer.textContent = `CurrentFocus: ${data.task}`;
		}
	} catch (error) {
		console.error("Error loading next task:", error);
	}
}

window.onload = async function () {
	let currentTaskListId = sessionStorage.getItem('current_task_list_id');
	console.log("Current task:", currentTaskListId);

	if (!currentTaskListId) {
		const taskListContainer = document.getElementById("dropdownContent");
		currentTaskListId = taskListContainer?.dataset.currentTaskListId || '';

		if (currentTaskListId) {
			sessionStorage.setItem('current_task_list_id', currentTaskListId);
		}
	}

	if (currentTaskListId) {
		await displayTasks(currentTaskListId);
		await displayNextTask(currentTaskListId);
	} else {
		footer.textContent = "Please select a task list from Tasks";
	}
};

