import pygame as pg
import random
import time


# Setup
pg.init()
clock = pg.time.Clock()

# Setting the screen up
screen = pg.display.set_mode((1920,1080))
pg.display.set_caption("Blackjack")

# Card class, with a suit from (1,5) and a number from (1,14)
class Card:
    def __init__ (self, suit, number):
        self.suit = int(suit)
        self.number = int(number)
        self.image = pg.image.load(f'images/{self.suit}_{self.number}.png')
        self.image = pg.transform.scale(self.image, (125, 175))  # Scale to a suitable size
        self.back_image = pg.image.load(f"images/card_back.png")
        self.back_image = pg.transform.scale(self.back_image, (125, 175))  

# Deck class, you get a Card, with a random suit from (1,5) and a random number from (1,14)
class Deck:
    def __init__(self):
            self.cards = [Card(suit, number) for suit in range(1,5) for number in range (1,14)]*6
    
    # Define and use function shuffle to shuffle self.cards list 
    def shuffle(self):
            random.shuffle(self.cards)

    # Define the deal, where you return the shuffled cards
    def deal(self):
        return self.cards.pop()
    
class Hand:
    def __init__(self):
        self.cards = []  # Store the cards in a list

    def add_card(self, card):
        """Add a card to the hand."""
        self.cards.append(card)

    def totalValue(self):
        """Calculate the total value of the hand."""
        total = 0
        aces = 0

        for card in self.cards:
            if card.number > 10:
                total += 10  # Face cards are worth 10
            elif card.number == 1:
                aces += 1
                total += 11  # Assume Ace is 11 first
            else:
                total += card.number  # Numbered cards keep their values

        # Adjust for Aces if total > 21
        while total > 21 and aces:
            total -= 10  # Convert an Ace from 11 to 1
            aces -= 1

        return total
    
    def resetting(self):
        self.cards = []

# Winning yippe GIF
yippee_image = []
for i in range(49):
    sejr = pg.image.load(f"images/GIF/17d2abd5-25ea-4925-80e8-450c6478e8f6-{i}.png")
    sejr = pg.transform.scale(sejr, (400,400))
    yippee_image.append(sejr)

# Angry GIF
angry_image = []
for i in range(49):
    tab = pg.image.load(f"images/GIF/d14b2dee-0143-45eb-ba8f-d882bd2e3bcd-{i}.png")
    tab = pg.transform.scale(tab, (400,400))
    angry_image.append(tab)

# Draw GIF
draw_image = []
for i in range(14):
    draw = pg.image.load(f"images/GIF/5d1636c7-3ce8-4545-8ba1-4e31a0974ad8-{i}.png")
    draw = pg.transform.scale(draw, (400,400))
    draw_image.append(draw)

# Filling the background with a image from the net.
background = pg.image.load(f'images/background.png')
background = pg.transform.scale(background, (1920,1080))

# Initialize deck and shuffle
deck = Deck()
deck.shuffle()

# Player and dealer hands
player_hand = Hand()
dealer_hand = Hand()
split_hand = None # New hand for split

dealer_card_dealt = False
player_card_dealt = False
dealer_card_dealt_time = None
player_card_dealt_time = None
dealer_draw_time = None
dealer_reveal = False
dealer_show = False
button_show = False
player_hit = False
lost = False
win = False
split_active = False
split_deal = False
player_dealt = False
split_button = False
scoreboard_update = False

click_pos = (0,0)
tick = 0
DarkGreen = (00,64,00)
LightGreen = (52,161,99)
fjern = 0
wins = 0
loss = 0
draws = 0
running = True
lost_win = False

