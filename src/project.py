import random
import pygame

# Makes deck of cards
def make_deck():
    deck = []
    suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
    values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
              "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10, "A": 11}
    
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

# Player action
def player_turn(deck, player_hand):
    while True:
        choice = input("HIT or STAND? ").lower()

        if choice == "hit":
            deal_card(deck, player_hand)
            print("Your Hand: ", player_hand)
            print("Total: ", calculate_hand(player_hand))

            if calculate_hand(player_hand) > 21:
                print("BUST!")
                break
        else:
            break

# Dealer action
def dealer_turn(deck, dealer_hand):
    while calculate_hand(dealer_hand) < 17:
        deal_card(deck, dealer_hand)

# Decides winner
def decide_winner(player_hand, dealer_hand):
    player_total = calculate_hand(player_hand)
    dealer_total = calculate_hand(dealer_hand)

    if player_total > 21:
        return "Dealer Wins!"
    elif dealer_total > 21:
        return "Player Wins!"
    elif player_total > dealer_total:
        return "Player Wins!"
    elif player_total < dealer_total:
        return "Dealer Wins!"
    else:
        return "Tie!"
    
def main():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Viva la 21")

    clock = pygame.time.Clock()
    running = True

    deck = make_deck()

    player_hand = []
    dealer_hand = []

    deal_card(deck, player_hand)
    deal_card(deck, player_hand)
    deal_card(deck, dealer_hand)
    deal_card(deck, dealer_hand)

    print("Your Hand: ", player_hand, "Total: ", 
          calculate_hand(player_hand))
    print("Dealer Shows: ", dealer_hand[0])

    # Player turn
    player_turn(deck, player_hand)

    # Dealer turn (if player does not bust)
    if calculate_hand(player_hand) <= 21:
        dealer_turn(deck, dealer_hand)

    print("Final Hands: ")
    print("Player:", player_hand, "Total:", calculate_hand(player_hand))
    print("Dealer:", dealer_hand, "Total:", calculate_hand(dealer_hand))

    # Winner decision
    result = decide_winner(player_hand, dealer_hand)
    print (result)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((0, 128, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()