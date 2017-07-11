import ccircle
from math import *

cache_font = {}
cache_image = {}

def distance(a, b):
  dx = a.x - b.x
  dy = a.y - b.y
  return sqrt(dx*dx + dy*dy)

def font(name='FiraMono'):
    global cache_font
    x = cache_font.get(name, None)
    if x:
        return x
    x = ccircle.Font('../../res/%s.ttf' % name)
    cache_font[name] = x
    return x

def image(name):
    global cache_images
    x = cache_image.get(name, None)
    if x:
        return x
    x = ccircle.Image('../image/%s' % name)
    cache_image[name] = x
    return x

def draw_image_centered(name, x, y, size):
    image(name).draw(x - size / 2, y - size / 2, size, size)

def draw_progress_bar(window, x, y, w, h, percent):
    window.drawRect(x - 4, y - 4, w + 8, h + 8, 0.1, 0.1, 0.1)
    window.drawRect(x, y, w, h, 1.0, 0.0, 0.2)
    window.drawRect(x, y, w * (percent / 100.0), h, 0.25, 1.0, 0.25)
