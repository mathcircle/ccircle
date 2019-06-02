from cc import *
from cc.window_input import RegisterInputFunctionality


class Window:
    """ Window class powered by GLFW.
        Provides intuitive 'wrapper' function calls to circumvent confusing GLFW and GL nuances.

    Args:
        width (int, optional): Width in pixels of the GLFW window.
        height (int, optional): Height in pixels of the GLFW window.
        win_title (str, optional): The title of the window.
        fullscreen (bool, optional): if the window should be fullscreen.
    """

    def __init__(self, width=960, height=520, win_title="Splash Window", fullscreen=False):
        """Create window, set context and register input callbacks."""
        monitor = glfw.get_primary_monitor() if fullscreen else None
        self.win = glfw.create_window(width=width, height=height, title=win_title, monitor=monitor, share=None)
        RegisterInputFunctionality(self.win)

    """ PUBLIC FUNCTIONS """

    def isOpen(self):
        """ Returns whether or not this window is open.

        Returns:
            True if open, False otherwise.
        """
        return not glfw.window_should_close(self.win)

    def get_top_left_corner(self):
        """ Gets the coordinates of the top left corner of the window.

        Returns:
            (top_left_x, top_left_y): The .
        """
        return tuple(glfw.get_window_pos(self.win))

    def get_size(self):
        """ Gets the size of the window.

        Returns:
            (width, height): The size of the window.
        """
        return tuple(glfw.get_window_size(self.win))

    def get_mouse_pos(self):
        """ The coordinates of the mouse position with respect to the top-left corner of the window.

        Returns:
            (x, y): A tuple of the mouse position.
        """
        return tuple(glfw.get_cursor_pos(self.win))

    def clear(self, r, g, b):
        self._set_active()
        self._set_viewport()
        gl.glClearColor(r, g, b, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

    def destroy(self):
        glfw.destroy_window(self.win)

    """ PUBLIC STATIC FUNCTIONS """

    @staticmethod
    def draw_circle(x, y, radius, r=1.0, g=1.0, b=1.0, a=1.0):
        """ Draws a circle centered at (x, y).

        Notes:
            Parameters in pixels.
            Parameters are NOT with respect to any window, but rather the main monitor (hence the static method).
        """
        fv = radius / 4.0
        fv = max(fv, 16)
        fv = max(fv, 64)
        verts = int(fv)

        gl.glBegin(gl.GL_POLYGON)
        gl.glColor4f(r, g, b, a)
        for i in range(verts):
            angle1 = 2 * math.pi * (i + 0) / fv
            angle2 = 2 * math.pi * (i + 1) / fv
            gl.glVertex2f(x, y)
            gl.glVertex2f(x + radius * math.cos(angle1), y + radius * math.sin(angle1))
            gl.glVertex2f(x + radius * math.cos(angle2), y + radius * math.sin(angle2))
        gl.glEnd()

    @staticmethod
    def draw_line(x1, y1, x2, y2, r=1.0, g=1.0, b=1.0, a=1.0):
        gl.glBegin(gl.GL_LINES)
        gl.glColor4f(r, g, b, a)
        gl.glVertex2f(x1, y1)
        gl.glVertex2f(x2, y2)
        gl.glEnd()

    @staticmethod
    def close_all_windows():
        glfw.terminate()

    """ PRIVATE FUNCTIONS """

    def _set_active(self):
        glfw.make_context_current(self.win)

    def _set_viewport(self):
        (fb_width, fb_height) = tuple(glfw.get_framebuffer_size(self.win))
        (winX, winY) = tuple(glfw.get_window_pos(self.win))
        gl.glViewport(winX, winY, fb_width, fb_height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glTranslated(-1.0, 1.0, 0.0)
        gl.glScaled(2.0 / fb_width, -2.0 / fb_height, 1.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

    def update(self):
        glfw.poll_events()
        glfw.swap_buffers(self.win)
        gl.glClearColor(0, 0, 0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
