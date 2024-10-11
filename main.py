from src import *

import pygame as pg
from pygame.locals import *

# 2 popy.void

def fps_cursor(win, start=(0,0)):
    x0, y0 = start
    for i in [1, 15, 30, 45, 60]:
        x1, y1 = (WIDTH - 12 + x0, i * 10 + y0)
        w1, h1 = (12, 1)
        pg.draw.rect(win, grey1, (x1,y1,w1,h1))
        write_text(win, i, (x1-10, y1), blue1, center=True, font=FONT13)

def disp_values(win, values, col=grey1):
    for i, (name, value) in enumerate(values.items()):
        write_text(win, name, (25, i * 18 + 30), col, font=FONT13)
        write_text(win, value, (68, i * 18 + 30), col, font=FONT13)


def set_indic_values(values):
    values['balls'] = len(player.net2)
    values['a1'] = player.free
    values['fps'] = FPS
    values['elem'] = len(all_elem)
    if len(all_walls) >= 2:
        w1 = all_walls[-1]
        w2 = all_walls[-2]
        values['w1'] = len(w1.points)
        values['w2'] = len(w2.points)
    return values


def main(win):
    global FPS
    values = {'p1': 600, 'p2': 0, 'p3': 400, 'a1': 0, 'fps': 0}
    game = Game(WIN, player)
    game.init_elems(all_elem, cursor)
    print(game.elems)
    run_main = True

    while run_main:
        game.draw(win)
        disp_values(win, values, graphic1)
        fps_cursor(win)
        pos = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == QUIT:
                run_main = False
            elif event.type == KEYDOWN:
                keys = pg.key.get_pressed()
                if event.key in [K_ESCAPE, K_q]:
                    run_main = False
                elif keys[K_f]:
                    FPS = 6
                elif keys[K_a]:
                    game.set_net(80)
                    game.pr()
                    game.toggle_spawn(SPAWN, 300)
                elif keys[K_z]:
                    game.set_orbit()
                elif keys[K_e]:
                    game.set_balls()
                elif keys[K_h]:
                    game.hide_elem(3)
                elif keys[K_m]:
                    game.toggle_player_move()
                elif keys[K_s]:
                    game.SHOW_TEAM = not game.SHOW_TEAM
                elif keys[K_SPACE]:
                    cursor.check_sel(pos, game.elems)
                    cursor.start_drag(pos)

            elif event.type == SPAWN:
                game.create_balls(2)

            elif event.type == MOUSEBUTTONDOWN:
                cursor.check_sel(pos, game.elems)
                cursor.start_drag(pos)
                if pos[0] > WIDTH - 30:
                    FPS = pos[1] // 10

            elif event.type == MOUSEBUTTONUP:
                cursor.release()

            elif pg.mouse.get_pressed()[0]:
                pass

            if cursor.state:
                cursor.drag(pos)

        game.update(pos)
        game.check_collision()

        v = set_indic_values(values)
        values_to_set = [values['p1'], values['p2'], values['p3']]
        update_indics(indics, values_to_set)

        clock.tick(FPS)
        pg.display.update()
    pg.quit()


SPAWN = pg.USEREVENT

ind_a = Indic((60, 45 + 0 * 16), (100, 12), 600)
ind_b = Indic((60, 45 + 1 * 16), (100, 12), 600)
ind_c = Indic((WIDTH - 50, 40), (20, 20), 600, 0)

player = Player((300, 300), (35, 35), purple1, team=1)
cursor = Cursor((560, 560), (10, 10), purple1)
indics = [ind_c]

all_walls = []
all_elem = [player]

main(WIN)

