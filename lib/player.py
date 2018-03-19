import pygame

from lib.cnst import *

from lib.sprite import myinc
from lib.sprite import Sprite3
from lib.sprite import init_bounds
from lib.sprite import init_codes
from lib.sprite import init_view
from lib.sprite import stop_standing
from lib.sprite import get_code
from lib.sprite import apply_gravity
from lib.sprite import apply_standing

from lib.tiles import t_put

from lib import shoot
from lib import drone
from lib import shield


def init(g, r, n, *params):
    s = Sprite3(g, r, 'player/right', (5, 2, 9, 28))  # left,top,width,height
    s.rect.bottom = r.bottom
    s.rect.centerx = r.centerx
    s.groups.add('player')
    s.groups.add('solid')
    g.sprites.append(s)
    s.loop = loop
    s.vx = 0
    s.vy = 0
    s.walk_frame = 1
    s.jumping = 0
    s.double_jumping = 0
    s.facing = 'right'
    s.flash_counter = 0
    s.flash_timer = 0
    s.shooting = 0
    s.powered_up = ''
    if hasattr(g.game, 'powerup'):
        s.powered_up = g.game.powerup
    s.powerup_transition = 0
    s.door_timer = None
    s.current_door = None
    s.door_pos = None
    g.player = s
    s.event = event
    s.pan = pan_screen
    s.damage = damage
    s.damaged_transition = 0
    s.kill = kill
    s.god_mode = False
    s.death_counter = -1
    s.canshoot = True
    s.got_hit = 0
    s.jump_timer = 0
    s.keep_jump = False

    s.jetpack = "jump"

    s.drone = None
    s.drone_sprite = None

    s.shield = False
    s.shield_sprite = None
    s.shield_countdown = 5*30
    s.shield_counter = 0

    s._prev = pygame.Rect(s.rect)
    s._prev2 = pygame.Rect(s.rect)
    s.looking = False

    init_bounds(g, s)
    init_view(g, s)
    init_codes(g, s)
    s.no_explode = False

    s.view_counter = 0

    s.speed = 1

    if hasattr(g.game, 'strength'):
        s.strength = g.game.strength

    return s

