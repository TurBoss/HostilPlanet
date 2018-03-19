import pygame
from lib.cnst import *
from lib import tiles
from lib import player

from lib import shoot
from lib import explosion


def hit_block(g, a, b, top=1, right=1, bottom=1, left=1):
    # print 'you hit a block'

    r, cur, prev = a.rect, b.rect, b.prev

    got_hit = False

    if top and prev.bottom <= r.top and cur.bottom > r.top:
        got_hit = True
        cur.bottom = r.top
        if hasattr(b, 'standing'): b.standing = a
    if right and prev.left >= r.right and cur.left < r.right:
        got_hit = True
        cur.left = r.right
    if bottom and prev.top >= r.bottom and cur.top < r.bottom:
        got_hit = True
        cur.top = r.bottom
        # if hasattr(b,'vy'): b.vy = 0
        if hasattr(b, 'standing') and b.standing != None:
            import sprite
            sprite.stop_standing(g, b)
    if left and prev.right <= r.left and cur.right > r.left:
        got_hit = True
        cur.right = r.left

    if got_hit and 'shoot' in b.groups:
        b.active = False
        shoot.sound(g)

    if got_hit and 'cannon' in b.groups:
        shoot.sound(g)
        explosion.init(g, b.rect, b)
        b.active = False

    if got_hit and 'granadelauncher' in b.groups:
        sprites.shoot.sound(g)
        sprites.explosion.init(g, b.rect, b)
        b.active = False

    if got_hit and 'enemyshoot' in b.groups:
        b.active = False


def hit_breakable(g, a, b, top=1, right=1, bottom=1, left=1):
    hit_block(g, a, b, top, right, bottom, left)
    if 'shoot' in b.groups:
        tile_explode(g, a)


def hit_replace(g, a, b, r):
    hit_block(g, a, b, 1, 1, 1, 1)
    if 'shoot' in b.groups:
        tiles.t_put(g, a.pos, r)


def hit_fally(g, a, b, top=1, right=1, bottom=1, left=1):
    hit_block(g, a, b, top, right, bottom, left)

    # if 'player' not in b.groups: return
    if not hasattr(b, 'standing'): return
    if b.standing != a: return

    from lib import tile
    from lib import sprite
    tile.tile_to_sprite(g, a)

    s = a
    s.timer = FPS / 4
    s.image = s.image + 1
    s.hit = hit_block
    s.vy = 0

    def loop(g, s):
        a.timer -= 1
        if a.timer > 0: return
        if a.timer == 0: g.game.sfx['fally'].play()
        sprite.apply_gravity(g, s)
        s.rect.y += s.vy

    s.loop = loop


def fally_init(g, r, n, *params):
    x, y = r.centerx / TW, r.centery / TH
    tiles.t_put(g, (x, y), 0x12)


def hit_fire(g, a, b):
    if hasattr(b, 'damage'):
        if hasattr(b, 'kill'):
            b.kill(g, b, 1)
    # print 'you hit fire oh no!'
    pass


def hit_dmg(g, a, b, top=1, right=1, bottom=1, left=1):
    r, cur, prev = a.rect, b.rect, b.prev

    got_hit = False

    if top and prev.bottom <= r.top and cur.bottom > r.top:
        got_hit = True
        cur.bottom = r.top
        if hasattr(b, 'standing'): b.standing = a
    if right and prev.left >= r.right and cur.left < r.right:
        got_hit = True
        cur.left = r.right
    if bottom and prev.top >= r.bottom and cur.top < r.bottom:
        got_hit = True
        cur.top = r.bottom
        # if hasattr(b,'vy'): b.vy = 0
        if hasattr(b, 'standing') and b.standing != None:
            import sprite
            sprite.stop_standing(g, b)
    if left and prev.right <= r.left and cur.right > r.left:
        got_hit = True
        cur.right = r.left

    # if got_hit and 'shoot' in b.groups:
    #   b.active = False
    #
    # if got_hit and 'laser' in b.groups:
    #   b.active = False

    player.damage(g, b, a)


def hit_chip(g, a, b, n):
    if not tile_close(g, a, b): return

    g.game.sfx['coin'].play()
    if n == 1:
        g.game.chips[0] = True
    elif n == 2:
        g.game.chips[1] = True
    elif n == 3:
        g.game.chips[2] = True
    elif n == 4:
        g.game.chips[3] = True
    # print '1-coin'

    tile_explode(g, a)


def hit_life(g, a, b):
    if not tile_close(g, a, b): return

    one_up(g, b)

    # print '1-up'
    tile_explode(g, a)


def hit_def(g, a, b):
    if not tile_close(g, a, b): return

    g.game.sfx['coin'].play()

    # print '+ def'
    if g.game.strength < 9:
        g.game.strength += 2
    elif g.game.strength == 9:
        g.game.strength += 1

    tile_explode(g, a)


def one_up(g, b):
    g.game.lives += 1
    g.game.sfx['powerup'].play()


def hit_item(g, a, b, pts):
    if not tile_close(g, a, b): return

    g.game.sfx['item'].play()
    # print '+ %s',pts
    g.game.score += pts
    tile_explode(g, a)

    from lib import sprites
    sprites.points.init(g, a.rect, pts)


def hit_power(g, a, b, weapon):
    if not tile_close(g, a, b): return

    g.game.sfx['powerup'].play()
    # print '+ power'

    g.game.powerup = weapon

    if weapon == "shootgun":
        g.game.weapons[1] = weapon
    elif weapon == "cannon":
        g.game.weapons[2] = weapon
    elif weapon == "granadelauncher":
        g.game.weapons[3] = weapon
    elif weapon == "laser":
        g.game.weapons[4] = weapon

    player.powerup(g, b, weapon)
    tile_explode(g, a)

def hit_drone(g, a, b, drone):
    if not tile_close(g, a, b): return

    g.game.sfx['powerup'].play()
    # print '+ power'
    g.game.drone = drone

    if drone == "guardian":
        g.game.drones[0] = drone
    elif drone == "defender":
        g.game.drones[1] = drone
    elif drone == "killer":
        g.game.drones[2] = drone

    tile_explode(g, a)

def hit_jetpack(g, a, b, jetpack):
    if not tile_close(g, a, b): return

    g.game.sfx['powerup'].play()
    # print '+ power'
    g.game.jetpack = jetpack

    if jetpack == "double_jump":
        g.game.jetpacks[1] = jetpack
    elif jetpack == "fly":
        g.game.jetpacks[2] = jetpack

    tile_explode(g, a)

def tile_close(g, a, b):
    r1 = pygame.Rect(a.rect)
    r2 = pygame.Rect(b.rect)
    pad = 2
    r1.x += pad
    r1.y += pad
    r1.w -= pad * 2
    r1.h -= pad * 2
    return r1.colliderect(r2)


def tile_explode(g, a):
    g.game.sfx['explode'].play()
    tiles.t_put(g, a.pos, 0)
    from lib import tile
    tile.tile_to_sprite(g, a)
    s = a
    s.hit_groups = set()

    def loop(g, s):
        s.exploded += 2
        if s.exploded > 8:
            s.active = False
            # if s in g.sprites:
            # g.sprites.remove(s)

    s.loop = loop
