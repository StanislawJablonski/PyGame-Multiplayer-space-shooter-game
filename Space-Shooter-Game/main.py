from enemys import *
from classes import *
from client import Network
import random
import time

players = {}
players_bullets = []
asteroids = []
enemies = []
enemies_bullets = []
score = 0
bosses = []
bosses_bullets = []


def draw_window(players, players_bullets, asteroids, enemies, enemies_bullets, score, bosses, bosses_bullets):
    WIN.blit(SPACE, (0, 0))

    score_text = SCORE_FONT.render("Score: " + str(score), 1, WHITE)
    hp_padding = 10

    for p in players:
        playerr = players[p]
        player = Player(playerr["x"], playerr["y"], playerr["health"], playerr["name"])
        player_health_text = HEALTH_FONT.render("Health[" + str(player.name) + "]: " + str(player.health), 1, WHITE)
        WIN.blit(PLAYER_SPACESHIP, (player.x, player.y))
        WIN.blit(player_health_text, (10, hp_padding))
        hp_padding += 40

    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    for asteroid in asteroids:
        WIN.blit(ASTEROID, (asteroid.x, asteroid.y))

    for e in enemies:
        enemy = Enemy(e[0], e[1], e[2], 100)
        enemy.draw(WIN)

    for player_bullet in players_bullets:
        bullet = pygame.Rect(player_bullet[0], player_bullet[1], 5, 10)
        pygame.draw.rect(WIN, YELLOW, bullet)

    for enemy_bullet in enemies_bullets:
        WIN.blit(ENEMY_BULLET_IMAGE, (enemy_bullet.x, enemy_bullet.y))

    for boss in bosses:
        boss = Enemy(boss[0], boss[1], "boss", 100)
        boss.draw(WIN)

    for boss_bullet in bosses_bullets:
        WIN.blit(BOSS_BULLET, (boss_bullet.x, boss_bullet.y))

    pygame.display.update()


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(1000)


def game_main(name):
    global players

    # start by connecting to the network
    server = Network()
    current_id = server.connect(name)
    players, players_bullets, enemies, enemies_bullets, asteroids, score, bosses, bosses_bullets = server.send("get")
    playerr = players[current_id]
    player = Player(playerr["x"], playerr["y"], playerr["health"], playerr["name"])

    counter = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        data = ""
        data2 = ""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(players_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(player.x + player.get_width() // 2, player.y + player.get_height() // 2 - 2, 5,
                                         10)
                    data2 = "players_bullets " + str(player.x + player.get_width() // 2) + " " \
                            + str(player.y + player.get_height() // 2 - 2)
                    players_bullets = server.send(data2)

            if event.type == PLAYER_HIT:  # obrazenia od asteroidy
                player.health -= 5

        counter += 1
        if counter % (2 * FPS) == 0:
            score += 1

        if player.health <= 0:
            player.x = -100  # wyrzucany poza mape
            winner_text = "GAME OVER" + "  SCORE : " + str(score)
            draw_winner(winner_text)
            # time.sleep(30)
            # break

        keys_pressed = pygame.key.get_pressed()
        player.handle_movement(keys_pressed)

        data = "move " + str(player.x) + " " + str(player.y) + " " + str(player.health)
        players, players_bullets, enemies, enemies_bullets, asteroids, score, bosses, bosses_bullets = server.send(data)

        handle_asteroids(player, asteroids, score)
        handle_enemy_spaceships(player, enemies, score)
        handle_enemy_bullets(player, enemies_bullets, bosses_bullets)
        draw_window(players, players_bullets, asteroids, enemies, enemies_bullets, score, bosses, bosses_bullets)

    game_main(name)


while True:
    name = input("Please enter your name: ")
    #name = "test"
    if 0 < len(name) < 20:
        break
    else:
        print("Error, this name is not allowed (must be between 1 and 19 characters [inclusive])")

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Game")
if __name__ == '__main__':
    game_main(name)