def event(g, s, e):
    # print 'player.event',e

    enemy_sprites = g.sprites[:]

    if s.door_timer is not None or s.exploded > 0:
        return

    if s.death_counter >= 0:
        return

    if s.jetpack == "double_jump":
        if e.type is USEREVENT and e.action == 'jump' and s.standing is not None and s.jumping == 0 and s.vy == 0:
            stop_standing(g, s)

            s.double_jumping = 1

            s.jumping = 1.18

            g.game.sfx['jump'].play()
        elif e.type is USEREVENT and e.action == 'jump' and s.double_jumping == 1:
            stop_standing(g, s)

            s.double_jumping = 0

            if s.vy > 0:
                #print("Down timer = %d" % s.jump_timer)
                if s.jump_timer >= 8:
                    s.jumping = 1.20
                elif 8 > s.jump_timer >= 2:
                    s.jumping = 1.25
                elif s.jump_timer < 2:
                    s.jumping = 1.60
            else:
                #print("UP timer = %d" % s.jump_timer)
                s.jumping = 0.60

            g.game.sfx['jump'].play()

    elif s.jetpack == "fly":
        if e.type is USEREVENT and e.action == 'jump':
            stop_standing(g, s)

            # s.vy = 0
            s.jumping = 0.4
            g.game.sfx['jump'].play()

    else:
        if e.type is USEREVENT and e.action == 'jump' and s.standing is not None and s.jumping == 0 and s.vy == 0:
            stop_standing(g, s)

            # s.vy = 0
            s.jumping = 1.21
            g.game.sfx['jump'].play()

    if e.type is USEREVENT and e.action == 'stop-jump':
        s.jumping = 0

    if e.type is USEREVENT and (e.action == 'up' or e.action == 'down'):
        if get_code(g, s, 0, 0) in DOOR_CODES:
            s.vx = 0
            s.vy = 0
            s.door_timer = DOOR_DELAY
            if s.current_door is not None:  # It should never be None actually...
                # print "door!"
                s.current_door.open = DOOR_DELAY
            s.image = None
            s.door_pos = s.rect.centerx / TW, s.rect.centery / TH
            # tiles.t_put(g,(x,y), 0x32)
            # tiles.t_put(g,(x,y-1), 0x22)

    if e.type is USEREVENT and e.action == 'shoot':
        enemy_objective = None
        for enemy in enemy_sprites:
            if "enemy" in enemy.groups:
                enemy_objective = enemy
        if s.canshoot:
            if s.powered_up == 'granadelauncher':
                s.shoot = shoot.init(g, s.rect, s, s.powered_up, enemy_objective, granade=1)
                s.shoot = shoot.init(g, s.rect, s, s.powered_up, enemy_objective, granade=2)
                s.shoot = shoot.init(g, s.rect, s, s.powered_up, enemy_objective, granade=3)
            else:
                s.shoot = shoot.init(g, s.rect, s, s.powered_up, enemy_objective)
            s.shooting = 10
            s.canshoot = False
    """
    if e.type is USEREVENT and e.action == 'stop-shoot':
        if s.powered_up == "granadelauncher" and s.shoot.active is True:
            explosion.init(g, s.shoot.rect, s.shoot)
            s.shoot.active = False
    """

    if e.type is KEYDOWN and e.key == K_F10:

        g.game.chips = [True, True, True, True]

        g.game.powerup = "laser"

        g.game.weapons[0] = 'gun'
        g.game.weapons[1] = 'shootgun'
        g.game.weapons[2] = 'cannon'
        g.game.weapons[3] = 'granadelauncher'
        g.game.weapons[4] = 'laser'

        g.game.drone = "killer"

        g.game.drones[0] = "guardian"
        g.game.drones[1] = "defender"
        g.game.drones[2] = "killer"

        g.game.jetpack = "fly"

        g.game.jetpacks[0] = "jump"
        g.game.jetpacks[1] = "double_jump"
        g.game.jetpacks[2] = "fly"

        s.god_mode = True


