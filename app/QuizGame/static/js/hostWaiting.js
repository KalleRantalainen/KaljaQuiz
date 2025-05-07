
async function fetchPlayers() {
    const res = await fetch("/players");
    if (!res.ok) return;
    const names = await res.json();
    const ul = document.getElementById("players-list");
    ul.innerHTML = "";

    if (names.length === 0) {
        ul.innerHTML = "<li><em>(no one yet)</em></li>";
    } else {
        for (const n of names) {
            const li = document.createElement("li");
            li.textContent = n;
            ul.appendChild(li);
        }
    }
}

// poll every 2s
setInterval(fetchPlayers, 2000);
fetchPlayers();


// add the start-game button logic
// const startGameButton = document.getElementById("start-game");
// console.log("start-game button", startGameButton);

// startGameButton.addEventListener("click", async () => {
//     console.log("start-game button clicked");
//     const res = await fetch("/quizgame/start_game", { method: "POST" });
//     if (res.ok) {
//         window.location.href = "/quizgame/game";
//         console.log("New href:", window.location.href);
//     } else {
//         alert("Failed to start the game. Please try again.");
//     }
// });

const socket = io();
const hostId = "{{ hostId }}"; // get the host ID from the template context
socket.emit("join_game", { player_id: hostId });    // host joins the "players" room, too

document.getElementById("start-game")
  .addEventListener("click", () => {
    socket.emit("start_game_loop", {});             // tell server to start
    window.location.href = "/quizgame/game";
  });
