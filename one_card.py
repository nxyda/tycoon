class OneCardGame:
    def __init__(self, game):
        self.game = game

    def play_turn(self, bot):
        print(f"Bot {self.game.current_player} is playing...")

        if not self.game.played_cards:
            card_to_play = min(bot.cards, key=lambda c: c.value)
            print(f"Bot {self.game.current_player} plays card: {card_to_play.value}")
        else:
            valid_cards = [card for card in bot.cards if card.value > self.game.played_cards[-1].value]
            if valid_cards:
                card_to_play = min(valid_cards, key=lambda c: c.value)
                print(f"Bot {self.game.current_player} plays card: {card_to_play.value}")
                self.game.last_player = self.game.current_player
            else:
                print(f"Bot {self.game.current_player} passes")
                self.game.passed[self.game.current_player] = True
                return

        self.game.played_cards.append(card_to_play)
        bot.cards.remove(card_to_play)
        self.game.passed[self.game.current_player] = False
