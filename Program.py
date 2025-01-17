import pygame as pg
import random

# Overvejer at lave Blackjack - Du har en hand og spiller mod dealer

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
# Deck class, you get a Card, with a random suit from (1,5) and a random number from (1,14)
class Deck:
      def __init__(self):
            self.cards = [Card(suit, number) for suit in range(1,5) for number in range (1,14)]*6

# Filling the background with a image from the net.
background = pg.image.load(f'images/background.png')
background = pg.transform.scale(background, (1920,1080))

# Game loop
while True:
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
        
    pg.display.flip()