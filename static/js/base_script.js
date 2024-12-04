const dropdownIcon = document.getElementById('dropdownIcon');
const dropdownContent = document.getElementById('dropdownContent');

dropdownIcon.addEventListener('click', () => {
	dropdownContent.classList.toggle('active');
});
