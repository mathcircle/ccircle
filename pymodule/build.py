import glob
from distutils.core import setup, Extension

VERSION = '0.7.6'

srcList = glob.glob('./src/*.c')
module_ccircle = Extension(
  'ccircle',

  include_dirs = [
    './extinclude/',
    './include/',
  ],

  libraries = [
    'gdi32',
    'opengl32',
    'user32',
    'freetype28MT',
  ],

  library_dirs = [
    './extlib/',
  ],

  sources = srcList,
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
