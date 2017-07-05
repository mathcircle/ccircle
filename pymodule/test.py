import ccircle
import random
from math import *

class Bullet:
  def __init__(self, x, y):
    self.x, self.y = x, y

  def draw(self, window):
    # window.drawLine(self.x - 2, self.y, self.x + 2, self.y, 2, 1, 0, 0.5)
    window.drawPoint(self.x, self.y, 4, 1, 0, 0.5)

  def update(self, dt):
    self.x += 5.0

class Player:
  def __init__(self, x, y, r, g, b):
    self.x, self.y, self.r, self.g, self.b = x, y, r, g, b

  def draw(self, window):
    window.drawTri(
      self.x - 16, self.y + 16,
      self.x,      self.y - 16,
      self.x + 16, self.y + 16,
      self.r, self.g, self.b)

window = ccircle.Window(
  title = 'CCircle Module Test',
  width = 800,
  height = 800)

window.hideMouse()

player = Player(64, 128, 0.1, 0.5, 1.0)
enemy = Player(640, 128, 1.0, 0.0, 0.2)
bullets = []

while window.isOpen():
  speed = 2
  dt = 1

  window.clear(0.1, 0.1, 0.1)

  if ccircle.isKeyDown('W'): player.y -= speed * dt
  if ccircle.isKeyDown('S'): player.y += speed * dt
  if ccircle.isMouseDown('right'):
    bullets.append(Bullet(player.x + 32, player.y))

  for bullet in bullets:
    bullet.update(dt)

  mx, my = window.getMousePos()
  window.drawPoint(mx, my, 8)

  player.draw(window)
  enemy.draw(window)
  for bullet in bullets:
    bullet.draw(window)

  window.update()
