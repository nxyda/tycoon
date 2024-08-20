import pygame
import random
import math
from card import Card
from bot import Bot
from animation import Animation
from one_card import OneCardGame
from two_cards import TwoCardsGame
from three_cards import ThreeCardsGame

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
        self.last_player = None

        self.passed = {
            'player': False,
            'bot1': False,
            'bot2': False,
            'bot3': False
        }

        self.font = pygame.font.SysFont(None, 36)

        self.animation = Animation()
        self.selected_cards = []  

        self.pulled_card = None  
        self.pulled_card_original_position = None

        self.accept_button_rect = pygame.Rect(150, self.screen_height - 60, 140, 50)
        self.pass_button_rect = pygame.Rect(self.screen_width - 150, self.screen_height - 60, 140, 50)

        self.one_cards = False
        self.two_cards = False
        self.three_cards = False

        self.one_card_game = OneCardGame(self)
        self.two_cards_game = TwoCardsGame(self)
        self.three_cards_game = ThreeCardsGame(self)

        self.finished_order = []  

        self.joker_played = False


    def draw_cards(self):
        self.player_cards.sort(key=lambda card: card.value, reverse=True)

        total_width = len(self.player_cards) * CARD_WIDTH + (len(self.player_cards) - 1) * CARD_SPACING
        start_x = (self.screen_width - total_width) // 2
        y = self.screen_height - CARD_HEIGHT - CARD_SPACING

        for i, card in enumerate(self.player_cards):
            x = start_x + i * (CARD_WIDTH + CARD_SPACING)
            y = self.screen_height - CARD_HEIGHT - CARD_SPACING

            card.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
            self.screen.blit(card.image, (x, y))

            if card in self.selected_cards:  
                y -= 20
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

        if self.one_cards:
            center_x = (self.screen_width - CARD_WIDTH) // 2
            center_y = (self.screen_height - CARD_HEIGHT) // 2
            

            for i, card in enumerate(self.played_cards):
                pos_index = i % 4
                offset_x, offset_y = positions[pos_index]
                x = center_x + offset_x
                y = center_y + offset_y
                self.screen.blit(card.image, (x, y))

        elif self.two_cards:
            center_x = (self.screen_width - CARD_WIDTH) // 2
            center_y = (self.screen_height - CARD_HEIGHT) // 2

            for i, card in enumerate(self.played_cards):
                pos_index = i % 4
                offset_x, offset_y = positions[pos_index]
                x = center_x + offset_x
                y = center_y + offset_y 
                card.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
                self.screen.blit(card.image, card.rect.topleft)

        elif self.three_cards:
            center_x = (self.screen_width - CARD_WIDTH) // 2
            center_y = (self.screen_height - CARD_HEIGHT) // 2

            for i, card in enumerate(self.played_cards):
                pos_index = i % 4
                offset_x, offset_y = positions[pos_index]
                x = center_x + offset_x
                y = center_y + offset_y
                card.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
                self.screen.blit(card.image, card.rect.topleft)
        
        self.draw_pass_info()
        self.draw_accept_button()
        self.draw_pass_button()

        self.draw_positions()  

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

    def draw_positions(self):
        if 'player' in self.finished_order:
            self.draw_position_text(self.finished_order.index('player') + 1, self.screen_width // 2, self.screen_height - CARD_HEIGHT - 80)

        if 'bot1' in self.finished_order:
            self.draw_position_text(self.finished_order.index('bot1') + 1, self.screen_width // 2, 10)

        if 'bot2' in self.finished_order:
            self.draw_position_text(self.finished_order.index('bot2') + 1, 10, self.screen_height // 2)

        if 'bot3' in self.finished_order:
            self.draw_position_text(self.finished_order.index('bot3') + 1, self.screen_width - 60, self.screen_height // 2)

    def draw_position_text(self, position, x, y):
        position_texts = ["1st", "2nd", "3rd", "4th"]
        text_surface = self.font.render(position_texts[position - 1], True, WHITE)
        self.screen.blit(text_surface, (x, y))

    def handle_button_click(self, pos):
        if self.accept_button_rect.collidepoint(pos):
            if not self.played_cards:
                if len(self.selected_cards) == 1:
                    self.one_cards = True
                    self.two_cards = False
                    self.three_cards = False
                    played_card = self.selected_cards[0]
                    print("nie wchodzi")
                    if self.joker_played and played_card.suit == 's' and played_card.value == 3:
                        print("XD")
                        played_card.value = 101 

                    self.played_cards.append(played_card)
                    self.player_cards.remove(played_card)
                    self.selected_cards = []

                    if played_card.value == 8:  
                        self.played_cards = []
                        self.passed = {key: False for key in self.passed}
                        self.current_player = 'player'
                        print("Zagrano kartę 8, kolejka zresetowana. Gracz zaczyna od nowa.")
                    elif played_card.value == 100:
                        self.joker_played = True                
                    else:
                        self.passed['player'] = False
                        self.last_player = 'player'
                        self.check_if_player_finished('player')
                        self.current_player = self.get_next_player()

                elif len(self.selected_cards) == 2 and self.selected_cards[0].value == self.selected_cards[1].value:
                    self.one_cards = False
                    self.two_cards = True
                    self.three_cards = False
                    self.played_cards.extend(self.selected_cards)
                    for card in self.selected_cards:
                        self.player_cards.remove(card)
                    self.selected_cards = []
                    self.passed['player'] = False
                    self.last_player = 'player'
                    self.check_if_player_finished('player')
                    self.current_player = self.get_next_player()

                elif len(self.selected_cards) == 3 and len(set(card.value for card in self.selected_cards)) == 1:
                    self.one_cards = False
                    self.two_cards = False
                    self.three_cards = True
                    self.played_cards.extend(self.selected_cards)
                    for card in self.selected_cards:
                        self.player_cards.remove(card)
                    self.selected_cards = []
                    self.passed['player'] = False
                    self.last_player = 'player'
                    self.check_if_player_finished('player')
                    self.current_player = self.get_next_player()

                else:
                    print("To jest niepoprawny ruch. Musisz wybrać jedną kartę na start, dwie karty tej samej wartości, lub trzy karty tej samej wartości!")

            else:
                if self.three_cards:
                    if len(self.selected_cards) == 3 and len(set(card.value for card in self.selected_cards)) == 1:
                        if self.selected_cards[0].value > self.played_cards[-1].value:
                            if self.joker_played and self.selected_cards[0].suit == 's' and self.selected_cards[0].value == 3:
                                self.selected_cards[0].value = 101 
                            self.played_cards.extend(self.selected_cards)
                            for card in self.selected_cards:
                                self.player_cards.remove(card)
                            self.selected_cards = []
                            if self.played_cards[-1].value == 8:  
                                self.played_cards = []
                                self.passed = {key: False for key in self.passed}
                                self.current_player = 'player'
                                print("Zagrano kartę 8, kolejka zresetowana. Gracz zaczyna od nowa.")
                            else:
                                self.passed['player'] = False
                                self.last_player = 'player'
                                self.check_if_player_finished('player')
                                self.current_player = self.get_next_player()
                        else:
                            print("Możesz zagrać trzy karty tylko o wyższej wartości niż karty na stole!")
                    else:
                        print("Musisz zagrać trzy karty tej samej wartości!")

                elif self.two_cards:
                    if len(self.selected_cards) == 2 and self.selected_cards[0].value == self.selected_cards[1].value:
                        if self.selected_cards[0].value > self.played_cards[-1].value:
                            if self.joker_played and self.selected_cards[0].suit == 's' and self.selected_cards[0].value == 3:
                                self.selected_cards[0].value = 101  
                            self.played_cards.extend(self.selected_cards)
                            for card in self.selected_cards:
                                self.player_cards.remove(card)
                            self.selected_cards = []
                            if self.played_cards[-1].value == 8:  
                                self.played_cards = []
                                self.passed = {key: False for key in self.passed}
                                self.current_player = 'player'
                                print("Zagrano kartę 8, kolejka zresetowana. Gracz zaczyna od nowa.")
                            else:
                                self.passed['player'] = False
                                self.last_player = 'player'
                                self.check_if_player_finished('player')
                                self.current_player = self.get_next_player()
                        else:
                            print("Możesz zagrać dwie karty tylko o wyższej wartości niż karty na stole!")
                    else:
                        print("Musisz zagrać dwie karty tej samej wartości!")

                else:
                    if len(self.selected_cards) == 1:
                        played_card = self.selected_cards[0]

                        if self.joker_played and played_card.suit == 's' and played_card.value == 3:
                            print("XD 2")
                            played_card.value = 101  
                        elif self.played_cards[-1].value == 100:
                            print("zmiana na 1000")
                            self.joker_played = True   

                        if played_card.value > self.played_cards[-1].value:
                            print("nie wchodzi 2") 
                            self.played_cards.append(played_card)
                            self.player_cards.remove(played_card)
                            self.selected_cards = []
                            if played_card.value == 8:  
                                self.played_cards = []
                                self.passed = {key: False for key in self.passed}
                                self.current_player = 'player'
                                print("Zagrano kartę 8, kolejka zresetowana. Gracz zaczyna od nowa.")
                            else:
                                self.passed['player'] = False
                                self.last_player = 'player'
                                self.check_if_player_finished('player')
                                self.current_player = self.get_next_player()
                        else:
                            print("Możesz zagrać kartę tylko o wyższej wartości niż karty na stole! 2222")
                    else:
                        print("Niepoprawny ruch! Musisz wybrać jedną kartę do zagrania.")

                    
        elif self.pass_button_rect.collidepoint(pos):
            self.pass_turn()


    def handle_click(self, pos):
        if self.current_player == 'player':
            self.handle_button_click(pos)
            
            for card in self.player_cards:
                if card.rect.collidepoint(pos):
                    if card in self.selected_cards:
                        self.selected_cards.remove(card)
                    elif len(self.selected_cards) < 3:
                        self.selected_cards.append(card)
                    break

    def pass_turn(self):
        self.passed[self.current_player] = True
        self.current_player = self.get_next_player()
        if self.all_bots_passed() and self.passed['player']:
            self.reset_round()
            self.current_player = self.last_player  
        else:
            if self.current_player != 'player':
                self.play_turn()

    def get_next_player(self):
        if self.all_bots_passed() and self.passed['player']:
            return self.last_player
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
        self.joker_played = False

    def check_if_player_finished(self, player):
        if player == 'bot1' and not self.bot1.cards:
            if player not in self.finished_order:
                self.finished_order.append(player)
        elif player == 'bot2' and not self.bot2.cards:
            if player not in self.finished_order:
                self.finished_order.append(player)
        elif player == 'bot3' and not self.bot3.cards:
            if player not in self.finished_order:
                self.finished_order.append(player)
        elif player == 'player' and not self.player_cards:
            if player not in self.finished_order:
                self.finished_order.append(player)

    def play_turn(self):
        while True:
            if self.current_player == 'player':
                break

            current_bot = None
            if self.current_player == 'bot1':
                current_bot = self.bot1
            elif self.current_player == 'bot2':
                current_bot = self.bot2
            elif self.current_player == 'bot3':
                current_bot = self.bot3

            if current_bot:
                if self.three_cards:
                    self.three_cards_game.play_turn(current_bot)
                elif self.two_cards:
                    self.two_cards_game.play_turn(current_bot)
                else:
                    self.one_card_game.play_turn(current_bot)

                if self.played_cards and self.played_cards[-1].value == 8:
                    self.played_cards = []
                    self.passed = {key: False for key in self.passed}
                    self.current_player = self.get_next_player()
                    continue

                self.check_if_player_finished(self.current_player)

            self.current_player = self.get_next_player()

            if self.all_bots_passed() and self.passed['player']:
                self.reset_round()
                self.current_player = self.last_player
                break

            if self.current_player == 'player':
                break

    def update(self):
        self.animation.move_card()

