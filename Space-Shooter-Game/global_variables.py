import pygame
import os


# WINDOW CONFIG
WIDTH, HEIGHT = 900, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")


# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# TEXT CONFIG
pygame.font.init()
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
LEVEL_FONT = pygame.font.SysFont('comicsans', 40)
SCORE_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 50)


# FPS VEL SIZES
FPS = 60
VEL = 5
BULLET_VEL = 10
ASTEROID_VEL = 3
ENEMY_VEL = 2
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
ASTEROID_WIDTH, ASTEROID_HEIGHT = 30, 30


# EVENTS
PLAYER_HIT = pygame.USEREVENT + 1  # Tak tworzymy rozne eventy
# RED_HIT = pygame.USEREVENT + 2     # Gdyby bylo 2 razy + 1 to bylby to ten sam event
ASTEROID_HIT = pygame.USEREVENT + 3
ASTEROID_DEAD = pygame.USEREVENT + 4
ENEMY_HIT = pygame.USEREVENT + 5

# IMAGES
PLAYER_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'ship_player.png'))
PLAYER_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(PLAYER_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)

ASTEROID_IMAGE = pygame.image.load(os.path.join('Assets', 'meteor_fixed.png'))
ASTEROID = pygame.transform.rotate(
    pygame.transform.scale(ASTEROID_IMAGE, (ASTEROID_WIDTH, ASTEROID_HEIGHT)), 30)

SPACE_IMAGE = pygame.image.load(os.path.join('Assets', 'space.png'))
SPACE = pygame.transform.rotate(pygame.transform.scale(SPACE_IMAGE, (HEIGHT, WIDTH)), 90)

ENEMY_BULLET_IMAGE = pygame.image.load(os.path.join('Assets', 'laser_red_fixed.png'))
ENEMY_BULLET = pygame.transform.rotate(
    pygame.transform.scale(ENEMY_BULLET_IMAGE, (20, 20)), 30)

BOSS_BULLET_IMAGE = pygame.image.load(os.path.join('Assets', 'boss_bullet.png'))
BOSS_BULLET = pygame.transform.rotate(
    pygame.transform.scale(BOSS_BULLET_IMAGE, (20, 20)), 300)

RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "ship_red.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "ship_green.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "ship_blue.png"))
BOSS_SPACE_SHIP = pygame.image.load(os.path.join("assets", "boss.png"))
BOSS_SPACE = pygame.transform.scale2x(BOSS_SPACE_SHIP)
RED_LASER = pygame.image.load(os.path.join("assets", "laser_red_fixed.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "laser_green_fixed.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "laser_blue_fixed.png"))

