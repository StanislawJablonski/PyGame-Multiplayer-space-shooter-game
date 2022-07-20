import socket
from _thread import *
import _pickle as pickle
import time
import random
from math import fabs
from classes import *
from enemys import *

# setup sockets
import pygame

S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set constants
PORT = 5555

WIDTH, HEIGHT = 900, 1000

HOST_NAME = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST_NAME)

# try to connect to server
try:
    S.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))
    print("[SERVER] Server could not start")
    quit()

S.listen()  # listen for connections

print(f"[SERVER] Server Started with local ip {SERVER_IP}")

# dynamic variables
players = {}
players_bullets = []
balls = []
enemies = []
enemies_bullets = []
asteroids = []
bosses = []
bosses_bullets = []
max_asteroids = 10
max_enemies = 5
asteroids_helper = 1
enemies_helper = 1
score = 0
dead_enemies = 0
dead_asteroids = 0

connections = 0
_id = 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

start = False
stat_time = 0
game_time = "Starting Soon"
nxt = 1


# FUNCTIONS
def move_players_bullets(players_bullets):
    for player_bullet in players_bullets:
        player_bullet[1] -= 10
        if player_bullet[1] < 0:
            players_bullets.remove(player_bullet)


def create_enemies():
    if random.randrange(0, 100) < 2:
        enemy = [random.randint(30, WIDTH-30), 0, random.choice(["red", "blue", "green"])]
        enemies.append(enemy)


def move_enemies(enemies):
    for enemy in enemies:
        enemy[1] += ENEMY_VEL
        if enemy[1] > HEIGHT:
            enemies.remove(enemy)


def shoot_enemies(enemies):
    for enemy in enemies:
        if random.randrange(0, 2 * 60) == 1:
            enemy_bullet = pygame.Rect(enemy[0] + 15, enemy[1] + 20, 30, 30)
            enemies_bullets.append(enemy_bullet)


def move_enemies_bullets(enemies_bullets):
    for enemy_bullet in enemies_bullets:
        enemy_bullet[1] += 5
        if enemy_bullet[1] > HEIGHT:
            enemies_bullets.remove(enemy_bullet)


def check_collision_enemy(enemies, players, players_bullets):
    global score, dead_enemies
    for enemy in enemies:
        ex = enemy[0]
        ey = enemy[1]
        for player in players:
            p = players[player]
            x = p["x"]
            y = p["y"]
            if fabs(x - ex) < 45 and fabs(y - ey) < 30:
                enemies.remove(enemy)
        for player_bullet in players_bullets:
            bx = player_bullet[0]
            by = player_bullet[1]
            if fabs(bx - ex) < 45 and fabs(by - ey) < 30:
                score += 15
                enemies.remove(enemy)
                players_bullets.remove(player_bullet)
                dead_enemies += 1


def create_asteroids():
    if random.randrange(0, 100) < 5:
        asteroid = pygame.Rect(random.randint(30, WIDTH)-30, 0, 30, 30)
        asteroids.append(asteroid)


def move_asteroids(asteroids):
    for asteroid in asteroids:
        asteroid.y += ASTEROID_VEL
        if asteroid.y > HEIGHT:
            # pygame.event.post(pygame.event.Event(ASTEROID_DEAD))
            asteroids.remove(asteroid)


def check_collision_asteroid(asteroids, players, players_bullets):
    global score, dead_asteroids
    for asteroid in asteroids:
        ax = asteroid[0]
        ay = asteroid[1]
        for player in players:
            p = players[player]
            x = p["x"]
            y = p["y"]
            if fabs(x - ax) < 30 and fabs(y - ay) < 30:
                asteroids.remove(asteroid)
        for player_bullet in players_bullets:
            bx = player_bullet[0]
            by = player_bullet[1]
            if fabs(bx - ax) < 30 and fabs(by - ay) < 30:
                score += 1
                asteroids.remove(asteroid)
                dead_asteroids += 1


def check_collision_bullets(enemies_bullets, bosses_bullets, players):
    for enemy_bullet in enemies_bullets:
        ebx = enemy_bullet[0]
        eby = enemy_bullet[1]
        for player in players:
            p = players[player]
            x = p["x"]
            y = p["y"]
            if fabs(x - ebx) < 30 and fabs(y - eby) < 30:
                enemies_bullets.remove(enemy_bullet)
    for boss_bullet in bosses_bullets:
        bbx = boss_bullet[0]
        bby = boss_bullet[1]
        for player in players:
            p = players[player]
            x = p["x"]
            y = p["y"]
            if fabs(x - bbx) < 30 and fabs(y - bby) < 30:
                bosses_bullets.remove(boss_bullet)


def create_boss(bosses):
    global dead_asteroids, dead_enemies
    if dead_asteroids >= 2 and dead_enemies >= 2:
        boss = [random.randint(60, WIDTH-60), 0, 5]
        bosses.append(boss)
        dead_asteroids = 0
        dead_enemies = 0


def move_boss(bosses):
    for boss in bosses:
        boss[1] += ENEMY_VEL
        if boss[1] > HEIGHT:
            bosses.remove(boss)


