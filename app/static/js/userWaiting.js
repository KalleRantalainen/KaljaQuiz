// TÄnne täytyy saada socket io event joka kuuntelee start_quiz_game eventtiä
const socket = io();

//const currentGame = "{{current_game}}";
const currentGame = document.getElementById("game-info").dataset.game;
console.log("EMITTING JOIN ", currentGame);


if (currentGame === "quizgame") {
    socket.emit("join_quizgame_lobby");
} else if (currentGame === "coinflipperZ") {
    socket.emit("join_coinflip_lobby");
} else {
    console.log("HOST EI OLE VIELÄ VALINNUT PELIÄ")
}

// Jos host ei ole vielä valinnut peliä niin:
socket.on("set_game_room", (data) => {
    const ROOM = data.ROOM;
    console.log("Game selected by host:", ROOM);

    if (ROOM === "quizgame") {
        console.log("EMITTING JOIN ", ROOM);
        socket.emit("join_quizgame_lobby");
    } else if (ROOM === "coinflip") {
        console.log("EMITTING JOIN ", ROOM);
        socket.emit("join_coinflip_room");
    }
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
    window.location.href = "/coinflipperZ/coin";
});