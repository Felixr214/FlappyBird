from pygame import*
gravity = -7
jump = 75
jump_speed = 14


class Bird:
    def __init__(self, id, map_height, size=(25, 20)):
        self.y = map_height - 28  # / 2
        self.id = id
        self.map_height = map_height
        self.alive = True
        self.width = size[0]
        self.height = size[1]
        self.img = transform.scale(image.load("images/alien.png"), (self.width, self.height))
        self.score = 0
        self.jumping = False
        self.jump_start = 0

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.jump_start = self.y

        else:
            if self.y - jump_speed > 0 and self.y - jump_speed >= self.jump_start - jump:
                self.y -= jump_speed
            elif self.y - jump_speed <= 0:
                self.y = 0
                self.jumping = False
            else:
                self.jumping = False

    def drop(self):
        if self.y - gravity < self.map_height - self.height:
            self.y -= gravity
        else:
            self.y = self.map_height - self.height
            self.alive = False

    def fly(self):
        if self.y + jump_speed <= self.map_height:
            self.y += jump_speed
        else:
            self.alive = False

    def fall(self):
        if self.y - jump_speed >= 0:
            self.y -= jump_speed
        else:
            self.y = 0
