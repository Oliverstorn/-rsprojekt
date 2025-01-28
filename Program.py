import pygame as pg
import random


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
    def __init__(self, cards):
        self.cards = cards

    def totalValue(self):
      self.handValue = 0
      for card in self.cards:
        if card.number > 10:
          self.handValue += 10
        else:
          self.handValue += card.number


# Filling the background with a image from the net.
background = pg.image.load(f'images/background.png')
background = pg.transform.scale(background, (1920,1080))

# Initialize deck and shuffle
deck = Deck()
deck.shuffle()

# Player and dealer hands
player_hand = []
dealer_hand = []

dealer_card_dealt = False
player_card_dealt = False

click_pos = (0,0)

BLACK = (00,64,00)

running = True

# Game loop
while running:

    # if stand:
    #   dealer += card
    #   if dealer_deck > 21:
    #       print("Player won")
    #       break
    #   elif dealer_deck >= 17 and <= 21 and player_deck < dealer_deck:
    #       print("Dealer won")
    #       break
    #   elif dealer_deck >= 17 and <= 21 and player_deck > dealer_deck: 
    #       print("Player won")
    #       break

    # if hit:
    #   player += card
    #   if player_deck > 21:
    #       print("Busted... Dealer won")
    #       break
    #
    #   elif player_deck >= 17 and <= 21 and stand:
    #       dealer += card
    #
    #       if dealer_deck > 21:
    #           print("Player won")
    #           break
    #
    #       elif dealer_deck >= 17 and <= 21 and player_deck < dealer_deck:
    #           print("Dealer won")
    #           break
    #
    #   elif stand:
    #       continue stand

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
                    player_hand.append(deck.deal())


        elif event.type == pg.MOUSEBUTTONDOWN:
            click_pos = event.pos

            

    if not running:
        break

    start = pg.draw.rect(screen, BLACK, (800,150,300,100),0) 
    pg.font.init()
    start_font = pg.font.SysFont("Comic Sans Ms",110)
    start_surface = start_font.render("Start", False, (0,0,0))
    screen.blit(start_surface, (800,120))
    

    # Button to start the game
    if start.collidepoint(click_pos):
        click_pos = (0,0)
        
        if len(player_hand) == 0 and not player_card_dealt:
            player_hand.append(deck.deal())
            player_card_dealt = True 

        # Check if the dealer needs a card (only when the player's first card is dealt)
        if len(player_hand) == 1 and not dealer_card_dealt:
            dealer_hand.append(deck.deal())
            dealer_card_dealt = True  # Set the flag to True so it doesn't deal again 

     # Draw player cards
    for i, card in enumerate(player_hand):
        screen.blit(card.image, (1650/2 + i*120, 750))  # Position cards in a row

     # Draw dealer cards
    for i, card in enumerate(dealer_hand):
        screen.blit(card.image, (1500/2 + i*120, 300))  # Position cards in a row
    
     
    pg.display.flip()
