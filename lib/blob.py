import pygame

from lib import player
from lib import sprite
from lib.cnst import *


def init(g, r, n, *params):
    s = sprite.Sprite3(g, r, 'blob', (0, 0, 16, 16))
    s.rect.bottom = r.bottom
    s.rect.centerx = r.centerx
    s.groups.add('solid')
    s.groups.add('enemy')
    s.hit_groups.add('player')
    s.hit = hit
    g.sprites.append(s)
    s.loop = loop

    s.vx = 0
    s.vy = 0

    s.next_jump = 0  # next_jump = 0

    s._prev = pygame.Rect(s.rect)
    s.strength = 4
    s.damage = 1

    s.standing = None
    return s


def loop(g, s):
    # print 'loop'
    sprite.apply_gravity(g, s)
    sprite.apply_standing(g, s)

    # print s.vy

    if s.next_jump == 0 and s.standing:
        s.vy = -4.0
        s.next_jump = FPS * 1
        sprite.stop_standing(g, s)
    if s.next_jump > 0:
        s.next_jump -= 1

    # if s.rect.x == s._prev.x:
    # s.vx = -s.vx
    s._prev = pygame.Rect(s.rect)

    # s.rect.x += s.vx
    s.rect.y += sprite.myinc(g.frame, s.vy)


def hit(g, a, b):
    player.damage(g, b, a)
    # print 'youve been spikeys!'
    pass
