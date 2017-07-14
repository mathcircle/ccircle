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
font = ccircle.Font('res/FiraMono.ttf')

sound = ccircle.Sound()
sound.addSine(0, 1, 120, 0.2)
sound.addSine(0, 1, 60, 0.2)
sound.addSine(0, 1, 90, 0.2)
sound.addSaw(1, 2, 60, 0.2)
sound.addSaw(1, 2, 240, 0.2)
sound.addSaw(1, 2, 480, 0.2)
sound.play()

t = 0
while window.isOpen():
  window.clear(0.1, 0.1, 0.1)
  mx, my = window.getMousePos()
  window.drawPoint(mx, my, 8)

  t += 1.0
  cat.draw(16, 16, 128, 128, t)

  cx, cy = cat.getSize()
  cat.drawSub(128, 32, 128, 128, cx / 4, cy / 4, cx / 8, cy / 8, -t)
  font.draw("I'm a cat! :3", 140, 64 + 32, 12)

  window.update()
