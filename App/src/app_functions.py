import pygame
from pygame.locals import *

from app_settings import *


# pygame.mixer.init()


def event_handler():
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            Power_Off()

        elif event.type == pygame.KEYUP:

            if event.key == K_ESCAPE:
                Power_Off()


def Display_Text(surface, text, size=20, color=WHITE, pos=None, centered=True):
    if pos is None:
        pos = [0, 0]
    font = pygame.font.Font(None, size)

    text_obj = font.render(text, True, color).convert_alpha()

    width, height = text_obj.get_size()

    if centered:
        pos[0] -= width // 2
        pos[1] -= height // 2

    surface.blit(text_obj, pos)


def Button(surface, x, y, target=False, old_state="title", new_state=False, option=False, args=None):
    pos = pygame.mouse.get_pos()
    keys = pygame.mouse.get_pressed()

    w, h = 200, 35
    x, y = x, y

    rect = pygame.surface.Surface([w, h])
    rect.convert()

    selected = False

    if pos[0] > x - w // 2 and pos[0] < x - w // 2 + w and pos[1] > y - h // 2 and pos[1] < y - h // 2 + h:
        selected = True
        rect.fill([200, 200, 255])
        surface.blit(rect, [x - w // 2, y - h // 2])

    else:
        selected = False
        rect.fill([170, 170, 255])
        surface.blit(rect, [x - w // 2, y - h // 2])

    if selected:
        if new_state:
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


def Power_Off():
    pygame.quit()
    raise SystemExit
