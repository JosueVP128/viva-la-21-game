import random
import pygame

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