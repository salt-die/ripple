#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulates damped ripples.

click on window to create a ripple
'r' to reset
'j' to jostle
'i' to toggle interference

If you want to adjust settings, try:
    damping constant in update_array
    force constant in user_input
    scale in ripple, though scale seems mostly arbitrary
    color_1, color_2 in color
"""
import numpy as np
import pygame
from pygame.mouse import get_pos
import scipy.ndimage as nd

def ripple():
    """
    Simulates ripples on a surface.
    """
    def update_array():
        """
        Ripple physics.

        We could avoid the padded_array if we wanted periodic boundary
        conditions, but I enjoy the ripples bouncing off the boundaries.
        """
        nonlocal surface_array
        nonlocal old_array
        weights = np.array([[0, 1, 0],\
                            [1, 0, 1],\
                            [0, 1, 0]])

        surface_array = nd.convolve(old_array, weights, mode='constant') / 2\
                        - surface_array
        surface_array *= .98 #damp waves--constant should be between 0 and 1

        temp = old_array
        old_array = surface_array
        surface_array = temp

    def color(surface_array):
        """
        Returns colors based on the values of surface_array. This is just a
        linear interpolation between color_1 and color_2.

        clipped prevents weird things from happening should a surface_array
        value be outside the range of our scale.
        """
        if interference:
            clipped = np.clip(abs(surface_array), 0, scale)
        else:
            clipped = np.clip(surface_array, -scale / 2, scale / 2)
            clipped += scale / 2
        color_1 = (16, 38, 89)
        color_2 = (35, 221, 221)
        return np.dstack([(clipped * (c2 - c1) / scale + c1).astype(int)\
                          for c1, c2 in zip(color_1, color_2)])

    def get_user_input():
        """
        Takes care of clicks and close events.
        """
        nonlocal surface_array
        nonlocal old_array
        for event in pygame.event.get():
            if event.type == 12: #quit
                nonlocal running
                running = False
            elif event.type == 5: #mouse down
                if event.button == 1: #left-Click
                    x, y = get_pos()
                    try:
                        force = 2
                        surface_array[x - 4:x + 5, y - 4:y + 5] -= poke * force
                    except ValueError:
                        print("Poked too close to border.")
            elif event.type == 2: #key down
                if event.key == 114: #r for reset
                    surface_array = np.zeros(window_dim)
                    old_array = np.copy(surface_array)
                elif event.key == 106: #j for jostle
                    surface_array = np.zeros(window_dim)
                elif event.key == 105: #i for interference
                    nonlocal interference
                    interference = not interference

    #Game variables-----------------------------------------------------------
    window_dim = [500, 500]
    window = pygame.display.set_mode(window_dim)
    surface_array = np.zeros(window_dim)
    old_array = np.copy(surface_array)
    clock = pygame.time.Clock() #For limiting fps
    scale = 10000
    poke = np.array([[0,   0,   1/6, 1/5, 1/4, 1/5, 1/6, 0,   0  ],\
                     [0,   1/6, 1/5, 1/4, 1/3, 1/4, 1/5, 1/6, 0  ],\
                     [1/6, 1/5, 1/4, 1/3, 1/2, 1/3, 1/4, 1/5, 1/6],\
                     [1/5, 1/2, 1/3, 1/2, 1,   1/2, 1/3, 1/4, 1/5],\
                     [1/4, 1/3, 1/2, 1,   1,   1,   1/2, 1/3, 1/4],\
                     [1/5, 1/2, 1/3, 1/2, 1,   1/2, 1/3, 1/4, 1/5],\
                     [1/6, 1/5, 1/4, 1/3, 1/2, 1/3, 1/4, 1/5, 1/6],\
                     [0,   1/6, 1/5, 1/4, 1/3, 1/4, 1/5, 1/6, 0  ],\
                     [0,   0,   1/6, 1/5, 1/4, 1/5, 1/6, 0,   0  ]])
    poke *= scale
    interference = True
    #Main Loop----------------------------------------------------------------
    running = True
    while running:
        update_array()
        pygame.surfarray.blit_array(window, color(surface_array))
        get_user_input()
        clock.tick(40)  #Limit frames per second (Comment out if you'd like)
        pygame.display.update()

def main():
    """
    Starts the simulation. Ends the simulation.
    """
    pygame.init()
    pygame.display.set_caption('ripple')
    ripple()
    pygame.quit()

if __name__ == "__main__":
    main()
