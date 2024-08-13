import pygame
import random
from card import Card

CARD_WIDTH = 60
CARD_HEIGHT = 90
CARD_SPACING = 10

class Bot:
    def __init__(self, position, screen_width, screen_height, remaning_cards):
        self.position = position
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cards = random.sample(remaning_cards, 13)
        for card in self.cards:
            remaning_cards.remove(card)

    def draw(self, screen):
        if self.position == "top":
            self.draw_top(screen)
        elif self.position == "left":
            self.draw_left(screen)
        elif self.position == "right":
            self.draw_right(screen)
    
    def draw_top(self, screen):
        total_width = len(self.cards) * CARD_WIDTH + (len(self.cards) - 1) * CARD_SPACING
        start_x = (self.screen_width - total_width) // 2
        y = 20
        for i, card in enumerate(self.cards):
            x = start_x + i * (CARD_WIDTH + CARD_SPACING)
            screen.blit(card.image, (x, y))

    def draw_left(self, screen):
        total_height = len(self.cards) * CARD_HEIGHT + (len(self.cards) - 1) * CARD_SPACING
        start_y = (total_height - self.screen_height) // 2
        x = 400
        for i, card in enumerate(self.cards):
            rotated_image = pygame.transform.rotate(card.image, 270)  
            y = start_y + i * (CARD_WIDTH + CARD_SPACING)
            screen.blit(rotated_image, (x, y))

    def draw_right(self, screen):
        total_height = len(self.cards) * CARD_HEIGHT + (len(self.cards) - 1) * CARD_SPACING
        start_y = (total_height - self.screen_height) // 2
        x = self.screen_width - CARD_HEIGHT - 400  
        for i, card in enumerate(self.cards):
            rotated_image = pygame.transform.rotate(card.image, 90)  
            y = start_y + i * (CARD_WIDTH + CARD_SPACING)
            screen.blit(rotated_image, (x, y))