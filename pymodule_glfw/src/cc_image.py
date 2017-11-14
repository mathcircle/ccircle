import cc_preconditions as preconditions
import numpy as np
from OpenGL.GL import *
import PIL.Image as pillow_image

class Image:

    def __init__(self, absolute_file_path):
        preconditions.file_exists(absolute_file_path)
        self.fp = absolute_file_path
        self.__load_image()
        assert self.is_init()

    @property
    def width(self):
        return self.image.size[0]

    @property
    def height(self):
        return self.image.size[1]

    def get_image_bytes(self):
        return self.image.tobytes("raw", "RGBA", 0, -1)

    def is_init(self):
        return self.texture_id is not None and self.image is not None

    def __load_image(self):
        self.image = pillow_image.open(self.fp)
        self.texture_id = glGenTextures(1)
        Image.__bind_texture(self.texture_id)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            3,
            self.width,
            self.height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            self.get_image_bytes()
        )

    def draw(self, x, y, width, height, r=1.0, g=1.0, b=1.0, a=1.0, angle=None):
        """ Draws an image given x, y, sx, sy."""
        Image.__draw_image(self.texture_id, x, y, width, height,
                           0.0, 0.0, 1.0, 1.0, r, g, b, a, angle)

    def erase_white(self):
        self.__color_transparent(1, 1, 1)
        self.upload_image()

    def __color_transparent(self, r, g, b):
        """ Computes a new image such that matching pixels (r, g, b) are transparent (alpha->0)."""
        color = Image.rgb_to_color(r, g, b)
        image_array = np.array(self.image) # Height x width x 4 numpy array
        r, g, b, a = image_array.T  # Temporarily unpack the bands for readability
        matching = (r == color[0]) & (g == color[1]) & (b == color[2])
        image_array[:, :, 3][matching] = 0.0
        self.image = pillow_image.fromarray(image_array)

    @staticmethod
    def rgb_to_color(r, g, b):
        """ RGB [0, 1] to "hex" co.lor [0, 255] tuple.
        e.g.
            WHITE: rgb_to_color(1.0, 1.0, 1.0) -> (255, 255, 255)
            BLACK: rgb_to_color(0.0) -> (0, 0, 0)

        Return: The Color tuple (r, g, b) corresponding to the hex tuple."""
        return (int(r * 255), int(g * 255),int(b * 255))

    def upload_image(self):
        """Sets the GL texture to reference the new self.image."""
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glTexImage2D(
            GL_TEXTURE_2D,
            0,
            3,
            self.width,
            self.height,
            0,
            GL_RGBA,
            GL_UNSIGNED_BYTE,
            self.get_image_bytes()
        )

    @staticmethod
    def __draw_image(texture_id, x, y, sx, sy, u1, v1, u2, v2, r, g, b, a, angle):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glColor4f(r, g, b, a)

        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(0.5 * sx + x, 0.5 * sy + y, 0)
        if angle:
            glRotatef(angle, 0, 0, -1)
        glTranslatef(-0.5 * sx, -0.5 * sy, 0)

        glBegin(GL_QUADS)
        glTexCoord2f(u1, v1)
        glVertex2f(0, 0)
        glTexCoord2f(u1, v2)
        glVertex2f(0, sy)
        glTexCoord2f(u2, v2)
        glVertex2f(sx, sy)
        glTexCoord2f(u2, v1)
        glVertex2f(sx, 0)
        glEnd()

        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    @staticmethod
    def __bind_texture(texture_id):
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)