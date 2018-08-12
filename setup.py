#!/usr/bin/env python

from setuptools import setup

from storage import __version__


setup(name="sensapp-storage",
      version=__version__,
      description="Persists the data received from the sensors",
      author="Franck Chauvel",
      author_email="franck.chauvel@sintef.no",
      url="https://github.com/fchauvel/storage",
      packages=["storage"],
      test_suite="tests",
      entry_points = {
          'console_scripts': [
              'sensapp-storage = storage.start:main'
          ]
      }
     )
