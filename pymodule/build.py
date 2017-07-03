from distutils.core import setup, Extension

module_ccircle = Extension(
  'ccircle',
  sources = [
    'ccircle.c',
    'ccircle_window.c',
  ]
)

setup(
  name = 'CodingCircle Python Extensions',
  version = '0.31',
  url = 'http://coding.mathcircle.us',
  description = 'For use by students of the LSU Coding Circle program.',
  author = 'Josh Parnell',
  author_email = 'josh@ltheory.com',
  ext_modules = [ module_ccircle ],
)
