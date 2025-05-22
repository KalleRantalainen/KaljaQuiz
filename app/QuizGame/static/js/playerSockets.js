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


socket.on('answers', (data) => {
    //Pelaajien äänestysvaihe alkaa tästä
    votingPhase(data.correct_answer, data.player_answers);
});

// Functiot ja tulevat alle -------------------

function loadPlayerView(viewName) {
    console.log("Loading partial for", viewName); // DEBUG
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
        socket.emit('return_player_answer', { answer });

        console.log("Submitted answer:", answer);
        
        // Optionally clear input or show confirmation
        document.getElementById('player-answer').value = '';
        loadPlayerView("answerSubmitted")
    }
}

function votingPhase(correctAnswer, playerAnswers) {
    fetch(`/quizgame/voting_phase_partial`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('submit-container').innerHTML = html;

            // Luodaan lista vastauksille --------------------------------
            const answersList = document.getElementById('answers');
            answersList.innerHTML = ''; // Clear previous

            playerAnswers.forEach(player => {

                const li = document.createElement("li");
                const button = document.createElement("button");

                button.textContent = player.answer;
                button.onclick = () => {
                    // 
                    vote(player);
                    
                    console.log("PELAAJA ÄÄNESTI PELAAJAN ", player.name, " VASTAUSTA");
                };

                li.appendChild(button);
                answersList.appendChild(li);
            });

            //Lisätään oikea vastaus myös listaan
            const li = document.createElement("li");
            const button = document.createElement("button");
            button.textContent = correctAnswer;
            button.onclick = () => {
                //TODO !!!!!!
                console.log("Pelaaja valitsi tietokoneen vastauksen")
                "Väliaikainen loadPlayerViev. Pitää saada piste tästä"
                loadPlayerView('afterVotingScreen')
            }
            li.appendChild(button);
            answersList.appendChild(li);
            //-------------------------------------------------------------
        });
}

// PLayer voted
function vote(player){
    socket.emit("voted_a_player", {voted_player: player.user_id})
    loadPlayerView('afterVotingScreen')
}