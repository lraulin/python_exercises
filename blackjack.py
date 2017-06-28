"""
A blackjack game made to practice OOP concepts.
"""

from random import shuffle

class Card():

    FACES = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}

    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank

    def get_name(self):
        return self

    def get_value(self):
        return self.rank

    def __str__(self):
        value = self.FACES.get(self.rank, self.rank)
        return "{0} of {1}".format(value, self.suit)

    def __lt__(self, other):
        return self.rank < other.rank

    def __gt__(self, other):
        return self.rank > other.rank

    def __eq__(self, other):
        return self.rank == other.rank

    def __ne__(self, other):
        return self.rank != other.rank

    def __repr__(self):
        return str(self)

class Deck():

    def __init__(self):
        self.reset()

    def reset(self):
        ranks = range(2, 15)
        suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        self.deck = []
        for r in ranks:
            for s in suits:
                self.deck.append(Card(r, s))
        shuffle(self.deck)
        print(self.deck)

    def shuffle_deck(self):
        shuffle(self.deck)
        print(self.deck)
        return self.deck

    def draw_card(self):
        print(self.deck[-1])
        return self.deck.pop()

    def get_size(self):
        return len(self.deck)

new_card = Card(4, "Clubs")
print(new_card.get_name())
print(new_card)
print(new_card.get_value())
deck = Deck()
deck.shuffle_deck()
print(deck.get_size())
deck.draw_card()
print(deck.get_size())
deck.reset()
deck.shuffle_deck()
print(deck.get_size())
deck.draw_card()
print(deck.get_size())