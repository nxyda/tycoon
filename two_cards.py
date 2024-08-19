class TwoCardsGame:
    def __init__(self, game):
        self.game = game

    def play_turn(self, bot):
        print(f"Bot {self.game.current_player} is playing...")

        if not self.game.played_cards:
            pair_to_play = self.find_pair(bot)
            if pair_to_play:
                print(f"Bot {self.game.current_player} plays pair: {pair_to_play[0].value}")
                for card in pair_to_play:
                    self.game.played_cards.append(card)
                    bot.cards.remove(card)
                self.game.last_player = self.game.current_player
                self.game.passed[self.game.current_player] = False
            else:
                print(f"Bot {self.game.current_player} passes")
                self.game.passed[self.game.current_player] = True
        else:
            valid_pairs = self.find_valid_pairs(bot)
            if valid_pairs:
                pair_to_play = min(valid_pairs, key=lambda pair: pair[0].value)
                print(f"Bot {self.game.current_player} plays pair: {pair_to_play[0].value}")
                for card in pair_to_play:
                    self.game.played_cards.append(card)
                    bot.cards.remove(card)
                self.game.last_player = self.game.current_player
                self.game.passed[self.game.current_player] = False
            else:
                print(f"Bot {self.game.current_player} passes")
                self.game.passed[self.game.current_player] = True

    def find_pair(self, bot):
        card_counts = {}
        for card in bot.cards:
            if card.value in card_counts:
                card_counts[card.value].append(card)
            else:
                card_counts[card.value] = [card]
        for value, cards in card_counts.items():
            if len(cards) >= 2:
                return cards[:2]
        return None

    def find_valid_pairs(self, bot):
        valid_pairs = []
        for card in bot.cards:
            potential_pairs = [c for c in bot.cards if c.value == card.value and c != card]
            if potential_pairs:
                pair = (card, potential_pairs[0])
                if pair[0].value > self.game.played_cards[-1].value:
                    valid_pairs.append(pair)
        return valid_pairs
