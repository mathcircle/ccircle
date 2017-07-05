# CCircle Module Documentation: Window

Here you will find functions related to creating and using on-screen windows,
as well as drawing things inside windows.

## Class : ccircle.Window

## `ccircle.Window(title='CCircle Window', width=640, height=480) -> new Window`
  Return a new window named `title` with size `width` x `height`.

## `window.clear(r, g, b) -> None`
  Clear the entire window with the color `(r, g, b)`

## `window.drawLine(x1, y1, x2, y2, [width=2.0, r=1.0, g=1.0, b=1.0]) -> None`
  Draw a line within the window from `(x1, y1)` to `(x2, y2)` that is `width`
  pixels thick and has color `(r, g, b)`.
