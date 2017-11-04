from splash import *

class Input:
    """Input for window class powered by GLFW.

    Args:
        win: An initialized GLFW window.

    """
    def __init__(self, win):
        # Register input callbacks.
        glfw.core.set_key_callback(win, on_key)
        glfw.core.set_mouse_button_callback(win, on_mouse_button)
        glfw.core.set_window_size_callback(win, on_resize)
        glfw.core.set_framebuffer_size_callback(win, on_framebuffer_resize)
        glfw.core.make_context_current(win)

@glfw.decorators.window_size_callback
def on_resize(win, width, height):
    fb_width, fb_height = glfw.get_framebuffer_size(win)
    gl.glViewport(0, 0, fb_width, fb_height)
    gl.glLoadIdentity()

@glfw.decorators.framebuffer_size_callback
def on_framebuffer_resize(win, width, height):
    gl.glViewport(0, 0, width, height)
    gl.glLoadIdentity()

@glfw.decorators.key_callback
def on_key(win, key, code, action, mods):
    # ESC -> Quit
    if key in [glfw.KEY_ESCAPE]:
        glfw.core.set_window_should_close(win, gl.GL_TRUE)

@glfw.decorators.mouse_button_callback
def on_mouse_button(win, button, action, mods):
    pass