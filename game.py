import pygame
import random
from card import Card
from bot import Bot
from animation import Animation

WHITE = (255, 255, 255)
CARD_WIDTH = 60
CARD_HEIGHT = 90
CARD_SPACING = 10
BUTTON_COLOR = (200, 0, 0)
BUTTON_HOVER_COLOR = (150, 0, 0)


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
        self.current_player = 'player'
        self.passed = {
            'player': False,
            'bot1': False,
            'bot2': False,
            'bot3': False
        }

        self.font = pygame.font.SysFont(None, 36)

        self.animation = Animation()
        self.selected_card = None

        self.pulled_card = None
        self.pulled_card_original_position = None

        self.accept_button_rect = pygame.Rect(150, self.screen_height - 60, 140, 50)
        self.pass_button_rect = pygame.Rect(self.screen_width - 150, self.screen_height - 60, 140, 50)

    def draw_cards(self):
        total_width = len(self.player_cards) * CARD_WIDTH + (len(self.player_cards) - 1) * CARD_SPACING
        start_x = (self.screen_width - total_width) // 2
        y = self.screen_height - CARD_HEIGHT - CARD_SPACING

        for i, card in enumerate(self.player_cards):
            x = start_x + i * (CARD_WIDTH + CARD_SPACING)
            y = self.screen_height - CARD_HEIGHT - CARD_SPACING

            if card == self.pulled_card:
                x, y = card.rect.topleft  # Użyj pozycji wysuniętej karty
            else:
                card.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            self.screen.blit(card.image, (x, y))

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

        self.draw_pass_info()
        self.draw_accept_button()
        self.draw_pass_button()

    def draw_pass_info(self):
        passed_count = sum(1 for player in self.passed.values() if player)
        pass_text = f"Pass: {passed_count}/4"
        text_surface = self.font.render(pass_text, True, WHITE)
        self.screen.blit(text_surface, (10, self.screen_height - 50))

    def draw_accept_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.accept_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR, self.accept_button_rect)
        else:
            pygame.draw.rect(self.screen, BUTTON_COLOR, self.accept_button_rect)

        text = self.font.render("Accept", True, WHITE)
        text_rect = text.get_rect(center=self.accept_button_rect.center)
        self.screen.blit(text, text_rect)

    def draw_pass_button(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.pass_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR, self.pass_button_rect)
        else:
            pygame.draw.rect(self.screen, BUTTON_COLOR, self.pass_button_rect)

        text = self.font.render("Pass", True, WHITE)
        text_rect = text.get_rect(center=self.pass_button_rect.center)
        self.screen.blit(text, text_rect)

    def handle_button_click(self, pos):
        if self.accept_button_rect.collidepoint(pos):
            if self.pulled_card:
                self.played_cards.append(self.pulled_card)
                self.player_cards.remove(self.pulled_card)
                self.pulled_card = None
                self.pulled_card_original_position = None
                self.animation.reset_card()
                self.passed['player'] = False
                self.current_player = self.get_next_player()
        elif self.pass_button_rect.collidepoint(pos):
            self.pass_turn()

    def handle_click(self, pos):
        if self.current_player == 'player':
            # Obsługuje kliknięcie przycisków
            self.handle_button_click(pos)
            
            for card in self.player_cards:
                if card.rect.collidepoint(pos):
                    # Jeśli karta nie jest wysunięta, wyciągnij ją
                    if self.pulled_card is None:
                        if not self.played_cards or card.value > self.played_cards[-1].value:
                            self.pulled_card = card
                            self.pulled_card_original_position = card.rect.topleft
                            self.animation.select_card(card)
                    # Jeśli karta jest wysunięta, przywróć ją na pierwotne miejsce
                    elif card == self.pulled_card:
                        self.pulled_card.rect.topleft = self.pulled_card_original_position
                        self.pulled_card = None
                        self.pulled_card_original_position = None
                    break

    def pass_turn(self):
        self.passed[self.current_player] = True
        self.current_player = self.get_next_player()
        if self.all_bots_passed() and self.passed['player']:
            self.reset_round()
        else:
            if self.current_player != 'player':
                self.play_turn()

    def get_next_player(self):
        if self.current_player == 'player':
            return 'bot1'
        elif self.current_player == 'bot1':
            return 'bot2'
        elif self.current_player == 'bot2':
            return 'bot3'
        elif self.current_player == 'bot3':
            return 'player'
        return 'player'

    def all_bots_passed(self):
        return all(self.passed[player] for player in ['bot1', 'bot2', 'bot3'])

    def reset_round(self):
        self.played_cards = []
        self.passed = {
            'player': False,
            'bot1': False,
            'bot2': False,
            'bot3': False
        }

    def play_turn(self):
        while True:
            if self.current_player == 'player':
                break

            if self.current_player == 'bot1':
                self.play_bot_turn(self.bot1)
            elif self.current_player == 'bot2':
                self.play_bot_turn(self.bot2)
            elif self.current_player == 'bot3':
                self.play_bot_turn(self.bot3)

            self.current_player = self.get_next_player()

            if self.all_bots_passed() and self.passed['player']:
                self.reset_round()
                break

            if self.current_player == 'player':
                break

    def play_bot_turn(self, bot):
        print(f"Bot {self.current_player} is playing...")

        if not self.played_cards:
            card_to_play = min(bot.cards, key=lambda c: c.value)
            print(f"Bot {self.current_player} plays card: {card_to_play.value}")
        else:
            valid_cards = [card for card in bot.cards if card.value > self.played_cards[-1].value]
            if valid_cards:
                card_to_play = min(valid_cards, key=lambda c: c.value)
                print(f"Bot {self.current_player} plays card: {card_to_play.value}")
            else:
                print(f"Bot {self.current_player} passes")
                self.passed[self.current_player] = True
                return

        self.played_cards.append(card_to_play)
        bot.cards.remove(card_to_play)
        self.passed[self.current_player] = False

    def update(self):
        self.animation.move_card()
