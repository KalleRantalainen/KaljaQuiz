const socket = io();

socket.on('connect', () => {
    console.log('Connected to server, emitting player_ready');
    socket.emit('player_ready', {"test": "test"});

    //Tyylii turha emit join lobby
    //socket.emit("join_lobby", { player_id: "{{ user_id }}" });
    console.log(" === Pelaaja {{ user_id }} liittyi lobbyyn");
});


// Functiot ja tulevat alle -------------------

function loadPlayerView(viewName) {
    fetch(`/quizgame/player_partial/${viewName}`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('submit-container').innerHTML = html;
        });
}