"""
Simulates damped ripples.

click or click-and-hold to create ripples
'r' to reset
'j' to jostle
'i' to toggle interference
'a' to toggle automatic ripples

If you want to adjust settings, try:
    convolution kernel (weights) in update_array
    damping constant in update_array
    force parameter in poke calls
    color_1, color_2 in color
"""
import numpy as np
import pygame
from pygame.mouse import get_pos
import cv2

#DROP determines the shape of a poke; square pokes are unsightly
DROP = np.array([[0.0, 0.0, 1/6, 1/5, 1/4, 1/5, 1/6, 0.0, 0.0],
                 [0.0, 1/6, 1/5, 1/4, 1/3, 1/4, 1/5, 1/6, 0.0],
                 [1/6, 1/5, 1/4, 1/3, 1/2, 1/3, 1/4, 1/5, 1/6],
                 [1/5, 1/2, 1/3, 1/2, 1.0, 1/2, 1/3, 1/4, 1/5],
                 [1/4, 1/3, 1/2, 1.0, 1.0, 1.0, 1/2, 1/3, 1/4],
                 [1/5, 1/2, 1/3, 1/2, 1.0, 1/2, 1/3, 1/4, 1/5],
                 [1/6, 1/5, 1/4, 1/3, 1/2, 1/3, 1/4, 1/5, 1/6],
                 [0.0, 1/6, 1/5, 1/4, 1/3, 1/4, 1/5, 1/6, 0.0],
                 [0.0, 0.0, 1/6, 1/5, 1/4, 1/5, 1/6, 0.0, 0.0]])
KERNEL = np.array([[0.25, 0.25, 0.25],
                   [0.25,  0.0, 0.25],
                   [0.25, 0.25, 0.25]])
COLOR_1 = (16, 38, 89)
COLOR_2 = (35, 221, 221)
RGBs = tuple(zip(COLOR_1, COLOR_2))

class ripple:
    """
    Simulates ripples on a surface.
    """
    def __init__(self, dim):
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
        """
        Ripple physics.
        """
        self.surface_array = cv2.filter2D(self.old_array, ddepth=-1, kernel=KERNEL,
                                          borderType=1) - self.surface_array
        self.surface_array *= .99 #damp waves--constant should be between 0 and 1
        self.old_array, self.surface_array = self.surface_array, self.old_array

    def color(self):
        """
        Returns colors based on the values of surface_array. This is just a
        linear interpolation between COLOR_1 and COLOR_2.

        clipped prevents weird things from happening should a surface_array
        value be outside the range 0-1.
        """
        if self.interference:
            clipped = np.clip(abs(self.surface_array), 0, 1)
        else:
            clipped = np.clip(self.surface_array, -.5, .5)
            clipped += .5
        return np.dstack([(clipped * (c2 - c1) + c1).astype(int) for c1, c2 in RGBs])

    def automatic_ripples(self):
        if np.random.random() < .05:
            self.poke(int(np.random.random() * self.dim[0]),
                      int(np.random.random() * self.dim[1]),
                      10 * np.random.random())
        if np.random.random() < .0018:
            self.surface_array = np.zeros(self.dim)
        if pygame.time.get_ticks() - self.now > 30000:
            self.now = pygame.time.get_ticks()
            self.interference = not self.interference

    def poke(self, mouse_x, mouse_y, force):
        """
        Creates the start of a ripple.
        """
        try:
            self.surface_array[mouse_x - 4:mouse_x + 5,
                               mouse_y - 4:mouse_y + 5] -= DROP * force
        except ValueError:
            pass

    def get_user_input(self):
        """
        Takes care of clicks, key presses, and close events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.mouse_down = True
                    self.poke(*get_pos(), 2.5)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_down = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.surface_array = np.zeros(self.dim)
                    self.old_array = np.zeros(self.dim)
                elif event.key == pygame.K_j:
                    self.surface_array = np.zeros(self.dim)
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
            self.get_user_input()
            if self.auto:
                self.automatic_ripples()
            if self.mouse_down:
                self.poke(*get_pos(), .1)
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    ripple((500,500)).start()
