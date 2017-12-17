import math
import glfw
from OpenGL.GL import *
import cc_window_input


class Window:
    """Window class powered by GLFW. Provides 'wrapper' function calls to circumvent confusing GLFW
            and GL nuances for a more intuitive end-user experience. """

    def __init__(self, width=1920, height=1080, win_title="Splash Window", fullscreen=False):
        """Create window, set context and register input callbacks."""
        if not glfw.init():
            raise RuntimeError(
                'Could not initialize GLFW. You must first install it. TODO(Brendan): Installer.')

        monitor = glfw.get_primary_monitor() if fullscreen else None
        self.win = glfw.create_window(width=width, height=height, title=win_title, monitor=monitor)
        if not self.win:
            raise RuntimeError('Could not create a GLFW Window. Ask Brendan for help.')
        self._set_active()

        glEnable(GL_POINT_SMOOTH)
        glEnable(GL_LINE_SMOOTH)
        glHint(GL_POINT_SMOOTH_HINT, GL_NICEST)
        glHint(GL_LINE_SMOOTH_HINT, GL_NICEST)
        glPointSize(2.0)
        glLineWidth(1.0)

        cc_window_input.AcceptInput(self.win)

    """ PUBLIC FUNCTIONS """

    def isOpen(self):
        return not glfw.core.window_should_close(self.win)

    def get_top_left_corner(self):
        """Gets the coordinates of the top left corner of the window.

        Returns:
            (top_left_x, top_left_y): The top-left corner's coordinate tuple.
        """
        return tuple(glfw.get_window_pos(self.win))

    def get_size(self):
        """Gets the size of the window.

        Returns:
            (width, height): The size of the window.
                """
        return tuple(glfw.get_window_size(self.win))

    def get_mouse_pos(self):
        """The coordinates of the mouse position with respect to the top-left corner of the window.

        Returns:
            (x, y): A tuple of the mouse position.
        """
        return tuple(glfw.get_cursor_pos(self.win))

    def clear(self, r, g, b):
        self._set_active()
        self._set_viewport()
        glClearColor(r, g, b, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

    def destroy(self):
        glfw.destroy_window(self.win)

    """ PUBLIC STATIC FUNCTIONS """

    @staticmethod
    def draw_circle(x, y, radius, r=1.0, g=1.0, b=1.0, a=1.0):
        """Draws a circle centered at (x, y).

        Notes:
            Parameters in pixels.
            Parameters are NOT with respect to any window, but rather the main monitor (hence the static method).
        """
        fv = radius / 4.0
        fv = max(fv, 16)
        fv = max(fv, 64)
        verts = int(fv)

        glBegin(GL_POLYGON)
        glColor4f(r, g, b, a)
        for i in range(verts):
            angle1 = 2 * math.pi * (i + 0) / fv
            angle2 = 2 * math.pi * (i + 1) / fv
            glVertex2f(x, y)
            glVertex2f(x + radius * math.cos(angle1), y + radius * math.sin(angle1))
            glVertex2f(x + radius * math.cos(angle2), y + radius * math.sin(angle2))
        glEnd()

    @staticmethod
    def draw_line(x1, y1, x2, y2, r=1.0, g=1.0, b=1.0, a=1.0):
        glBegin(GL_LINES)
        glColor4f(r, g, b, a)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()

    @staticmethod
    def close_all_windows():
        glfw.core.terminate()

    """ PRIVATE FUNCTIONS """

    def _set_active(self):
        glfw.core.make_context_current(self.win)

    def _set_viewport(self):
        (fb_width, fb_height) = tuple(glfw.get_framebuffer_size(self.win))
        (winX, winY) = tuple(glfw.get_window_pos(self.win))
        glViewport(winX, winY, fb_width, fb_height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glTranslated(-1.0, 1.0, 0.0)
        glScaled(2.0 / fb_width, -2.0 / fb_height, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def update(self):
        glfw.core.poll_events()
        glfw.core.swap_buffers(self.win)
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
