import random
import pygame

# Makes deck of cards
def make_deck():
    deck = []
    suits = ["Hearts", "Diamonds", "Spades, Clubs"]
    values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
              "7": 7, "8": 8, "9": 9, "10": 10, "A": 11}
    
    for suit in suits:
        for value in values:
            deck.append((value, values[value], suit))
    
    random.shuffle(deck)
    return deck

# Deals the cards
def deal_card(deck, hand):
    card = deck.pop()
    hand.append(card)

# Hand value calculating
def calculate_hand(hand):
    total = sum(card[1] for card in hand)
    ace = sum(1 for card in hand if card[0] == "A")

    while total > 21 and ace:
        total -= 10
        ace -= 1
    
    return total