def loop(g, s):
    s._prev2 = pygame.Rect(s.rect)

    if s.powered_up == 'cannon':
        s.weapon = 'cannon'
    elif s.powered_up == 'shootgun':
        s.weapon = 'shootgun'
    elif s.powered_up == 'laser':
        s.weapon = 'laser'
    elif s.powered_up == 'granadelauncher':
        s.weapon = 'granadelauncher'
    else:
        s.weapon = 'player'

    inpt = g.game.input

    if s.vy < 0:
        s.image = s.jetpack + "/" + s.weapon + '/%s-jump' % s.facing
    elif s.shooting > 0:
        if s.shooting > 5:
            s.image = s.jetpack + "/" + s.weapon + '/%s-shoot-1' % s.facing
        else:
            s.image = s.jetpack + "/" + s.weapon + '/%s-shoot-2' % s.facing
        s.shooting -= 1
    elif inpt.right or inpt.left and s.standing:
        s.image = s.jetpack + "/" + s.weapon + '/%s-walk-%s' % (s.facing, int(s.walk_frame))
        s.walk_frame += 0.2
        if s.walk_frame > 4:
            s.walk_frame = 1
    else:
        s.image = s.jetpack + "/" + s.weapon + '/%s' % s.facing
    if s.vx > 0:
        s.facing = 'right'
    elif s.vx < 0:
        s.facing = 'left'

    if s.image is not None:
        if s.damaged_transition > 0:
            if (s.damaged_transition % 10) > 5:
                s.image = None
            else:
                if s.vy < 0:
                    s.image = s.jetpack + "/" + s.weapon + '/%s-jump' % s.facing

                elif inpt.right or inpt.left and s.standing:
                    s.image = s.jetpack + "/" + s.weapon + '/%s-walk-%s' % (s.facing, int(s.walk_frame))
                else:
                    s.image = s.jetpack + "/" + s.weapon + '/%s' % (s.facing)

            s.damaged_transition -= 1
        """
        elif s.powerup_transition > 0:
            if (s.powerup_transition % 10) > 5:
                s.image = s.image
            s.powerup_transition -= 1
        elif s.powered_up == '':
            s.image = s.image
            """

    if s.got_hit:
        if s.facing == "right":
            s.rect.x -= 2
        else:
            s.rect.x += 2
        s.got_hit -= 1

    if s.death_counter > 0:
        s.groups = set()
        if not s.no_explode:
            s.exploded += 1
            if s.exploded > FPS / 2:
                s.image = None
        else:
            s.image = None
        s.death_counter -= 1
        return
    if s.death_counter == 0:
        g.status = 'dead'
        return

    if s.exploded > 0:
        s.exploded -= 1
        return

    apply_gravity(g, s)
    apply_standing(g, s)

    if s.door_timer is not None:
        if s.door_timer == 0:
            x, y = s.door_pos  # s.rect.centerx/TW,s.rect.centery/TH
            from lib import door
            # door.hit(g,g.layer[y][x],s)
            door.hit(g, (x, y), s)
            # tiles.t_put(g,(x,y), 0x30)
            # tiles.t_put(g,(x,y-1), 0x20)
            s.door_timer = None
        else:
            s.door_timer -= 1
            return

    # if s.standing: s.rect.bottom = s.standing.rect.top

    # check if we hit the ceiling
    if not s.jumping and s.vy < 0 and s.rect.y == s._prev.y:
        s.vy = 0

    # We have universal input code now (>__>)
    # move by keyboard
    # keys = pygame.key.get_pressed()

    if s.jumping:
        # print s.vy
        s.vy -= s.jumping

        if s.vy < -4:
            s.vy = -4

        if s.jetpack == "double_jump":
            s.jump_timer += 5
            s.jumping = max(0, s.jumping - 0.2)

        elif s.jetpack == 'fly':
            s.jumping = max(0, s.jumping)

        else:
            s.jump_timer += 4
            s.jumping = max(0, s.jumping - 0.2)

    if s.jump_timer and not s.jumping:
        s.jump_timer -= 1
        x_speed = 1.0
    else:
        x_speed = 1.0

    if g.frame % s.speed == 0:
        if inpt.right:
            s.vx = x_speed
            s.fancing = 'right'
        elif not inpt.right and s.vx > 0:
            s.vx = 0
        if inpt.left:
            s.vx = -x_speed
            s.facing = 'left'
        elif not inpt.left and s.vx < 0:
            s.vx = 0

        s._prev = pygame.Rect(s.rect)

        vx, vy = s.vx, s.vy
        s.rect.x += vx
        s.rect.y += myinc(g.frame, s.vy)


    # if keys[K_UP]: vy -= 1
    # if keys[K_DOWN]: vy += 1

    if s.flash_counter > 0:
        if s.flash_timer < 4:
            s.image = None
        if s.flash_timer == 0:
            s.flash_timer = 8
            s.flash_counter -= 1
        s.flash_timer -= 1

    s.looking = False

    if inpt.up:
        s.view_counter += 1
        if s.view_counter >= 60:
            g.view.y -= 2
            s.looking = True

    elif inpt.down:
        s.view_counter += 1
        if s.view_counter >= 60:
            g.view.y += 2
            s.looking = True
    else:
        s.view_counter = 0

    n = get_code(g, s, 0, 0)
    if n == CODE_EXIT and (g.game.chips[0] and g.game.chips[1] and g.game.chips[2] and g.game.chips[3]):
        g.status = 'exit'
    if n == CODE_DOOR_AUTO:
        x, y = s.rect.centerx / TW, s.rect.centery / TH
        from lib import door
        door.hit(g, (x, y), s)

    # pan_screen(g,s)

    # if (g.frame%FPS)==0: print 'player vy:',s.vy

    if hasattr(g, 'boss'):
        # print g.boss.phase, g.boss.phase_frames
        if g.boss.phase == 2 and g.boss.phase_frames == 60:
            for y in range(len(g.layer)):
                for x in range(len(g.layer[y])):
                    if g.data[2][y][x] == CODE_BOSS_PHASE2_BLOCK:
                        t_put(g, (x, y), 0x01)  # solid tile
        if g.boss.dead:
            g.status = 'exit'
            # pygame.mixer.music.load("
            # g.game.music.play('finish',1)

    if hasattr(s, "shoot"):
        s.shoot.cooldown -= 1
        if s.shoot.cooldown == 0:
            s.canshoot = True

    if g.game.drone is not None and s.drone != g.game.drone:
        s.drone = g.game.drone

        if hasattr(s.drone_sprite, "active"):
            s.drone_sprite.active = False
        s.drone_sprite = drone.init(g, s.rect, s, s.drone)

        if s.drone == "defender" and s.shield is False:
            s.shield_sprite = shield.init(g, s.rect, s)
            s.shield = True

    if s.drone != "defender" and s.shield is True:
        s.shield_sprite.active = False
        s.shield = False

    if s.shield is False and s.shield_counter:
        if s.shield_counter > 1:
            s.shield_counter -= 1
        else:
            s.shield_counter = 0
            if s.drone == "defender" and s.shield is False:
                s.shield_sprite = shield.init(g, s.rect, s)
                s.shield = True

    s.jetpack = g.game.jetpack
    s.strength = g.game.strength
    s.powered_up = g.game.powerup


