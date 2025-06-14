#!/usr/bin/env python

# The following distutils seems to stop working with newer
# Python version >= 3.12
# Someone with Python knowlege, please fix.
from distutils.core import setup, Extension

core_ext = Extension(
    name                = 'core',
    sources             = ['rgbmatrix/core.cpp'],
    include_dirs        = ['../lib/rgbmatrix/include'],
    library_dirs        = ['../lib/rgbmatrix'],
    libraries           = ['rgbmatrix'],
    extra_compile_args  = ["-O3", "-Wall"],
    language            = 'c++'
)

graphics_ext = Extension(
    name                = 'graphics',
    sources             = ['rgbmatrix/graphics.cpp'],
    include_dirs        = ['../lib/rgbmatrix/include'],
    library_dirs        = ['../lib/rgbmatrix'],
    libraries           = ['rgbmatrix'],
    extra_compile_args  = ["-O3", "-Wall"],
    language            = 'c++'
)

setup(
    name                = 'rgbmatrix',
    version             = '0.0.1',
    author              = 'Christoph Friedrich',
    author_email        = 'christoph.friedrich@vonaffenfels.de',
    classifiers         = ['Development Status :: 3 - Alpha'],
    ext_package         = 'rgbmatrix',
    ext_modules         = [core_ext, graphics_ext],
    packages            = ['rgbmatrix']
)
