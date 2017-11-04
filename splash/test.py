from splash_window import *

# Open Window.
win = Window()

while win.isOpen():
    # Clear Window.
    win.clear(0, 0, 0)

    # Specify scene.
    Window.draw_circle(100, 200, 50, 0.0, 0.0, 0.7)
    Window.draw_line(100, 100, 300, 300, 0.0, 0.0, 0.7)

    # Update window with new scene.
    win.update()

# Close Window.
win.destroy()