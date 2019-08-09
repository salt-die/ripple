#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulate dampled ripples.
"""
from numpy import array, zeros
import pygame
from pygame.mouse import get_pos as mouse_xy

def ripples():
    def update_values():
        pass
    
    def poke_array():
        pass
    
    def get_user_input():
        for event in pygame.event.get():
            if event.type == 12: #Quit
                nonlocal running
                running = False
            elif event.type == 5: #Mouse down
                if event.button == 1: #left-Click
                    poke_array(array(mouse_xy()))
    
    #Game variables-----------------------------------------------------------
    window_dim = array([800.0, 800.0])
    window = pygame.display.set_mode(window_dim.astype(int))
    surface_array = zeros((int(window_dim[0]),int(window_dim[1])))
    clock = pygame.time.Clock() #For limiting fps
    
    #Main Loop----------------------------------------------------------------
    running = True
    while running:
        update_values()
        pygame.surfarray.blit_array(window, surface_array)
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