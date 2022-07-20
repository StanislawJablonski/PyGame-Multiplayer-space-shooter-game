from global_variables import *


class Bullet:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.rect = pygame.Rect(self.x, self.y, self.get_width(), self.get_height())

    def draw(self, WIN):
        WIN.blit(self.img, (self.x, self.y))

    def move(self):
        self.y += BULLET_VEL
        self.rect.y += BULLET_VEL

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()


class Ship:
    COOLDOWN = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        #self.health = 100
        self.ship_img = None
        self.bullet_img = None
        self.bullets = []
        self.cool_down_counter = 0
        # no rect here

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(window)

    def shoot(self):
        if self.cool_down_counter == 0:
            bullet = Bullet(self.x, self.y, self.bullet_img)
            self.bullets.append(bullet)
            self.cool_down_counter = 1

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.bullets:
            laser.move()
            if laser.off_screen(HEIGHT):
                self.bullets.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.bullets.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1


class Player(Ship):
    def __init__(self, x, y, health, name):
        super().__init__(x, y)
        self.ship_img = PLAYER_SPACESHIP
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.health = health
        self.name = name
        self.max_health = health
        self.rect = pygame.Rect(425, 400, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    def move_lasers(self, vel, objs):
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(HEIGHT):
                self.bullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collision(obj):
                        objs.remove(obj)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)

    def handle_bullets(self):
        for bullet in self.bullets:
            bullet.y -= BULLET_VEL
            if bullet.y < 0:
                self.bullets.remove(bullet)

    def handle_movement(self, keys_pressed):
        if keys_pressed[pygame.K_LEFT] and self.rect.x - VEL > 0:  # LEFT
            self.rect.x -= VEL
            self.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and self.rect.x + VEL + self.get_width() < WIDTH:  # RIGHT
            self.rect.x += VEL
            self.x += VEL
        if keys_pressed[pygame.K_UP] and self.rect.y - VEL > 0:  # UP
            self.rect.y -= VEL
            self.y -= VEL
        if keys_pressed[pygame.K_DOWN] and self.rect.y + VEL + self.get_height() < HEIGHT:  # DOWN
            self.rect.y += VEL
            self.y += VEL

    def get_width(self):
        return SPACESHIP_WIDTH

    def get_height(self):
        return SPACESHIP_HEIGHT

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0),
                         (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (
        self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health),
        10))


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER, 100),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER, 80),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER, 40),
        "boss": (BOSS_SPACE, BOSS_BULLET, 200)
    }

    def __init__(self, x, y, color, health):
        super().__init__(x, y)
        self.ship_img, self.laser_img, self.health = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.rect = pygame.Rect(self.x, self.y, self.get_width(), self.get_height())
        self.health = health

    def move(self, vel):
        self.y += vel
        self.rect.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Bullet(self.x - 20, self.y, self.laser_img)
            self.bullets.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


def collide(obj1, obj2):
    return obj1.rect.colliderect(obj2.rect)
