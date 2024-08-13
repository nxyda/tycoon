import pygame
import random
from card import Card
from bot import Bot

WHITE = (255, 255, 255)
CARD_WIDTH = 60
CARD_HEIGHT = 90
CARD_SPACING = 10

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()

        self.cards = Card.load_cards()
        self.player_cards = random.sample(self.cards, 13)
        remaining_cards = [card for card in self.cards if card not in self.player_cards]

        self.bot1 = Bot('top', self.screen_width, self.screen_height, remaining_cards)
        self.bot2 = Bot('left', self.screen_width, self.screen_height, remaining_cards)
        self.bot3 = Bot('right', self.screen_width, self.screen_height, remaining_cards)

        self.played_cards = []
        self.current_player = 'player'  # 'player', 'bot1', 'bot2', 'bot3'

    def draw_cards(self):
        total_width = len(self.player_cards) * CARD_WIDTH + (len(self.player_cards) - 1) * CARD_SPACING
        start_x = (self.screen_width - total_width) // 2
        y = self.screen_height - CARD_HEIGHT - CARD_SPACING

        for i, card in enumerate(self.player_cards):
            x = start_x + i * (CARD_WIDTH + CARD_SPACING)
            self.screen.blit(card.image, (x, y))
            card.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

        self.bot1.draw(self.screen)
        self.bot2.draw(self.screen)
        self.bot3.draw(self.screen)

        positions = [
            (0, -CARD_HEIGHT // 2),
            (CARD_WIDTH // 2, 0),
            (0, CARD_HEIGHT // 2),
            (-CARD_WIDTH // 2, 0)
        ]

        center_x = (self.screen_width - CARD_WIDTH) // 2
        center_y = (self.screen_height - CARD_HEIGHT) // 2
        for i, card in enumerate(self.played_cards):
            pos_index = i % 4
            offset_x, offset_y = positions[pos_index]
            x = center_x + offset_x
            y = center_y + offset_y
            self.screen.blit(card.image, (x, y))

    def handle_click(self, pos):
        if self.current_player == 'player':
            for card in self.player_cards:
                if card.rect.collidepoint(pos):
                    if not self.played_cards or card.value > self.played_cards[-1].value:
                        self.played_cards.append(card)
                        self.player_cards.remove(card)
                        self.current_player = 'bot1'  # Change to the next player
                    break

    def play_turn(self):
        if self.current_player == 'bot1':
            self.play_bot_turn(self.bot1)
            self.current_player = 'bot2'
        elif self.current_player == 'bot2':
            self.play_bot_turn(self.bot2)
            self.current_player = 'bot3'
        elif self.current_player == 'bot3':
            self.play_bot_turn(self.bot3)
            self.current_player = 'player'

    def play_bot_turn(self, bot):
        if not self.played_cards:
            # If no cards have been played yet, the bot plays the lowest card
            card_to_play = min(bot.cards, key=lambda c: c.value)
        else:
            # Filter out cards that cannot be played
            valid_cards = [card for card in bot.cards if card.value > self.played_cards[-1].value]
            if valid_cards:
                card_to_play = min(valid_cards, key=lambda c: c.value)
            else:
                # If no valid card, the bot cannot play
                return

        self.played_cards.append(card_to_play)
        bot.cards.remove(card_to_play)
