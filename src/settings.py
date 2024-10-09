import pygame as pg
import math
import random as rd
import pprint
from math import cos, sin, pi, atan2
from pprint import pp

from pygame import Vector2

# 2 popy.void

pg.init()

WIDTH, HEIGHT = (800,600)

WIN = pg.display.set_mode((WIDTH, HEIGHT))
FPS = 20
clock = pg.time.Clock()

FONT13 = pg.font.SysFont('helvetica', 13)
FONT15 = pg.font.SysFont('helvetica', 15)
FONT20 = pg.font.SysFont('helvetica', 20)
FONT30 = pg.font.SysFont('arial', 30)
FONT35 = pg.font.SysFont('arial', 35)

bg_color = '#142033'
# bg_color = '#101428'
graphic1 = '#7272A3'

yellow1 = '#CDCD20'
green1 = '#127040'
seagreen1 = '#106030'
darkgreen1 = '#005020'
lightgreen1 = '#289980'
cyan1 = '#2680aa'
darkblue1 = '#002342'
blue1 = '#005677'
blue2 = '#2070B5'
lightblue1 = '#4080CC'
purple1 = '#500077'
purple2 = '#c745d2'
red1 = '#AA1020'
orange1 = '#C06815'
orange2 = '#D1AA40'
darkgrey1 = '#272727'
grey1 = '#585858'
grey2 = '#989898'

r1 = 170
c1 = (300, 300)
vec0 = Vector2(0, 0)
poly1 = ((0, 0), (0, 0), (0, 0))
orbit_vel = 0.042

s3 = (80, 80)
s4 = (100, 120)
cap1 = 80


class Indic:
    def __init__(self, pos, size, val, SHOW=True):
        self.pos = pos
        self.max_size = size
        self.size = size
        self.col = graphic1
        self.val = val
        self.SHOW = SHOW

    def draw(self, win):
        x, y = self.pos
        w, h = self.size
        W, H = self.max_size
        if self.SHOW:
            pg.draw.rect(win, self.col, (x, y, w, h))
        pg.draw.rect(win, self.col, (x, y, W, h), 2)
        pg.draw.rect(win, self.col, (x + 1, y + 1, W - 2, h - 2), 1)

    def update(self, val):
        x, y = self.max_size

        self.val = val
        self.size = (x, y)


