const socket = io();

socket.on('connect', () => {
    console.log('Connected to server, emitting player_ready');
    socket.emit('player_ready', {"test": "test"});

    //Tyylii turha emit join lobby
    socket.emit("join_lobby", { player_id: "{{ user_id }}" });
    console.log(" === Pelaaja {{ user_id }} liittyi lobbyyn");
});

// Pelaajat saavat vastauslaatikon
socket.on('next_submit', () => {
    console.log("Pelaaja otti vastaan next_question, submit box esillä")

    loadPlayerView("submit")
})


// Functiot ja tulevat alle -------------------

function loadPlayerView(viewName) {
    fetch(`/quizgame/player_partial/${viewName}`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('submit-container').innerHTML = html;
        });
}

function submitAnswer() {
    const answer = document.getElementById('player-answer').value.trim();
    if (answer) {
        // TODO: emit via Socket.IO, for example:
        // socket.emit('player_answer', { answer });

        console.log("Submitted answer:", answer);
        
        // Optionally clear input or show confirmation
        document.getElementById('player-answer').value = '';
    }
}