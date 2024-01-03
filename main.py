import math

from graph_axis import GraphAxis
from pigeon import Pigeon
from rifle import Rifle
from screen import PyGameScalableGraphScreen

# Set the height and width of the screen
graphScreen = PyGameScalableGraphScreen("Tire au pigeon", 1600, 900)

pigeon = Pigeon("black", 0, 5, 100)
rifle = Rifle("red", 2)

graphScreen.add_graph_line(pigeon)
graphScreen.add_graph_line(rifle)

graphScreen.add_axe(GraphAxis("width", "meters", "black", 25, False))
graphScreen.add_axe(GraphAxis("height", "meters", "black", 25, True))

graphScreen.update()
# mousePosition = pygame.mouse.get_pos()
# angle = math.atan2(mousePosition[1], mousePosition[0])
# print(angle)
