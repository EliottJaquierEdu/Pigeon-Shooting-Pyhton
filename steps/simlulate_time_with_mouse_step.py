from abc import ABC

import pygame

from steps.step import Step


def no_space_convertion(vector):
    return [vector[0], vector[1]]


class SimulateTimeWithMouseStep(Step, ABC):
    def __init__(self, rifle, pigeon):
        super().__init__(rifle, pigeon)
        self.is_auto_simulating = False
        self.is_options_panel_visible = False
        self.is_playing_audio = False
        self.box_width = 500
        self.box_height = 400
        self.time = 0
        self.intersecting_time = self.rifle.time_intersecting_with_pigeon(self.pigeon)
        self.rifle.wait_time = self.rifle.waiting_time_to_intersect(self.pigeon)

        self.title_font = pygame.font.SysFont('Open Sans', 30)
        self.title_color = pygame.Color(40, 60, 90)

    def next_step(self):
        return None

    def update(self, screen, mouse_position, playtime):
        if self.is_done:
            return
        mouse_position_vector_space = screen.convert_screen_to_vector(mouse_position)
        self.time = self.pigeon.t(mouse_position_vector_space[0])
        if self.is_auto_simulating:
            times = self.pigeon.time_when_zeros()
            landing = max(times[0], times[1])
            self.time = playtime % (landing + 2)

        if self.is_playing_audio:
            self.rifle.play_audio(self.time, playtime, 1 if self.is_auto_simulating else 20)

        if self.is_options_panel_visible:
            self.pigeon.draw_point_in_time(screen.screen, screen.convert_vector_to_screen,
                                          "white", 7)

            self.rifle.draw_point_in_time(screen.screen, screen.convert_vector_to_screen,
                                          "white", 7)

        self.pigeon.draw_image_representation(screen.screen, self.time, self.intersecting_time,
                                              screen.convert_vector_to_screen)
        self.rifle.draw_image_representation(screen.screen, self.time, screen.convert_vector_to_screen)

    def on_hud(self, screen, width, height, draw_text_function, default_font, default_color):
        super().on_hud(screen, width, height, draw_text_function, default_font, default_color)
        if (not self.is_options_panel_visible):
            return
        surface = pygame.Surface([self.box_width, self.box_height], pygame.SRCALPHA)
        pygame.draw.rect(surface, (150, 200, 250, 128 + 64), (0, 0, self.box_width, self.box_height))
        draw_text_function(surface, self.title_font, "Situation de départ:", self.title_color, self.box_width / 2, 6)
        draw_text_function(surface, default_font,
                           "Pigeon " + self.get_string_from_vector(self.pigeon.get_point(0, no_space_convertion), "[m]",
                                                                   1) + " ,  a = " + str(
                               round(self.pigeon.angle, 1)) + "°" + ",  v  = " + str(
                               round(self.pigeon.speed, 1)) + " [m/s]", default_color, 6, 24 * 1 + 12, 0)
        draw_text_function(surface, default_font,
                           "Fusil " + self.get_string_from_vector(self.rifle.get_point(0, no_space_convertion), "[m]",
                                                                  1) + " ,  a = " + str(
                               round(self.rifle.angle, 1)) + "°" + ", v  = " + str(
                               round(self.rifle.speed, 1)) + " [m/s]", default_color, 6, 24 * 2 + 12, 0)
        draw_text_function(surface, default_font, "g = " + str(-self.pigeon.acceleration) + " [m/s2]", default_color, 6,
                           24 * 3 + 12, 0)
        draw_text_function(surface, default_font,
                           "Temps d'attente du fusil = " + str(round(self.rifle.wait_time, 3)) + " [s]", default_color,
                           6, 24 * 4 + 12, 0)
        draw_text_function(surface, default_font, "Point de rencontre " + self.get_string_from_vector(
            self.rifle.get_point(self.intersecting_time, no_space_convertion), "[m]", 3) + " ,  t = " + str(
            round(self.intersecting_time, 3)) + " [s]", default_color, 6, 24 * 5 + 12, 0)
        draw_text_function(surface, self.title_font, "Situation actuelle:", self.title_color, self.box_width / 2,
                           24 * 7)
        draw_text_function(surface, default_font, "Temps = " + str(round(self.time, 2)) + " [s]", default_color, 6,
                           24 * 8 + 12, 0)
        draw_text_function(surface, default_font, "Pigeon " + self.get_string_from_vector(
            self.pigeon.get_point(self.time, no_space_convertion), "[m]", 1), default_color, 6, 24 * 9 + 12, 0)
        draw_text_function(surface, default_font,
                           "Balle " + self.get_string_from_vector(self.rifle.get_point(self.time, no_space_convertion),
                                                                  "[m]", 1), default_color, 6, 24 * 10 + 12, 0)
        draw_text_function(surface, self.title_font, "Options en plus:", self.title_color, self.box_width / 2, 24 * 12)
        draw_text_function(surface, default_font, "Lecteur en temps rééle (touche espace) : " + (
            "automatique" if self.is_auto_simulating else "manuelle"), default_color, 6, 24 * 13 + 12, 0)
        draw_text_function(surface, default_font,
                           "Sond (touche 's') : " + ("activé" if self.is_playing_audio else "désactivé"), default_color,
                           6, 24 * 14 + 12, 0)
        screen.blit(surface, (0, 48 + 24))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.is_auto_simulating = not self.is_auto_simulating

        if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
            self.is_options_panel_visible = not self.is_options_panel_visible

        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            self.is_playing_audio = not self.is_playing_audio

    def step_description(self):
        return "Tout est prêt! Parcourez le graphe avec votre souris pour voir la simulation et appuyez sur la touche 'i' pour voir plus d'infos."
