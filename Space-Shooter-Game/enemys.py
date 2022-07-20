from math import fabs

from global_variables import *


def handle_asteroids(player, asteroids, score):
    for asteroid in asteroids:
        asteroid.y += ASTEROID_VEL
        if player.rect.colliderect(asteroid):
            pygame.event.post(pygame.event.Event(PLAYER_HIT))
            asteroids.remove(asteroid)
        for bullet in player.bullets:
            if bullet.colliderect(asteroid):
                asteroids.remove(asteroid)
                player.bullets.remove(bullet)
                score += 5
        if asteroid.y > HEIGHT:
            pygame.event.post(pygame.event.Event(ASTEROID_DEAD))
            asteroids.remove(asteroid)


def handle_enemy_spaceships(player, enemies, score):
    for enemy in enemies:
        ex = enemy[0]
        ey = enemy[1]
        if fabs(player.x - ex) < 50 and fabs(player.y - ey) < 35:
            enemies.remove(enemy)
            player.health -= 10
        for bullet in player.bullets:
            if bullet.colliderect(enemy):
                player.bullets.remove(bullet)
                enemy.health -= 40
                if enemy.health <= 0:
                    if enemy.ship_img == RED_SPACE_SHIP:
                        score += 18
                    elif enemy.ship_img == GREEN_SPACE_SHIP:
                        score += 13
                    elif enemy.ship_img == BLUE_SPACE_SHIP:
                        score += 7
                    enemies.remove(enemy)


def handle_enemy_bullets(player, enemies_bullets, bosses_bullets):
    for enemy_bullet in enemies_bullets:
        if player.rect.colliderect(enemy_bullet):
            player.health -= 15
            enemies_bullets.remove(enemy_bullet)
    for boss_bullet in bosses_bullets:
        if player.rect.colliderect(boss_bullet):
            player.health = 0
            bosses_bullets.remove(boss_bullet)

