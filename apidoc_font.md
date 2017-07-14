# CCircle Module Documentation: Font

## [Back to Index](index)

## Class : ccircle.Font

## `ccircle.Font(path) -> new Font`
  Load a font from `path`.

## `font.draw(text, x, y, [size=10, r=1.0, g=1.0, b=1.0]) -> None`
  Draw the string `text` with an approximate pixel height of `size`, starting at
  `(x, y)` and with color `(r, g, b)`.

  _NOTE: Drawing text requires that you have a window open!_
