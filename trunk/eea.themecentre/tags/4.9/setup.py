""" EEA Theme centre installer
"""
import os
from setuptools import setup, find_packages

name = 'eea.themecentre'
path = ['src'] + name.split('.') + ['version.txt']
version = open(os.path.join(*path)).read().strip()

setup(name='eea.themecentre',
      version=version,
      description='EEA Theme centre',
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='EEA theme centre plone zope python',
      author='Tim Terlegard, Sasha Vincic, Antonio De Marinis (EEA), '
             'European Environment Agency (EEA)',
      author_email='webadmin@eea.europa.eu',
      url="https://svn.eionet.europa.eu/projects/"
          "Zope/browser/trunk/eea.themecentre",
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['eea'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'p4a.video',
          'Products.PloneHelpCenter',
          'Products.ATVocabularyManager',
          'Products.LinguaPlone',
          'Products.EEAPloneAdmin',
          'valentine.linguaflow',
          'eea.design',
          'eea.promotion',
          'eea.mediacentre',
          'eea.rdfrepository',
          'eea.vocab',
          'Products.EEAContentTypes',
          'eea.versions', #because of @@get_interfaces. TODO plone4: fix this
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
