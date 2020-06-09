from datetime import datetime

import pygame


class PacMan:
    pacman1 = pygame.transform.scale(pygame.image.load("pacman1.png"), (24, 24))
    pacman2 = pygame.transform.scale(pygame.image.load("pacman2.png"), (24, 24))
    pacman3 = pygame.transform.scale(pygame.image.load("pacman3.png"), (24, 24))
    imgs_left = [pacman1, pacman2, pacman3, pacman2]
    imgs_right = [pygame.transform.rotate(img, 180) for img in imgs_left]
    imgs_up = [pygame.transform.rotate(img, 270) for img in imgs_left]
    imgs_down = [pygame.transform.rotate(img, 90) for img in imgs_left]

    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.rect = pygame.Rect(self.x - self.width / 2, self.y - self.width / 2, self.width, self.width)
        self.imgs = self.imgs_right
        self.img = self.imgs[0]
        self.imgcnt = 0
        self.count = 0
        self.count_increment = 1
        self.dirchange = 2
        self.dirx = 0
        self.diry = 0
        self.sep = 3

    def move(self, dirn, walls):
        if self.check_move(dirn, walls):
            if dirn == "left":
                self.dirx = - self.dirchange
                self.diry = 0
                self.imgs = self.imgs_left
            elif dirn == "right":
                self.dirx = self.dirchange
                self.diry = 0
                self.imgs = self.imgs_right
            elif dirn == "up":
                self.dirx = 0
                self.diry = - self.dirchange
                self.imgs = self.imgs_up
            elif dirn == "down":
                self.dirx = 0
                self.diry = self.dirchange
                self.imgs = self.imgs_down
            else:
                self.dirx = 0
                self.diry = 0

    def check_move(self, dirn, walls):
        if dirn == "left":
            rect = pygame.Rect(self.x - self.width / 2 - self.sep, self.y - self.width / 2, self.width, self.width)
        elif dirn == "right":
            rect = pygame.Rect(self.x - self.width / 2 + self.sep, self.y - self.width / 2, self.width, self.width)
        elif dirn == "up":
            rect = pygame.Rect(self.x - self.width / 2, self.y - self.width / 2 - self.sep, self.width, self.width)
        elif dirn == "down":
            rect = pygame.Rect(self.x - self.width / 2, self.y - self.width / 2 + self.sep, self.width, self.width)
        else:
            return True
        for wall in walls:
            if rect.colliderect(wall):
                return False
        return True

    def update(self, W, H, dots, walls):
        self.update_movement(W, H, walls)
        self.update_imgs()
        return self.collide(dots)

    def update_imgs(self):
        self.imgcnt += 1
        if self.imgcnt > 15:
            self.imgcnt = 0
        self.img = self.imgs[self.imgcnt // 4]

    def update_movement(self, W, H, walls):
        self.count += 1
        if self.count % self.count_increment == 0:
            if (self.dirx < 0 and self.check_move("left", walls)) or (
                    self.dirx > 0 and self.check_move("right", walls)) or (
                    self.diry < 0 and self.check_move("up", walls)) or (
                    self.diry > 0 and self.check_move("down", walls)):
                self.x += self.dirx
                self.y += self.diry
        if self.x > W:
            self.x = 0
        if self.x < 0:
            self.x = W
        if self.y > H:
            self.y = 0
        if self.y < 0:
            self.y = H
        self.rect = pygame.Rect(self.x - self.width / 2, self.y - self.width / 2, self.width, self.width)

    def draw(self, win):
        win.blit(self.img, (self.x - 12, self.y - 12))

    def collide(self, dots):
        for dot in dots:
            dot_rect = pygame.Rect(dot[0] - 4, dot[1] - 4, 8, 8)
            if self.rect.colliderect(dot_rect):
                return dot
        return None


class Ghost():
    imgs = [pygame.image.load("ghost.png")]
    boundaries = {
        "left": 176,
        "right": 272,
        "up": 223,
        "down": 271,
    }

    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        for x, img in enumerate(self.imgs):
            self.imgs[x] = pygame.transform.scale(img, (self.width, self.width))
        self.img = self.imgs[0]
        self.rect = pygame.Rect(self.x - self.width / 2, self.y - self.width / 2, self.width, self.width)
        self.dirx = 0
        self.diry = 0
        self.wait_time = 20
        self.start_time = datetime.now()
        self.use_super = True

    def move(self):
        self.get_dirns()
        self.x += self.dirx
        self.y += self.diry
        self.rect = pygame.Rect(self.x - self.width / 2, self.y - self.width / 2, self.width, self.width)

    def get_dirns(self):
        if self.x < self.boundaries["left"]:
            self.dirx = 0
            self.diry = -1
        if self.x + self.width > self.boundaries["right"]:
            self.dirx = 0
            self.diry = 1
        if self.y < self.boundaries["up"]:
            self.dirx = 1
            self.diry = 0
        if self.y + self.width > self.boundaries["down"]:
            self.dirx = -1
            self.diry = 0
        if self.rect.collidepoint(223, 223) and (datetime.now() - self.start_time).seconds > 0.5:
            self.dirx = 0
            self.diry = -1
            return False
        return True

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class Blinky(Ghost):
    imgs = [pygame.image.load("ghost.png"),
            pygame.image.load("blinky.png")]

    def __init__(self, x, y, width):
        super().__init__(x, y, width)
        self.img = self.imgs[1]
        self.dirx = -1

    def get_dirns(self):
        if self.use_super:
            self.use_super = super().get_dirns()


class Pinky(Ghost):
    imgs = [pygame.image.load("ghost.png"),
            pygame.image.load("pinky.png")]

    def __init__(self, x, y, width):
        super().__init__(x, y, width)
        self.img = self.imgs[1]
        self.dirx = -1

    def get_dirns(self):
        if self.use_super:
            self.use_super = super().get_dirns()


class Inky(Ghost):
    imgs = [pygame.image.load("ghost.png"),
            pygame.image.load("inky.png")]

    def __init__(self, x, y, width):
        super().__init__(x, y, width)
        self.img = self.imgs[1]
        self.dirx = -1

    def get_dirns(self):
        if self.use_super:
            self.use_super = super().get_dirns()


class Clyde(Ghost):
    imgs = [pygame.image.load("ghost.png"),
            pygame.image.load("clyde.png")]

    def __init__(self, x, y, width):
        super().__init__(x, y, width)
        self.img = self.imgs[1]
        self.dirx = -1

    def get_dirns(self):
        if self.use_super:
            self.use_super = super().get_dirns()
