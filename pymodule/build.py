import glob
from distutils.core import setup, Extension

VERSION = '0.8.9'

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
    'winmm',
  ],

  library_dirs = [
    './extlib/',
  ],

  sources = srcList,
)

setup(
  name = 'CodingCircle Module',
  version = VERSION,
  url = 'http://coding.mathcircle.us',
  description = 'For use by students of the LSU Coding Circle program.',
  author = 'Josh Parnell',
  author_email = 'josh@ltheory.com',
  ext_modules = [ module_ccircle ],
)
