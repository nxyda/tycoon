class FourCardsGame:
    def __init__(self, game):
        self.game = game

    def play_turn(self, bot):
        print(f"Bot {self.game.current_player} is playing...")

        if not bot.cards:
            print(f"Bot {self.game.current_player} has no more cards and passes.")
            self.game.passed[self.game.current_player] = True
            return
        else:
            self.game.check_if_player_finished(self.game.current_player)

        if not self.game.played_cards:
            quartet_to_play = self.find_quartet(bot)
            if quartet_to_play:
                print(f"Bot {self.game.current_player} plays quartet: {quartet_to_play[0].value}")
                for card in quartet_to_play:
                    self.game.played_cards.append(card)
                    bot.cards.remove(card)
                self.game.last_player = self.game.current_player
                self.game.passed[self.game.current_player] = False
            else:
                print(f"Bot {self.game.current_player} passes")
                self.game.passed[self.game.current_player] = True
        else:
            valid_quartets = self.find_valid_quartets(bot)
            if valid_quartets:
                quartet_to_play = min(valid_quartets, key=lambda quartet: quartet[0].value)
                print(f"Bot {self.game.current_player} plays quartet: {quartet_to_play[0].value}")
                for card in quartet_to_play:
                    self.game.played_cards.append(card)
                    bot.cards.remove(card)
                self.game.last_player = self.game.current_player
                self.game.passed[self.game.current_player] = False
            else:
                print(f"Bot {self.game.current_player} passes")
                self.game.passed[self.game.current_player] = True

    def find_quartet(self, bot):
        card_counts = {}
        for card in bot.cards:
            if card.value in card_counts:
                card_counts[card.value].append(card)
            else:
                card_counts[card.value] = [card]
        for value, cards in card_counts.items():
            if len(cards) >= 4:
                return cards[:4]
        return None

    def find_valid_quartets(self, bot):
        valid_quartets = []
        for card in bot.cards:
            potential_quartets = [c for c in bot.cards if c.value == card.value and c != card]
            if len(potential_quartets) >= 3:
                quartet = (card, potential_quartets[0], potential_quartets[1], potential_quartets[2])
                if quartet[0].value > self.game.played_cards[-1].value:
                    valid_quartets.append(quartet)
        return valid_quartets
