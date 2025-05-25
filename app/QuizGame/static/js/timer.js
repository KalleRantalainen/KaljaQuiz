let timerInterval = null;

export function startTimer(duration, displayElement, onEnd = null) {
    let timer = duration;
    clearInterval(timerInterval); 

    displayElement.textContent = timer;

    timerInterval = setInterval(() => {
        timer--;
        displayElement.textContent = timer;

        if (timer <= 0) {
            clearInterval(timerInterval);
            displayElement.textContent = "AIKA!";
            if (onEnd) onEnd();
        }
    }, 1000);

    return timerInterval; // You can clear it manually if needed
}

export function stopTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
}