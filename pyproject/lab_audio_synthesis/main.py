import ccircle
import time
import random
import util
from math import *

window = ccircle.Window('Lab: Audio Synthesis')
mysound = ccircle.Sound()

def sawtooth(t, f):
    return 2.0 * ((t * f) % 1.0) - 1.0

def sine(t, f):
    return sin(2.0 * pi * t * f)

mysound.addSine(0, 1, util.getNoteFrequency(60), 1)
mysound.play()
time.sleep(1)