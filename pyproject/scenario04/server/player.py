import ccircle
import random
from gameconfig import *
from math import *

class Player:
    def __init__(self, id):
        self.id = id
        self.name = 'Player %d' % self.id
        self.score = 0
        self.idle = 0

        self.x, self.y = random.randint(32, 640), random.randint(50, 150)
        self.vx, self.vy = 0, 0
        self.facing = FACING_RIGHT
        self.phase = random.uniform(0, 2.0*pi)
        self.freq = random.uniform(1, 1.25) * 2
        self.size = 48

    def draw(self, game, window):
        game._get_image('ghost_red_%s.png' % self.facing).draw(
            self.x - self.size / 2,
            self.y - self.size / 2 + 4 * cos(self.freq * game._time + self.phase),
            self.size,
            self.size)
        tx = len(self.name)
        game._font.draw(
            self.name,
            int(self.x - 4 * tx),
            int(self.y - self.size / 2 - 8),
            14)

    def update(self, game, dt):
        self.x += dt * self.vx
        self.y += dt * self.vy
        self.x = max(self.size / 2, min(self.x, game._sx - self.size / 2))
        self.y = max(self.size / 2, min(self.y, game._sy - self.size / 2))
        if self.vx > 0: self.facing = FACING_RIGHT
        if self.vx < 0: self.facing = FACING_LEFT
