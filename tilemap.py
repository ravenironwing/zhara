import pygame as pg
import pytmx
from settings import *
from os import path
import pyscroll
import copy
import logging
logger = logging.getLogger('orthographic')
logger.setLevel(logging.ERROR)

class TiledMap:
    def __init__(self, game, filename):
        self.game = game
        self.filename = filename
        tm = pytmx.load_pygame(filename)
        ov = pytmx.load_pygame(filename)
        self.width = tm.width * tm.tilewidth
        self.tile_size = tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        #self.overlay_data = ov
        #self.image = self.make_map()
        #self.rect = self.image.get_rect()
        #self.rect.center = self.game.player.rect.center
        #self.overlay = MapOverlay(tm)
        map_data = pyscroll.data.TiledMapData(self.tmxdata)
        self.map_layer = pyscroll.BufferedRenderer(map_data, (self.game.screen_width, self.game.screen_height), clamp_camera=True)
        #self.overlay = self.generate_over_layer()
        self.minimap = MiniMap(tm)

    def toggle_visible_layers(self):
        if self.game.player_inside:
            for layer in self.tmxdata.visible_layers:
                if ('roof' in layer.name or 'tree' in layer.name):
                    if isinstance(layer, pytmx.TiledTileLayer):
                        layer.visible = False
        else:
            for layer in self.tmxdata:
                if ('roof' in layer.name or 'tree' in layer.name):
                    if isinstance(layer, pytmx.TiledTileLayer):
                        layer.visible = True
        self.map_layer.redraw_tiles(self.map_layer._buffer)

    #def generate_under_layer(self):
    #    for layer in self.tmxdata.visible_layers:
    #        if isinstance(layer, pytmx.TiledTileLayer):
    #            if ('roof' in layer.name or 'tree' in layer.name or 'high shadow' in layer.name):
    #                layer.visible = False
    #            else:
    #                layer.visible = True
    #    map_data = pyscroll.data.TiledMapData(self.tmxdata)
    #    return pyscroll.BufferedRenderer(map_data, (self.game.screen_width, self.game.screen_height), clamp_camera=True, tall_sprites=1)

    #def generate_over_layer(self):
    #    for layer in self.overlay_data.visible_layers:
    #        if isinstance(layer, pytmx.TiledTileLayer):
    #            if ('roof' in layer.name or 'tree' in layer.name or 'high shadow' in layer.name):
    #                layer.visible = True
    #            else:
    #                layer.visible = False
    #    map_data = pyscroll.data.TiledMapData(self.overlay_data)
    #    return pyscroll.BufferedRenderer(map_data, (self.game.screen_width, self.game.screen_height), clamp_camera=True, alpha=True, tall_sprites=1)

    #def render(self, surface):
    #    ti = self.tmxdata.get_tile_image_by_gid
    #    for layer in self.tmxdata.visible_layers:
    #        if not ('roof' in layer.name or 'tree' in layer.name or 'high shadow' in layer.name):
    #            if isinstance(layer, pytmx.TiledTileLayer):
    #                for x, y, gid, in layer:
    #                    tile = ti(gid)
    #                    if tile:
    #                        surface.blit(tile, (x * self.tmxdata.tilewidth,
    #                                            y * self.tmxdata.tileheight))

    #def test_render(self, surface):
    #    ti = self.tmxdata.get_tile_image_by_gid
    #    blank_surface = pg.Surface((self.tile_size, self.tile_size)).convert()
    #    playerx = int(self.game.player.pos.x / self.tile_size)
    #    playery = int(self.game.player.pos.y / self.tile_size)
    #    for layernum, layer in enumerate(self.tmxdata.visible_layers):
    #        if isinstance(layer, pytmx.TiledTileLayer):
    #            for j, y in enumerate(range(playery - 5, playery + 5)):
    #                for i, x in enumerate(range(playerx - 8, playerx + 8)):
    #                    try:
    #                        tile_img = self.tmxdata.get_tile_image(x, y, layernum)
    #                        if tile_img != None:
    #                            surface.blit(tile_img, (i * self.tmxdata.tilewidth, j * self.tmxdata.tileheight))
    #                    except:
    #                        surface.blit(blank_surface, (i * self.tmxdata.tilewidth, j * self.tmxdata.tileheight))

    #def update(self):
    #    self.image = self.make_map()
    #    self.rect = self.image.get_rect()
    #    self.rect.center = self.game.player.rect.center

    #def make_map(self):
    #    #temp_surface = pg.Surface((self.width, self.height)).convert()
    #    temp_surface = pg.Surface((self.tile_size * 16, self.tile_size * 10)).convert()
    #    self.render(temp_surface)
    #    return temp_surface

    # This section creates the map image that is drawn over the player: for roofs and trees.

"""
class MapOverlay:
    def __init__(self, tm):
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.image = self.make_map()
        self.rect = self.image.get_rect()
    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if 'roof' in layer.name or 'tree' in layer.name  or 'high shadow' in layer.name:
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, gid, in layer:
                        tile = ti(gid)
                        if tile:
                            surface.blit(tile, (x * self.tmxdata.tilewidth,
                                                y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height), pg.SRCALPHA).convert_alpha()  # SRCALPHA does per pixel transparency and allows the transparency of this layer to show through on the bellow layers.
        self.render(temp_surface)
        return temp_surface
"""

class MiniMap:
    def __init__(self, tm):
        #self.width = tm.width * tm.tilewidth
        #self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.size = 256
        self.tile_size = int(self.size / tm.width)
        self.image = self.make_map()
        self.rect = self.image.get_rect()

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        small_tile = pg.transform.scale(tile, (self.tile_size, self.tile_size))
                        surface.blit(small_tile, (x * self.tile_size,
                                            y * self.tile_size))
        mini_surface = surface
        return mini_surface

    def make_map(self):
        temp_surface = pg.Surface((self.size, self.size)).convert()
        temp_surface = self.render(temp_surface)
        return temp_surface

    def resize(self, enlarge = True):
        if enlarge:
            self.size += 128
            if self.size > HEIGHT:
                self.size = 128
        else:
            self.size -= 128
            if self.size < 128:
                self.size = 128

        self.tile_size = int(self.size / 64)
        self.image = self.make_map()
        self.rect = self.image.get_rect()


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target): #Centers camera on player. target = player
        self.x = -target.rect.centerx + int(WIDTH / 2)
        self.y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        self.x = min(0, self.x)  # left
        self.y = min(0, self.y)  # top
        self.x = max(-(self.width - WIDTH), self.x)  # right
        self.y = max(-(self.height - HEIGHT), self.y)  # bottom

        self.camera = pg.Rect(self.x, self.y, self.width, self.height)