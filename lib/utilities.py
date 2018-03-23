import os

from pygame import RLEACCEL
from pygame import image as py_image
from pygame import error as py_error


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    try:
        image = py_image.load_basic(fullname)
    except py_error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()
