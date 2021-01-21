# -*- coding: utf-8 -*-

"""
@author: Gallien FRESNAIS
"""

import pygame
from pygame.locals import *

# - Local - #
from App.src.app_settings import *

# pygame.mixer.init()

"""
Handles the events from the main pygame program
"""


def event_handler():
    for event in pygame.event.get():
        # if there's a QUIT event, power off the app
        if event.type == pygame.QUIT:
            Power_Off()
        elif event.type == pygame.KEYUP:
            # if there's a key pressed and it's the ESCAPE key, power off the app
            if event.key == K_ESCAPE:
                Power_Off()


"""
Displays text
"""


def Display_Text(surface, text, size=20, color=WHITE, pos=None, centered=True):
    # if no position is given, initialize it to 0,0
    if pos is None:
        pos = [0, 0]
    # initialize the text font
    font = pygame.font.Font(None, size)

    # render the text
    text_obj = font.render(text, True, color).convert_alpha()

    # get the text dimensions
    width, height = text_obj.get_size()

    # if the text needs to be centered, center it
    if centered:
        pos[0] -= width // 2
        pos[1] -= height // 2

    # add the text to the window surface
    surface.blit(text_obj, pos)


"""
Creates a Button
"""


def Button(surface, x, y, target=None, old_state="title", new_state=False, option=False, args=None):
    # gets the mouse position
    pos = pygame.mouse.get_pos()
    # gets the pressed mouse click event
    keys = pygame.mouse.get_pressed()

    w, h = 200, 35
    x, y = x, y

    # creates the button surface
    rect = pygame.surface.Surface([w, h])
    rect.convert()

    selected = False

    if x - w // 2 < pos[0] < x - w // 2 + w and y - h // 2 < pos[1] < y - h // 2 + h:
        selected = True
        rect.fill([200, 200, 255])
    else:
        selected = False
        rect.fill([170, 170, 255])

    surface.blit(rect, [x - w // 2, y - h // 2])

    if selected:
        if new_state:
            # if left click is pressed
            if keys[0]:
                return new_state
            else:
                return old_state

        elif target:
            if keys[0]:
                if args is not None:
                    return target(args)
                else:
                    return target()

        elif option:
            if keys[0]:
                return True
            else:
                return False

    else:
        if new_state:
            return old_state

        elif option:
            return False


"""
Creates a multi-line text
"""


def multi_line_text(surface, size=20, spacing=20, color=WHITE, pos=None, centered=True, *text):
    if pos is None:
        pos = [0, 0]
    next_line = 0

    for i in text:
        if i == "<n>":
            next_line += spacing
        else:
            Display_Text(surface, i, size, color, [pos[0], pos[1] + next_line], centered)
            next_line += spacing


"""
Exits the application
"""


def Power_Off():
    pygame.quit()
    raise SystemExit
