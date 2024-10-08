import pygame
import random
from card import Card

CARD_WIDTH = 60
CARD_HEIGHT = 90
CARD_SPACING = 10

class Bot:
    def __init__(self, position, screen_width, screen_height, remaining_cards):
        self.position = position
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cards = random.sample(remaining_cards, 13)
        for card in self.cards:
            remaining_cards.remove(card)
        self.card_back_image = pygame.image.load("cards/back.png")
        self.card_back_image = pygame.transform.scale(self.card_back_image, (CARD_WIDTH, CARD_HEIGHT))
        

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
            screen.blit(self.card_back_image, (x, y))

    def draw_left(self, screen):
        total_height = len(self.cards) * CARD_WIDTH + (len(self.cards) - 1) * CARD_SPACING
        start_y = (self.screen_height // 2) - (total_height // 2)
        x = 400
        for i, card in enumerate(self.cards):
            rotated_image = pygame.transform.rotate(self.card_back_image, 90)
            y = start_y + i * (CARD_WIDTH + CARD_SPACING)
            screen.blit(rotated_image, (x, y))

    def draw_right(self, screen):
        total_height = len(self.cards) * CARD_WIDTH + (len(self.cards) - 1) * CARD_SPACING
        start_y = (self.screen_height // 2) - (total_height // 2)
        x = self.screen_width - CARD_HEIGHT - 400
        for i, card in enumerate(self.cards):
            rotated_image = pygame.transform.rotate(self.card_back_image, 270)
            y = start_y + i * (CARD_WIDTH + CARD_SPACING)
            screen.blit(rotated_image, (x, y))

    def reset(self, remaining_cards):
        self.cards = random.sample(remaining_cards, 13)
        remaining_cards[:] = [card for card in remaining_cards if card not in self.cards]
