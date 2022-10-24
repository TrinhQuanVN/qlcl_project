import random

cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

class Player:
    def __init__(self,name,money=0) -> None:
        self.name = name
        self.money = money
        self.card_in_hands = []
        
    def draw(self):
        self.card_in_hands.append(random.choice(cards))
        
    def score(self):
        return sum(self.card_in_hands)
    

win = False
dealer = Player('dealer')
player = Player(input('Tell me your name>>> '),input('how much money do you want to play>>> '))