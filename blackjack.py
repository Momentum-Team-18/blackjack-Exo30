import random
import re
import math
# Write your blackjack game here.
SUITS = ['❤️', '♣️', '♦️', '♠️']
RANKS = ['A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __repr__(self):
        return f'{self.rank} of {self.suit}  '

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
        if len(self.cards) == 0:
            for suit in self.suits:
                for rank in self.ranks:
                    self.cards.append(Card(suit, rank))
            random.shuffle(self.cards)
        return self.cards.pop(0)

class Player:
    def __init__(self, name):
        self.hand = []
        self.name = name
        self.total = 0
        self.stay = False
        self.bust = False
        self.wins = 0
        self.out = False
    
    def __str__(self):
        return self.name

    def calc_total(self):
        self.total = 0
        self.ace = 0
        for card in self.hand:
            card = str(card)
            num = [int(s) for s in re.findall(r'\b\d+\b', card)]
            if num != []:
                self.total += int(num[0])
            elif card[0].find('A') != -1:
                self.ace += 1
            else:
                self.total += 10
        while self.ace != 0:
            if self.total + 11 > 21:
                self.total += 1
            else:
                self.total += 11
            self.ace -= 1
        if self.total > 21:
            self.bust = True

    def hit(self, card):
        self.hand.append(card)
        self.calc_total()
        
    
    def bet(self, bet):
        pass

class Dealer(Player):
    def __init__(self):
        self.name = 'Dealer'
        self.hand = []
        self.total = 0
        self.stay = False
        self.bust = False
        self.wins = 0
    
    def __str__(self):
        return 'Dealer'
    


class Game: 
    def __init__(self, suits, ranks):
        self.play_num = self.get_player_count()
        self.play_count = 0
        self.players = []
        while self.play_count != self.play_num:
            self.players.append(Player(self.get_player_name()))
            self.play_count += 1
        self.dealer = Dealer()
        self.deck = Deck(suits, ranks)
        self.done = 0
        self.dealer_done = False
        self.bust_count = 0
        self.pot = 0
        self.entry_bet = 3
        self.players_out = 0
        self.starting_money = 10
        self.game_over = False
        for player in self.players:
            player.money = self.starting_money

    def get_player_name(self):
        name = input('What is your name?   ')
        return name

    def get_player_count(self):
        count = input("How many players are playing?  ")
        return int(count)
    
    def draw(self, person):
        self.person = person
        card = self.deck.draw()
        print(card)
        person.hit(card)
        person.calc_total()

    def start_draw(self, person):
        if person.bust == False and person.out == False:
            person.hit(self.deck.draw())
            person.hit(self.deck.draw())
            print(str(person) + "'s hand:  " + str(person.hand))
            person.calc_total()

    def turn(self, person):
        print("#############################################")
        print("#############################################")
        if person == self.dealer:
            if person.total < 16:
                self.draw(person)
            if person.total > 21:
                person.bust = True
                self.dealer_done = True
            elif person.total >= 16: 
                person.stay = True
                self.dealer_done = True                      
        else:
            print(person.name + "'s hand:  " + str(person.hand))
            turn = input('(s)tay, or (h)it?   ')
            if turn == 's':
                person.stay = True
                self.done += 1 
            if turn == 'h':
                self.draw(person)
                print('Player total is : ' + str(person.total))
                if person.total > 21:
                    person.bust = True
                    self.done += 1 
                    self.bust_count += 1

    def determine_winner(self, players):
        winners = []
        winner_total = 0
        if (self.done == len(players)):
            if (self.dealer.bust == False):
                winners.append(self.dealer)
                winner_total = self.dealer.total
            if (len(players) == 1):
                if players[0].bust == False:
                    if players[0].total > winner_total:
                        winner_total = players[0].total
                        winners = [(players[0])]
                    elif players[0].total == winner_total:
                        winners.append(players[0])
            else:
                for player in players:
                    if player.bust == False and player.total <= 21:
                        if player.total > winner_total:
                            winner_total = player.total
                            winners = [player]
                        elif player.total == winner_total:
                            if str(player) in winners == False:
                                winners.append(player)
                                print('Should be tie  ' + str(winners))
        if (winners != []):
            if (winners[0] != self.dealer and self.dealer_done == False):
                self.turn(self.dealer)
                return self.determine_winner(players)
            elif(len(winners) > 1):
                split = math.floor(self.pot/int(len(winners)))
                print("We've got a " + str(len(winners)) + "-way tie!!! ")
                for player in winners:
                    player.money += split
                    print(str(player))
                print("All of these are winners! The pot will be split")
                return ''
            elif(len(winners) == 1):
                print(str(winners[0]) + ' is the winner!!! With a total of ' + str(winners[0].total) +  ' and a hand of ' + str(winners[0].hand))
                if winners[0] != self.dealer:
                    winners[0].money += self.pot
                winners[0].wins += 1
                return ''
            else:
                print("We've got an error boys")
                return ''
        if (winners == [] and self.dealer.bust == True and self.bust_count == len(players)):
            print('Everyone busts and the House wins!!!!')
            return ''
        winners = []
        print("whoops")
        return winners

    def round(self, players):
        print("#############################################")
        print("-----------------NEW ROUND-------------------")
        print("#############################################")
        print("Dealers hand: " + str(self.dealer.hand))
        for person in players:
            if person.bust == False:
                pass
            if person.bust == False and person.stay == False:
                turn = self.turn(person)
                if turn and turn > 0:
                    self.call_round(person, players, turn)
    
    def start_bet(self, player):
        print("You have " + str(player.money) + " left to bet")
        if player.money >= self.entry_bet:
            player.money -= self.entry_bet
            self.pot += self.entry_bet
        else:
            player.bust == True
            self.done += 1
            self.players_out += 1
            player.out = True
            print(str(player) + ' is out of the game!!!')
        if player.money >= self.starting_money * 5:
            print("You have won five times more than what you started with, CONGRATS!!! However, The House would like a word with you in the back......")
            player.bust == True
            self.done += 1
            self.players_out += 1
            print(str(player) + ' is out of the game!!!')
            player.out = True


    def special_options(self, player):
        double = input("If you like your hand you can double down on your bet.... (y)es or (n)o? ")
        if double == 'y':
            player.stay = True
            self.done += 1
            player.money - self.entry_bet
            self.pot += self.entry_bet + self.entry_bet
            self.draw(player)

    def cash_out(self, player):
        question = input(str(player) + ' would you like to cash out? (y)es or (n)o?  ')
        if question == 'y':
            self.players_out += 1
            player.out = True
            print(str(player) + ' escaped the table with ' + str(player.money) + " coins left!!!")

    def play(self, players, dealer):
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("------------------NEW GAME-------------------")
        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        for player in players:
            if player.out != True:
                self.start_bet(player)
                self.start_draw(player)
                self.special_options(player)
        if self.players_out == len(players):
            print("THE HOUSE ALWAYS WINS")
            self.game_over = True
            return ''
        self.start_draw(dealer)
        self.pot += self.entry_bet
        winner = []

        while (winner == []):
            self.round(players)
            winner = self.determine_winner(players)

        for player in players:
            player.hand = []
            player.stay = False
            player.bust = False
        dealer.hand = []
        dealer.bust = False
        dealer.stay = False
        self.done = 0
        self.pot = 0
        winner = []
        





new_game = Game(SUITS, RANKS)
new_game.deck.shuffle()
count = 0
while new_game.game_over == False:
    new_game.play(new_game.players, new_game.dealer)

