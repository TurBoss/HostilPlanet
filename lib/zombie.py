import pygame

from lib import player
from lib import sprite
from lib.cnst import *


def init(g, r, n, facing='left', *params):
    s = sprite.Sprite3(g, r, 'zombie/walk-%s-0' % facing, (0, 0, 16, 32))
    s.rect.bottom = r.bottom
    s.rect.centerx = r.centerx
    s.groups.add('solid')
    s.groups.add('enemy')
    s.hit_groups.add('player')
    s.hit = hit
    g.sprites.append(s)
    s.loop = loop
    s.next_frame = 12
    s.frame = 0
    s.facing = facing
    s.frame_speed = 10
    s.speed = 2

    s.vx = 1.0

    if s.facing == 'left':
        s.vx = -s.vx
    else:
        s.vx = s.vx

    s.vy = 0
    s.jumping = False
    s.walking = True
    # make sure this is always different at startup
    s._prev = None

    s.strength = 7
    s.damage = 2
    s.vy_jump = -5

    s.standing = None
    return s


def loop(g, s):
    sprite.apply_gravity(g, s)
    sprite.apply_standing(g, s)

    # if s.standing != None and s.vx != 0:
    # next_tile = g.layer[s.standing.pos[1]][s.standing.pos[0] + s.direction]
    # next2_tile = g.layer[s.standing.pos[1]][s.standing.pos[0] + s.direction*2]
    # if (next_tile.standable == 0) or (next2_tile.standable == 0):
    # s.rect.x = s._prev.x
    # s.direction = - s.direction
    # s.next_frame = 1


    if g.frame % s.speed == 0:
        if s.walking:
            if s._prev != None:
                if s.rect.x == s._prev.x or sprite.get_code(g, s, sign(s.vx), 0) == CODE_ZOMBIE_TURN:
                    s.vx = -s.vx
                    s.next_frame = 1
                    if s.vx < 0:
                        s.facing = 'left'
                    else:
                        s.facing = 'right'

            if s.standing != None and sprite.get_code(g, s, sign(s.vx), 1) == CODE_ZOMBIE_JUMP:
                # s.vy_jump = -3.1
                """
				if sprite.get_code(g,s,sign(s.vx)*2,1) == CODE_ZOMBIE_JUMP:
					s.vy_jump = -3.0
					if sprite.get_code(g,s,sign(s.vx)*3,1) == CODE_ZOMBIE_JUMP:
						s.vy_jump = -4.1
				"""
                s.jumping = True
                s.walking = False
                s.next_frame = 20
                s.image = 'zombie/prejump-%s' % s.facing

            s._prev = pygame.Rect(s.rect)

            s.rect.x += s.vx
            s.rect.y += s.vy
        else:
            s._prev = pygame.Rect(s.rect)
            if (s.next_frame <= 0):
                if (s.standing != None):
                    s.walking = True
                    s.jumping = False
                    s.next_frame = 1
                # s.vx*1
                vx = s.vx
                s.rect.x += sprite.myinc(g.frame, vx)
                s.rect.y += sprite.myinc(g.frame, s.vy)

        s.next_frame -= 1
        if s.next_frame == 0:
            if s.jumping:
                sprite.stop_standing(g, s)
                s.vy = s.vy_jump
                s.image = 'zombie/jump-%s' % s.facing
            else:
                s.next_frame = s.frame_speed
                s.frame += 1
                if s.frame > 3:
                    s.frame = 0
                s.image = 'zombie/walk-%s-%s' % (s.facing, s.frame)


def hit(g, a, b):
    player.damage(g, b, a)
