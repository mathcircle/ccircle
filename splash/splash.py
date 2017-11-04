import math

import glfw
if not glfw.init():
    raise RuntimeError('Could not initialize GLFW')

import OpenGL.GL as gl

__all__ = ['glfw', 'gl', 'math']