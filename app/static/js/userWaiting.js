// TÄnne täytyy saada socket io event joka kuuntelee start_quiz_game eventtiä
const socket = io();

console.log("@@@@@@@EMITTING join_lobby from app/templates/user_waiting.html");
// Emit event join lobby

socket.emit("join_lobby", { player_id: "{{ user_id }}" });


// Kuunnellaan start_quizgame eventtiä ja siirrytään oikeaan näkymään
// -> Muillekkin peleille voi tehdä tänne samanlaisen eventin kuuntelun
//    jos ne vaatii socketteja
socket.on('start_quizgame', () => {
    console.log("Pelaaja otti vastaan start_quizgame eventin");
    window.location.href = '/quizgame/player_game';
});

socket.on("start_coinflip", () => {
    socket.emit("join_coinflip_room")
    console.log("Received start_coinflip, redirecting...");
    window.location.href = "/coinflipperZ/coin";
});