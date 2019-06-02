""" Example based off of http://cegui.org.uk/wiki/Using_PyCEGUI_with_glfw3_and_PyOpenGL_(0.8)"""

from cc.window import Window

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