from __future__ import print_function
from setuptools import setup, find_packages, Command
from setuptools.command.sdist import sdist
from setuptools.command.build_py import build_py
from setuptools.command.egg_info import egg_info
from subprocess import check_call
import os
import sys
import platform
from os.path import (
    join, dirname, abspath, exists
)

here = dirname(abspath(__file__))
node_root = join(here, 'js')
is_repo = exists(join(here, '.git'))

npm_path = os.pathsep.join([
    join(node_root, 'node_modules', '.bin'),
                os.environ.get('PATH', os.defpath),
])

from distutils import log
log.set_verbosity(log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

LONG_DESCRIPTION = 'An Interactive Grid for Sorting and Filtering DataFrames in Jupyter Notebook'

def update_package_data(distribution):
    """update package_data to catch changes during setup"""
    build_py = distribution.get_command_obj('build_py')
    # distribution.package_data = find_package_data()
    # re-init build_py options which load package_data
    build_py.finalize_options()

version_ns = {}
with open(join(here, 'qgrid', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

def read_requirements(basename):
    reqs_file = join(dirname(abspath(__file__)), basename)
    with open(reqs_file) as f:
        return [req.strip() for req in f.readlines()]

reqs = read_requirements('requirements.txt')

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths

data_files = package_files('qgrid/static')


def extras_require():
    return {
        "test": [
            "pytest>=2.8.5",
            "flake8>=3.6.0"
        ],
    }

setup_args = {
    'name': 'qgrid',
    'version': version_ns['__version__'],
    'description': 'An Interactive Grid for Sorting and Filtering DataFrames in Jupyter Notebook',
    'long_description': LONG_DESCRIPTION,
    'include_package_data': True,
    'data_files': [
        ('share/jupyter/nbextensions/qgrid', data_files),
    ],
    'install_requires': reqs,
    'extras_require': extras_require(),
    'packages': find_packages(),
    'zip_safe': False,
    'cmdclass': {
        'build_py': build_py,
        'egg_info': egg_info,
        'sdist': sdist
    },

    'author': 'Quantopian Inc.',
    'author_email': 'opensource@quantopian.com',
    'url': 'https://github.com/quantopian/qgrid',
    'license': 'Apache-2.0',
    'keywords': [
        'ipython',
        'jupyter',
        'widgets',
    ],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Framework :: IPython',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Office/Business :: Financial',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Multimedia :: Graphics',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
}

setup(**setup_args)
