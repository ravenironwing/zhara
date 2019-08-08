import pygame as pg
import pytmx
from settings import *
from os import path

map = '0bE.tmx'
filename = (path.join(map_folder, map)

class Transform_tmx:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.new_map = self.make_map()

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))
    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height)).convert()
        self.render(temp_surface)
        return temp_surface