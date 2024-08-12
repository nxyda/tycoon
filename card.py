import pygame
import os

CARD_WIDTH = 60
CARD_HEIGHT = 90

class Card:
    def __init__(self, suit, value, image):
        self.suit = suit
        self.value = value
        self.image = image
        self.image = pygame.transform.scale(self.image, (CARD_WIDTH, CARD_HEIGHT))
        self.rect = None

    def load_cards():
        card_folders = ['c', 'd', 'h', 's']
        cards = []

        for folder in card_folders:
            folder_path = os.path.join('cards', folder)
            for filename in os.listdir(folder_path):
                if filename.endswith('.png'):
                    suit = folder  
                    value = filename[:-4]  
                    image = pygame.image.load(os.path.join(folder_path, filename))
                    card = Card(suit, value, image)
                    cards.append(card)
        
        return cards