class Game:
    def __init__(self, win, player, elems=[]):
        self.win = win
        self.elems = elems
        self.player = player
        self.cursor = None

        self.a1 = 0
        self.timer = 150
        self.SHOW_TEAM = True
        self.TOGGLE_SPAWN = False
        self.TOGGLE_PLAYER_MOVE = False
        self.k1 = 0
        self.k2 = 0
        self.ELEM_LIMIT = 50
        self.logs = []

    def init_elems(self, elems, cursor=None):
        self.elems.clear()
        self.append(self.player)
        for elem in elems:
            if elem not in self.elems:
                self.append(elem)
        if cursor:
            self.cursor = cursor
        self.set_spell()

    def hide_elem(self, type=3):
        for elem in self.elems:
            if elem.type == type:
                elem.SHOW = False

    def pr(self):
        print(self.elems)

    def pr2(self, m=0, n=3):
        n = min(n, len(self.elems))
        t = pg.time.get_ticks() / 1000
        t = round(t, 2)
        end = " "
        for i, elem in enumerate(self.elems[m:n]):
            if i == n - 1:
                end = "_"
            if elem.type in [2]:
                print(f'[{t}]', 'game', 'i:', i, "-", elem, end)

    def log(self, log):
        logs = self.logs
        if (log not in logs) and len(logs) < 7 + self.a1 // 100:
            logs.append(log)
            pp([len(logs), logs])

    def draw(self, win):
        v = self.player.spell.val
        win.fill(bg_color)
        for elem in self.elems:
            if elem.SHOW:
                elem.draw(win)
                if self.SHOW_TEAM:
                    elem.draw_team(win)
                if elem.type == 5:
                    self.a1 += 1
        self.draw_info(win)
        self.cursor.draw(win)
        write_text(win, (self.a1, v, len(self.logs)), (550, 24), grey2)

    def draw_info(self, win):
        w1, h1 = (12, self.k1 / 4)
        x1, y1 = (WIDTH - 70, 150 - h1)
        w2, h2 = (12, self.k2 / 4)
        x2, y2 = (WIDTH - 45, 150 - h2)

        pg.draw.rect(win, blue2, (x1, y1, w1, h1), 0, 3)
        pg.draw.rect(win, red1, (x2, y2, w2, h2), 0, 3)

    def set_net(self, n=2):
        balls = self.player.set_net(n)
        self.elems += balls

    def set_orbit(self):
        player = self.player
        for nod in player.net2:
            nods = nod.set_orbit()
            self.elems += nods
        # self.hide_elem(3)

    def set_balls(self):
        player = self.player
        balls = player.set_balls()
        self.elems += balls

    def set_spell(self):
        player = self.player
        spell = player.set_spell()
        self.append(spell)

    def create_balls(self, n, team=2):
        if len(self.elems) < self.ELEM_LIMIT:
            width, height = pg.display.get_window_size()
            for i in range(n):
                x = rd.randint(40, width - 130)
                y = rd.randint(86, 525)
                size = (15, 15)
                col = blue2
                new_ball = Ball((x, y), size, col, type=4, team=team)
                self.append(new_ball)

    def check_collision(self):
        for e1 in self.elems:
            for e2 in self.elems:
                if (e1.team != e2.team) and (e1 is not e2) and e1.is_collided(e2):
                    e1.collide(e2)
                    if e2.timer == 0 and e2.type == 4:
                        self.k2 += 1
                    elif e2.timer != 0 and e2.type == 4:
                        self.k1 += 1
                    #self.log((e1, e2))

    def update(self):
        for elem in self.elems:
            elem.update(self.elems)
            if not elem.state:
                self.elems.remove(elem)
        self.timer += 1
        if self.timer > 300:
            self.pr2(1, 8)
            self.timer = 0

    def toggle_spawn(self, event, timer=10):
        self.TOGGLE_SPAWN = not self.TOGGLE_SPAWN
        if self.TOGGLE_SPAWN:
            pg.time.set_timer(event, timer)
        else:
            pg.time.set_timer(event, 0)

    def toggle_player_move(self):
        self.player.MOVE = not self.player.MOVE

    def append(self, new_elem):
        self.elems.append(new_elem)


class Unit:
    def __init__(self, pos, size, col, type=0, team=0):
        self.pos = Vector2(pos)
        self.size = size

        self.col = col
        if type in [2, 3]:
            self.lw = 1
        elif type in [5]:
            self.lw = 2
        else:
            self.lw = 0

        self.angle = 0
        self.vel = Vector2(0, 0)

        self.pair = []
        self.team = team

        self.timer = 20
        self.type = type
        self.state = 1
        self.SHOW = True
        self.update_rect()

    def __repr__(self):
        x, y = self.pos
        x, y = (round(x, 3), round(y, 3))
        return repr((self.state, self.type, (x, y)))

    def draw(self, win):
        x, y = self.pos
        w, h = self.size
        pg.draw.circle(win, self.col, (x, y), w / 2, self.lw)
        r1 = self.scale_rect(5)
        self.draw_hitbox(win)

    def draw_hitbox(self, win):
        if self.type in [4, 5]:
            pg.draw.rect(win, darkgreen1, self.rect, 1)
            #pg.draw.rect(win, darkgreen1, (x,y,40,40), 3)
            write_text(win, self.type, self.pos, grey2)

    def ten(self, win, n=10):
        x, y = self.pos
        w, h = self.pos
        for i in range(n):
            x2, y2 = randpoint(self.pos, (0,130))
            pg.draw.rect(win, grey1, (x2, y2, w, h), 1)

    def draw_team(self, win):
        x, y = self.pos
        w, h = self.size
        team_col = ['white', cyan1, red1]
        pg.draw.circle(win, team_col[self.team], (x, y), w / 2 + 3, 2)

    def move(self):
        self.pos += self.vel

    def is_collided(self, elem):
        pass

    def collide(self, elem):
        pass

    def update_rect(self):
        x1, y1 = self.pos
        w, h = self.size
        x2, y2 = (x1 - w / 2, y1 - h / 2)
        self.rect = pg.Rect(x2, y2, w, h)

    def update(self, elems=None):
        self.update_rect()
        if self.timer > 0:
            self.timer -= 1

    def scale_rect(self, scaling):
        x, y, w, h = self.rect
        w2, h2 = (w+4) * scaling, h * scaling
        return pg.Rect(x, y, w2, h2)


