from distutils.core import setup


setup(name='mkvtomp4',
      version='1.6.0',
      description='FFmpeg wrapper for converting .mkv files to .mp4',
      author='Kevin Barnes',
      author_email='kbarnes3@gmail.com',
      url='http://www.kbarnes3.com',
      packages=['MKVtoMP4'],
      entry_points={
          'console_scripts': [
              'MKVtoMP4 = MKVtoMP4.__main__:entry_point'
          ]
      },
      )
