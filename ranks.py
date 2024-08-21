class Ranks:
    RANKS = ["Tycoon", "Rich", "Commoner", "Poor", "Beggar"]

    def __init__(self):
        self.rankings = {
            'player': "Commoner",
            'bot1': "Commoner",
            'bot2': "Commoner",
            'bot3': "Commoner"
        }

    def update_ranks(self, finished_order):
        if len(finished_order) == 4:
            self.rankings[finished_order[0]] = "Tycoon"
            self.rankings[finished_order[1]] = "Rich"
            self.rankings[finished_order[2]] = "Poor"
            self.rankings[finished_order[3]] = "Beggar"

    def get_rank(self, player):
        return self.rankings[player]

    def reset_ranks(self):
        for player in self.rankings:
            self.rankings[player] = "Commoner"
