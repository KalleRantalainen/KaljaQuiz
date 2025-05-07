from QuizGameLogic.GameStateStore import GameStateStore

# Object to store the user's scores, answers, etc.
# Luodaan täällä, että saadaan ns. globaali muuttuja tästä
# joka ei nollaudu kesken pelin.
game_state_store = GameStateStore()