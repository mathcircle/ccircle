# CCircle Module Documentation: Window

## [Back to Index](index)

Here you will find functions related to creating and using on-screen windows,
as well as drawing things inside windows.

## Class : ccircle.Window

## `ccircle.Window([title='CC Window', width=640, height=480]) -> new Window`
  Return a new window named `title` with size `width` x `height`

## `window.clear(r, g, b) -> None`
  Clear the entire window with the color `(r, g, b)`

## `window.drawCircle(x, y, radius, [r=1.0, g=1.0, b=1.0]) -> None`
  Draw a centered at `(x, y)` with radius `radius` and color `(r, g, b)`

## `window.drawLine(x1, y1, x2, y2, [width=2.0, r=1.0, g=1.0, b=1.0]) -> None`
  Draw a from `(x1, y1)` to `(x2, y2)` that is `width`
  pixels thick and has color `(r, g, b)`

## `window.drawPoint(x, y, [size=2.0, r=1.0, g=1.0, b=1.0]) -> None`
  Draw a point at `(x, y)` that is `size` pixels wide and has color `(r, g, b)`

## `window.drawRect(x, y, width, height, [r=1.0, g=1.0, b=1.0]) -> None`
  Draw a rectangle starting at `(x, y)` (the top-left corner) that is `width`
  pixels wide and `height` pixels tall and has color `(r, g, b)`

## `window.drawTri(x1, y1, x2, y2, x3, y3, [r=1.0, g=1.0, b=1.0]) -> None`
  Draw a triangle with corners `(x1, y1)`, `(x2, y2)`, and `(x3, y3)` and color
  `(r, g, b)`

## `window.getMousePos() -> (x, y)`
  Return the position, in pixels, of the mouse relative to the top-left corner of
  the window

## `window.getSize() -> (width, height)`
  Return the size of the window in pixels

## `window.hideMouse() -> None`
  Set the mouse cursor to be invisible when inside the window

## `window.isOpen() -> Bool`
  Return whether or not the window is still open; use `while window.isOpen():`
  to loop until the window close button is clicked or the window is otherwise
  killed

## `window.setSize(width, height) -> None`
  Set the size of the window to `width` x `height`

## `window.showMouse() -> None`
  Set the mouse cursor to be visible when inside the window (this is the default
  behavior)

## `window.toggleMaximized() -> None`
  Toggle the maximized state of the window; windows are not maximized by default,
  so the first call to toggleMaximized will maximize the window

## `window.update() -> None`
  Update the window, causing drawn elements to be visible; call this function
  once per loop *at the end of all drawing-related calls*

  Typical window loops should look like this:

    ```python
    win = ccircle.Window('SuperWindow!!')
    while win.isOpen():
      # Do your drawing and other stuff here!
      win.update()
    ```
