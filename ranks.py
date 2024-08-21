class Ranks:
    RANKS = ["Tycoon", "Rich", "Commoner", "Poor", "Beggar"]
    POINTS = [30, 20, 10, 0] 

    def __init__(self):
        self.rankings = {
            'player': "Commoner",
            'bot1': "Commoner",
            'bot2': "Commoner",
            'bot3': "Commoner"
        }
        self.scores = {
            'player': 0,
            'bot1': 0,
            'bot2': 0,
            'bot3': 0
        }

    def update_ranks(self, finished_order):
        if len(finished_order) == 4:
            self.rankings[finished_order[0]] = "Tycoon"
            self.rankings[finished_order[1]] = "Rich"
            self.rankings[finished_order[2]] = "Poor"
            self.rankings[finished_order[3]] = "Beggar"

            for rank, player in enumerate(finished_order):
                self.scores[player] += self.POINTS[rank]

    def get_rank(self, player):
        return self.rankings[player]
    
    def get_score(self, player):
        return self.scores[player]

    def reset_ranks(self):
        for player in self.rankings:
            self.rankings[player] = "Commoner"

    def reset_scores(self):
        for player in self.scores:
            self.scores[player] = 0
