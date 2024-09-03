import pygame
import random
import math
from card import Card
from bot import Bot
from animation import Animation
from one_card import OneCardGame
from two_cards import TwoCardsGame
from three_cards import ThreeCardsGame
from four_cards import FourCardsGame
from ranks import Ranks


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
        self.four_cards = False

        self.one_card_game = OneCardGame(self)
        self.two_cards_game = TwoCardsGame(self)
        self.three_cards_game = ThreeCardsGame(self)
        self.four_cards_game = FourCardsGame(self)

        self.finished_order = []  

        self.joker_played = False

        self.ranks = Ranks() 
        self.round_number = 1
        self.reset_game()
        
    def reset_game(self):
        self.reset_ranks()
        self.reset_scores()

    def reset_ranks(self):
        self.ranks.reset_ranks()

    def reset_scores(self):
        self.ranks.reset_scores()

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
            offset_between_cards = 50 

            for i, card in enumerate(self.played_cards):
                pair_index = i // 2
                pos_index = pair_index % len(positions)
                offset_x, offset_y = positions[pos_index]

                if i % 2 == 0:  
                    x = center_x + offset_x
                    y = center_y + offset_y
                else:  
                    if i % 3 == 0:
                        offset_between_cards = 5
                    else:
                        offset_between_cards = -5
                    x = center_x + offset_x + CARD_WIDTH + offset_between_cards
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

        elif self.four_cards:
            center_x = (self.screen_width - CARD_WIDTH) // 2
            center_y = (self.screen_height - CARD_HEIGHT) // 2

            for i, card in enumerate(self.played_cards):
                pos_index = i % 4
                offset_x, offset_y = positions[pos_index]
                x = center_x + offset_x
                y = center_y + offset_y
                card.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
                self.screen.blit(card.image, card.rect.topleft)
        
        self.draw_positions()  
        self.draw_round_info() 

        self.draw_pass_info()
        self.draw_accept_button()
        self.draw_pass_button()
        self.draw_scoreboard()

        self.draw_positions()  

    def draw_pass_info(self):
        passed_count = sum(1 for player in self.passed.values() if player)
        pass_text = f"Pass: {passed_count}/4"
        text_surface = self.font.render(pass_text, True, WHITE)
        self.screen.blit(text_surface, (10, self.screen_height - 50))

    def draw_round_info(self):
        round_text = f"Round: {self.round_number}/3"
        text_surface = self.font.render(round_text, True, WHITE)
        self.screen.blit(text_surface, (10, 10))  

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
        round_text = f"Round: {self.round_number}/3"
        round_surface = self.font.render(round_text, True, WHITE)
        round_rect = round_surface.get_rect(center=(10 + round_surface.get_width() // 2, 10 + round_surface.get_height() // 2))  
        self.screen.blit(round_surface, round_rect.topleft) 

        rank_texts = {
            'player': self.ranks.get_rank('player'),
            'bot1': self.ranks.get_rank('bot1'),
            'bot2': self.ranks.get_rank('bot2'),
            'bot3': self.ranks.get_rank('bot3')
        }

        positions = {
            'player': (self.screen_width // 2, self.screen_height - CARD_HEIGHT - 80),
            'bot1': (self.screen_width // 2, 180),
            'bot2': (580, self.screen_height // 2),  
            'bot3': (self.screen_width - 580, self.screen_height // 2) 
        }

        for player, pos in positions.items():
            rank_text = self.ranks.get_rank(player)
            text_surface = self.font.render(f"{rank_text}", True, WHITE)
            
            if player == 'bot2':
                text_surface = pygame.transform.rotate(text_surface, 90)  
            elif player == 'bot3':
                text_surface = pygame.transform.rotate(text_surface, 270) 
            
            text_rect = text_surface.get_rect(center=pos)  
            self.screen.blit(text_surface, text_rect.topleft)

    def draw_position_text(self, position, x, y, rank):
        position_texts = ["1st", "2nd", "3rd", "4th"]
        text_surface = self.font.render(f"{position_texts[position - 1]} ({rank})", True, WHITE)
        self.screen.blit(text_surface, (x, y))

    def handle_button_click(self, pos):
        if self.accept_button_rect.collidepoint(pos):
            if not self.played_cards:
                if len(self.selected_cards) == 1:
                    self.one_cards = True
                    self.two_cards = False
                    self.three_cards = False
                    self.four_cards = False
                    played_card = self.selected_cards[0]

                    if self.joker_played and played_card.suit == 's' and played_card.value == 3:
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

                elif len(self.selected_cards) in [2, 3, 4]:
                    card_values = [card.value for card in self.selected_cards if card.value != 100]  
                    unique_values = set(card_values)

                    if len(unique_values) == 1: 
                        joker_count = len([card for card in self.selected_cards if card.value == 100])

                        if joker_count + len(card_values) == len(self.selected_cards):  
                            self.one_cards = len(self.selected_cards) == 1
                            self.two_cards = len(self.selected_cards) == 2
                            self.three_cards = len(self.selected_cards) == 3
                            self.four_cards = len(self.selected_cards) == 4

                            if self.joker_played:
                                for card in self.selected_cards:
                                    if card.value == 100:  
                                        card.value = unique_values.pop()

                            self.played_cards.extend(self.selected_cards)
                            for card in self.selected_cards:
                                self.player_cards.remove(card)
                            self.selected_cards = []
                            self.passed['player'] = False
                            self.last_player = 'player'
                            self.check_if_player_finished('player')
                            self.current_player = self.get_next_player()
                        else:
                            print(f"Zagranie niepoprawne! Musisz zagrać {len(self.selected_cards)} karty tej samej wartości.")
                    else:
                        print(f"Zagranie niepoprawne! Musisz zagrać {len(self.selected_cards)} karty tej samej wartości.")
                else:
                    print("To jest niepoprawny ruch. Musisz wybrać jedną kartę na start, dwie karty tej samej wartości, trzy karty tej samej wartości lub cztery karty tej samej wartości!")

            else:
                if self.four_cards:
                    if len(self.selected_cards) == 4:
                        card_values = [card.value for card in self.selected_cards if card.value != 100]
                        unique_values = set(card_values)

                        if len(unique_values) == 1:
                            joker_count = len([card for card in self.selected_cards if card.value == 100])

                            if joker_count + len(card_values) == 4 and self.selected_cards[0].value > self.played_cards[-1].value:
                                if self.joker_played:
                                    for card in self.selected_cards:
                                        if card.value == 100:
                                            card.value = unique_values.pop()
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
                                print("Możesz zagrać cztery karty tylko o wyższej wartości niż karty na stole!")
                        else:
                            print("Musisz zagrać cztery karty tej samej wartości!")

                elif self.three_cards:
                    if len(self.selected_cards) == 3:
                        card_values = [card.value for card in self.selected_cards if card.value != 100]
                        unique_values = set(card_values)

                        if len(unique_values) == 1:
                            joker_count = len([card for card in self.selected_cards if card.value == 100])

                            if joker_count + len(card_values) == 3 and self.selected_cards[0].value > self.played_cards[-1].value:
                                if self.joker_played:
                                    for card in self.selected_cards:
                                        if card.value == 100:
                                            card.value = unique_values.pop()
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
                    if len(self.selected_cards) == 2:
                        card_values = [card.value for card in self.selected_cards if card.value != 100]
                        unique_values = set(card_values)

                        if len(unique_values) == 1:
                            joker_count = len([card for card in self.selected_cards if card.value == 100])

                            if joker_count + len(card_values) == 2 and self.selected_cards[0].value > self.played_cards[-1].value:
                                if self.joker_played:
                                    for card in self.selected_cards:
                                        if card.value == 100:
                                            card.value = unique_values.pop()
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
                            played_card.value = 101  
                        elif self.played_cards[-1].value == 100:
                            self.joker_played = True   

                        if played_card.value > self.played_cards[-1].value:
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
                            print("Możesz zagrać kartę tylko o wyższej wartości niż karty na stole!")
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
                    elif len(self.selected_cards) < 4:
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

    def end_round(self):
        self.ranks.update_ranks(self.finished_order)
        
        self.reset_round()  
        self.finished_order = []  
        self.player_cards = random.sample(self.cards, 13)  
        remaining_cards = [card for card in self.cards if card not in self.player_cards]
        self.bot1.reset(remaining_cards)
        self.bot2.reset(remaining_cards)
        self.bot3.reset(remaining_cards)
        
        self.round_number += 1  
        if self.round_number > 3:
            self.round_number = 1  
            self.reset_ranks()

    def draw_player_ranks(self):
        positions = {
            'player': (self.screen_width // 2, self.screen_height - CARD_HEIGHT - 80),
            'bot1': (self.screen_width // 2, 10),
            'bot2': (10, self.screen_height // 2),
            'bot3': (self.screen_width - 60, self.screen_height // 2)
        }

        for player, pos in positions.items():
            rank = self.ranks.get_rank(player)
            text_surface = self.font.render(f"{player}: {rank}", True, WHITE)
            self.screen.blit(text_surface, pos)

    def draw_scoreboard(self):
        y_offset = self.screen_height // 2
        for player in ['player', 'bot1', 'bot2', 'bot3']:
            rank_text = self.ranks.get_rank(player)
            score_text = f"Score: {self.ranks.get_score(player)}"
            text_surface = self.font.render(f"{player.capitalize()}: {rank_text} | {score_text}", True, WHITE)
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 30


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

        if len(self.finished_order) == 4:
            self.end_round()

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
                if self.four_cards:
                    self.four_cards_game.play_turn(current_bot)
                elif self.three_cards:
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

