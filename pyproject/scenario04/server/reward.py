import util
import random
from gameconfig import *

class Reward:
    def __init__(self, id, x, y):
        self.id = id
        self.x, self.y = x, y
        self.size = 48
        self.money = random.randint(REWARD_MIN, REWARD_MAX)
        self.remove = False

    def draw(self, game, window):
        util.draw_image_centered('reward.png', self.x, self.y, self.size)

    def update(self, game, dt):
      if not self.remove:
        for player in game.players.values():
          if util.distance(self, player) < self.size:
            player.money += self.money
            self.remove = True

