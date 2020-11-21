"""
Simulates damped ripples.

click or click-and-hold to create ripples
'r' to reset
'j' to jostle
'i' to toggle interference
'a' to toggle automatic ripples
"""
import numpy as np
import pygame
from pygame.mouse import get_pos
from scipy.ndimage import convolve

# DROP determines the shape of a poke; square pokes are unsightly
DROP = np.array([[0.0, 0.0, 1/6, 1/5, 1/4, 1/5, 1/6, 0.0, 0.0],
                 [0.0, 1/6, 1/5, 1/4, 1/3, 1/4, 1/5, 1/6, 0.0],
                 [1/6, 1/5, 1/4, 1/3, 1/2, 1/3, 1/4, 1/5, 1/6],
                 [1/5, 1/4, 1/3, 1/2, 1.0, 1/2, 1/3, 1/4, 1/5],
                 [1/4, 1/3, 1/2, 1.0, 1.0, 1.0, 1/2, 1/3, 1/4],
                 [1/5, 1/4, 1/3, 1/2, 1.0, 1/2, 1/3, 1/4, 1/5],
                 [1/6, 1/5, 1/4, 1/3, 1/2, 1/3, 1/4, 1/5, 1/6],
                 [0.0, 1/6, 1/5, 1/4, 1/3, 1/4, 1/5, 1/6, 0.0],
                 [0.0, 0.0, 1/6, 1/5, 1/4, 1/5, 1/6, 0.0, 0.0]])

KERNEL = .25 * np.array([[1.0, 1.0, 1.0],
                         [1.0, 0.0, 1.0],
                         [1.0, 1.0, 1.0]])

COLOR_1 = 16, 38, 89
COLOR_2 = 35, 221, 221
RGBs = tuple(zip(COLOR_1, COLOR_2))

POKE_FORCE = 2.5
DRAG_FORCE = .1


class Ripple:
    def __init__(self, *dim):
        self.dim = dim
        self.window = pygame.display.set_mode(dim)
        self.surface_array = np.zeros(dim)
        self.old_array = np.zeros(dim)

        self.interference = True
        self.mouse_down = False
        self.auto = False
        self.now = 0
        self.running = True

    def update_array(self):
        self.surface_array = .99 * (convolve(self.old_array, KERNEL, mode="wrap") - self.surface_array)
        self.old_array, self.surface_array = self.surface_array, self.old_array

    def color(self):
        """
        Returns colors based on the values of surface_array. This is just a
        linear interpolation between COLOR_1 and COLOR_2.
        """
        if self.interference:
            clipped = np.clip(abs(self.surface_array), 0, 1)
        else:
            clipped = np.clip(self.surface_array, -.5, .5) + .5
        return np.dstack([(clipped * (c2 - c1) + c1).astype(int) for c1, c2 in RGBs])

    def automatic_ripples(self):
        if np.random.random() < .05:
            self.poke(*(np.random.random(2) * self.dim).astype(int), 10 * np.random.random())
        if np.random.random() < .0018:
            self.surface_array[:] = 0
        if pygame.time.get_ticks() - self.now > 30000:
            self.now = pygame.time.get_ticks()
            self.interference = not self.interference

    def poke(self, x=None, y=None, force=POKE_FORCE):
        if x is y is None:
            x, y = get_pos()
        try:
            self.surface_array[x - 4: x + 5, y - 4: y + 5] -= DROP * force
        except ValueError:
            pass

    def user_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.mouse_down = True
                    self.poke()
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.surface_array[:] = 0
                    self.old_array[:] = 0
                elif event.key == pygame.K_j:
                    self.surface_array[:] = 0
                elif event.key == pygame.K_i:
                    self.interference = not self.interference
                elif event.key == pygame.K_a:
                    self.auto = not self.auto
                    if self.auto:
                        self.now = pygame.time.get_ticks()

    def start(self):
        pygame.init()
        pygame.display.set_caption('ripple')
        while self.running:
            self.update_array()
            pygame.surfarray.blit_array(self.window, self.color())
            self.user_input()
            if self.auto:
                self.automatic_ripples()
            if self.mouse_down:
                self.poke()
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    Ripple(500, 500).start()
