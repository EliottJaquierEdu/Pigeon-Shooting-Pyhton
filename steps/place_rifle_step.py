from abc import ABC

from steps.step import Step


class PlaceRifleStep(Step, ABC):
    def previous_step(self):
        return None

    def next_step(self):
        return None

    def update(self, screen, mouse_position, mouse_buttons, rifle, pigeon):
        if self.is_done:
            return
        mouse_position_vector_space = screen.convert_screen_to_vector(mouse_position)
        rifle.start_x = mouse_position_vector_space[0]
        rifle.start_y = mouse_position_vector_space[1]

        max_height = pigeon.y(pigeon.t(rifle.start_x))

        if rifle.start_y < max_height and rifle.start_y > 0 and rifle.start_x > 0:
            rifle.color = "Black"
            if mouse_buttons[2]:
                self._is_done = True
        else:
            rifle.color = "Red"


    def step_description(self):
        return "Placez le fusil avec un click droit (déplacez-vous avec un click gauche et zoomez avec la molette)"
