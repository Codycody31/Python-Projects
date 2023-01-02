# Make a flappy bird game using pygame

import pygame
import random
import os

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

directory = os.path.dirname(__file__) + "\\"

# Background
background = pygame.image.load(directory + 'background.png')
background = pygame.transform.scale(background, (800, 600))
backgroundX = 0

# Caption and Icon
pygame.display.set_caption("Flappy Bird")
icon = pygame.image.load(directory + 'logo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load(directory + 'bird.png')
playerX = 400
playerY = 300
playerX_change = 0
playerY_change = 0
num_of_obstacles = 0
# Spawn Player
screen.blit(playerImg, (playerX, playerY))

def player(x, y):
    # Move the player up smoothly by a block
    if y < 0:
        y = 0
    elif y > 600:
        y = 600
    screen.blit(playerImg, (x, y))

# funtion to check if player is out of bounds
def checkBounds(x, y):
    if x < 0 or x > 800 or y < 0 or y > 600:
        return True
    return False

def spawnObstacle():
    # draw the obstacle pipe, randomly
    obstacle = pygame.image.load(directory + 'obstacle.png')
    obstacleX = random.randint(0, 800)
    obstacleY = random.randint(0, 600)
    screen.blit(obstacle, (obstacleX, obstacleY))

# Game Loop
running = True
while running:
    playerX_change = 0
    playerY_change = 0

    # RGB - Red, Green, Blue
    screen.fill((0, 0, 0))

    backgroundX -= 0.1
    if backgroundX < -800:
        backgroundX = 0
    screen.blit(background, (backgroundX, 0))
    screen.blit(background, (backgroundX + 800, 0))
    if num_of_obstacles < 10:
        spawnObstacle()
        num_of_obstacles += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                playerY_change = -10
                pygame.mixer.music.load(directory + 'jump.wav')
                pygame.mixer.music.play(0)

    playerX += playerX_change
    playerY += playerY_change
    print("X = " + str(playerX))
    print("Y = " + str(playerY))
    player(playerX, playerY)
    if checkBounds(playerX, playerY):
        pygame.mixer.music.load(directory + 'gameover.wav')
        pygame.mixer.music.play(0)
        running = False
        print("Game Over")
    pygame.display.update()