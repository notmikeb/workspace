from distutils.core import setup, Extension
import sipdistutils

setup(
  name = 'word',
  versione = '1.0',
  ext_modules=[
    Extension("word", ["word.sip", "word.cpp"], include_dirs=['.']),
    ],

  cmdclass = {'build_ext': sipdistutils.build_ext}
)