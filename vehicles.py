from settings import *
from random import choice, randrange
from weapons import *
from character_positions import *
import pygame as pg

TANK_HIT_RECT = pg.Rect(0, 0, 234, 234)

BOATS = ['boat']
AMPHIBIOUS_VEHICLES = ['horse']
LAND_VEHICLES = ['tank']
FLYING_VEHICLES = ['airship']

VEHICLES = {}
VEHICLES['skiff'] = {'location': [145, 44, 27, 38], 'acceleration': 8, 'hit sound': 'knock', 'hit rect': XLARGE_HIT_RECT, 'image': 0, 'cat': 'boat', 'weapons': 'oar', 'weapons2': 'oar', 'layer': MOB_LAYER, 'hp': 300, 'walk animation': ROW, 'rattack animation': SWIPE, 'lattack animation': L_SWIPE, 'mountable': False}
VEHICLES['tank'] = {'location': [64, 17, 59, 53], 'acceleration': 8,'hit sound': 'metal hit', 'hit rect': TANK_HIT_RECT, 'image': 1, 'cat': 'tank', 'weapons': 'tank mini gun', 'weapons2': None, 'layer': BULLET_LAYER, 'hp': 4000, 'walk animation': TANK, 'rattack animation': TANK, 'lattack animation': TANK, 'mountable': False}
VEHICLES['airship'] = {'location': [85, 96, 17, 53], 'fuel':500, 'acceleration': 15,'hit sound': 'metal hit', 'hit rect': TANK_HIT_RECT, 'image': 2, 'cat': 'airship', 'weapons': 'ship cannon', 'weapons2': 'fire bombs', 'layer': SKY_LAYER, 'hp': 3000, 'walk animation': TANK, 'rattack animation': TANK, 'lattack animation': TANK, 'mountable': False}
