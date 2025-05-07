
class GameStateStore():
    def __init__(self):
        self.scoreboard = {}
        self.questions_and_answers = {}
        self.current_question = 0
        self.players = []
    
    # Metodeja koko paskan nollaamiseen, pisteiden hakuun,
    # kysymysten hakuun etc.