class Ball(Unit):
    def __init__(self, pos, size, col, type=1, team=0):
        super().__init__(pos, size, col, type, team)
        self.pair_dist = 0
        self.decel_factor = 0.98

    def draw(self, win):
        x, y = self.pos
        w, h = self.size
        pg.draw.circle(win, self.col, (x, y), w / 2, self.lw)
        self.draw_outline(win)
        self.draw_hitbox(win)

    def draw_outline(self, win):
        if self.pair:
            x, y = self.pos
            w, h = self.size
            d = self.pair_dist * 2
            r, g, b = (255 - d, 255 - d, 255 - d)
            r, g, b = (max(0, r), max(0, g), max(0, b))
            pg.draw.circle(win, (r, g, b), (x, y), w / 2 + 1, 1)

    def draw_outline(self, win):
        if self.timer:
            x, y = self.pos
            w, h = self.size
            pg.draw.circle(win, orange2, (x, y), w / 2 + 1, 1)

    def move(self):
        self.pos += self.vel

    def decelerate(self):
        self.vel *= 0.5

    def apply_force(self):
        A = self.pos
        for p in self.pair:
            B = p.pos
            m = p.mass
            angle = get_angle(A, B)
            d = get_dist(A, B)
            f = get_vec(angle) * min(15, max(0.0, d / 20)) * m
            self.vel += f

    def update(self, elems=None):
        if self.pair:
            self.pair_dist = get_dist(self.pos, self.pair[0].pos)
        self.apply_force()
        self.move()
        self.decelerate()
        self.update_rect()
        if self.timer > 0:
            self.timer -= 1


class Nod(Unit):
    STATE_1 = {'mass': 0, 'dist': 0}
    STATE_2 = {'mass': 0, 'dist': 0}
    def __init__(self, pos, size, col, center, center_dist=7, mass=1, angle=0, type=2, team=0):
        super().__init__(pos, size, col, type)
        self.mass = mass
        self.angle = angle
        self.vel = 0.00
        self.center = center
        self.center_dist = center_dist
        self.orbit = []
        self.set_spec()

        self.i = 0

    def count(self, i):
        self.i = i

    def set_spec(self):
        self.STATE_1['mass'] = self.mass
        self.STATE_1['dist'] = self.center_dist
        self.STATE_2['mass'] = 5 * self.mass
        self.STATE_2['dist'] = 2 * self.center_dist

    def draw(self, win):
        x, y = self.pos
        w, h = self.size
        if self.type in [2, 3]:
            pg.draw.circle(win, self.col, (x, y), w / 2, self.lw)

    def set_orbit(self):
        pos = self.pos
        size = self.size
        col = purple2
        n1 = Nod(pos, size, col, self, 10, 1, angle=0, type=3)
        self.orbit = [n1]
        self.state = "active"
        return self.orbit

    def move(self):
        self.angle += self.vel
        A = self.center.pos
        a = self.angle
        d = self.center_dist
        self.pos = get_point_from_angle(A, a, d)

    def update(self, elems=None):
        if self.type in [2, 3]:
            self.move()
        self.update_rect()
        self.timer -= 1
        if self.timer < 0:
            self.timer = 500
            print(111, self, self.center_dist)


