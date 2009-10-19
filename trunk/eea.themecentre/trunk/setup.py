from setuptools import setup, find_packages

setup(name='eea.themecentre',
      version = '0.1',
      url = 'http://svn.eionet.europa.eu/repositories/Zope',
      description = 'ThemeCentre',
      author = 'Tim Terlegard, Sasha Vincic',
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
