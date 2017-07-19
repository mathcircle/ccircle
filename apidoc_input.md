# CCircle Module Documentation: Input

## [Back to Index](index)

## `ccircle.isKeyDown(key) -> Bool`
  Return whether or not the given key is currently pressed down.

  Use the following strings to specify the key:

    'a' through 'z' -> letter keys
    '0' through '9' -> number keys (not numpad)
    'backspace'     -> backspace
    'enter'         -> enter / return
    'esc'           -> escape
    'space'         -> spacebar
    'left'          -> left arrow key
    'right'         -> right arrow key
    'up'            -> up arrow key
    'down'          -> down arrow key

## `ccircle.wasKeyPressed(key) -> Bool`
  Like `isKeyDown`, except returns `True` for only a single frame when
  the key goes from up to down (i.e., the moment the key is pressed).

## `ccircle.wasKeyReleased(key) -> Bool`
  Like `isKeyDown`, except returns `True` for only a single frame when
  the key goes from down to up (i.e., the moment the key is released).

## `ccircle.isMouseDown(button) -> Bool`
  Return whether or not the given mouse button is currently pressed down

  Use the following strings to specify the button:

    'left'     -> left button
    'middle'   -> middle button (scroll wheel)
    'right'    -> right button
    'x1'       -> extra button 1 (not applicable to all mice)
    'x2'       -> extra button 2 (not applicable to all mice)
