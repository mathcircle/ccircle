# CCircle Module Documentation: Image

## [Back to Index](index)

## Class : ccircle.Image

## `ccircle.Image(path) -> new Image`
  Load an image from `path`.

  _NOTE: Loading an image requires that you have a window open!_

## `image.draw(x, y, width, height, [angle=0]) -> None`
  Draw the image on the active window at the point `(x, y)` and with size
  `width` x `height` pixels. The optional `angle` parameter can be used to
  draw the image with a rotation of `angle` _degrees_ about its origin.

## `image.drawSub(x, y, width, height, subX, subY, subWidth, subHeight, [angle=0]) -> None`
  Like `image.draw`, except can be used to draw a specific rectangular
  sub-region of the image. The sub-region that will be drawn in place of the
  full image is the rectangle that starts at `(subX, subY)` in
  _image coordinates_, and spans `subWidth` x `subHeight` pixels _in image space_.

  This function is particularly useful for atlases that contain many images,
  like sprite sheets or texture tiles.

  If, for example, you have a 512 x 512 pixel image that is split evenly into
  four quadrants (each of size 256 x 256), the following calls could be used
  to draw each sub-piece of the image in isolation:

    img.drawSub(x, y, 256, 256, 0, 0, 256, 256)     # Draws the top-left sub-image
    img.drawSub(x, y, 256, 256, 256, 0, 256, 256)   # Draws the top-right sub-image
    img.drawSub(x, y, 256, 256, 0, 256, 256, 256)   # Draws the bottom-left sub-image
    img.drawSub(x, y, 256, 256, 256, 256, 256, 256) # Draws the bottom-right sub-image

## `image.eraseRed() -> None`
  Erases every pixel that is pure red, turning that pixel fully-transparent.

## `image.eraseGreen() -> None`
  Erases every pixel that is pure green, turning that pixel fully-transparent.

## `image.eraseBlue() -> None`
  Erases every pixel that is pure blue, turning that pixel fully-transparent.

## `image.eraseWhite() -> None`
  Erases every pixel that is pure white, turning that pixel fully-transparent.

## `image.getPixel(x, y) -> (r, g, b, a)`
  Return the color of the image pixel `(x, y)` as a red, green, blue, alpha tuple.
  The pixel coordinates must be in-bounds:

    0 <= x < image.width
    0 <= y < image.height

## `image.getSize() -> (width, height)`
  Return the size of the image in pixels.

## `image.recolor(r0, g0, b0, r1, g1, b1, [tolerance=1.0/128.0]) -> None`
  Modify the image such that every pixel within a maximum of `tolerance` shades
  of `(r0, g0, b0)` is recolored to `(r1, g1, b1)`.

