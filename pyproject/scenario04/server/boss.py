import ccircle
from gameconfig import *
from math import *

class Boss:
    def __init__(self):
        self.x = 256
        self.y = 350
        self.vx, self.vy = 0, 0
        self.facing = FACING_RIGHT
        self.size = 128
        self.speed = 100
        self.vx = self.speed

    def draw(self, game, window):
        game._get_image('cat_%s.png' % self.facing).draw(
            self.x - self.size / 2,
            self.y - self.size / 2,
            self.size,
            self.size)

    def think(self, game):
        self.vy = 10.0 * cos(game._time)

    def update(self, game, dt):
        self.think(game)
        self.x += dt * self.vx
        self.y += dt * self.vy

        if self.x < 0:
            self.x = 0
            self.vx *= -1.0

        if self.x > game._sx:
            self.x = game._sx
            self.vx *= -1.0

        if self.vx > 0: self.facing = FACING_RIGHT
        if self.vx < 0: self.facing = FACING_LEFT