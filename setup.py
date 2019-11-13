from distutils.core import Extension, setup
from distutils.command.install import INSTALL_SCHEMES
import os

# http://stackoverflow.com/questions/1612733/including-non-python-files-with-setup-py
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']


def find_data_files(srcdir, *wildcard):
    file_list = []
    if not srcdir.endswith('/'):
        srcdir += '/'
    for files in os.listdir(srcdir):
        if files.endswith(wildcard):
            file_list.append(srcdir + files)
    return file_list


bkgr = find_data_files('data/bkgr/', '.png')
chips = find_data_files('data/chips/', '.png')
ending = find_data_files('data/ending/', '.png')
images = find_data_files('data/images/', '.png')
intro = find_data_files('data/intro/', '.png')
statusbar = find_data_files('data/statusbar/', '.png')


levels = find_data_files('data/levels/', '.tga')
music = find_data_files('data/music/', '.ogg')
sfx = find_data_files('data/sfx/', '.ogg')

setup(name='HostilPlanet',
      version='1.0.0',
      author='turboss',
      author_email='turboss@mail.com',
      description='Plaform robot game',
      url='http://github.com/TurBoss/HostilPlanet',
      download_url='http://github.com/TurBoss/HostilPlanet',
      license='GPL license',
      long_description=open('readme.md').read(),
      scripts=['run_game.py'],
      packages=['lib', 'lib.pgu'],
      data_files=[('data/fonts', ['data/fonts/04B_20__.TTF']),
                  ('data/bkgr', bkgr),
                  ('data/chips', chips),
                  ('data/ending', ending),
                  ('data/images', images),
                  ('data/intro', intro),
                  ('data/statusbar', statusbar),

                  ('data/levels', levels),
                  ('data/music', music),
                  ('data/sfx', sfx),
                  ],
      requires=[
          "pygame",
          "numpy",
          "pyrex",
      ],
)
