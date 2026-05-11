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
    player_blackjack = (player_total == 21 and len(player_hand) == 2)
    dealer_blackjack = (dealer_total == 21 and len(dealer_hand) == 2)

    if player_blackjack and not dealer_blackjack:
        return "Blackjack!"
    elif dealer_blackjack and not player_blackjack:
        return "Dealer Blackjack!"
    elif player_blackjack and dealer_blackjack:
        return "Push!"
    elif player_total > 21:
        return "Dealer Wins!"
    elif dealer_total > 21:
        return "Player Wins!"
    elif player_total > dealer_total:
        return "Player Wins!"
    elif player_total < dealer_total:
        return "Dealer Wins!"
    else:
        return "Push!"

def reset_round():
    deck = make_deck()
    player_hand = []
    dealer_hand = []
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

# Loads dealer reactions into PyGame
def load_dealer_images():
    dealer_images = {}
    reactions = ["lose", "neutral", "win", "push", "blackjack", 
                 "playerblackjack"]
    
    for reaction in reactions:
        filename = f"assets/dealer_reactions/dealer_{reaction}.png"
        img = pygame.image.load(filename)
        img = pygame.transform.scale(img, (200, 300))

        dealer_images[reaction] = img

    return dealer_images

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
    
    # Loading card and dealer images
    card_images, back_image = load_card_images()
    dealer_images = load_dealer_images()

    # Loading title screen
    title_screen = pygame.image.load("assets/vivala21_titlescreen.png")

    deck = make_deck()

    player_hand = []
    dealer_hand = []

    # Game state
    game_state = "title"

    player_turn_active = True
    game_over = False
    reveal_dealer = False
    round_paid = False
    no_credits = False
    betting_phase = True

    dealing_cards = False
    deal_timer = 0
    deal_delay = 500
    deal_queue = []

    results_timer_started = False
    results_start_time = 0
    results_delay = 4000

    dealer_reaction = "neutral"

    play_again_btn = None
    cash_out_btn = None
    hit_button = None
    stand_button = None
    dd_button = None
    plus_button = None
    minus_button = None
    start_button = None

    # Credit system
    credits = 250
    bet = 50

    font = pygame.font.SysFont(None, 30)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Player interaction
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if game_state == "title":
                    if start_button and start_button.collidepoint(mouse_pos):
                        game_state = "betting"

                elif betting_phase:
                    # Increase bet
                    if plus_button and plus_button.collidepoint(mouse_pos):
                        if bet + 50 <= credits:
                            bet += 50
                    # Decrese bet
                    if minus_button and minus_button.collidepoint(mouse_pos):
                        if bet > 50:
                            bet -= 50
                    # Start game
                    if start_button and start_button.collidepoint(mouse_pos):
                        credits -= bet
                        deck, player_hand, dealer_hand = reset_round()
                        dealer_reaction = "neutral"

                        deal_queue = [dealer_hand, player_hand,
                                      dealer_hand, player_hand]
                        
                        dealing_cards = True
                        deal_timer = pygame.time.get_ticks()

                        player_turn_active = True
                        game_over = False
                        reveal_dealer = False
                        round_paid = False
                        betting_phase = False
                
                if not betting_phase and not dealing_cards:
                    if hit_button and hit_button.collidepoint(mouse_pos) and player_turn_active:
                        deal_card(deck, player_hand)

                        if calculate_hand(player_hand) > 21:
                            player_turn_active = False
                            reveal_dealer = True
                            game_over = True
                
                    if stand_button and stand_button.collidepoint(mouse_pos) and player_turn_active:
                        player_turn_active = False
                        reveal_dealer = True
                        dealer_turn(deck, dealer_hand)
                        game_over = True
                
                    if (dd_button and dd_button.collidepoint(mouse_pos)
                        and player_turn_active
                        and len(player_hand) == 2
                        ):
                            if credits >= bet:
                                credits -= bet
                                bet *= 2

                                deal_card(deck, player_hand)

                                player_turn_active = False
                                reveal_dealer = True

                                if calculate_hand(player_hand) <= 21:
                                    dealer_turn(deck, dealer_hand)
                        
                                game_over = True
                
                if reveal_dealer:
                    dealer_score = calculate_hand(dealer_hand)
                    dealer_text = font.render(f"DEALER: {dealer_score}", True, 
                                              (255, 255, 255))
                else:
                    dealer_text = font.render(f"DEALER: ?", True,
                                              (255, 255, 255))
                
                if game_over and not no_credits and play_again_btn:
                    if play_again_btn.collidepoint(mouse_pos):
                        deck, player_hand, dealer_hand = reset_round()
                        dealer_reaction = "neutral"
                        player_turn_active = True
                        game_over = False
                        reveal_dealer = False
                        round_paid = False
                        no_credits = False
                        bet = 50
                        betting_phase = True
                        cash_out_btn = None
                
                if game_over and not no_credits and cash_out_btn:
                    if cash_out_btn.collidepoint(mouse_pos):
                        game_state = "results"
                        
        # Title screen
        if game_state == "title":
            screen.blit(title_screen, (0, 0))
            start_button = draw_button(screen, "START", 320, 500,
                                       160, 50)
            pygame.display.flip()
            clock.tick(60)
            continue

        # Results screen
        if game_state == "results":
            screen.blit(title_screen, (0, 0))
            results_text = font.render(f"FINAL CREDITS: {credits}", 
                                     True, (255, 255, 255))
            screen.blit(results_text, (290, 430))
            thanks_text = font.render("THANKS FOR PLAYING!", 
                                     True, (255, 255, 255))
            screen.blit(thanks_text, (270, 460))
            pygame.display.flip()
            clock.tick(60)
            continue
        
        # Draw background
        screen.fill((0, 128, 0))

        # Draw bet phase text
        if betting_phase:
            betting_text = font.render("PLACE YOUR BET", True, 
                                       (255, 255, 255))
            screen.blit(betting_text, (300, 100))
        
        # Card dealing
        if dealing_cards:
            current_time = pygame.time.get_ticks()
            if current_time - deal_timer > deal_delay:
                if len(deal_queue) > 0:
                    next_hand = deal_queue.pop()
                    deal_card(deck, next_hand)
                    deal_timer = current_time
                else:
                    dealing_cards = False

                    # Check for Blackjack
                    player_blackjack = (calculate_hand(player_hand)
                                        == 21 and len(player_hand) == 2)
                    if player_blackjack:
                        reveal_dealer = True
                        player_turn_active = False
                        game_over = True

        # Draw player cards
        draw_hand(screen, player_hand, card_images, 100, 400)

        # Draw dealer cards
        draw_hand(screen, dealer_hand, card_images, 100, 100,
                  hide_card=not reveal_dealer,
                  back_image=back_image)

        # Draw buttons
        if not betting_phase:
            hit_button = draw_button(screen, "HIT", 100, 525, 100, 50)
            stand_button = draw_button(screen, "STAND", 250, 525, 120, 50)
            dd_button = draw_button(screen, "DOUBLE", 400, 525, 140, 50)
        if betting_phase:
            plus_button = draw_button(screen, "+", 250, 250, 50, 50)
            minus_button = draw_button(screen, "-", 100, 250, 50, 50)
            start_button = draw_button(screen, "START!", 
                                       400, 250, 140, 50)
        if game_over and not no_credits:
            play_again_btn = draw_button(screen, "Play again?",
                                         550, 525, 200, 50)
            cash_out_btn = draw_button(screen, "Cash Out",
                                       550, 460, 200, 50)

        # Draw scores
        player_score = calculate_hand(player_hand)
        player_text = font.render(f"PLAYER: {player_score}", True, 
                                  (255, 255, 255))
        
        # Draw credits
        credits_text = font.render(f"CREDITS: {credits}", True,
                                   (255, 255, 255))
        screen.blit(credits_text, (600, 20))
        bet_text = font.render(f"BET: {bet}", True,
                               (255, 255, 255))
        screen.blit(bet_text, (600, 60))
        
        if reveal_dealer:
            dealer_score = calculate_hand(dealer_hand)
            dealer_text = font.render(f"DEALER: {dealer_score}", True, 
                                  (255, 255, 255))
        else:
            if len(dealer_hand) > 1:
                vis_card_value = dealer_hand[1][1]
                dealer_text = font.render(f"DEALER: {vis_card_value}", 
                                          True, (255, 255, 255))
            else:
                dealer_text = font.render("DEALER: ?", True, 
                                          (255, 255, 255))
        
        screen.blit(player_text, (100, 350))
        screen.blit(dealer_text, (100, 50))

        # Draw dealer reactions
        screen.blit(dealer_images[dealer_reaction], (575, 1))

        # Results if game over
        if game_over:
            result = decide_winner(player_hand, dealer_hand)
            if not round_paid:
                if result == "Blackjack!":
                    dealer_reaction = "playerblackjack"
                    credits += int(bet * 2.5)
                elif result == "Player Wins!":
                    dealer_reaction = "lose"
                    credits += bet * 2
                elif result == "Dealer Wins!":
                    dealer_reaction = "win"
                elif result == "Dealer Blackjack!":
                    dealer_reaction = "blackjack"
                elif result == "Push!":
                    dealer_reaction = "push"
                    credits += bet
                round_paid = True
                if credits < 50:
                    no_credits = True
            result_text = font.render(result, True, (255, 255, 255))
            screen.blit(result_text, (300, 300))
        
        # Game over message
        if no_credits:
            game_over_text = font.render("GAME OVER", True,
                                         (255, 0, 0))
            screen.blit(game_over_text, (300, 250))
            if not results_timer_started:
                results_start_time = pygame.time.get_ticks()
                results_timer_started = True
            current_time = pygame.time.get_ticks()
            if current_time - results_start_time > results_delay:
                game_state = "results"

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()