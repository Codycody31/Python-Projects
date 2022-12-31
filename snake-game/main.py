# Imports
import os
import random
import time

import psutil
import pygame

from config import GameData

# init and check for errors
if not pygame.font:
    print('Warning, fonts disabled')
if not pygame.mixer:
    print('Warning, sound disabled')
if not pygame.image:
    print('Warning, images disabled')

# init pygame and mixer
pygame.init()

# Path
directory = os.path.dirname(__file__) + "\\"

# Check if their are any other instances of the game running
for proc in psutil.process_iter():
    if proc.name() == "python.exe":
        if proc.cmdline()[1] == directory + "main.py":
            print("Another instance of the game is already running")
            quit()

# set icon of the game
icon = pygame.image.load(directory + 'snek-logo.png')
icon = pygame.transform.scale(icon, (32, 32))
pygame.display.set_icon(icon)

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (90, 136, 64)
blue = (0, 0, 255)

# Display
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Snek')

# Clock
clock = pygame.time.Clock()

# FPS
FPS = 20

# Scale
scale = 0.8

# Fonts
small_font = pygame.font.SysFont("comicsansms", 25)
med_font = pygame.font.SysFont("comicsansms", 50)
large_font = pygame.font.SysFont("comicsansms", 80)

# Images
img = pygame.image.load(directory + 'snekhead.png')
apple_img = pygame.image.load(directory + 'apple.png')
Snake_Game_Logo = pygame.image.load(directory + 'Snake-Game-Logo.png')

# Scale down the image
img = pygame.transform.scale(img, (30, 30))
img = pygame.transform.rotate(img, 180)
Snake_Game_Logo = pygame.transform.scale(Snake_Game_Logo, (int(
    Snake_Game_Logo.get_width() * scale), int(Snake_Game_Logo.get_height() * scale)))

# Variables
appleThickness = 30
block_size = 20
direction = "right"

# Scale images to fit the block size
img = pygame.transform.scale(img, (block_size, block_size))
apple_img = pygame.transform.scale(apple_img, (appleThickness, appleThickness))

# Config path
config_path = directory + 'config.ini'

# Game data
game_data = GameData(config_path)


# Functions


def pause():
    """
    It creates a loop that will only end when the user presses the C key.
    """
    paused = True
    message_to_screen("Paused", black, -100, size="large")
    message_to_screen("Press C to continue or Q to quit.", black, 25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_c:
                    paused = False
        clock.tick(5)


def score(score):
    """
    It takes the score and displays it on the screen

    param score: The score to be displayed
    """
    text = small_font.render("Score: " + str(score), True, black)
    gameDisplay.blit(text, [0, 0])
    if (int(game_data.get('highscore')) < int(score)):
        game_data.set('highscore', str(score))


def show_fps():
    """
    It gets the current fps, renders it to a surface, gets the rect of the surface, sets the top right
    corner of the rect to the top right corner of the screen, and then blits the surface to the screen
    """
    fps = str(int(clock.get_fps()))
    fps_text = small_font.render(fps, True, black)
    # set location to the top right corner
    loc = fps_text.get_rect()
    loc.topright = [display_width, 0]
    gameDisplay.blit(fps_text, loc)
    if (int(game_data.get('max_fps')) < int(fps)):
        game_data.set('max_fps', str(fps))


def randAppleGen():
    """
    It returns a random number between 0 and the width of the screen minus the width of the apple
    :return: randAppleX and randAppleY
    """
    randAppleX = round(random.randrange(
        0, display_width - appleThickness))  # /10.0)*10.0
    randAppleY = round(random.randrange(
        0, display_height - appleThickness))  # /10.0)*10.0

    return randAppleX, randAppleY


def game_intro():
    """
    This function is used to display the game's intro screen
    """
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        message_to_screen("Welcome to Snek",
                          green,
                          -100,
                          "large")
        message_to_screen("The objective of the game is to eat red apples",
                          black,
                          -30)
        message_to_screen("The more apples you eat, the longer you get",
                          black,
                          10)
        message_to_screen("If you run into yourself, or the edges, you die!",
                          black,
                          50)
        message_to_screen("Press C to play, P to pause or Q to quit.",
                          black,
                          180)

        pygame.display.update()
        clock.tick(15)


def snake(block_size, snakelist):
    """
    It draws the snake's head and body.

    param block_size: the size of the snake's body
    param snakelist: The list of coordinates of the snake's body
    """
    global head
    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img, 180)

    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))

    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [
            XnY[0], XnY[1], block_size, block_size])


