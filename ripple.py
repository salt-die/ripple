#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulated damped ripples.
"""
from numpy import array, zeros, pad, clip, dstack, concatenate
import pygame
from pygame.mouse import get_pos

def ripples():
    """
    Simulates ripples on a surface.
    """
    def update_array():
        """
        Ripple physics.
        """
        def pad_naughts(vector, pad_width, iaxis, kwargs):
            """
            Extra arguments needed for compatibility with numpy.
            """
            vector[:pad_width[0]] = 0
            vector[-pad_width[1]:] = 0

        nonlocal surface_array
        old_array = pad(surface_array, 1, pad_naughts) #pad borders with zeros
        shift_left = concatenate((old_array.T[-1:], old_array.T[:-1])).T
        shift_right = concatenate((old_array.T[1:], old_array.T[:1])).T
        shift_up = concatenate((old_array[1:], old_array[:1]))
        shift_down = concatenate((old_array[-1:], old_array[:-1]))

        surface_array = ((shift_left +\
                          shift_right +\
                          shift_up +\
                          shift_down) / 2)[1:-1, 1:-1] - surface_array

        surface_array *= .86 #damp waves
        clip(surface_array, -scale/2, scale/2, surface_array)
        #surface_array[abs(surface_array) < .1] = 0

    def color(surface_array):
        """
        Returns colors based on the values of surface_array.
        """
        color_1 = (65, 234, 186)
        color_2 = (13, 29, 135)
        return dstack([(abs(surface_array) * (c2 - c1) / scale + c1).astype(int)\
                       for c1, c2 in zip(color_1, color_2)])

    def get_user_input():
        """
        Takes care of clicks and close events.
        """
        nonlocal surface_array
        for event in pygame.event.get():
            if event.type == 12: #quit
                nonlocal running
                running = False
            elif event.type == 5: #mouse down
                if event.button == 1: #left-Click
                    surface_array[get_pos()] += 100
            elif event.type == 2: #key down
                if event.key == 114:
                    
                    surface_array = zeros((int(window_dim[0]),\
                                           int(window_dim[1])))

    #Game variables-----------------------------------------------------------
    window_dim = array([500.0, 500.0])
    window = pygame.display.set_mode(window_dim.astype(int))
    surface_array = zeros((int(window_dim[0]), int(window_dim[1])))
    clock = pygame.time.Clock() #For limiting fps
    scale = 1000
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
