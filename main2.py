from copy import deepcopy
from pygame import *
from time import time
from Bird import Bird
from World import World
from Net2_2 import Net2

best2_200 = ([[[-0.588, 0.338, 0.531, 0.657], [-0.09, -0.708, -0.205, 0.417]], [[0.09, -0.46], [-0.65, -0.385], [0.706, 0.483], [-0.474, 0.604]]], [[-0.241, -0.066, 0.629, 0.057], [-0.279, 0.178]])
best1_200 = ([[[-0.999, 0.6], [0.574, -0.253]]], [[-0.716, -0.38]])

decisions = ["jump", "stay"]
pattern = [4]
n1 = Net2(layers=1, dec=decisions, input_am=2)
best_net = n1.export(True)

score = 0
highscore = 0
generation = 0

gap = 200
dist = 500

fps = 60
delay = 1 / fps

bar_width = 50
bird_size = (25, 20)
screen_size = (1000, 500)
alien1 = transform.scale(image.load("images/alien.png"), bird_size)

speed = 10
running = True
jumping = False
pause = False
lh = 0
jump_cooldown = 0.1

screen = display.set_mode(screen_size)
init()
font = font.Font('freesansbold.ttf', 24)

w1 = World(screen_size[0], screen_size[1], bar_width, dist=dist, gap=gap)
tj = 0
players = []
nets = []

player_am = 50

while True:
    for event_ in event.get():
        if event_.type == QUIT:
            running = False
        if event_.type == KEYDOWN:
            if event_.key == K_SPACE:
                pause = False

    if not running:
        players = []
        nets = []
        score = 0
        w1.obst = []
        w1.last_obst = dist
        running = True
        for a in range(player_am):
            players.append(Bird(a, screen_size[1], bird_size))
            nets.append(Net2(dec=decisions, fnet=deepcopy(best_net)))
            if a != 0:
                for b in range(1000):
                    nets[-1].vari_net()

    while running and not pause:
        t1 = time()
        w1.new_obst()
        for event_ in event.get():
            if event_.type == QUIT:
                running = False
            if event_.type == KEYDOWN and not jumping:
                if event_.key == K_SPACE:
                    pause = True
                if event_.key == K_r:
                    print(nets[0].export(True))

        if time() - tj >= jump_cooldown:
            jumping = False

        if w1.move():
            score += 1

        for b1 in players:
            next_obst = w1.obst[0]
            for obs in w1.obst:
                if obs[0].alive:
                    next_obst = obs
                    if b1 == players[0]:
                        ah = obs[0].height
                        if ah != lh:
                            # print(ah)
                            pass
                        lh = ah
                    break

            data = [screen_size[1] - next_obst[0].height - (b1.y + bird_size[1]),
                    b1.y - (screen_size[1] - next_obst[0].height - gap)]

            normed_data = [data[0] / screen_size[1], data[1] / screen_size[1]]

            if b1.jumping:
                b1.jump()
                if b1 == players[0] and pause:
                    print(data, b1.y)
                    break

                if b1 == players[0]:
                    screen.fill((0, 0, 0))

            else:

                player_decision = nets[players.index(b1)].decide(normed_data)
                if b1 == players[0] and pause:
                    print(data, b1.y)
                    break

                if b1 == players[0]:
                    screen.fill((0, 0, 0))

                if player_decision == "jump":
                    b1.jump()
                    # b1.fly()
                elif player_decision == "drop":
                    b1.fall()

            b1.drop()
            for obstacle in w1.obst:
                down, up = obstacle
                if down.collide((150, b1.y), bird_size, screen_size[1], True):
                    b1.alive = False
                screen.blit(down.img, (down.x, screen_size[1] - down.height))

                if up.collide((150, b1.y), bird_size, screen_size[1], False):
                    b1.alive = False
                screen.blit(up.img, (up.x, 0))
            if players[0] == b1:
                screen.blit(alien1, (150, b1.y))
            else:
                screen.blit(b1.img, (150, b1.y))
            if not b1.alive:
                nets.remove(nets[players.index(b1)])
                players.remove(b1)

        if score > highscore and len(players) > 0:
            best_net = nets[-1].export(True)
            highscore = score

        showhighscore = font.render("Highscore: " + str(highscore), True, (255, 175, 0))
        showscore = font.render("Score: " + str(score), True, (255, 175, 0))
        gen = font.render("Generation: " + str(generation), True, (255, 175, 0))
        player = font.render("Player: " + str(len(players)), True, (255, 175, 0))

        screen.blit(gen, (0, 0))
        screen.blit(player, (0, 25))
        screen.blit(showscore, (0, 50))
        screen.blit(showhighscore, (0, 75))
        if score > 10:
            while time() - t1 < delay:
                pass
        display.update()

        if len(players) == 0:
            running = False
            generation += 1
