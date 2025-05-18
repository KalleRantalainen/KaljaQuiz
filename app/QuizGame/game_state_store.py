class GameStateStore():
    def __init__(self):
        self.current_player_count = 0
        self.is_game_active = False

    def increase_player_count(self):
        self.current_player_count += 1
    
    def get_player_count(self):
        return self.current_player_count
    
    def get_game_status(self):
        # Onko peli käynnissä
        return self.is_game_active

gameStateStore = GameStateStore()
