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
    ace = sum(1 for card in hand if card[0] == "ace")

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

def reset_round():
    deck = make_deck()
    player_hand = []
    dealer_hand = []
    deal_card(deck, player_hand)
    deal_card(deck, player_hand)
    deal_card(deck, dealer_hand)
    deal_card(deck, dealer_hand)
    return deck, player_hand, dealer_hand

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
            card_images[(value, suit)] = img
    
    back_img = pygame.image.load("assets/cards/back_of_card.png")
    back_img = pygame.transform.scale(back_img, (70, 110))

    return card_images, back_img

# Draws cards on screen and hides dealer card
def draw_hand(screen, hand, card_images, x, y, hide_card=False, 
              back_image=None):
    for i, card in enumerate(hand):
        value, _, suit, = card

        if i == 0 and hide_card:
            screen.blit(back_image, (x + i * 90, y))
        else:
            img = card_images[(value, suit)]
            screen.blit(img, (x + i * 90, y))

# Draws button on screen (for now)
def draw_button(screen, text, x, y, width, height):
    font = pygame.font.SysFont(None, 36)
    rect = pygame.Rect(x, y, width, height)

    pygame.draw.rect(screen, (200, 200, 200), rect)
    pygame.draw.rect(screen, (0, 0, 0), rect, 2)

    words = font.render(text, True, (0, 0, 0))
    screen.blit(words, (x + 10, y + 10))

    return rect
    
def main():
    pygame.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Viva la 21")

    clock = pygame.time.Clock()
    running = True
    
    # Loading card images
    card_images, back_image = load_card_images()

    deck = make_deck()

    player_hand = []
    dealer_hand = []

    deal_card(deck, player_hand)
    deal_card(deck, player_hand)
    deal_card(deck, dealer_hand)
    deal_card(deck, dealer_hand)

    # Game state
    player_turn_active = True
    game_over = False
    reveal_dealer = False

    play_again_btn = None

    # Credit system
    credits = 600
    bet = 100
    credits -= bet

    font = pygame.font.SysFont(None, 30)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Player interaction
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if hit_button.collidepoint(mouse_pos) and player_turn_active:
                    deal_card(deck, player_hand)

                    if calculate_hand(player_hand) > 21:
                        player_turn_active = False
                        reveal_dealer = True
                        game_over = True
                
                if stand_button.collidepoint(mouse_pos) and player_turn_active:
                    player_turn_active = False
                    reveal_dealer = True
                    dealer_turn(deck, dealer_hand)
                    game_over = True
                
                if reveal_dealer:
                    dealer_score = calculate_hand(dealer_hand)
                    dealer_text = font.render(f"DEALER: {dealer_score}", True, 
                                              (255, 255, 255))
                else:
                    dealer_text = font.render(f"DEALER: ?", True,
                                              (255, 255, 255))
                    
                if game_over and play_again_btn:
                    if play_again_btn.collidepoint(mouse_pos):
                        if credits >= bet:
                            deck, player_hand, dealer_hand = reset_round()

                            player_turn_active = True
                            game_over = False
                            reveal_dealer = False

                            credits -= bet
                        else:
                            print("GAME OVER: NO CREDITS!")
                            running = False
        
        # Draw background
        screen.fill((0, 128, 0))

        # Draw player cards
        draw_hand(screen, player_hand, card_images, 100, 400)

        # Draw dealer cards
        draw_hand(screen, dealer_hand, card_images, 100, 100,
                  hide_card=not reveal_dealer,
                  back_image=back_image)

        # Draw buttons
        hit_button = draw_button(screen, "HIT", 100, 525, 100, 50)
        stand_button = draw_button(screen, "STAND", 250, 525, 120, 50)
        if game_over:
            play_again_btn = draw_button(screen, "Play again?",
                                         500, 500, 100, 50)

        # Draw scores
        player_score = calculate_hand(player_hand)
        player_text = font.render(f"PLAYER: {player_score}", True, 
                                  (255, 255, 255))
        
        # Draw credits
        credits_text = font.render(f"CREDITS: {credits}", True,
                                   (255, 255, 255))
        screen.blit(credits_text, (600, 20))
        
        if reveal_dealer:
            dealer_score = calculate_hand(dealer_hand)
            dealer_text = font.render(f"DEALER: {dealer_score}", True, 
                                  (255, 255, 255))
        else:
            dealer_text = font.render("DEALER: ?", True, (255, 255, 255))
        
        screen.blit(player_text, (100, 350))
        screen.blit(dealer_text, (100, 50))

        # Results if game over
        if game_over:
            result = decide_winner(player_hand, dealer_hand)
            if result == "Player Wins!":
                credits += bet * 2
            elif result == "Tie!":
                credits += bet
            result_text = font.render(result, True, (255, 255, 255))
            screen.blit(result_text, (300, 300))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()