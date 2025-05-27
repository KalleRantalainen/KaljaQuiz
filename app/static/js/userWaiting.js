// TÄnne täytyy saada socket io event joka kuuntelee start_quiz_game eventtiä
const socket = io();

//const currentGame = "{{current_game}}";
const currentGame = document.getElementById("game-info").dataset.game;
console.log("EMITTING JOIN ", currentGame);

// Varalta nyt jää tälleen
if (currentGame === "quizgame") {
    socket.emit("join_game_lobby");
} else if (currentGame === "coinflip") {
    socket.emit("join_game_lobby");
} else {
    console.log("HOST EI OLE VIELÄ VALINNUT PELIÄ")
}

// Jos host valitsee pelin ja pelaajia on jo liittynyt:
socket.on("set_game_room", (data) => {
    const ROOM = data.ROOM;
    console.log("Game selected by host:", ROOM);

    if (ROOM === "quizgame") {
        console.log("EMITTING JOIN ", ROOM);
    } else if (ROOM === "coinflip") {
        console.log("EMITTING JOIN ", ROOM);
    } else {
        return
    }

    socket.emit("join_game_lobby")
});

// Kuunnellaan start_quizgame eventtiä ja siirrytään oikeaan näkymään
// -> Muillekkin peleille voi tehdä tänne samanlaisen eventin kuuntelun
//    jos ne vaatii socketteja
socket.on('start_quizgame', () => {
    console.log("Pelaaja otti vastaan start_quizgame eventin");
    window.location.href = '/quizgame/player_game';
});

socket.on("start_coinflip", () => {
    console.log("Received start_coinflip, redirecting...");
    window.location.href = "/coinflip/..";
});