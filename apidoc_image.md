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

## `image.getSize() -> (width, height)`
  Returns the size of the image in pixels.

