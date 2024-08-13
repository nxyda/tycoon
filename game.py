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
        for card in self.player_cards:
            if card.rect.collidepoint(pos):
                if not self.played_cards or card.value > self.played_cards[-1].value:
                    self.played_cards.append(card)
                    self.player_cards.remove(card)
                break
