const socket = io();
        
console.log("player_coins js file");

// Server should embed this as a JS variable
const isHost = document.body.dataset.isHost === "true";

if (isHost) {
    document.getElementById("coin").style.display = "block";
    document.getElementById("coin").addEventListener("click", () => {
        socket.emit("flip_coin");
    });
}

document.querySelectorAll('input[name="side"]').forEach(radio => {
    radio.addEventListener("change", e => {
      socket.emit("player_choice", { choice: e.target.value });
    });
  });


socket.on("animate_flip", (data) => {
    const coin = document.getElementById("coin");
    coin.classList.add("flip");
    setTimeout(() => coin.classList.remove("flip"), 1000);
  });
  
socket.on("flip_result", (data) => {
  document.getElementById("result").textContent =
    `Result: ${data.result} — You ${data.win ? "won!" : "lost."}`;
});