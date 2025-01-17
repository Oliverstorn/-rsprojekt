import pygame as pg
import random

# Overvejer at lave Blackjack - Du har en hand og spiller mod dealer

# Setup
pg.init()
clock = pg.time.Clock()

# Setting the screen up
screen = pg.display.set_mode((1920,1080))
pg.display.set_caption("Blackjack")

clubs = []
hearts = []
diamonds = []
spades = []

while True:
    screen.fill("black")
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