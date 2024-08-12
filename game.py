import pygame
import random
from card import Card

WHITE = (255, 255, 255)
CARD_WIDTH = 60
CARD_HEIGHT = 90
CARD_SPACING = 20

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.cards = Card.load_cards()
        self.random_cards = random.sample(self.cards, 14)
        self.played_card = None

    def draw_cards(self):
        total_width = 14 * CARD_WIDTH + (13 * CARD_SPACING)
        start_x = (self.screen_width - total_width) // 2
        y = self.screen_height - CARD_HEIGHT - 20  

        for i, card in enumerate(self.random_cards):
            x = start_x + i * (CARD_WIDTH + CARD_SPACING)
            self.screen.blit(card.image, (x, y))
            card.rect = pygame.Rect(x, y, CARD_HEIGHT, CARD_WIDTH)

        if self.played_card:
            center_x = (self.screen_width - CARD_WIDTH) // 2
            center_y = (self.screen_height - CARD_HEIGHT) // 2
            self.screen.blit(self.played_card.image, (center_x, center_y))
        
    def handle_click(self, pos):
        for card in self.random_cards:
            if card.rect.collidepoint(pos):
                self.played_card = card
                self.random_cards.remove(card)
                break