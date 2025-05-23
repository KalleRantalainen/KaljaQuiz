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
            // Jos partial on ladattu tälleen ^^^ niin ajastin scriptit on pakko ladata
            // myös täälä, koska suoraan partial html tiedostossa se ei toimi

            // AFTER partial is inserted, manually run any scripts:
            if (viewName === 'submit') {
                import('/quizgame/static/js/timer.js')
                    .then(module => {
                        const display = document.getElementById('timer');
                        if (display) {
                            module.startTimer(60, display, () => {
                                console.log("Timer ended!");
                            });
                        } else {
                            console.warn("No #timer element found.");
                        }
                    })
                    .catch(err => console.error("Failed to load timer module:", err));
            }
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
            const currentUserId = document.getElementById('answers-container').dataset.userId;

            const answersList = document.getElementById('answers');
            answersList.innerHTML = ''; // Clear previous

            playerAnswers.forEach(player => {
                
                const li = document.createElement("li");
                const button = document.createElement("button");
                button.textContent = player.answer;

                // Näytetään pelaajalle myös oma vastaus mutta ei pysty äänestämään
                if(player.user_id === currentUserId) {
                    button.onclick = () => {                    
                    console.log("PELAAJA ÄÄNESTI PELAAJAN KOITTI ÄÄNESTÄÄ ITSEÄÄN");
                    };
                }
                else {
                    button.onclick = () => {
                    vote(player);
                    console.log("PELAAJA ÄÄNESTI PELAAJAN ", player.name, " VASTAUSTA");
                    };
                }

                li.appendChild(button);
                answersList.appendChild(li);
            });

            //Lisätään oikea vastaus myös listaan
            const li = document.createElement("li");
            const button = document.createElement("button");
            button.textContent = correctAnswer;
            button.onclick = () => {
                console.log("Pelaaja valitsi tietokoneen vastauksen")
                // +1 piste
                socket.emit("voted_real_answer")
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