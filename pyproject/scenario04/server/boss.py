import ccircle
import util

from gameconfig import *
from math import *

class Boss:
    def __init__(self):
        self.vx, self.vy = 0, 0
        self.facing = FACING_RIGHT
        self.reset()

    def draw(self, game, window):
        util.draw_image_centered('boss_%s.png' % self.facing,
            self.x, self.y, self.size)
        util.draw_progress_bar(
          window,
          self.x - self.size / 2,
          self.y - self.size / 2,
          self.size, 8,
          self.health)

    def reset(self):
        self.x = 256
        self.y = 350

        self.size = BOSS_SIZE
        self.speed = 100
        self.vx = self.speed

        self.health = 100.0
        self.dead = False
        self.enable_ai = True

    def think(self, game):
        self.vy = 10.0 * cos(game.time)

    def update(self, game, dt):
        # Update health
        if self.health <= 0:
          self.dead = True

        if not self.dead:
          self.health += dt * BOSS_HEALTH_REGEN
          self.health = min(self.health, 100.0)

        # Update position
        if not self.dead:
          if self.enable_ai:
            self.think(game)
          self.x += dt * self.vx
          self.y += dt * self.vy

          if self.x < 0:
              self.x = 0
              self.vx *= -1.0

          if self.x > game.sx:
              self.x = game.sx
              self.vx *= -1.0

          if self.vx > 0: self.facing = FACING_RIGHT
          if self.vx < 0: self.facing = FACING_LEFT

          for player in game.players.values():
            if util.distance(self, player) < BOSS_HIT_RADIUS:
              player.reset()
