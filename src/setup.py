__author__ = "LikKee"
__date__ = "$Aug 19, 2015 1:27:44 PM$"

from setuptools import setup, find_packages

setup (
       name='Music Artinizer',
       version='0.3',
       packages=find_packages(),

       # Declare your packages' dependencies here, for eg:
       install_requires=['foo>=3'],

       # Fill in these to make your Egg ready for upload to
       # PyPI
       author='LikKee',
       author_email='pisces_sky15@yahoo.com',

       summary='Sort all music file by artist.',
       url='',
       license='',
       long_description='Support only MP3, WAV, WMA & FLAC. Sort all music file by artist, create new folder named by artist, move from old folder to respective artist folder.',

       # could also include long_description, download_url, classifiers, etc.

  
       )