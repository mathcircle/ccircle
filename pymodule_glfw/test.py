import os
from cc_window import Window
from cc_image import Image

# Open Window.
win = Window()

while win.isOpen():
    # Clear Window.
    win.clear(0, 0, 0)

    # Specify what to draw - a cat looking at a ball on a string.
    # Ball and String.
    Window.draw_line(300, 100, 300, 500, 1.0, 0.0, 0.0)
    Window.draw_circle(300, 400, 50, 0.0, 1.0, 0.0)
    # Cat.
    cat_file = '%s/res/%s' % (os.path.dirname(__file__), 'cat_w.png')
    cat = Image(cat_file)
    cat.erase_white()
    cat.draw(300, 400, 500, 500, angle=180)

    # Update window with new scene.
    win.update()

# Close Window.
win.destroy()