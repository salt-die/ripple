#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulates damped ripples.

click on window to create a ripple
'r' to reset
'j' to jostle
"""
from numpy import zeros, pad, dstack, roll, copy, clip
import pygame
from pygame.mouse import get_pos

def ripples():
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

        padded_array = pad(old_array, 1, 'constant') #pad borders with zeros
        shift_left = roll(padded_array, -1, axis=1)[1:-1, 1:-1]
        shift_right = roll(padded_array, 1, axis=1)[1:-1, 1:-1]
        shift_up = roll(padded_array, -1, axis=0)[1:-1, 1:-1]
        shift_down = roll(padded_array, 1, axis=0)[1:-1, 1:-1]

        surface_array = (shift_left + shift_right + shift_up + shift_down) / 2\
                        - surface_array
        surface_array *= .96 #damp waves

        temp = old_array
        old_array = surface_array
        surface_array = temp

    def color(surface_array):
        """
        Returns colors based on the values of surface_array. This is just a
        linear interpolation between color_1 and color_2.

        clipped prevents weird things from happening should a surface_array
        value be outside the range of our scale.

        Alternatively to current clipped, one can take the absolute value of
        surface array and clip from 0 to scale.
        """
        clipped = clip(surface_array, -scale / 2, scale / 2)
        clipped += scale / 2
        #clipped = clip(abs(surface_array), 0, scale)
        color_1 = (65, 234, 186)
        color_2 = (13, 29, 135)
        return dstack([(clipped * (c2 - c1) / scale + c1).astype(int)\
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
                    surface_array[x - 4:x + 4, y - 4:y + 4] -= scale
            elif event.type == 2: #key down
                if event.key == 114: #r
                    surface_array = zeros(window_dim)
                    old_array = copy(surface_array)
                elif event.key == 106: #j for jostle
                    surface_array = zeros(window_dim)

    #Game variables-----------------------------------------------------------
    window_dim = [500, 500]
    window = pygame.display.set_mode(window_dim)
    surface_array = zeros(window_dim)
    old_array = copy(surface_array)
    clock = pygame.time.Clock() #For limiting fps
    scale = 10000
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
    pygame.display.set_caption('ripples')
    ripples()
    pygame.quit()

if __name__ == "__main__":
    main()
