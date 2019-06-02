from cc import *


class RegisterInputFunctionality:
    """Defines what (mouse, keyboard, etc.) input does to a window via callbacks.

    Args:
        win: An initialized GLFW window.
    """

    def __init__(self, win):
        # Register input callbacks.
        glfw.set_key_callback(win, _on_key)
        glfw.set_mouse_button_callback(win, _on_mouse_button)
        glfw.set_window_size_callback(win, _on_resize)
        glfw.set_framebuffer_size_callback(win, _on_framebuffer_resize)
        glfw.make_context_current(win)


def _on_resize(win, width, height):
    fb_width, fb_height = glfw.get_framebuffer_size(win)
    gl.glViewport(0, 0, fb_width, fb_height)
    gl.glLoadIdentity()


def _on_framebuffer_resize(win, width, height):
    gl.glViewport(0, 0, width, height)
    gl.glLoadIdentity()


def _on_key(win, key, code, action, mods):
    # ESC -> Quit
    if key in [glfw.KEY_ESCAPE]:
        glfw.set_window_should_close(win, gl.GL_TRUE)


def _on_mouse_button(win, button, action, mods):
    pass
