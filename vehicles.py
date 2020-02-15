from settings import *
from random import choice, randrange
from weapons import *
from character_positions import *
import pygame as pg

TANK_HIT_RECT = pg.Rect(0, 0, 250, 250)

BOATS = ['boat']
AMPHIBIOUS_VEHICLES = ['horse']
LAND_VEHICLES = ['tank']
FLYING_VEHICLES = ['airship']

VEHICLES = {}
VEHICLES['skiff'] = {'acceleration': 8, 'rot speed': 100, 'hit sound': 'knock', 'hit rect': XLARGE_HIT_RECT, 'image': 0, 'damage': 0, 'wcat': 'boat', 'weapons': 'oar', 'weapons2': 'oar', 'layer': MOB_LAYER, 'hp': 300, 'walk animation': ROW, 'rattack animation': SWIPE, 'lattack animation': L_SWIPE, 'mountable': False}
VEHICLES['tank'] = {'drive sound': 'tank', 'run sound': 'tank engine', 'acceleration': 8, 'rot speed': 50,'hit sound': 'metal hit', 'hit rect': TANK_HIT_RECT, 'image': 1, 'damage': 50, 'cat': 'tank', 'weapons': 'tank mini gun', 'weapons2': None, 'layer': VEHICLE_LAYER, 'hp': 4000, 'walk animation': TANK, 'rattack animation': TANK, 'lattack animation': TANK, 'mountable': False}
VEHICLES['airship'] = {'fuel':500, 'rot speed': 50, 'acceleration': 15,'hit sound': 'metal hit', 'hit rect': TANK_HIT_RECT, 'image': 2, 'damage': 0, 'cat': 'airship', 'weapons': 'ship cannon', 'weapons2': 'fire bombs', 'layer': SKY_LAYER, 'hp': 3000, 'walk animation': TANK, 'rattack animation': TANK, 'lattack animation': TANK, 'mountable': False}
