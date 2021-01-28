# -*- coding: utf-8 -*-

"""
@author: Gallien FRESNAIS
"""

# - Local - #
from App.src.pygame_test.app_menus import *
from App.src.pygame_test.app_settings import *

# - Global variables - #
decision_made = False
PlayerChoice = False
BotChoice = False
Wins = 0
Losses = 0
Draws = 0
game_done = False
winner = None

"""
Main program with pygame
"""


def Main():
    pygame.init()
    # pygame.display.set_icon(IMG_ICON)

    window = pygame.display.set_mode([WINDOW_W, WINDOW_H])
    # window.fill([170, 170, 255])
    pygame.display.update()

    global PlayerChoice
    global BotChoice
    global decision_made
    global game_done
    global winner
    global Wins
    global Losses
    global Draws

    winner = None
    decision_made = PlayerChoice = BotChoice = game_done = False
    Wins = Losses = Draws = 0

    increase_text = True
    text_size = 10

    state = "title"

    # loop indefinitely, will exit if it receives a QUIT signal from pygame.QUIT
    while True:

        window.fill([170, 170, 255])

        event_handler()

        if state == "title":
            pygame.display.set_caption(APP_NAME + " | Title Screen")
            state = Title_Screen(window)

        elif state == "main_menu":
            pygame.display.set_caption(APP_NAME + " | Main Menu")
            state = Main_Menu(window)

        elif state == "game_loop":
            pygame.display.set_caption(
                APP_NAME + " | {0} {1} - {2} BOT | Draws {3}".format("Player", Wins, Losses, Draws))
            state = Game_Loop(window)

        # if we are in the title screen or main menu screen
        if state in ["title", "main_menu"]:
            if text_size == 17:
                increase_text = False
            elif text_size == 10:
                increase_text = True
            if increase_text:
                text_size += 1
            else:
                text_size -= 1

            # prints the animated text
            Display_Text(window, "Hello", text_size, WHITE, [WINDOW_W // 2, 140])

            # prints the app name as the title
            Display_Text(window, APP_NAME, 55, pos=[WINDOW_W // 2, 100])

        # prints the application version at the bottom left
        Display_Text(window, "version {0} - by {1} - 2021".format(GAME_VERSION, AUTHOR), 15,
                     [200, 200, 255], [10, WINDOW_H - 23], False)

        pygame.time.delay(SCRIPT_DELAY)
        pygame.display.update()


"""
Loops the game
"""


def Game_Loop(window):
    # window.fill([170, 170, 255])

    state = "game_loop"

    global decision_made
    global PlayerChoice
    global BotChoice

    Display_Text(window, "Player", 40, pos=[WINDOW_W // 4, WINDOW_H // 8])
    Display_Text(window, "Computer", 40, pos=[WINDOW_W - WINDOW_W // 4, WINDOW_H // 8])

    # window.blit(IMG_HUM, [WINDOW_W // 4 - 75, WINDOW_H // 5])
    # window.blit(IMG_BOT, [WINDOW_W - WINDOW_W // 4 - 75, WINDOW_H // 5])

    if not decision_made:

        # Creates 3 buttons which are linked to the Player choice
        PlayerChoice = [
            Button(window, WINDOW_W // 5, WINDOW_H - 170, option=True),
            Button(window, WINDOW_W // 2, WINDOW_H - 170, option=True),
            Button(window, WINDOW_W - WINDOW_W // 5, WINDOW_H - 170, option=True)]

        Display_Text(window, "Rock", 25, pos=[WINDOW_W // 5, WINDOW_H - 170])
        Display_Text(window, "Paper", 25, pos=[WINDOW_W // 2, WINDOW_H - 170])
        Display_Text(window, "Scissors", 25, pos=[WINDOW_W - WINDOW_W // 5, WINDOW_H - 170])

        if True in PlayerChoice:
            decision_made = True

            if PlayerChoice[0]:
                PlayerChoice = "rock"

            elif PlayerChoice[1]:
                PlayerChoice = "paper"

            elif PlayerChoice[2]:
                PlayerChoice = "scissors"

    if decision_made:
        state = Result_Screen(window)

    return state


"""
Displays the result screen
"""


def Result_Screen(window):
    global PlayerChoice
    global BotChoice
    global Wins
    global Losses
    global Draws
    global game_done
    global winner

    if not game_done:
        if PlayerChoice == "scissors":
            if BotChoice == "paper":
                Wins += 1
                winner = "player"
            else:
                Losses += 1
                winner = "com"

        elif PlayerChoice == "paper":
            if BotChoice == "rock":
                Wins += 1
                winner = "player"
            else:
                Losses += 1
                winner = "com"

        elif PlayerChoice == "rock":
            if BotChoice == "scissors":
                Wins += 1
                winner = "player"
            else:
                Losses += 1
                winner = "com"

    game_done = True

    Display_Text(window, "Wins {0}".format(Wins), 20, pos=[WINDOW_W // 4, WINDOW_H // 15])
    Display_Text(window, "Wins {0}".format(Losses), 20, pos=[WINDOW_W - WINDOW_W // 4, WINDOW_H // 15])

    if winner == "player":
        Display_Text(window, "Won!", 30, color=GREEN, pos=[WINDOW_W // 4, WINDOW_H // 5 + 175])
        Display_Text(window, "Lost!", 30, color=RED, pos=[WINDOW_W - WINDOW_W // 4, WINDOW_H // 5 + 175])
        # window.blit(IMG_BOTLOSE, [WINDOW_W - WINDOW_W // 4 - 41, WINDOW_H // 5 + 41])

    elif winner == "com":
        Display_Text(window, "Lost!", 30, color=RED, pos=[WINDOW_W // 4, WINDOW_H // 5 + 175])
        Display_Text(window, "Won!", 30, color=GREEN,
                     pos=[WINDOW_W - WINDOW_W // 4, WINDOW_H // 5 + 175])
        # window.blit(IMG_BOTWIN, [WINDOW_W - WINDOW_W // 4 - 41, WINDOW_H // 5 + 41])

    else:
        Display_Text(window, "Draw", 30, pos=[WINDOW_W // 2, WINDOW_H // 5 + 175])

    Display_Text(window, PlayerChoice, 20, pos=[WINDOW_W // 4, WINDOW_H // 8 + 25])
    # Display_Text(window, BotChoice, 20, pos=[WINDOW_W - WINDOW_W // 4, WINDOW_H // 8 + 25])

    Button(window, WINDOW_W // 3, WINDOW_H - 120, target=Reset_Game)

    exit = Button(window, WINDOW_W - WINDOW_W // 3, WINDOW_H - 120, target=Reset_Game, args=True)

    Display_Text(window, "Play Again", 25, pos=[WINDOW_W // 3, WINDOW_H - 120])
    Display_Text(window, "Main Menu", 25, pos=[WINDOW_W - WINDOW_W // 3, WINDOW_H - 120])

    if exit:
        # window.fill([170, 170, 255])
        return "main_menu"
    else:
        return "game_loop"


"""
Resets the game
"""


def Reset_Game(change_state=False):
    global decision_made
    global PlayerChoice
    global BotChoice
    global game_done
    global winner

    game_done = PlayerChoice = BotChoice = decision_made = False
    winner = None

    if change_state:
        return True
    else:
        return False


if __name__ == '__main__':
    Main()
