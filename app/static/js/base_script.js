const dropdownIcon = document.getElementById('dropdownIcon');
const dropdownContent = document.getElementById('dropdownContent');

dropdownIcon.addEventListener('click', () => {
	dropdownContent.classList.toggle('active');
});

window.onLoad = async function () {
	const currentTaskListId = dropdownContent.dataset.currentTaskListId;

	if (currentTaskListId) {
		const taskListToDo = document.getElementById("taskListToDo");
		const taskListDone = document.getElementById("taskListDone");

		taskListToDo.innerHTML = "";
		taskListDone.innerHTML = "";

		try {
			const response = await fetch(`/tasks/api/get_tasks/${currentTaskListId}`);

			if (!reponse.ok) {
				throw new Error("Failed to fetch tasks");
			}

			const data = await response.json();

			if (data.error) {
				taskListDo.innerHTML = `<li>${data.error}</li>`;
				return;
			}


			data.tasks.forEach(task => {
				const li = document.createElement("li");
				li.textContent = task.task;

				if (task.complete) {
					taskListdone.appendChild(li);
				} else {
					taskListToDo.appendChild(li);
				}
			});
		} catch (error) {
			console.error("Error loading tasks:", error);
			taskListToDo.innerHTML = '<li>Error loading tasks</li>;
		}
	}
}
