import pygame


def no_space_convertion(vector):
    return [vector[0], vector[1]]


class DebugBar:
    def __init__(self):
        self.is_visible = False
        self.box_width = 500
        self.box_height = 400

        self.title_font = pygame.font.SysFont('Open Sans', 30)
        self.title_color = pygame.Color(40, 60, 90)

    def get_string_from_vector(self, vector, unit, ndigits):
        return "x = " + str(round(vector[0], ndigits)) + " " + unit + " ,  y = " + str(
            round(vector[1], ndigits)) + " " + unit

    def draw(self, screen, draw_txt_fn, default_font, default_color, pigeon, rifle, time, intersecting_time,
             is_playing_audio, is_auto_simulating):
        if not self.is_visible:
            return

        surface = pygame.Surface([self.box_width, self.box_height], pygame.SRCALPHA)
        pygame.draw.rect(surface, (150, 200, 250, 128 + 64), (0, 0, self.box_width, self.box_height))

        draw_txt_fn(surface, self.title_font, "Situation de départ:", self.title_color, self.box_width / 2, 6)
        draw_txt_fn(surface, default_font,
                    "Pigeon " + self.get_string_from_vector(pigeon.get_point(0, no_space_convertion), "[m]",
                                                            1) + " ,  a = " + str(
                        round(pigeon.angle, 1)) + "°" + ",  v  = " + str(
                        round(pigeon.speed, 1)) + " [m/s]", default_color, 6, 24 * 1 + 12, 0)
        draw_txt_fn(surface, default_font,
                    "Fusil " + self.get_string_from_vector(rifle.get_point(0, no_space_convertion), "[m]",
                                                           1) + " ,  a = " + str(
                        round(rifle.angle, 1)) + "°" + ", v  = " + str(
                        round(rifle.speed, 1)) + " [m/s]", default_color, 6, 24 * 2 + 12, 0)
        draw_txt_fn(surface, default_font, "g = " + str(-pigeon.acceleration) + " [m/s2]", default_color, 6,
                    24 * 3 + 12, 0)
        draw_txt_fn(surface, default_font,
                    "Temps d'attente du fusil = " + str(round(rifle.wait_time, 3)) + " [s]", default_color,
                    6, 24 * 4 + 12, 0)
        draw_txt_fn(surface, default_font, "Point de rencontre " + self.get_string_from_vector(
            rifle.get_point(intersecting_time, no_space_convertion), "[m]", 3) + " ,  t = " + str(
            round(intersecting_time, 3)) + " [s]", default_color, 6, 24 * 5 + 12, 0)
        draw_txt_fn(surface, self.title_font, "Situation actuelle:", self.title_color, self.box_width / 2,
                    24 * 7)
        draw_txt_fn(surface, default_font, "Temps = " + str(round(time, 2)) + " [s]", default_color, 6,
                    24 * 8 + 12, 0)
        draw_txt_fn(surface, default_font, "Pigeon " + self.get_string_from_vector(
            pigeon.get_point(time, no_space_convertion), "[m]", 1), default_color, 6, 24 * 9 + 12, 0)
        draw_txt_fn(surface, default_font,
                    "Balle " + self.get_string_from_vector(rifle.get_point(time, no_space_convertion),
                                                           "[m]", 1), default_color, 6, 24 * 10 + 12, 0)
        draw_txt_fn(surface, self.title_font, "Options en plus:", self.title_color, self.box_width / 2, 24 * 12)
        draw_txt_fn(surface, default_font, "Lectur en temps réél (touche espace) : " + (
            "automatique" if is_auto_simulating else "manuelle"), default_color, 6, 24 * 13 + 12, 0)
        draw_txt_fn(surface, default_font,
                    "Sond (touche 's') : " + ("activé" if is_playing_audio else "désactivé"), default_color,
                    6, 24 * 14 + 12, 0)

        screen.blit(surface, (0, 48 + 24))
