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
        self.stay = False
        self.bust = False
        self.money = 10
    
    def __str__(self):
        return self.name

    def calc_total(self):
        self.total = 0
        for card in self.hand:
            card = str(card)
            num = [int(s) for s in re.findall(r'\b\d+\b', card)]
            if num != []:
                self.total += int(num[0])
                if self == 'Matt':
                    print(self.total)
            elif card[0].find('A') != -1:
                if self.total + 11 > 21:
                    self.total += 1
                else:
                    self.total += 11
            else:
                self.total += 10

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
            #self.eval(f'{"_".join(["player", str(self.play_count)])}') = Player(self.get_player_name())
        self.dealer = Dealer()
        self.deck = Deck(suits, ranks)
        self.done = 0
        self.dealer_done = False
        self.bust_count = 0

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
        person.hit(self.deck.draw())
        person.hit(self.deck.draw())
        print(str(person) + "'s hand:  " + str(person.hand))
        person.calc_total()

    def call_round(self, better, players, bet):
        for person in players:
            if person != better:
                next_bet = input(str(person) + "'s Bet!!  Would you like to (c)all, (r)aise or (f)old?  ")
                if next_bet == "c":
                    pass
                if next_bet =="r":
                    new_bet = input("How much would you like to bet?  ")
                    if new_bet > bet:
                        self.call_round(person, players, new_bet)
                    else:
                        print("Please input a valid bet")
                if next_bet == 'f':
                    person.bust = True

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
            turn = input('(s)tay, (h)it or (b)et?   ')
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
            if turn == "b":
                bet = input("How much are you betting? (Enter c to cancel)   ")
                if bet == 'c':
                    return turn(self, person)
                else:
                    bet = int(bet)
                    if bet > 0:
                        return bet

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
                    if player.bust == False:
                        print(player.total, winner_total, player.total > winner_total)
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
                print("We've got a " + str(len(winners)) + "-way tie!!! ")
                for player in winners:
                    print(str(player))
                print("All of these are winners! The pot will be split")
                return ''
            elif(len(winners) == 1):
                print(str(winners[0]) + ' is the winner!!! With a total of ' + str(winners[0].total) +  ' and a hand of ' + str(winners[0].hand))
                return ''
            else:
                print("We've got an error boys")
                return ''
        if (winners == [] and self.dealer.bust == True and self.bust_count == len(players)):
            print('Everyone busts and the House wins!!!!')
            return ''
        winners = []
        return winners

    def round(self, players):
        print("#############################################")
        print("#############################################")
        for person in players:
            if person.bust == False:
                pass
                # self.determine_winner(players)
            if person.bust == False and person.stay == False:
                turn = self.turn(person)
                if turn and turn > 0:
                    self.call_round(person, players, turn)


    def play(self, players, dealer):
        for player in players:
            self.start_draw(player)
        self.start_draw(dealer)
        winner = []

        while (winner == []):
            self.round(players)
            winner = self.determine_winner(players)





new_game = Game(SUITS, RANKS)
new_game.deck.shuffle()
new_game.play(new_game.players, new_game.dealer)

