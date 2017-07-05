from distutils.core import setup, Extension

VERSION = '0.6.3'

module_ccircle = Extension(
  'ccircle',

  sources = [
    'ccircle.c',
    'ccircle_image.c',
    'ccircle_image_load.c',
    'ccircle_input.c',
    'ccircle_window.c',
  ],

  libraries = [
    'gdi32',
    'opengl32',
    'user32',
  ],
)

setup(
  name = 'CodingCircle Python Extensions',
  version = VERSION,
  url = 'http://coding.mathcircle.us',
  description = 'For use by students of the LSU Coding Circle program.',
  author = 'Josh Parnell',
  author_email = 'josh@ltheory.com',
  ext_modules = [ module_ccircle ],
)
