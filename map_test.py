from tilemap import *
import pygame as pg
from settings import *

screen = pg.display.set_mode((WIDTH, HEIGHT))
map = '21.tmx'
temp_map = TiledMap(path.join(map_folder, map))
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()
            running = False
        if event.type == pg.KEYDOWN:
            running = False