def text_objects(text, color, size):
    """
    It takes a string, a color, and a size, and returns a surface and a rectangle

    param text: The text you want to render
    param color: The color of the text
    param size: The size of the text
    return: The textSurface and the textSurface.get_rect()
    """
    global textSurface
    if size == "small":
        textSurface = small_font.render(text, True, color)
    elif size == "medium":
        textSurface = med_font.render(text, True, color)
    elif size == "large":
        textSurface = large_font.render(text, True, color)

    return textSurface, textSurface.get_rect()


def message_to_screen(msg, color, y_displace=0, size="small"):
    """
    The function takes in a message, a color, a y displacement, and a size, and then it displays the
    message on the screen

    :param msg: The message to be displayed
    :param color: The color of the text
    :param y_displace: This is the y-coordinate of the text, defaults to 0 (optional)
    :param size: The size of the text, defaults to small (optional)
    """
    textSurf, textRect = text_objects(msg, color, size)
    # screen_text = font.render(msg, True, color)
    # gameDisplay.blit(screen_text, [display_width/2, display_height/2])
    textRect.center = (display_width / 2), (display_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)


def gameLoop():
    """
    The game loop is the main function of the game, it contains the game logic and is the function that
    is called to start the game
    """
    global direction

    direction = 'right'
    gameExit = False
    gameOver = False

    lead_x = display_width / 2
    lead_y = display_height / 2

    lead_x_change = 10
    lead_y_change = 0

    snakelist = []
    snakeLength = 1

    randAppleX, randAppleY = randAppleGen()

    while not gameExit:

        while gameOver:
            gameDisplay.fill(white)
            message_to_screen("Game over",
                              red,
                              y_displace=-50,
                              size="large")

            message_to_screen("Press C to play again or Q to quit",
                              black,
                              50,
                              size="medium")

            message_to_screen("Score: " + str(snakeLength - 1),
                              black,
                              15,
                              size="small")

            # TODO: Add a high score system to the game

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change

        gameDisplay.fill(white)

        # Add grid to background with spacing matching block size, adjust y-axis spacing to match apple size
        for x in range(0, display_width, block_size):
            pygame.draw.line(gameDisplay, black, (x, 0), (x, display_height))
        for y in range(0, display_height, block_size):
            pygame.draw.line(gameDisplay, black, (0, y), (display_width, y))

        # Apple
        apple_Thickness = 30
        gameDisplay.blit(apple_img, (randAppleX, randAppleY))

        head = []
        head.append(lead_x)
        head.append(lead_y)
        snakelist.append(head)

        if len(snakelist) > snakeLength:
            del snakelist[0]

        for eachSegment in snakelist[:-1]:
            if eachSegment == head:
                gameOver = True

        snake(block_size, snakelist)

        score(snakeLength - 1)
        show_fps()

        pygame.display.update()

        if lead_x > randAppleX and lead_x < randAppleX + apple_Thickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + apple_Thickness:
            if lead_y > randAppleY and lead_y < randAppleY + apple_Thickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1
            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + apple_Thickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1

        clock.tick(FPS)

    pygame.quit()
    quit()


def game():
    """
    It loads an image, scales it, sets the window size to the image size, sets the caption, blits the
    image to the screen, centers the window, updates the display, waits 5 seconds, sets the window size
    to the display_width and display_height variables, sets the caption, and calls the game_intro() and
    gameLoop() functions.
    """
    width, height = Snake_Game_Logo.get_size()
    pygame.display.set_mode((width, height), pygame.NOFRAME)
    pygame.display.set_caption('Snake Game')
    gameDisplay.blit(Snake_Game_Logo, (0, 0))
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
    pygame.display.update()
    time.sleep(5)
    pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('Snake Game')
    game_intro()
    gameLoop()


game()
