import ccircle
import random
import time
from math import *

import ball
import cloud
import world

# Create a window
window = ccircle.Window('Lab 3: Modeling a World with Objects & Physics', 800, 800)

# Create a world
world = world.World('Earth')

# Add clouds to the world
for i in range(1000):
    world.add(cloud.generate())

# Add bouncy balls to the world, as well as a list that we can use
# to loop through the balls and apply forces
balls = []
for i in range(100):
    x = random.randint(0, 800)
    y = random.randint(100, 400)
    size = random.randint(4, 32)
    this_ball = ball.Ball(x, y, size)
    balls.append(this_ball)
    world.add(this_ball)

# Main Loop
time_last = time.time()
dt = 1.0 / 60.0
repel_strength = 5e6

while window.isOpen():
    window.clear(0.1, 0.1, 0.1)

    # Apply a gravitational force to each ball
    for ball in balls:
        ball.apply_force(0, ball.mass * 300.0)

    # Apply a repelling force from the mouse to the ball
    mouse_x, mouse_y = window.getMousePos()
    for ball in balls:
        fx, fy = ball.x - mouse_x, ball.y - mouse_y
        length = sqrt(fx*fx + fy*fy)
        fx /= (length ** 3.0)
        fy /= (length ** 3.0)
        ball.apply_force(fx * repel_strength, fy * repel_strength)

    world.update(dt)
    world.draw(window)
    window.update()

    # Compute elapsed time and update dt accordingly
    time_now = time.time()
    dt = time_now - time_last
    time_last = time_now