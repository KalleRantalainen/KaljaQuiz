class GameStateStore():
    def __init__(self):
        self.current_player_count = 0

    def increase_player_count(self):
        self.current_player_count += 1
    
    def get_player_count(self):
        return self.current_player_count

gameStateStore = GameStateStore()
