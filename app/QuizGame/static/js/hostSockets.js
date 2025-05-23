// Tänne täytyy tehdä socket io event joka emittoi start_quiz_game eventin kun painetaan start_game nappia
const socket = io();

function loadView(viewName) {
    fetch(`/quizgame/host_partial/${viewName}`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('main-container').innerHTML = html;

            if (viewName === "waiting") {
                document.getElementById("start_game").addEventListener("click", startGame);
                if (typeof startPollingPlayers === "function") startPollingPlayers();
            } else {
                if (typeof stopPollingPlayers === "function") stopPollingPlayers();
            }
        });
}

// Emittoi start_quizgame, kun host painaa nappia.
// Pelaajat ottavat tämän vastaan waiting roomissa ja siirtyvät quizgame_player näkymään.
// itse eventin broadcastays tapahtuu sockets.py tiedostosta, että se lähtee pelaajille.
function startGame() {
    socket.emit('start_quizgame', {"test": "test"});
    console.log("HOST EMIT start_quizgame");

    //Host liittyy lobbyyn
    socket.emit("join_lobby", { player_id: "{{ host_id }}" });
    console.log("HOST EMIT join_game (host joins the game room)");

    
}

socket.on('start_game', async () => {
    console.log("HOST otti vastaan start_game eventin");
    // Tää vois olla countdown pelaajille 5..4..3..2..1
    loadView("host_question")
});


// Aloittaa seuraavan kysymyksen      
socket.on('next_question', () => {
    console.log("Pelaajat otti vastaan next_question")
    loadQuestion();  // Later: use server state or timer to pass the real question index
    console.log("Kysymys näkyvissä")

})

// Partiaali kysymyksen näyttämiselle
function loadQuestion() {
    fetch(`/quizgame/quest_partial`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('question-container').innerHTML = html;
        });

    console.log("Kysymyksen lataaminen onnistui!")
}


//vastaukset
function loadAnswersView(correctAnswer, playerAnswers) {
    fetch(`/quizgame/show_answers_partial`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('question-container').innerHTML = html;

            // Insert correct answer
            document.getElementById('correct-answer').textContent = correctAnswer;

            // Insert player answers
            const answersList = document.getElementById('player-answers');
            answersList.innerHTML = ''; // Clear previous

            playerAnswers.forEach(player => {
                const item = document.createElement('li');
                item.textContent = `${player.name}: ${player.answer || '—'}`;
                answersList.appendChild(item);
            });
            
            const nextBtn = document.getElementById("round-results-btn");
            if (nextBtn) {
                nextBtn.addEventListener("click", () => {
                    console.log("Host pressed load round results button");
                    loadRoundResult();
                });
            } else {
                console.log("Next Question button not found");
            }
        });
}

socket.on('answers', (data) => {
    console.log("LADATAAN PELAAJIEN VASTAUKSET:", data.answer);
    loadAnswersView(data.correct_answer, data.player_answers);
});


function on_show_answers(button) {
    const question = button.getAttribute('data-question');
    console.log("Host pressed show answers");

    // Kuljetetaan kysymys jotta sen avulla saadaan vastaus
    socket.emit('show_answers', { question: question });

}


window.addEventListener("DOMContentLoaded", () => {
    loadView("waiting");
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


function loadRoundResult() {
        fetch(`/quizgame/round_result_partial`)
        .then(response => response.text())
        .then(html => {
            document.getElementById('question-container').innerHTML = html;
            
            const nextBtn = document.getElementById("next-question-btn");
            if (nextBtn) {
                nextBtn.addEventListener("click", () => {
                    console.log("Host pressed next question after results where shown");
                    loadQuestion();
                    socket.emit('next_submit');
                });
            } else {
                console.log("Next Question button not found");
            }
        });
}