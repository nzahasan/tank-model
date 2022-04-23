#!/usr/bin/env python3
from distutils.core import setup
from tank_core import __version__, __author__

readme_contents = open('readme.md','r').read()

scritps_list = [
	'scripts/hms_to_project.py',
	'scripts/tank_cmd.py',
	'scripts/optimize_project.py',
	'scripts/compute_project.py',
]


setup(
	name='tank_hydrological_model',
	version= __version__,
	author= __author__,
	packages= ['tank_core'],
	scripts = scritps_list,
	
	license = 'MIT',
	python_requires = '>=3.6',
	description= 'Python implementation of Tank Hydrologic Model, a conceptual rainfall-runoff model proposed by Sugawara and Funiyuki (1956)',
	long_description = readme_contents,
	long_description_content_type = 'text/markdown',
	keywords = ['hydrologic-model', 'tank-model'],
	url = 'https://github.com/nzahasan/tank-model',
	
	include_package_data = True,
    zip_safe = False,

	install_requires=[
        'numpy',
		'scipy',
		'pandas',
		'fiona',
		'shapely',
		'pyscissor',
		'click'

    ]


)