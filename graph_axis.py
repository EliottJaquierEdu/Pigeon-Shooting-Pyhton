import pygame.draw


class GraphAxis:
    def __init__(self, name, unit, color, text_size, is_vertical):
        self.name = name
        self.unit = unit
        self.color = color
        self.washed_color = pygame.Color(89, 120, 180)
        self.is_vertical = is_vertical
        self.font = pygame.font.SysFont('Open Sans', text_size)
        self.line_width = 1
        self.line_width_on_ten = 3

    def draw(self, surface, screen_width, screen_height, x_offset, y_offset, mantissa, multiplier):
        lines_width = 20

        draw_count = int((screen_height if self.is_vertical else screen_width) / mantissa)
        offset_count = int(((y_offset + screen_height) if self.is_vertical else x_offset) / mantissa)
        for i in range(-offset_count, draw_count + 1 - offset_count):
            # Draw whole line
            pygame.draw.line(surface, self.color if (i % 10 == 0) else self.washed_color,
                             [-screen_width, y_offset + screen_height + i * mantissa] if self.is_vertical else
                             [x_offset + i * mantissa, -screen_height],
                             [screen_width, y_offset + screen_height + i * mantissa] if self.is_vertical else
                             [x_offset + i * mantissa, screen_height], self.line_width)
            # Draw line marker at axis
            pygame.draw.line(surface, self.color,
                             [x_offset - lines_width, y_offset + screen_height + i * mantissa] if self.is_vertical else
                             [x_offset + i * mantissa, -lines_width + screen_height + y_offset],
                             [x_offset + lines_width, y_offset + screen_height + i * mantissa] if self.is_vertical else
                             [x_offset + i * mantissa, lines_width + screen_height + y_offset],
                             self.line_width_on_ten if (i % 10 == 0) else self.line_width)
            # Draw text
            number = i * 10 / multiplier
            if self.is_vertical:
                number = -number
            if number == int(number):
                number = int(number)
            text_surface = self.font.render(str(number), False, self.color)
            surface.blit(text_surface,
                         [x_offset + 10, y_offset - 10 + screen_height + i * mantissa] if self.is_vertical else
                         [x_offset + i * mantissa - 5, -30 + screen_height + y_offset])
