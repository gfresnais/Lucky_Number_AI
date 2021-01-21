from app_menus import *
from app_settings import *

decision_made = False
PlayerChoice = False
BotChoice = False
Wins = 0
Losses = 0
Draws = 0
Combo = 0
game_done = False
winner = None


def Main():
    pygame.init()
    # pygame.display.set_icon(IMG_ICON)

    window = pygame.display.set_mode([WINDOW_W, WINDOW_H])
    window.fill([170, 170, 255])
    pygame.display.update()

    FPS = pygame.time.Clock()

    global PlayerChoice
    global BotChoice
    global decision_made
    global game_done
    global winner
    global Wins
    global Losses
    global Draws
    global Combo

    winner = None
    decision_made = PlayerChoice = BotChoice = game_done = False
    Wins = Losses = Draws = Combos = 0

    increase_text = True
    text_size = 10

    state = "title"

    while True:

        app_functions.event_handler()

        if state == "title":
            pygame.display.set_caption(APP_NAME + " | Title Screen")
            state = Title_Screen(window)

        elif state == "main_menu":
            pygame.display.set_caption(APP_NAME + " | Main Menu")
            state = Main_Menu(window)


        elif state == "controls":
            pygame.display.set_caption(APP_NAME + " | Controls")
            state = Controls(window)

        elif state == "game_loop":
            pygame.display.set_caption(
                APP_NAME + " | {0} {1} - {2} BOT | Combo x{3} | Draws {4}".format("Player", Wins, Losses,
                                                                                   Combo, Draws))
            state = Game_Loop(window)

        if state in ["title", "main_menu", "controls"]:
            if state != "controls":
                if text_size == 17:
                    increase_text = False

                elif text_size == 10:
                    increase_text = True

                if increase_text:
                    text_size += 1

                else:
                    text_size -= 1

                app_functions.Display_Text(window, "Hello", text_size, WHITE, [WINDOW_W // 2, 140])

            app_functions.Display_Text(window, APP_NAME, 55, pos=[WINDOW_W // 2, 100])
            app_functions.Display_Text(window, "version {0} - by {1} - 2018".format(GAME_VERSION, AUTHOR), 15,
                                       [200, 200, 255], [10, WINDOW_H - 23], False)

        pygame.time.delay(SCRIPT_DELAY)
        pygame.display.update()
        FPS.tick(FRAMES)


def Game_Loop(window):
    window.fill([170, 170, 255])

    state = "game_loop"

    global decision_made
    global PlayerChoice
    global BotChoice
    global bot

    app_functions.Display_Text(window, "Player", 40, pos=[WINDOW_W // 4, WINDOW_H // 8])
    app_functions.Display_Text(window, "Computer", 40, pos=[WINDOW_W - WINDOW_W // 4, WINDOW_H // 8])

    #window.blit(IMG_HUM, [WINDOW_W // 4 - 75, WINDOW_H // 5])
    #window.blit(IMG_BOT, [WINDOW_W - WINDOW_W // 4 - 75, WINDOW_H // 5])

    if not decision_made:

        PlayerChoice = [
            app_functions.Button(window, WINDOW_W // 5, WINDOW_H - 170, option=True),
            app_functions.Button(window, WINDOW_W // 2, WINDOW_H - 170, option=True),
            app_functions.Button(window, WINDOW_W - WINDOW_W // 5, WINDOW_H - 170, option=True)]

        app_functions.Display_Text(window, "Rock", 25, pos=[WINDOW_W // 5, WINDOW_H - 170])
        app_functions.Display_Text(window, "Paper", 25, pos=[WINDOW_W // 2, WINDOW_H - 170])
        app_functions.Display_Text(window, "Scissors", 25, pos=[WINDOW_W - WINDOW_W // 5, WINDOW_H - 170])

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


def Result_Screen(window):
    global PlayerChoice
    global BotChoice
    global Wins
    global Losses
    global Combo
    global Draws
    global game_done
    global winner

    if not game_done:
        if PlayerChoice != BotChoice:
            if PlayerChoice == "scissors":
                if BotChoice == "paper":
                    Wins += 1
                    Combo += 1
                    winner = "player"

                else:
                    Losses += 1
                    Combo = 0
                    winner = "com"

            elif PlayerChoice == "paper":
                if BotChoice == "rock":
                    Wins += 1
                    Combo += 1
                    winner = "player"

                else:
                    Losses += 1
                    Combo = 0
                    winner = "com"

            elif PlayerChoice == "rock":
                if BotChoice == "scissors":
                    Wins += 1
                    Combo += 1
                    winner = "player"

                else:
                    Losses += 1
                    Combo = 0
                    winner = "com"

            game_done = True

        if PlayerChoice == BotChoice:
            Combo = 0
            Draws += 1
            game_done = True

    app_functions.Display_Text(window, "Wins {0}".format(Wins), 20, pos=[WINDOW_W // 4, WINDOW_H // 15])
    app_functions.Display_Text(window, "Wins {0}".format(Losses), 20, pos=[WINDOW_W - WINDOW_W // 4, WINDOW_H // 15])

    if Combo > 1:
        app_functions.Display_Text(window, "x{0}".format(Combo), 20, color=[255, 255, 0],
                                   pos=[WINDOW_W // 4 + 60, WINDOW_H // 5 + 175])

    if winner == "player":
        app_functions.Display_Text(window, "Won!", 30, color=GREEN, pos=[WINDOW_W // 4, WINDOW_H // 5 + 175])
        app_functions.Display_Text(window, "Lost!", 30, color=RED, pos=[WINDOW_W - WINDOW_W // 4, WINDOW_H // 5 + 175])
        #window.blit(IMG_BOTLOSE, [WINDOW_W - WINDOW_W // 4 - 41, WINDOW_H // 5 + 41])

    elif winner == "com":
        app_functions.Display_Text(window, "Lost!", 30, color=RED, pos=[WINDOW_W // 4, WINDOW_H // 5 + 175])
        app_functions.Display_Text(window, "Won!", 30, color=GREEN,
                                   pos=[WINDOW_W - WINDOW_W // 4, WINDOW_H // 5 + 175])
        #window.blit(IMG_BOTWIN, [WINDOW_W - WINDOW_W // 4 - 41, WINDOW_H // 5 + 41])

    else:
        app_functions.Display_Text(window, "Draw", 30, pos=[WINDOW_W // 2, WINDOW_H // 5 + 175])

    app_functions.Display_Text(window, PlayerChoice, 20, pos=[WINDOW_W // 4, WINDOW_H // 8 + 25])
    # app_functions.Display_Text(window, BotChoice, 20, pos=[WINDOW_W - WINDOW_W // 4, WINDOW_H // 8 + 25])

    app_functions.Button(window, WINDOW_W // 3, WINDOW_H - 120, target=Reset_Game)

    exit = app_functions.Button(window, WINDOW_W - WINDOW_W // 3, WINDOW_H - 120, target=Reset_Game, args=True)

    app_functions.Display_Text(window, "Play Again", 25, pos=[WINDOW_W // 3, WINDOW_H - 120])
    app_functions.Display_Text(window, "Main Menu", 25, pos=[WINDOW_W - WINDOW_W // 3, WINDOW_H - 120])

    if exit:
        window.fill([170, 170, 255])
        return "main_menu"

    else:
        return "game_loop"


def Reset_Game(change_state=False):
    global decision_made
    global PlayerChoice
    global BotChoice
    global game_done
    global winner

    game_done = False
    winner = None
    PlayerChoice = False
    BotChoice = False
    decision_made = False

    if change_state:
        return True

    else:
        return False


if __name__ == '__main__':
    Main()