# Game loop
while running:

    screen.blit(background,(0,0)) 

    events = pg.event.get()
    for event in events:

        # Close window (pressing [x], Alt+F4 etc.)
        if event.type == pg.QUIT:
            running = False
        
        # Keypresses
        elif event.type == pg.KEYDOWN:

            if event.key == pg.K_ESCAPE:
                running = False
                pg.quit()
    
            # Deal a card to the player on pressing "H" (Hit)
            elif event.key == pg.K_h:  # "H" for Hit
                if len(deck.cards) > 0:
                    player_hand.add_card(deck.deal())


        elif event.type == pg.MOUSEBUTTONDOWN:
            click_pos = event.pos     

    if not running:
        break
    
    # Then you press start, its removing the start button
    if fjern < 1:
        start = pg.draw.rect(screen, DarkGreen, (800,120,300,100),0) 
        start_font = pg.font.SysFont("Comic Sans Ms",110)
        start_surface = start_font.render("Start", False, (0,0,0))
        screen.blit(start_surface, (800,90))
    

    # Button to start the game
    if start.collidepoint(click_pos):
        click_pos = (0,0)
        # Tilføjer +1 på fjern, for at fjerne if-statementet (if fjern)
        fjern += 1
        
        if len(player_hand.cards) == 0 and not player_card_dealt:
            player_hand.add_card(deck.deal())
            player_card_dealt = True 
            dealer_card_dealt_time = pg.time.get_ticks()

    # Check if the dealer needs a card (only when the player's first card is dealt)
    if dealer_card_dealt_time and not dealer_card_dealt:
        if pg.time.get_ticks() - dealer_card_dealt_time >= 1000:
            dealer_hand.add_card(deck.deal())
            dealer_card_dealt = True  # Set the flag to True so it doesn't deal again 
            player_card_dealt_time = pg.time.get_ticks()

    # Gives the player the last hand, before hit and stand buttons
    if player_card_dealt_time and player_card_dealt == True:
        if pg.time.get_ticks() - player_card_dealt_time >= 1000:
            player_hand.add_card(deck.deal())
            player_card_dealt = False
            dealer_card_dealt_time = pg.time.get_ticks()
    
    # Gives the last card and shown card to the dealer
    if len(player_hand.cards) == 2 and len(dealer_hand.cards) == 1:
        if pg.time.get_ticks() - dealer_card_dealt_time >=1000:
            dealer_hand.add_card(deck.deal())
            dealer_card_dealt = True
            stand_button_time = pg.time.get_ticks()
            print("Player's hand value:", player_hand.totalValue())
            
    
    # Draw player cards
    for i, card in enumerate(player_hand.cards):
        x_offset = 450 + i * 120 if split_active else 825 + i * 120
        screen.blit(card.image, (x_offset, 750))
    
    # If spliting is active, then its blitting a card to the split hand
    if split_active:
        for i, card in enumerate(split_hand.cards):
            screen.blit(card.image, (1050 + i * 120, 750))

    # Draw dealer cards
    for i, card in enumerate(dealer_hand.cards):
        if i == 0 and not dealer_reveal:
            # Show card back for the first dealer card
            screen.blit(card.back_image, (1650/2 + i*120, 300))
        else:
            # Show the front image for all other dealer cards
            screen.blit(card.image, (1650/2 + i*120, 300))

    # When all cards have been dealed, to both dealer and player, hit and stand button is showing
    if len(dealer_hand.cards) == 2 and fjern == 1:
        stand = pg.draw.rect(screen, LightGreen, (1075,653,150,54),0)
        stand_font = pg.font.SysFont("Comic Sans Ms",49)
        stand_surface = stand_font.render("Stand", False, (0,0,0))
        screen.blit(stand_surface, (1075,650))
        hit = pg.draw.rect(screen, LightGreen, (675,653,150,54),0)
        hit_font = pg.font.SysFont("Comic Sans Ms",49)
        hit_surface = hit_font.render("Hit", False, (0,0,0))
        screen.blit(hit_surface, (675,650))
        button_show = True

    # If you hit stand, dealer is showing its hand, while hitting adding extra hard.
    if button_show == True and split_active == False:
        if stand.collidepoint(click_pos):
            click_pos = (0,0)
            dealer_show = True
            fjern += 1
            dealer_draw_time = pg.time.get_ticks()
        elif hit.collidepoint(click_pos):
            click_pos = (0,0)
            player_hit = True

    # If you bust nor stand, this function is being called, and showing the sum of the dealer, to look if player or dealer won        
    if dealer_show == True:   
        for i, card in enumerate(dealer_hand.cards):
            screen.blit(card.image, (1650/2 + i*120, 300))
            if dealer_draw_time and pg.time.get_ticks() - dealer_card_dealt_time >= 1000:
                # Check if BOTH hands are busted
                if player_hand.totalValue() > 21 and (not split_active or split_hand.totalValue() > 21):
                    dealer_show = True  # Just reveal dealer's cards, no more dealing
                else:
                    if dealer_hand.totalValue() < 17:
                        dealer_hand.add_card(deck.deal())

    # If the player press hit, its adding a card to his hand
    if player_hit == True:
        for i in range(1):
            player_hand.add_card(deck.deal())
            player_hit = False


    # When there is 2 cards dealt, and the last and second last (0) and (1) with .number is equal draw split square
    if len(player_hand.cards) == 2 and player_hand.cards[0].number == player_hand.cards[1].number:
        if split_button == False:
            split = pg.draw.rect(screen, LightGreen, (875,653,150,54),0)
            split_font = pg.font.SysFont("Comic Sans Ms",40)
            split_surface = split_font.render("Split", False, (0,0,0))
            screen.blit(split_surface, (895,650))
        if split.collidepoint(click_pos):
            click_pos = (0,0)
            split_active = True
            split_button = True
            split_hand = Hand()
            split_hand.add_card(player_hand.cards.pop())
            player_hand.add_card(deck.deal())
            split_hand.add_card(deck.deal())

    # This is the section to press hit and stand on whether player hand, and split hand
    if split_active:
        if split_active:
            if hit.collidepoint(click_pos):
                click_pos = (0,0)
                if not player_dealt:  # Playing left hand
                    player_hand.add_card(deck.deal())
                    if player_hand.totalValue() > 21:  # Left hand busts
                        player_dealt = True  # Switch to right hand automatically
                else:  # Playing right hand
                    split_hand.add_card(deck.deal())
                    if split_hand.totalValue() > 21:
                        dealer_show = True
                        fjern += 1
                        dealer_draw_time = pg.time.get_ticks()
                        lost = True
        if stand.collidepoint(click_pos):
            click_pos = (0,0)
            if not split_deal:
                split_deal = True
                player_dealt = True
            else:
                dealer_show = True
                fjern +=1
                dealer_draw_time = pg.time.get_ticks()

    # Display player's hand value
    if split_active == False:    
        pg.font.init()
        font = pg.font.SysFont("Comic Sans MS", 50)
        hand_value_text = font.render(f"Player: {player_hand.totalValue()}", True, (255, 255, 255))
        screen.blit(hand_value_text, (200, 700)) 
    
    # Displaying players hand and split hand value
    if split_active == True:
        font = pg.font.SysFont("Comic Sans MS", 50)
        player1_value_text = font.render(f"Left hand: {player_hand.totalValue()}", True, (255, 255, 255))
        screen.blit(player1_value_text,(200,650))
        font = pg.font.SysFont("Comic Sans MS", 50)
        player2_value_text = font.render(f"Right hand: {split_hand.totalValue()}", True, (255, 255, 255))
        screen.blit(player2_value_text, (1380,650))

    # Display dealer's hand value (if showing cards)
    if dealer_show:
        dealer_value_text = font.render(f"Dealer: {dealer_hand.totalValue()}", True, (255, 255, 255))
        screen.blit(dealer_value_text, (200, 100)) 
 
    # The player bust nad loses
    if player_hand.totalValue() >= 22 and split_active == False:  # Player busts instantly
        for i, card in enumerate(dealer_hand.cards):
            screen.blit(card.image, (1650/2 + i*120, 300))
        lost = True

    # If dealer bust, the player wins
    elif dealer_hand.totalValue() >= 22:  # Dealer busts
        win = True
    
    # If player got blackjack, its showing if dealer got less, if not its a draw, if he got less the player won    
    elif player_hand.totalValue() == 21 and len(player_hand.cards) == 2 and split_active == False:  # Player Blackjack (win instantly)
        dealer_show = True
        
    result_processed = False

    # Only process results when the dealer has finished drawing cards
    if dealer_show and dealer_hand.totalValue() >= 17 and dealer_hand.totalValue() <= 21 and not result_processed:

        if dealer_hand.totalValue() >= 17 and player_hand.totalValue() <= 21:  # Dealer stands
            if dealer_hand.totalValue() > player_hand.totalValue():  # Dealer wins by higher value
                lost = True
            elif dealer_hand.totalValue() < player_hand.totalValue():  # Player wins by higher value
                win = True
            else:  # If values are the same, it's a draw
                draw = True

            result_processed = True
        else:
            lost = True

        # 4 functions for left hand and right hand
        if split_active:
            left_win = False
            right_win = False
            left_lose = False
            right_lose = False

            # Check left hand result
            if player_hand.totalValue() > 21:
                left_lose = True
            elif player_hand.totalValue() > dealer_hand.totalValue():
                left_win = True
            elif player_hand.totalValue() < dealer_hand.totalValue():
                left_lose = True

            # Check right hand result
            if split_hand.totalValue() > 21:
                right_lose = True
            elif split_hand.totalValue() > dealer_hand.totalValue():
                right_win = True
            elif split_hand.totalValue() < dealer_hand.totalValue():
                right_lose = True

            # Determine final game state after both hands are resolved
            if left_win and right_win:
                win = True
            elif left_lose and right_lose:
                lost = True
            elif (left_win and right_lose) or (right_win and left_lose):
                draw = True  # Mixed result

    # If you win, its displaying a winner GIF
    if win == True:
        lost_win = True
        r = int(tick/2) % 49
        screen.blit(yippee_image[r], (200,240))
    
    # If you lose, its displaying a loser GIF
    elif lost == True:
        lost_win = True
        r = int(tick/2) % 49
        screen.blit(angry_image[r], (200,240))
        dealer_show = True
    
    # If you draw, its displayign a draw GIF
    elif draw == True:
        lost_win = True
        r = int(tick/2) % 14
        screen.blit(draw_image[r], (200,240))

    # Updating the update, if you win += 1 on wins etc
    if not scoreboard_update and result_processed:
        if win:
            wins += 1
        elif lost:
            loss += 1
        elif draw:
            draws += 1
        scoreboard_update = True    
        

    # Scoreboard
    font = pg.font.SysFont("Comic Sans MS", 50)
    scoreboard_text = font.render(f"Wins: {wins}  " f"Loss: {loss}  " f"Draw: {draws}", True, (255, 255, 255))
    screen.blit(scoreboard_text, (670, 225)) 

    # When you are done, its proceding this section
    if lost_win == True:
        reset = pg.draw.rect(screen, DarkGreen, (1400,150,200,75),0)
        reset_font = pg.font.SysFont("Comic Sans Ms",49)
        reset_surface = reset_font.render("Reset", False, (0,0,0))
        screen.blit(reset_surface, (1400,150))
        
        # If you are pressing on the reset, button, alot functions are getting reseted and you can begin on new.
        if reset.collidepoint(click_pos):
            click_pos = (0,0)
            dealer_reveal = False
            dealer_show = False
            button_show = False
            split_button = False
            player_hit = False
            dealer_card_dealt = False
            player_card_dealt = False
            dealer_card_dealt_time = None
            player_card_dealt_time = None
            win = False
            lost = False
            draw = False
            split_hit = False
            split_active = False
            split_deal = False
            player_dealt = False
            scoreboard_update = False
            result_processed = False
            screen.blit(background,(0,0))
            fjern = 0
            dealer_hand.cards.clear()
            player_hand.cards.clear()
            if split_active == True:
                split_hand.cards.clear()
            


    # Limit/fix frame rate (fps)
    clock.tick(30)
    tick += 1
     
    pg.display.flip()