#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulate dampled ripples.
"""
from numpy import array, zeros, copy
import pygame
from pygame.mouse import get_pos

def ripples():


    def update_array():
        nonlocal surface_array
        nonlocal old_array
        old_array = copy(surface_array)
        max_x = surface_array.shape[0]
        max_y = surface_array.shape[1]
        #update interior
        def get_value(x, y):
            if  x < 0 or x > max_x:
                return 0
            elif y < 0 or y > max_y:
                return 0
            return old_array[x][y]

        for x in range(1, surface_array.shape[0]-1):
            for y in range(1, surface_array.shape[1]-1):
                surface_array[x][y] = (get_value[x - 1][y] +\
                                       get_value[x][y + 1] +\
                                       get_value[x + 1][y] +\
                                       get_value[x][y - 1]) / 4 -\
                                      get_value[x][y]

    def color(surface_array):
        pass

    def poke_array(loc):
        nonlocal surface_array
        x, y = loc
        surface_array[x][y] +=100

    def get_user_input():
        for event in pygame.event.get():
            if event.type == 12: #Quit
                nonlocal running
                running = False
            elif event.type == 5: #Mouse down
                if event.button == 1: #left-Click
                    poke_array(get_pos())

    #Game variables-----------------------------------------------------------
    window_dim = array([800.0, 800.0])
    window = pygame.display.set_mode(window_dim.astype(int))
    surface_array = zeros((int(window_dim[0]),int(window_dim[1])))
    old_array = copy(surface_array)
    clock = pygame.time.Clock() #For limiting fps

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