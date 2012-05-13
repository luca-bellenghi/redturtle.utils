from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='redturtle.utils',
      version=version,
      description="plone site maintenance utilities",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        "Intended Audience :: Developers",
        ],
      keywords='plone site maintenance',
      author='lucabel',
      author_email='luca.bellenghi@redturtle.it',
      url='https://github.com/luca-bellenghi/redturtle.utils',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['redturtle'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
