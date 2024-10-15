from src.settings import Button

import pygame as pg


gold1 = '#D0A040'
yellow1 = '#CDCD20'
green1 = '#127040'
seagreen1 = '#106030'
darkgreen1 = '#005020'
lightgreen1 = '#147B65'
cyan1 = '#268092'
darkblue1 = '#002342'
blue1 = '#005677'
blue2 = '#2070B5'
lightblue1 = '#4080CC'
purple1 = '#600880'
purple2 = '#6620BB'
red1 = '#AA1020'
red2 = '#C02030'
orange1 = '#BB5010'
orange2 = '#C07124'
brown1 = '#602010'
darkgrey1 = '#272727'
grey1 = '#585858'
grey2 = '#989898'


BUTTON_SHOW_VEC = Button((300, 70), (50, 50), blue1)
BUTTON_SHOW = Button((360, 70), (50, 50), blue1)
BUTTON_START = Button((420, 70), (50, 50), blue1)

buttons = [BUTTON_SHOW_VEC, BUTTON_SHOW, BUTTON_START]

def set_buttons(game, buttons):
    BUTTON_SHOW_VEC.action = game.hide_vec
    BUTTON_SHOW.action = game.toggle_show
    BUTTON_START.action = game.start_spawn

    game.buttons = buttons


def check_click(elems, pos):
    for elem in elems:
        return elem.is_clicked(pos)











