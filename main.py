import math

import pygame
from math import pi

from pigeon import Pigeon
from rifle import Rifle
from screen import GraphScreen

# Initialize pygame
pygame.init()

# Set the height and width of the screen
graphScreen = GraphScreen(1200, 800)
screen = pygame.display.set_mode([graphScreen.width, graphScreen.height])

pygame.display.set_caption("Tire au pigeon")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()

rifle = Rifle()
pigeon = Pigeon()

curvePoints = []
timeSamples = 100
maxTime = 5
graphSize = 30
for i in range(timeSamples):
    time = (i/timeSamples) * maxTime
    curvePoints.append(graphScreen.convertVectorToScreen([pigeon.x(time), pigeon.y(time)]))

while not done:
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    # Clear the screen and set the screen background
    screen.fill("white")

    # Draw on the screen 3 black lines, each 5 pixels wide.
    # The 'False' means the first and last points are not connected.
    pygame.draw.lines(
        screen, "black", False, curvePoints, 5
    )

    mousePosition = pygame.mouse.get_pos()
    angle = math.atan2(mousePosition[1], mousePosition[0])
    print(angle)

    riflePoints = [graphScreen.convertVectorToScreen([rifle.x(0), rifle.y(0)]),
                   graphScreen.convertVectorToScreen([rifle.x(1), rifle.y(1)])]

    pygame.draw.lines(
        screen, "red", False, riflePoints, 5
    )

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()