def shoot_boss(bosses):
    for boss in bosses:
        if random.randrange(0, 2 * 60) == 1:
            boss_bullet = pygame.Rect(boss[0] + 60, boss[1] + 20, 30, 30)
            bosses_bullets.append(boss_bullet)


def move_bosses_bullets(bosses_bullets):
    for boss_bullet in bosses_bullets:
        boss_bullet[1] += 5
        if boss_bullet[1] > HEIGHT:
            bosses_bullets.remove(boss_bullet)


def check_boss_collision(bosses, players_bullets):
    global score
    for boss in bosses:
        bx = boss[0]
        by = boss[1]
        for player_bullet in players_bullets:
            pbx = player_bullet[0]
            pby = player_bullet[1]
            if fabs(pbx - bx) < 80 and fabs(pby - by) < 30:
                boss[2] -= 1
                players_bullets.remove(player_bullet)
                if boss[2] <= 0:
                    bosses.remove(boss)
                    score += 250


def increase_max_asteroids_and_enemies():
    global score, max_asteroids, max_enemies, asteroids_helper, enemies_helper
    if score / 10 >= asteroids_helper:
        max_asteroids += 1
        asteroids_helper += 1
    if score / 50 >= enemies_helper:
        max_enemies += 1
        enemies_helper += 1


def threaded_client(conn, _id):
    global connections, score, players, players_bullets, balls, enemies, enemies_bullets, asteroids, nxt, start

    current_id = _id

    data = conn.recv(16)
    name = data.decode("utf-8")
    print("[LOG]", name, "connected to the server.")

    # Setup properties for each new player
    players[current_id] = {"x": 425, "y": 400, "health": 100, "name": name}

    # pickle data and send initial info to clients
    conn.send(str.encode(str(current_id)))

    # server will recieve basic commands from client
    # it will send back all of the other clients info
    clock = pygame.time.Clock()
    while True:
        clock.tick(FPS/2)
        try:
            # Recieve data from client
            data = conn.recv(32)

            if not data:
                break

            data = data.decode("utf-8")
            # print("[DATA] Received", data, "from client id:", current_id)

            # look for specific commands from received data
            if data.split(" ")[0] == "move":
                split_data = data.split(" ")
                x = int(split_data[1])
                y = int(split_data[2])
                health = int(split_data[3])
                players[current_id]["x"] = x
                players[current_id]["y"] = y
                players[current_id]["health"] = health

                if len(enemies) < max_enemies:
                    create_enemies()
                move_enemies(enemies)
                check_collision_enemy(enemies, players, players_bullets)

                if len(asteroids) < max_asteroids:
                    create_asteroids()

                move_asteroids(asteroids)
                check_collision_asteroid(asteroids, players, players_bullets)
                check_collision_bullets(enemies_bullets, bosses_bullets, players)
                move_players_bullets(players_bullets)
                shoot_enemies(enemies)
                move_enemies_bullets(enemies_bullets)
                create_boss(bosses)
                move_boss(bosses)
                shoot_boss(bosses)
                move_bosses_bullets(bosses_bullets)
                check_boss_collision(bosses, players_bullets)
                increase_max_asteroids_and_enemies()

                # only check for collison if the game has started
                '''if start:
                    #check_collision(players, balls)
                    #player_collision(players)
                    #create_asteroids()'''

                send_data = pickle.dumps(
                    (players, players_bullets, enemies, enemies_bullets, asteroids, score, bosses, bosses_bullets))

            elif data.split(" ")[0] == "id":
                send_data = str.encode(str(current_id))  # if user requests id then send it
            # elif data.split(" ")[0] == "score":
            #     split_data = data.split(" ")
            #     score = int(split_data[1])
            #     send_data = pickle.dumps(score)
            elif data.split(" ")[0] == "players_bullets":
                split_data = data.split(" ")
                x = int(split_data[1])
                y = int(split_data[2])
                players_bullets.append([x, y])
                send_data = pickle.dumps(players_bullets)
            else:
                # any other command just send back list of players
                send_data = pickle.dumps(
                    (players, players_bullets, enemies, enemies_bullets, asteroids, score, bosses, bosses_bullets))

            # send data back to clients
            conn.send(send_data)

        except Exception as e:
            print(e)
            break  # if an exception has been reached disconnect client

        time.sleep(0.001)

    # When user disconnects
    print("[DISCONNECT] Name:", name, ", Client Id:", current_id, "disconnected")

    connections -= 1
    del players[current_id]  # remove client information from players list
    conn.close()  # close connection


# MAINLOOP

# setup level with balls
# create_balls(balls, random.randrange(200, 250))

print("[GAME] Setting up level")
print("[SERVER] Waiting for connections")

# Keep looping to accept new connections
while True:

    host, addr = S.accept()
    print("[CONNECTION] Connected to:", addr)

    # start game when a client on the server computer connects
    if addr[0] == SERVER_IP and not (start):
        start = True
        start_time = time.time()
        print("[STARTED] Game Started")

    # increment connections start new thread then increment ids
    connections += 1
    start_new_thread(threaded_client, (host, _id))
    _id += 1

# when program ends
print("[SERVER] Server offline")
