class Animation:
    def __init__(self):
        self.selected_card = None
        self.original_position = None
        self.card_moving = False
        self.target_y = None

    def select_card(self, card):
        self.selected_card = card
        self.original_position = card.rect.topleft
        self.target_y = self.original_position[1] - 50  
        self.card_moving = True
        print(f"Card selected: {card}, moving to: {self.target_y}")

    def move_card(self):
        if self.card_moving and self.selected_card:
            current_x, current_y = self.selected_card.rect.topleft
            if current_y > self.target_y:
                new_y = max(current_y - 5, self.target_y)
                self.selected_card.rect.topleft = (current_x, new_y)
                print(f"Moving card to: {self.selected_card.rect.topleft}")
            if new_y <= self.target_y:
                self.card_moving = False  
                self.card_moved = True 
                print(f"Card stopped at: {self.selected_card.rect.topleft}")

    def reset_card(self):
        if self.selected_card and not self.card_moved:
            self.selected_card.rect.topleft = self.original_position
            self.selected_card = None
            self.card_moving = False
            print(f"Card reset to position: {self.selected_card.rect.topleft}")
