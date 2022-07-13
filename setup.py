#!/usr/bin/env python3
from distutils.core import setup
from tank_core import __version__, __author__

README_CONTENT = open('readme.md','r').read()

SCRIPTS = [
    'scripts/tank_cmd.py',
    'scripts/cpc_et.py',
]

PACKAGES = [
    'tank_core'
]

REQUIRED_PACKAGES = [
    'numpy',
    'scipy',
    'pandas',
    'pyscissor',
    'click',
    'matplotlib',
    'tabulate',
    'pathlib',
    'pytest',
    'python-dateutil',
    'pytz'
]

KEYWORDS = [
    'hydrology', 
    'rainfall-runoff-model',
    'hydrologic-model'
    'tank-model', 
    'tank-hydrologic-model',
]

setup(
    name='tank_hydrological_model',
    version= __version__,
    author= __author__,
    packages= PACKAGES,
    scripts = SCRIPTS,
    license = 'MIT',
    python_requires = '>=3.6',
    description= 'Python implementation of Tank Hydrologic Model, a conceptual rainfall-runoff model proposed by Sugawara and Funiyuki (1956)',
    long_description = README_CONTENT,
    long_description_content_type = 'text/markdown',
    keywords = KEYWORDS,
    url = 'https://github.com/nzahasan/tank-model',
    include_package_data = True,
    zip_safe = False,
    install_requires= REQUIRED_PACKAGES
)