# CCircle Module Documentation: Input

## [Back to Index](index)

## `ccircle.isKeyDown(key) -> Bool`
  Return whether or not the given key is currently pressed down

  Use the following strings to specify the key:

    'a' through 'z' -> letter keys
    'backspace'     -> backspace
    'enter'         -> enter / return
    'esc'           -> escape
    'space'         -> spacebar
    'left'          -> left arrow key
    'right'         -> right arrow key
    'up'            -> up arrow key
    'down'          -> down arrow key

## `ccircle.isMouseDown(button) -> Bool`
  Return whether or not the given mouse button is currently pressed down

  Use the following strings to specify the button:

    'left'     -> left button
    'middle'   -> middle button (scroll wheel)
    'right'    -> right button
    'x1'       -> extra button 1 (not applicable to all mice)
    'x2'       -> extra button 2 (not applicable to all mice)
