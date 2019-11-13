import pygame

from lib import player
from lib import spikey
from lib import platform
from lib import spiner
from lib import shoot
from lib import frog
from lib import tiles_basic
from lib import parasit
from lib import parasitshoot
from lib import door
from lib import sentinel
from lib import tentactul
from lib import tentactulshoot
from lib import brobo
from lib import guardianshoot
from lib import points
from lib import blob
from lib import guardian
from lib import boss
from lib import fireball
from lib import capsule
from lib import zombie
from lib import draco
from lib import dracoshoot
from lib import bat
from lib import tower
from lib import wibert
from lib import wibertshoot
from lib import rock
from lib import raider
from lib import explosion
from lib import drone
from lib import shield
from lib import ship

from lib.init import init_bkgr, init_bkgr_scroll, init_music

from lib.cnst import *


def _pass(*params): pass


INIT_CODES = {
    0x00: [_pass, ],
    0x10: [player.init, ],
    0xA0: [boss.init, ],
}

CODES = {
    # numerical codes for magic uses?
    0x00: [_pass, ],
    0x01: [_pass, ],
    0x02: [_pass, ],
    0x03: [_pass, ],
    0x04: [_pass, ],
    0x05: [_pass, ],
    0x06: [_pass, ],
    0x07: [_pass, ],
    0x08: [_pass, ],
    0x09: [_pass, ],
    0x0A: [_pass, ],
    0x0B: [_pass, ],
    0x0C: [_pass, ],
    0x0D: [_pass, ],
    0x0E: [_pass, ],
    0x0F: [_pass, ],

    # player related (16 codes)
    # 0x10 ...
    # 0x13 ...

    # spiner related (8 codes)
    0x20: [spiner.init, 1],
    0x21: [spiner.init, -1],
    0x22: [_pass, ],  # CODE_SPINER_TURN

    # spikey related (8 codes)
    0x28: [spikey.init, ],

    # platform related (8 codes)
    0x30: [platform.init, 1, 0],
    0x31: [platform.init, 0, -1],
    0x32: [platform.init, -1, 0],
    0x33: [platform.init, 0, 1],
    0x34: [_pass, ],  # CODE_PLATFORM_TURN

    # sentinel related (8 codes)

    0x38: [sentinel.init, ],
    0x39: [_pass, ],  # CODE_SENTINEL_TURN

    # frog related (8 codes)
    0x40: [frog.init, 1],
    0x41: [frog.init, -1],
    0x42: [_pass, ],  # CODE_FROG_TURN
    0x43: [_pass, ],  # CODE_FROG_JUMP

    # parasit related (8 codes)
    0x48: [parasit.init, ],
    0x49: [_pass, ],  # CODE_PARASIT_TURN

    # fally related (8 codes)
    0x50: [tiles_basic.fally_init, ],

    # tentactul related (8 codes)
    0x58: [tentactul.init, ],
    0x59: [_pass, ],  # CODE_TENTACTUL_TURN

    # door related
    0x60: [door.init, ],  # CODE_DOOR (press shoot/up to be transported)
    0x61: [_pass, ],  # CODE_DOOR_AUTO (you are instantly transported)
    0x62: [door.init, True],  # CODE_DOOR_HIDDEN (hidden regular door)

    # brobo related
    0x68: [brobo.init, 'left'],
    0x69: [brobo.init, 'right'],
    0x6A: [_pass, ],  # CODE_BROBO_TURN

    # level related
    0x70: [_pass, ],  # CODE_BOUNDS
    0x78: [init_bkgr, ],  # bkgr initializer
    0x79: [init_bkgr_scroll, 0, 6],  # bkgr scrolly magic stuff
    0x80: [init_music, ],  # music ..
    0x88: [_pass, ],  # CODE_EXIT

    # blob related (8 codes)
    0x90: [blob.init, ],

    # guardian (8 codes)
    0x98: [guardian.init, ],
    0x99: [_pass, ],  # CODE_GUARDIAN_TURN

    # boss related
    0xA1: [_pass, ],
    0xA2: [_pass, ],

    # zombie related

    0xA8: [zombie.init, 'left'],
    0xA9: [zombie.init, 'right'],
    0xAA: [_pass, ],  # CODE_ZOMBIE_TURN
    0xAB: [_pass, ],  # CODE_ZOMBIE_JUMP

    # draco related
    0xB8: [draco.init, 'left'],
    0xB9: [draco.init, 'right'],

    # bat related

    0xC8: [bat.init, 'left'],
    0xC9: [bat.init, 'right'],
    0xCA: [_pass, ],  # CODE_BAT_TURN
    0xCB: [_pass, ],  # CODE_BAT_ATTACK

    # tower related
    0xD8: [tower.init, 'left'],
    0xD9: [tower.init, 'right'],

    # wibert (8 codes)
    0xE8: [wibert.init, ],
    0xE9: [_pass, ],  # CODE_WIBERT_TURN

    # rock related (8 codes)
    0x91: [rock.init, 'left'],
    0x92: [rock.init, 'right'],
    0x93: [_pass, ],  # CODE_ROCK_TURN

    # raider ralated
    0xF8: [raider.init, ],
    0xF9: [_pass, ],  # CODE_RAIDER_TURN

    # ship related
    0xB0: [ship.init, ],

}


def c_init(g, pos, n):
    x, y = pos
    if n not in INIT_CODES and n not in CODES:
        print('undefined code:', x, y, '0x%2x' % n)
        return
    if n not in INIT_CODES: return
    v = INIT_CODES[n]
    return v[0](g, pygame.Rect(x * TW, y * TH, TW, TH), n, *v[1:])


def c_run(g, pos, n):
    x, y = pos
    if n not in INIT_CODES and n not in CODES:
        print('undefined code:', x, y, '0x%2x' % n)
        return
    if n not in CODES: return
    v = CODES[n]
    return v[0](g, pygame.Rect(x * TW, y * TH, TW, TH), n, *v[1:])
