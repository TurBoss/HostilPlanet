import pygame
from lib.cnst import *
from lib import sprite
from lib import player


def init(g, r, n, facing, *params):
    s = sprite.Sprite3(g, r, 'rock/%s-0' % facing, (0, 0, 48, 12))
    # s.rect.bottom = r.bottom
    s.rect.centery = r.centery
    s.rect.centerx = r.centerx
    s.groups.add('solid')
    # s.groups.add('enemy')
    s.hit_groups.add('player')
    s.hit = hit
    g.sprites.append(s)
    s.loop = loop

    s.vx = 1
    s.vy = 0

    s.facing = facing

    s._prev = None  # pygame.Rect(s.rect)
    s.strength = 4
    s.damage = 1

    return s


def loop(g, s):
    if s.facing == 'left':
        if s.vx > 0:
            speed = 3
        else:
            speed = 1
    else:
        if s.vx > 0:
            speed = 1
        else:
            speed = 3

    if g.frame % speed == 0:
        if s._prev != None:
            if s.rect.x == s._prev.x or sprite.get_code(g, s, sign(s.vx), 0) == CODE_ROCK_TURN:
                s.vx = -s.vx
        s._prev = pygame.Rect(s.rect)

        s.rect.x += s.vx * 1
        s.rect.y += s.vy


def hit(g, a, b):
    player.damage(g, b, a)
