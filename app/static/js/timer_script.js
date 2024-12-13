let mode = "pomodoro";
let timerInterval;
let timeRemaining = 25 * 60;
let stopwatchTime = 0;
const timerDisplay = document.getElementById("timer");
const toggleButton = document.getElementById("toggle");

function formatTime(seconds) {
	const mins = Math.floor(seconds / 60).toString().padStart(2, "0");
	const secs = (seconds % 60).toString().padStart(2, "0");
	return `${mins}:${secs}`;
}

function updateDisplay() {
	if (mode === "pomodoro") {
		timerDisplay.textContent = formatTime(timeRemaining);
	} else if (mode === "stopwatch") {
		timerDisplay.textContent = formatTime(stopwatchTime);
	}
}

function startTimer() {
	if (timerInterval) return;

	if (mode === "pomodoro") {
		timerInterval = setInterval(() => {
			if (timeRemaining > 0) {
				timeRemaining--;
				updateDisplay();
			} else {
				clearInterval(timerInterval);
				timerInterval = null;
				alert("Pomodoro complete!");
			}
		}, 1000);
	} else if (mode === "stopwatch") {
		timerInterval = setInterval(() => {
			stopwatchTime++;
			updateDisplay();
		}, 1000);
	}
}

function stopTimer() {
	clearInterval(timerInterval);
	timerInterval = null;
}

function resetTimer() {
	stopTimer();
	if (mode === "pomodoro") {
		timeRemaining = 25 * 60;
	} else if (mode === "stopwatch") {
		stopwatchTime = 0;
	}
	updateDisplay();
}

function toggleMode() {
	stopTimer();
	if (mode === "pomodoro") {
		mode = "stopwatch";
		toggleButton.textContent = "Switch to Pomodoro";
		stopwatchTime = 0;
	} else {
		mode = "pomodoro";
		toggleButton.textContent = "Switch to Stopwatch";
		timeRemaining = 25 * 60;
	}
	updateDisplay();
}


document.getElementById("start").addEventListener("click", startTimer);
document.getElementById("stop").addEventListener("click", stopTimer);
document.getElementById("reset").addEventListener("click", resetTimer);
toggleButton.addEventListener("click", toggleMode);

updateDisplay();
