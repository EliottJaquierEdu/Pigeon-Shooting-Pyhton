import math

from pigeon import Pigeon
from rifle import Rifle
from screen import PyGameScalableGraphScreen

# Set the height and width of the screen
graphScreen = PyGameScalableGraphScreen("Tire au pigeon", 1200, 800)

rifle = Rifle("red", 0, 1, 2)
pigeon = Pigeon("black", 0, 5, 100)

graphScreen.add_graph_line(pigeon)
graphScreen.add_graph_line(rifle)

graphScreen.update()
# mousePosition = pygame.mouse.get_pos()
# angle = math.atan2(mousePosition[1], mousePosition[0])
# print(angle)