class Spell(Unit):
    def __init__(self, home, pos, size, col, type=5, team=0):
        super().__init__(pos, size, col, type, team)
        self.home = home
        self.target = None
        self.val = 0
        self.max_size = (440, 440)
        self.min_size = (25, 25)

    def grow(self, scaling=1):
        w0, h0 = self.size
        incr = w0 * 0 + 2 - w0 / 400
        w0 += incr * scaling
        h0 += incr * scaling

        if self.size < self.max_size:
            self.size = (w0, h0)
        else:
            self.size = self.min_size

    def is_collided(self, elem):
        if self.rect.colliderect(elem.rect):
            return elem

    def collide(self, elem):
        SCALING_MAP = {0: 1, 1: 0.2}
        if elem.type in [6]:
            self.target = elem
            elem.state = 0
            elem.col = purple1
            scaling = SCALING_MAP[elem.timer > 0]
            self.grow(scaling)
            self.val += 1
        elif elem.type in [4]:
            self.pair_elem(elem)

    def pair_elem(self, elem):
        net2 = self.home.net2
        if self.home.free and elem.state != 2:
            elem.pair.clear()
            nod = self.home.randnod()
            if nod:
                elem.pair.append(nod)
                nod.pair.append(elem)
                print(101, net2)
                print(102, [elem.pair for elem in net2])
                net2.sort(key=lambda x: len(x.pair))
                self.home.free -= 1
                elem.state = 2
                elem.col = orange1


    def update(self, elems=None):
        self.pos = self.home.pos
        self.update_rect()


class Player(Unit):
    def __init__(self, pos, size, col, type=1, team=0):
        super().__init__(pos, size, col, type, team)
        self.net1 = []
        self.net2 = []
        self.free = 0
        self.pair = None
        self.scale = 1
        self.target = None

        self.mass_1 = 1
        self.mass_2 = 5

        self.spell = None
        self.MOVE = False
        self.timer = 50

    def move(self):
        self.pos += self.vel
        if not self.target:
            self.vel *= 0.90
        if get_dist(self.pos, (300, 300)) > 250:
            self.apply_forceA((300, 300))

    def apply_forceA(self, pos):
        A = self.pos
        B = pos
        d = get_dist(A, B)
        a = get_angle(A, B)
        f = get_vec(a) * min(3.5, max(2, d/100))
        self.vel += f

    def apply_force(self):
        if self.target:
            A = self.pos
            B = self.target.pos
            d = get_dist(A, B)
            a = get_angle(A, B)
            f = get_vec(a) * min(2, max(0.7, d/100))
            self.vel += f

    def check_target(self, elems):
        elems1 = {}
        elems2 = {}
        new_target = None
        if elems and (not self.target or self.target.state == 0):
            # elems1 = {elem: get_dist(elem.pos, self.pos) for elem in elems if get_dist(elem.pos, self.pos) < 400}
            for elem in elems:
                if elem.type == 4 and elem.state != 2:
                    dist = get_dist(elem.pos, self.pos)
                    if dist < 400:
                        elems1[elem] = dist
                    else:
                        elems2[elem] = dist
            if elems1:
                sorted1 = sort_dict(elems1)
                sorted1 = sorted(elems1, key=lambda x: elems1[x])
                new_target = sorted1[0]
            elif elems2:
                sorted2 = sort_dict(elems2)
                sorted2 = sorted(elems2, key=lambda x: elems2[x])
                new_target = sorted2[0]
        self.target = new_target

    def set_net(self, n=2):
        balls = []
        x0, y0 = self.pos
        for i in range(n):
            x1, y1 = randpoint(self.pos, (25, 80))
            angle = rd.randint(0,620) / 100
            dist = rd.randint(25, 80)
            b1 = Nod((x1, y1), (8, 8), grey1, self, dist, 1, angle, type=2)
            balls.append(b1)
            self.net2.append(b1)
        self.free = n
        return balls

    def set_balls(self, n=1):
        balls = []
        for nod in self.net2:
            if 1:
                pos = nod.pos
                size = (12, 12)
                col = blue2
                ball = Ball(pos, size, col, type=4)
                ball.pair.append(nod)
                balls.append(ball)
                self.net1.append(ball)
        return balls

    def set_pairs(self, b1, b2):
        b1.pair.clear()
        for nod in b2.orbit:
            b1.pair.append(nod)

    def set_spell(self):
        spell = Spell(self, self.pos, (90,90), red1, type=5, team=self.team)
        self.spell = spell
        return spell

    def increase_mass(self):
        for nod in self.net2:
            nod.mass = nod.STATE_2['mass']
            nod.center_dist = nod.STATE_2['dist']
            print(113, nod, nod.center_dist, nod.STATE_2)

    def decrease_mass(self):
        for nod in self.net2:
            nod.mass = nod.STATE_1['mass']
            nod.center_dist = nod.STATE_1['dist']

    def randnod(self):
        if self.net2:
            n = self.free
            nod = rd.choice(self.net2[:n])
            return nod

    def mouse_start_drag(self):
        self.increase_mass()

    def mouse_release(self):
        self.decrease_mass()

    def update_free(self):
        pass

    def update(self, elems=None):
        if self.MOVE:
            self.move()
            self.apply_force()
            self.check_target(elems)
        self.update_rect()
        self.timer -= 1
        if self.timer <= 0:
            print(109, self, self.vel)
            self.timer = 150


