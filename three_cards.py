class ThreeCardsGame:
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
            triplet_to_play = self.find_triplet(bot)
            if triplet_to_play:
                print(f"Bot {self.game.current_player} plays triplet: {triplet_to_play[0].value}")
                for card in triplet_to_play:
                    self.game.played_cards.append(card)
                    bot.cards.remove(card)
                self.game.last_player = self.game.current_player
                self.game.passed[self.game.current_player] = False
            else:
                print(f"Bot {self.game.current_player} passes")
                self.game.passed[self.game.current_player] = True
        else:
            valid_triplets = self.find_valid_triplets(bot)
            if valid_triplets:
                triplet_to_play = min(valid_triplets, key=lambda triplet: triplet[0].value)
                print(f"Bot {self.game.current_player} plays triplet: {triplet_to_play[0].value}")
                for card in triplet_to_play:
                    self.game.played_cards.append(card)
                    bot.cards.remove(card)
                self.game.last_player = self.game.current_player
                self.game.passed[self.game.current_player] = False
            else:
                print(f"Bot {self.game.current_player} passes")
                self.game.passed[self.game.current_player] = True

    def find_triplet(self, bot):
        card_counts = {}
        for card in bot.cards:
            if card.value in card_counts:
                card_counts[card.value].append(card)
            else:
                card_counts[card.value] = [card]
        for value, cards in card_counts.items():
            if len(cards) >= 3:
                return cards[:3]
        return None

    def find_valid_triplets(self, bot):
        valid_triplets = []
        for card in bot.cards:
            potential_triplets = [c for c in bot.cards if c.value == card.value and c != card]
            if len(potential_triplets) >= 2:
                triplet = (card, potential_triplets[0], potential_triplets[1])
                if triplet[0].value > self.game.played_cards[-1].value:
                    valid_triplets.append(triplet)
        return valid_triplets
