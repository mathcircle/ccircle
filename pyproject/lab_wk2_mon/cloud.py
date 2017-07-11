import random
from math import *

class Cloud:
    def __init__(self, x, y, size, color, vx):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.vx = vx

    def draw(self, window):
        window.drawCircle(self.x, self.y, self.size, 1, 1, 1, 0.1)

    def update(self, dt):
        self.x += dt * self.vx
        if self.x < 0:
            self.x = 800
        if self.x > 800:
            self.x = 0

def generate():
    x = random.randint(0, 800)
    y = random.randint(100, 200)
    size = abs(random.gauss(20 ** 0.5, 10 ** 0.5)) ** 2.0
    color = random.uniform(0.25, 1.0) ** 0.5
    vx = random.uniform(0, 25)
    return Cloud(x, y, size, color, vx)