def pan_screen(g, s):
    # adjust the view
    border = pygame.Rect(s.rect)
    # pad = 100
    pad = (SW / 2) - TW
    border.x -= pad
    border.w += pad * 2
    # pad = 80
    pad = (SH / 2) - TH
    if s.looking:
        pad = TH * 2
    border.y -= pad
    border.h += pad * 2

    dest = pygame.Rect(g.view)
    dest.top = min(dest.top, border.top)
    dest.right = max(dest.right, border.right)
    dest.bottom = max(dest.bottom, border.bottom)
    dest.left = min(dest.left, border.left)

    dx, dy = dest.x - g.view.x, dest.y - g.view.y
    # mx,my = 6,6
    mx = max(2, abs(s._prev2.x - s.rect.x))
    my = max(2, abs(s._prev2.y - s.rect.y))
    if abs(dx) > mx: dx = sign(dx) * mx
    if abs(dy) > my: dy = sign(dy) * my
    g.view.x += dx
    g.view.y += dy


def powerup(g, s, weapon):
    s.powered_up = weapon


def damage(g, s, a):
    if s.god_mode:
        return

    if s.door_timer is not None:
        return

    if s.shield is True:
        s.shield = False
        s.shield_sprite.active = False
        g.game.sfx['hit'].play()
        s.damaged_transition = 100
        s.shield_counter = s.shield_countdown
        return

    if s.damaged_transition == 0 and s.strength > 0:

        s.got_hit = 12

        g.game.sfx['hit'].play()
        s.damaged_transition = 100

        s.strength -= 1
        if hasattr(g.game, 'strength'):
            g.game.strength -= a.damage

    elif s.flash_counter == 0 and s.strength <= 0:
        s.kill(g, s)


def kill(g, s, no_explode=False):

    if hasattr(g.game, 'powerup'):
        g.game.powerup = 'gun'

    s.flash_counter = 10
    s.no_explode = no_explode
    g.game.music_play('death', 1)
    s.death_counter = int(FPS * 2.25)
