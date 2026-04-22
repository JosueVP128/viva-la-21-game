import random
import pygame

# Makes deck of cards
def make_deck():
    deck = []
    suits = ["hearts", "diamonds", "spades", "clubs"]
    values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8,
              "9": 9, "10": 10, "jack": 10, "queen": 10, "king": 10, "ace": 11}
    
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

# Loads card images into PyGame
def load_card_images():
    card_images = {}

    values = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
             "ace", "jack", "queen", "king"]
    suits = ["hearts", "diamonds", "spades", "clubs"]

    for suit in suits:
        for value in values:
            filename = f"assets/cards/{value}_of_{suit}.png"
            img = pygame.image.load(filename)
            img = pygame.transform.scale(img, (70, 110))
            card_images[(value, suit.capitalize())] = img
    
    back_img = pygame.image.load("assets/cards/back_of_card.png")
    back_img = pygame.transform.scale(back_img, (70, 110))

    return card_images, back_img

# Draws cards on screen
def draw_hand(screen, hand, card_images, x, y):
    for i, card in enumerate(hand):
        value, _, suit = card
        img = card_images[(value, suit)]
        screen.blit(img, (x + i * 90, y))
    
def main():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Viva la 21")

    clock = pygame.time.Clock()
    running = True
    card_images, back_image = load_card_images()

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
    # player_turn(deck, player_hand)

    # Dealer turn (if player does not bust)
    # if calculate_hand(player_hand) <= 21:
    #    dealer_turn(deck, dealer_hand)

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

        # Draw player cards
        draw_hand(screen, player_hand, card_images, 100, 400)

        # Draw dealer cards
        draw_hand(screen, dealer_hand, card_images, 100, 100)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()