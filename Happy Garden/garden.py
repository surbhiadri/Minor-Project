from random import randint
import time
import pgzrun
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pgzero.clock import clock

WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

game_over = False
finalized = False
garden_happy = True
fangflower_collision = False

time_elapsed = 0
start_time = time.time()

cow = Actor("cow")  # these values set the cow's starting post. on the screen.
cow.pos = 100, 500

flower_list = []  # each time new flower actors created & added to the list.
wilted_list = []  # this list will store how long a flower has been wilted.
fangflower_list = []  # this list will store the fangflower actors.

fangflower_vy_list = (
    []
)  # it will hold the velocities of the fangflowers along the y-axis.
fangflower_vx_list = []  # it will hold the velocities in the x-axis.


def draw():
    global game_over, time_elapsed, finalized
    if not game_over:
        screen.clear()
        screen.blit("garden", (0, 0))

        cow.draw()
        for flower in flower_list:
            flower.draw()

        for fangflower in fangflower_list:
            fangflower.draw()

        time_elapsed = int(time.time() - start_time)
        screen.draw.text(
            "Garden happy for: " + str(time_elapsed) + " seconds",
            topleft=(10, 10),
            color="black",
        )
    else:
        if not finalized:
            cow.draw()
            screen.draw.text(
                "Garden happy for: " + str(time_elapsed) + " seconds",
                topleft=(10, 10),
                color="black",
            )
            if not garden_happy:
                screen.draw.text(
                    "GARDEN UNHAPPY GAME OVER!", color="black", topleft=(10, 100)
                )
                finalized = True
            else:
                screen.draw.text(
                    "FANGFLOWER ATTACK GAME OVER!", color="black", topleft=(10, 50)
                )
                finalized = True


def new_flower():
    global flower_list, wilted_list
    flower_new = Actor("flower")
    flower_new.pos = randint(50, WIDTH - 50), randint(150, HEIGHT - 100)
    flower_list.append(flower_new)
    wilted_list.append("happy")


def add_flowers():
    global game_over
    if not game_over:
        new_flower()
        clock.schedule(add_flowers, 4)


def check_wilt_times():
    global wilted_list, game_over, garden_happy
    for index, wilted_since in enumerate(wilted_list):
        if not wilted_since == "happy":
            time_wilted = int(time.time() - wilted_since)
            if time_wilted > 10:
                garden_happy = False
                game_over = True
                break


def wilt_flowers():
    global flower_list, wilted_list, game_over
    if not game_over:
        if flower_list:
            rand_flower = randint(0, len(flower_list) - 1)
            if flower_list[rand_flower].image == "flower":
                flower_list[rand_flower].image = "flower-wilt"
                wilted_list[rand_flower] = time.time()


def check_flower_collision():
    global cow, flower_list, wilted_list
    for index, flower in enumerate(flower_list):
        if flower.colliderect(cow) and flower.image == "flower-wilt":
            flower.image = "flower"
            wilted_list[index] = "happy"


def check_fangflower_collision():
    global cow, fangflower_list, fangflower_collision
    global game_over
    for fangflower in fangflower_list:
        if fangflower.colliderect(cow):
            cow.image = "zap"
            game_over = True


def velocity():
    random_dir = randint(0, 1)
    random_velocity = randint(2, 3)
    if random_dir == 0:
        return -random_velocity
    else:
        return random_velocity


def mutate():
    global flower_list, fangflower_list, fangflower_vy_list
    global fangflower_vx_list, game_over
    if not game_over and flower_list:
        rand_flower = randint(0, len(flower_list) - 1)
        fangflower_pos_x = flower_list[rand_flower].x
        fangflower_pos_y = flower_list[rand_flower].y
        del flower_list[rand_flower]
        fangflower = Actor("fangflower")
        fangflower.pos = fangflower_pos_x, fangflower_pos_y
        fangflower_vx = velocity()
        fangflower_list.append(fangflower)
        fangflower_vy = velocity()
        fangflower_vx_list.append(fangflower_vx)
        fangflower_vy_list.append(fangflower_vy)
        clock.schedule(mutate, 20)


def update_fangflowers():
    global fangflower_list, game_over
    if not game_over:
        index = 0
        for fangflower in fangflower_list:
            fangflower_vx = fangflower_vx_list[index]
            fangflower_vy = fangflower_vy_list[index]
            fangflower.x += fangflower_vx
            if fangflower.left < 0:
                fangflower_vx_list[index] = -fangflower_vx
            if fangflower.right > WIDTH:
                fangflower_vx_list[index] = -fangflower_vx
            fangflower.y += fangflower_vy
            if fangflower.top < 150:
                fangflower_vy_list[index] = -fangflower_vy
            if fangflower.bottom > HEIGHT:
                fangflower_vy_list[index] = -fangflower_vy
            index += 1


def reset_cow():
    global game_over
    if not game_over:
        cow.image = "cow"


add_flowers()
wilt_flowers()


def update():
    global game_over, fangflower_collision
    global time_elapsed

    fangflower_collision = check_fangflower_collision()
    check_wilt_times()

    if not game_over:
        if keyboard.space:
            cow.image = "cow-water"
            clock.schedule(reset_cow, 0.5)
            check_flower_collision()
        if keyboard.left and cow.x > 0:
            cow.x -= 5
        elif keyboard.right and cow.x < WIDTH:
            cow.x += 5
        elif keyboard.up and cow.y > 150:
            cow.y -= 5
        elif keyboard.down and cow.y < HEIGHT:
            cow.y += 5
        if time_elapsed > 15 and not fangflower_list:
            mutate()
        update_fangflowers()
