import os
d = os.path.dirname(os.path.realpath(__file__))
import sys
sys.path.append(d + '\\dist')

import ccircle
import random
import time
from math import *

window = ccircle.Window('CCircle Module Test', 800, 800)
cat = ccircle.Image('res/cat.png')
bg = ccircle.Image('res/pizza.png')
cat.eraseRed()
font = ccircle.Font('res/FiraMono.ttf')

catPixels = [ (x, y, cat.getPixel(4 * x, 4 * y)) for y in range(int(cat.height/4)) for x in range(int(cat.width/4)) ]

t = 0
while window.isOpen():
  window.clear(0.1, 0.1, 0.1)
  wx, wy = window.getSize()
  mx, my = window.getMousePos()
  window.drawPoint(mx, my, 8)
  bg.draw(0, 0, wx, wy)

  t += 1.0
  cat.draw(16, 16, 128, 128, t)

  cx, cy = cat.getSize()
  cat.drawSub(128, 32, 128, 128, cx / 4, cy / 4, cx / 8, cy / 8, -t)
  if ccircle.isKeyDown('1'):
    font.drawCentered("I'm a cat! :3", mx, my, 20)

  if ccircle.wasKeyPressed('left'):
    cat = ccircle.Image('res/cat.png')
    cat.eraseRed()
    cat.recolor(0.8, 0.8, 0.8, random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 0.3)

  for x, y, (r, g, b, a) in catPixels:
    window.drawRect(100 + 4 * x, 100 + 4 * y, 4, 4, r, g, b, a)

  window.update()
