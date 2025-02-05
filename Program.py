import pygame as pg
import random
import time


# Overvejer at lave Blackjack - Du har en hand og spiller mod dealer

# Setup
pg.init()
clock = pg.time.Clock()
pg.display.set_caption("Blackjack")

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


# Filling the background with a image from the net.
background = pg.image.load(f'images/background.png')
background = pg.transform.scale(background, (1920,1080))

# Initialize deck and shuffle
deck = Deck()
deck.shuffle()

# Player and dealer hands
player_hand = Hand()
dealer_hand = Hand()

dealer_card_dealt = False
player_card_dealt = False
dealer_card_dealt_time = None
player_card_dealt_time = None
dealer_reveal = False
dealer_show = False
button_show = False
player_hit = False

click_pos = (0,0)
tick = 0
DarkGreen = (00,64,00)
LightGreen = (52,161,99)
fjern = 0
running = True

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
    if fjern < 1:
        start = pg.draw.rect(screen, DarkGreen, (800,150,300,100),0) 
        pg.font.init()
        start_font = pg.font.SysFont("Comic Sans Ms",110)
        start_surface = start_font.render("Start", False, (0,0,0))
        screen.blit(start_surface, (800,120))
    

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

    if player_card_dealt_time and player_card_dealt == True:
        if pg.time.get_ticks() - player_card_dealt_time >= 1000:
            player_hand.add_card(deck.deal())
            player_card_dealt = False
            dealer_card_dealt_time = pg.time.get_ticks()

    if len(player_hand.cards) == 2 and len(dealer_hand.cards) == 1:
        if pg.time.get_ticks() - dealer_card_dealt_time >=1000:
            dealer_hand.add_card(deck.deal())
            dealer_card_dealt = True
            stand_button_time = pg.time.get_ticks()
            print("Player's hand value:", player_hand.totalValue())
            
    
    # Draw player cards
    for i, card in enumerate(player_hand.cards):
        screen.blit(card.image, (1650/2 + i*120, 750))  # Position cards in a row

    # Draw dealer cards
    for i, card in enumerate(dealer_hand.cards):
        if i == 0 and not dealer_reveal:
            # Show card back for the first dealer card
            screen.blit(card.back_image, (1650/2 + i*120, 300))
        else:
            # Show the front image for all other dealer cards
            screen.blit(card.image, (1650/2 + i*120, 300))

    if len(dealer_hand.cards) == 2 and fjern == 1:
        stand = pg.draw.rect(screen, LightGreen, (1200,833,150,54),0)
        pg.font.init()
        stand_font = pg.font.SysFont("Comic Sans Ms",49)
        stand_surface = stand_font.render("Stand", False, (0,0,0))
        screen.blit(stand_surface, (1200,820))
        hit = pg.draw.rect(screen, LightGreen, (500,833,150,54),0)
        pg.font.init() 
        hit_font = pg.font.SysFont("Comic Sans Ms",49)
        hit_surface = hit_font.render("Hit", False, (0,0,0))
        screen.blit(hit_surface, (500,820))
        button_show = True

    if button_show == True:
        if stand.collidepoint(click_pos):
            click_pos = (0,0)
            dealer_show = True
            fjern += 1
        elif hit.collidepoint(click_pos):
            click_pos = (0,0)
            player_hit = True
        
    if dealer_show == True:
        for i, card in enumerate(dealer_hand.cards):
            screen.blit(card.image, (1650/2 + i*120, 300))
            pg.font.init()
            if dealer_hand.totalValue() < 17:
                for i in range(1):
                    dealer_hand.add_card(deck.deal())
                    if dealer_hand.totalValue() > 17 or dealer_hand.totalValue() < 21:
                        continue

    if player_hit == True:
        for i in range(1):
            player_hand.add_card(deck.deal())
            player_hit = False

    # Display player's hand value
    pg.font.init()
    font = pg.font.SysFont("Comic Sans MS", 50)
    hand_value_text = font.render(f"Player: {player_hand.totalValue()}", True, (255, 255, 255))
    screen.blit(hand_value_text, (200, 700)) 

    # Display dealer's hand value (if showing cards)
    if dealer_show:
        dealer_value_text = font.render(f"Dealer: {dealer_hand.totalValue()}", True, (255, 255, 255))
        screen.blit(dealer_value_text, (200, 100)) 
       
    if player_hand.totalValue() > 21:
        print("Du tabte")
        break

    # Limit/fix frame rate (fps)
    clock.tick(30)
    tick += 1
     
    pg.display.flip()
