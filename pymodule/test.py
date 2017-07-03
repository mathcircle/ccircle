import ccircle
import random
from math import *

window = ccircle.Window(title = 'SuperWindow 3000', width = 800, height = 800, x = 0, y = 0)

face = []
for i in range(1024):
  face.append([
    random.randint(-100, 1024), random.randint(-100, 1024),
    random.randint(-100, 1024), random.randint(-100, 1024),
    random.randint(-100, 1024), random.randint(-100, 1024),
    random.uniform(0, 1),
    random.uniform(0, 1),
    random.uniform(0, 1),
    random.uniform(0, 0.05),
  ])

t = 0.0

while window.isOpen():
  t += 0.001
  window.clear(0.1, 0.1, 0.1)
  for tri in face:
    window.drawTri(*tri)
  for tri in face:
    tri[random.randint(0, 5)] += random.randint(-5, 5)

  window.update()
