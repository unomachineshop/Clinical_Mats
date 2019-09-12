class Game_Manager:
    
    def __init__(self, running, game_state):
        # Game loop
        self.running = running

        # Game state
        self.game_state = game_state
        
        # Countdown timer
        self.timer = 5
        self.start_ticks = 0

        # Trial selection
        self.trial_type = 1

        # Target mat
        self.target_mat = 0

        # Used to switch sides, dependent on algorithm
        # (ex: Switching from Top to Bottom logic)
        # (ex: Switching from Left to Right logic)
        self.switch = True

        # Trial step counter
        self.steps = 0

        # Trial timer
        self.trial_timer_start_ticks = 0
        self.trial_timer = 0

    def reset(self):
        self.game_state = 1
        self.timer = 5
        self.start_ticks = 0
        self.trial_type = 1
        self.target_mat = 0
        self.switch = True
        self.count = 1
        self.steps = 0
        self.trial_timer_start_ticks = 0
        self.trial_timer = 0
