# -*- coding: utf-8 -*-

"""
@author: Gallien FRESNAIS
"""

import pygame

# - Local - #
from App.src.app_functions import *
from App.src.app_settings import *

"""
Handles the title screen
"""


def Title_Screen(window):
    window.fill([170, 170, 255])

    # gets the mouse left click event
    keys = pygame.mouse.get_pressed()

    Display_Text(window, "Press the Left Mouse Button", 25, pos=[WINDOW_W // 2, WINDOW_H // 2 + 50])
    # if the left click is pressed, go to the main menu
    if keys[0]:
        return "main_menu"
    # else stay at the title screen
    else:
        return "title"


"""
Handles the main menu
"""


def Main_Menu(window):
    window.fill([170, 170, 255])

    state = "main_menu"

    # Creates the "play" button
    game = Button(window, WINDOW_W // 2, WINDOW_H // 2, old_state="main_menu", new_state="game_loop")
    # Creates the "exit" button
    Button(window, WINDOW_W // 2, WINDOW_H // 2 + 50, target=Power_Off)

    multi_line_text(window, 25, 50, WHITE, [WINDOW_W // 2, WINDOW_H // 2], True,
                    "Play",
                    "Exit")

    if game != state:
        return game
    else:
        return state