class Cursor:
    def __init__(self, start, size, col):
        self.start = Vector2(start)
        self.end = Vector2(start)
        self.size = size
        self.col = col

        self.vec = Vector2(0, 0)
        self.sel = None
        self.sel_start = Vector2(0, 0)
        self.state = 0
        self.update_rect()

    def draw(self, win):
        pg.draw.rect(win, self.col, self.rect)
        pg.draw.line(win, darkgreen1, self.start, self.end)

    def drag(self, pos):
        self.end = Vector2(pos)
        self.vec = self.end - self.start
        self.drag_sel()
        self.update_rect()

    def drag_sel(self):
        if self.sel:
            self.sel.pos = self.sel_start + self.vec

    def start_drag(self, pos):
        self.start = Vector2(pos)
        self.state = 1
        self.col = red1
        if self.sel and self.sel.type in [1]:
            self.sel.increase_mass()

    def release(self):
        self.state = 0
        self.start = self.end
        self.col = purple2
        if self.sel and self.sel.type in [1]:
            self.sel.decrease_mass()
        self.sel = None

    def toggle_drag(self, pos):
        self.state = not self.state
        if self.state:
            self.start_drag(pos)
        else:
            self.release()

    def check_sel(self, pos, elems):
        for elem in elems:
            if elem.rect.collidepoint(pos):
                self.sel = elem
                self.sel_start = elem.pos
                self.col = yellow1
                break

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def update_rect(self):
        x1, y1 = self.end
        w, h = self.size
        x2, y2 = (x1 - w / 2, y1 - h / 2)
        self.rect = pg.Rect(x2, y2, w, h)

    def update(self):
        pass


def update_all(elems):
    for elem in elems:
        elem.update()


def update_indics(indics, values):
    for indic, value in zip(indics, values):
        indic.update(value)


def append_elem(elem, elems):
    for e in elem:
        elems.append(e)


def set_net(player, elems):
    balls = player.set_net()
    append_elem(balls, elems)


def get_dist(A, B):
    x1, y1 = A
    x2, y2 = B
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def get_point_from_angle(pos, angle, rad):
    x, y = pos
    # x2, y2 = (cos(angle), sin(angle)) * rad + Vector2(pos)
    x2 = cos(angle) * rad + x
    y2 = sin(angle) * rad + y
    return (x2, y2)


def randpoint(pos, dist_range):
    min_dist, max_dist = dist_range
    angle = rd.randint(0, 620) / 100
    dist = rd.randint(min_dist, max_dist)
    return get_point_from_angle(pos, angle, dist)


def randpointS(dist_range):
    x = rd.randint(0, dist_range)
    y = rd.randint(0, dist_range)
    return (x, y)


def get_angle(A, B):
    x1, y1 = A
    x2, y2 = B
    return atan2((y2 - y1), (x2 - x1))


def get_vec(angle):
    return Vector2(cos(angle), sin(angle))


def sort_dict(dict_to_sort):
    sorted_list = sorted(dict_to_sort, key=lambda x: dict_to_sort[x])
    return {key: dict_to_sort[key] for key in sorted_list}


def write_text(screen, data, pos, col=grey1, font=FONT15, center=False):
    text_surf = font.render(str(data), 1, col)
    size = text_surf.get_size()
    if center:
        x, y = pos[0] - size[0] / 2, pos[1] - size[1] / 2
    else:
        x, y = pos
    screen.blit(text_surf, (x, y))


def linex(win, y, col=darkblue1, w=2):
    pg.draw.line(win, col, (0, y), (WIDTH, y), w)




