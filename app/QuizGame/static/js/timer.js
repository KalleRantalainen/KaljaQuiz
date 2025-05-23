export function startTimer(duration, displayElement, onEnd = null) {
    let timer = duration;
    displayElement.textContent = timer;

    const interval = setInterval(() => {
        timer--;
        displayElement.textContent = timer;

        if (timer <= 0) {
            clearInterval(interval);
            displayElement.textContent = "Time's up!";
            if (onEnd) onEnd();
        }
    }, 1000);

    return interval; // You can clear it manually if needed
}
