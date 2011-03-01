from setuptools import setup, find_packages
import os
from os.path import join

name = 'eea.themecentre'
path = ['src'] + name.split('.') + ['version.txt']
version = open(join(*path)).read().strip()

setup(name='eea.themecentre',
      version=version,
      url = 'http://svn.eionet.europa.eu/repositories/Zope',
      description = 'ThemeCentre',
      author = 'Tim Terlegard, Sasha Vincic, Antonio De Marinis (EEA), European Environment Agency (EEA)',
      author_email = "webadmin@eea.europa.eu",
      long_description = file('README.txt').read(),
      classifiers = ['Development Status :: 5 - Production/Stable',
                    'Framework :: Zope3',
                    'Intended Audience :: Developers'],
      packages = find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages = ['eea'],
      include_package_data = True,
      zip_safe = False,
      )
