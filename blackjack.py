import random
import re
# Write your blackjack game here.
SUITS = ['❤️', '♣️', '♦️', '♠️']
RANKS = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __repr__(self):
        return f'{self.rank} of {self.suit}  '
    #def __str__(self):
        #return f'{self.rank} of {self.suit}'
    
#deck_of_cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
#print(deck_of_cards)

class Deck:
    def __init__(self, suits, ranks):
        self.cards = []
        self.suits = suits
        self.ranks = ranks
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))
    def __repr__(self):
        return str('  ' + self.cards + '  ')
    def __str__(self):
        deck_string = ''
        for card in self.cards:
            deck_string += '  ' + str(card) + '  '
        return deck_string
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw(self):
        return self.cards.pop(0)

class Player:
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.total = 0
        self.stayed = False
        self.bust = False
    
    def __str__(self):
        return self.name

    def calc_total(self):
        self.total = 0
        for card in self.hand:
            card = str(card)
            num = [int(s) for s in re.findall(r'\b\d+\b', card)]
            if num != []:
                self.total += int(card[0])
            if card[0].find('A') != -1:
                if self.total + 11 > 21:
                    self.total += 1
                else:
                    self.total += 11
            if (card[0].find('J') != -1) or (card[0].find('K') != -1) or (card[0].find('Q') != -1):
                self.total += 11

    def hit(self, card):
        self.hand.append(card)
        self.calc_total()

    def stay(self):
        pass

    def money(self, money):
        self.money = money
    
    def bet(self, money):
        pass

class Dealer(Player):
    def __init__(self):
        self.name = 'Dealer'
        self.hand = []
        self.total = 0
        self.stayed = False
        self.bust = False
    
    def __str__(self):
        return 'Dealer'
    


class Game: 
    def __init__(self, suits, ranks):
        self.player = Player(self.get_player_name())
        self.dealer = Dealer()
        self.deck = Deck(suits, ranks)
    
    def get_player_name(self):
        name = input('What is your name?')
        return name
    
    def draw(self, person):
        self.person = person
        card = self.deck.draw()
        print(card)
        person.hit(card)
        person.calc_total()

    def start_draw(self, person):
        person.hit(self.deck.draw())
        person.hit(self.deck.draw())
        print(str(person) + "'s hand:  " + str(person.hand))
        person.calc_total()

    def turn(self, person):
        if person.bust == False and person.stayed == False:
            if person == self.dealer:
                if person.total < 16:
                    self.draw(person)
                else:
                    person.stayed = True
            if person == self.player:
                print(person.hand)
                print(person.total)
                turn = input('Stay, Hit or Bet?   ')
                if turn == 'stay' or turn == 'Stay' or turn == 'STAY':
                    person.stayed = True
                if turn == 'hit' or turn == 'HIT' or turn =='Hit':
                    self.draw(person)
                    print(person.total)
                    if person.total > 21:
                        person.bust = True

    def play(self, players):
        for player in players:
            new_game.start_draw(player)


#deck_of_cards = Deck(SUITS, RANKS)
#deck_of_cards.shuffle()

#print(deck_of_cards.draw())
new_game = Game(SUITS, RANKS)
new_game.deck.shuffle()
count = 0
#print(new_game.deck.cards)
new_game.play([new_game.player, new_game.dealer])
new_game.turn(new_game.player)
new_game.turn(new_game.dealer)
#print(new_game.deck.cards)
#print(Card('heart', 'two'))
#print(len(new_game.deck.cards))
