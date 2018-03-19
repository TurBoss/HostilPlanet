import pygame
from lib.cnst import *
from lib import sprite
from lib import levels


def init(g, r, n, hidden=False, *params):
    door_type = levels.LEVELS[g.game.lcur][2]

    s = sprite.Sprite3(g, r, 'doors/door-close-%d' % door_type, (0, 0, 16, 32))  # 3
    s.rect.centerx = r.centerx
    s.rect.centery = r.centery - (32 - 16) / 2
    s.loop = loop
    s.hit = sprite_hit
    s.open = None
    s.hit_groups.add('player')
    s.hidden = hidden
    if hidden:
        s.image = None
    # s.hit = hit
    g.sprites.insert(0, s)

    s.door_type = door_type

    return s


def loop(g, s):
    if s.hidden:
        s.image = None
        return

    if s.open > 0:
        if (s.open == 40):
            s.image = 'doors/door-1-%d' % s.door_type
        elif (s.open == 30):
            s.image = 'doors/door-2-%d' % s.door_type
        elif (s.open == 20):
            s.image = 'doors/door-3-%d' % s.door_type
        elif (s.open == 10):
            s.image = 'doors/door-open-%d' % s.door_type
            s.open = None
            return
        s.open -= 1


def sprite_hit(g, a, b):
    b.current_door = a


def hit(g, pos, b):
    cx, cy = pos

    from lib import sprite
    # n_code = sprite.get_code(g,a,1,0)
    dx = 1
    while g.data[2][int(cy)][int(cx) + dx] in DOOR_CODES:
        dx += 1
    n_code = g.data[2][int(cy)][int(cx) + dx]

    if n_code == 0: return

    layer = g.data[2]

    w, h = g.size
    xx, yy = cx, cy
    for y in range(0, h):
        for x in range(0, w):
            if layer[y][x] in DOOR_CODES and layer[y][x - 1] == n_code:
                xx, yy = x, y

    # t = g.layer[yy][xx]
    rect = pygame.Rect(xx * TW, yy * TH, TW, TH)
    s = b
    s.rect.centerx = rect.centerx
    s.rect.bottom = rect.bottom
    if s.standing != None:
        sprite.stop_standing(g, s)

    sprite.init_bounds(g, s)
    sprite.init_view(g, s)
    sprite.init_codes(g, s)
    s.prev = pygame.Rect(s.rect)
    s._prev = pygame.Rect(s.rect)

    g.status = 'transition'

    g.game.sfx['door'].play()
