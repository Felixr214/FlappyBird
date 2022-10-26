from random import randint
from pygame import *
from copy import deepcopy


class Obstacle:
    def __init__(self, start_pos, height, width, gap):
        self.height = height
        self.width = width
        self.img = transform.scale(image.load("images/Bar.png"), (self.width, self.height))
        self.x = start_pos
        self.gap = gap
        self.alive = True
        self.remove = False

    def collide(self, player_pos, player_size, screen_height, down):
        player_x, player_y = player_pos
        player_width, player_height = player_size
        if self.x <= player_x <= self.x + self.width or self.x <= player_x + player_width <= self.x + self.width:
            if down:
                if player_y + player_height >= screen_height - self.height:
                    return True
            else:
                if player_y <= self.height:
                    return True
        return False

    def move(self, speed):
        self.x -= speed


class World:
    def __init__(self, x, y, bar=20, **kwargs):
        self.x = x
        self.y = y
        self.obst = []
        self.speed = 10
        self.bar = bar
        self.gap = 150
        if "gap" in kwargs:
            self.gap = kwargs["gap"]
        self.distance = 300
        if "dist" in kwargs:
            self.distance = kwargs["dist"]
        self.last_obst = self.distance
        self.last_height = 0

    def new_obst(self):
        if self.last_obst < self.distance:
            return False
        else:
            obs_height = randint(0, self.y - self.gap)
            while -50 < obs_height - self.last_height < 50 and len(self.obst) != 0:
                obs_height = randint(0, self.y - self.gap)
            self.obst.append([Obstacle(self.x, obs_height, self.bar, self.gap),
                              Obstacle(self.x, self.y - obs_height - self.gap, self.bar, self.gap)])
            self.last_obst = 0
            self.last_height = obs_height
            return True

    def move(self):
        raise_score = False
        for obst in self.obst:
            down, up = obst
            down.move(self.speed)
            up.move(self.speed)
            if down.alive and up.alive and down.x <= 150 - self.bar:
                down.alive = False
                up.alive = False
                raise_score = True

            if down.x <= 0:
                self.obst.remove(obst)

        self.last_obst += self.speed
        return raise_score
