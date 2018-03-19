import pygame
from lib import sprite
from lib import player
from lib import parasitshoot
from lib.cnst import *


def init(g, r, n, facing='left', *params):
    s = sprite.Sprite3(g, r, 'parasit/parasit-%s-0' % (facing), (0, 0, 16, 32))
    s.rect.bottom = r.bottom
    s.rect.centerx = r.centerx
    s.groups.add('solid')
    s.groups.add('enemy')
    s.hit_groups.add('player')
    s.hit = hit
    g.sprites.append(s)
    s.loop = loop
    s.facing = facing

    s.speed = 2

    s.shoot = 120
    s.shooting = 0
    s.vx = 1.0

    if s.facing == 'left':
        s.vx = -s.vx
    else:
        s.vx = s.vx
    s.vy = 0

    s._prev = pygame.Rect(-1, -1, 0, 0)
    s.strength = 4
    s.damage = 1

    s.standing = None
    return s


def loop(g, s):
    sprite.apply_gravity(g, s)
    sprite.apply_standing(g, s)

    # if s.rect.x == s._prev.x: # or sprite.get_code(g,s,sign(s.vx),0) == CODE_PARASIT_TURN:
    #    s.vx = -s.vx
    if g.frame % s.speed == 0:
        s._prev = pygame.Rect(s.rect)

        if g.player.rect.centerx > s.rect.centerx:
            s.vx += 0.02
        elif g.player.rect.centerx < s.rect.centerx:
            s.vx -= 0.02

        if s.vx > 0.0:
            s.facing = 'right'
        elif s.vx < 0.0:
            s.facing = 'left'
        s.image = 'parasit/parasit-%s-%s' % (s.facing, (g.frame / 10) % 4)

        if sprite.get_code(g, s, sign(s.vx), 0) == CODE_PARASIT_TURN:
            s.vx = 0.0

        s.vx = min(1.0, s.vx)
        s.vx = max(-1.0, s.vx)

        if s.shoot == 0:
            shot = parasitshoot.init(g, s.rect, s)
            # g.sprites.append(shot)
            s.shoot = 120
            s.shooting = 3

        if s.shooting > 0:
            s.image = 'parasit/parasit-%s-shoot' % (s.facing)
            s.shooting -= 1

        s.shoot -= 1

        s.rect.x += sprite.myinc(g.frame, s.vx)
        s.rect.y += sprite.myinc(g.frame, s.vy)


def hit(g, a, b):
    player.damage(g, b, a)
