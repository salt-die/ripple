#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
    force constant in user_input
    color_1, color_2 in color
"""
import numpy as np
import pygame
from pygame.mouse import get_pos
import scipy.ndimage as nd
from random import random

def ripple():
    """
    Simulates ripples on a surface.
    """
    def update_array():
        """
        Ripple physics.
        """
        nonlocal surface_array
        nonlocal old_array
        weights = np.array([[1, 1, 1],\
                            [1, 0, 1],\
                            [1, 1, 1]])
        #mode='wrap' if one wants periodic boundary conditions
        surface_array = nd.convolve(old_array, weights, mode='constant')\
                        / (np.sum(weights) / 2) - surface_array
        surface_array *= .99 #damp waves--constant should be between 0 and 1

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

    def automatic_ripples():
        nonlocal surface_array
        nonlocal interference
        nonlocal now
        if random() < .05:
            poke(int(random() * window_dim[0]),\
                 int(random() * window_dim[1]),\
                 10 * random())
        if random() < .0018:
            surface_array = np.zeros(window_dim)
        if pygame.time.get_ticks() - now > 30000:
            now = pygame.time.get_ticks()
            interference = not interference

    def poke(mouse_x, mouse_y, force):
        """
        Creates the start of a ripple.
        """
        nonlocal surface_array
        try:
            surface_array[mouse_x - 4:mouse_x + 5,\
                          mouse_y - 4:mouse_y + 5] -= drop * force
        except ValueError:
            #print("Poked too close to border.")
            pass

    def get_user_input():
        """
        Takes care of clicks, key presses, and close events.
        """
        nonlocal mouse_down
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                nonlocal running
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    mouse_down = True
                    poke(*get_pos(), 2.5)
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
            elif event.type == pygame.MOUSEMOTION and mouse_down:
                poke(*get_pos(), .1)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    nonlocal surface_array
                    nonlocal old_array
                    surface_array = np.zeros(window_dim)
                    old_array = np.copy(surface_array)
                elif event.key == pygame.K_j:
                    surface_array = np.zeros(window_dim)
                elif event.key == pygame.K_i:
                    nonlocal interference
                    interference = not interference
                elif event.key == pygame.K_a:
                    nonlocal auto
                    auto = not auto
                    if auto:
                        nonlocal now
                        now = pygame.time.get_ticks()

    #Game variables-----------------------------------------------------------
    window_dim = [500, 500]
    window = pygame.display.set_mode(window_dim)
    surface_array = np.zeros(window_dim)
    old_array = np.copy(surface_array)
    clock = pygame.time.Clock() #For limiting fps
    scale = 1000 #scale is arbitrary, but should be greater than 0
    #drop determines the shape of a poke; square pokes are unsightly
    drop = np.array([[0.0, 0.0, 1/6, 1/5, 1/4, 1/5, 1/6, 0.0, 0.0],\
                     [0.0, 1/6, 1/5, 1/4, 1/3, 1/4, 1/5, 1/6, 0.0],\
                     [1/6, 1/5, 1/4, 1/3, 1/2, 1/3, 1/4, 1/5, 1/6],\
                     [1/5, 1/2, 1/3, 1/2, 1.0, 1/2, 1/3, 1/4, 1/5],\
                     [1/4, 1/3, 1/2, 1.0, 1.0, 1.0, 1/2, 1/3, 1/4],\
                     [1/5, 1/2, 1/3, 1/2, 1.0, 1/2, 1/3, 1/4, 1/5],\
                     [1/6, 1/5, 1/4, 1/3, 1/2, 1/3, 1/4, 1/5, 1/6],\
                     [0.0, 1/6, 1/5, 1/4, 1/3, 1/4, 1/5, 1/6, 0.0],\
                     [0.0, 0.0, 1/6, 1/5, 1/4, 1/5, 1/6, 0.0, 0.0]])
    drop *= scale
    interference = True
    mouse_down = False
    auto = False
    now = 0
    #Main Loop----------------------------------------------------------------
    running = True
    while running:
        update_array()
        pygame.surfarray.blit_array(window, color(surface_array))
        get_user_input()
        if auto:
            automatic_ripples()
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
