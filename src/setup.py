from distutils.core import setup
from Cython.Build import cythonize


setup(
	name='tank_core',
    ext_modules = cythonize("tank_core.py")
)