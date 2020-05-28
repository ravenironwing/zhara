# The Legend of Sky Realm by Raven Dewey (aka Ravenwing)

import tracemalloc
import gc
import pygame as pg
import sys
import pickle
import pygame.surfarray as surfarray
from random import choice, random, choices
from os import path, makedirs
from settings import *
from npcs import *
from quests import *
from menu import *
from sprites import *
from tilemap import *
import datetime
from time import sleep, perf_counter
import math


from pygame.locals import *
from pytmx.util_pygame import load_pygame
import pyscroll
import pyscroll.data
from pyscroll.group import PyscrollGroup

tracemalloc.start()

#npc_q = Queue()

def group_draw(self, surface, game = None): # This is a modded version of the pyscroll group draw function that only draws sprites that are on screen (otherwise it's super slow).
    """ Draw all sprites and map onto the surface
    :param surface: pygame surface to draw to
    :type surface: pygame.surface.Surface
    """
    ox, oy = self._map_layer.get_center_offset()

    new_surfaces = list()
    spritedict = self.spritedict
    gl = self.get_layer_of_sprite
    new_surfaces_append = new_surfaces.append

    if game == None: #Used if there is not game running yet... kind of useless, but makes it not error out.
        for spr in self.sprites():
            new_rect = spr.rect.move(ox, oy)
            try:
                new_surfaces_append((spr.image, new_rect, gl(spr), spr.blendmode))
            except AttributeError:  # generally should only fail when no blendmode available
                new_surfaces_append((spr.image, new_rect, gl(spr)))
            spritedict[spr] = new_rect

    else:
        for spr in self.sprites(): # This modded version only adds the sprite images that are on screen using the game.camera and the on_screen method
            if game.on_screen_no_edge(spr):
                new_rect = spr.rect.move(ox, oy)
                try:
                    new_surfaces_append((spr.image, new_rect, gl(spr), spr.blendmode))
                except AttributeError:  # generally should only fail when no blendmode available
                    new_surfaces_append((spr.image, new_rect, gl(spr)))
                spritedict[spr] = new_rect
        #hits = pg.sprite.spritecollide(game.camera, self.sprites(), False)
        #for spr in hits: # This modded version only adds the sprite images that are on screen by using only the sprites that collide with the camera object.
        #    new_rect = spr.rect.move(ox, oy)
        #    try:
        #        new_surfaces_append((spr.image, new_rect, gl(spr), spr.blendmode))
        #    except AttributeError:  # generally should only fail when no blendmode available
        #        new_surfaces_append((spr.image, new_rect, gl(spr)))
        #    spritedict[spr] = new_rect

    self.lostsprites = []
    return self._map_layer.draw(surface, surface.get_rect(), new_surfaces)

PyscrollGroup.draw = group_draw # Replaces the default PyscrollGroup.draw method

def trace_mem():
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')

    print("[ Top 10 ]")
    for stat in top_stats[:10]:
        print(stat)

# HUD functions
def draw_player_stats(surf, x, y, pct, color = GREEN, bar_length = 100):
    if pct < 0:
        pct = 0
    bar_height = 20
    fill = pct * bar_length
    outline_rect = pg.Rect(x, y, bar_length, bar_height)
    fill_rect = pg.Rect(x, y, fill, bar_height)
    if pct > 0.6:
        col = color
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

# Used for loading sprite sheet images into a list of images

def load_spritesheet(sheet, size):
    image_list = []
    sheet_width = sheet.get_width()
    sheet_height = sheet.get_height()
    columns = int(sheet_width / size)
    rows = int(sheet_height / size)
    # Create a new blank image

    for col in range(0, columns):
        y = col * size
        for row in range(0, rows):
            x = row * size
            image = pg.Surface([size, size], pg.SRCALPHA).convert_alpha()
            # Copy the sprite from the large sheet onto the smaller image
            image.blit(sheet, (0, 0), (x, y, size, size))
            image_list.append(image)
    # Return the separate images stored in a list.
    return image_list

# Used to see if the player is in talking range of an Npc
def npc_talk_rect(one, two):
    if one.hit_rect.colliderect(two.talk_rect):
        return True
    else:
        return False

def mob_hit_rect(one, two):
    if one.hit_rect.colliderect(two.hit_rect):
        return True
    else:
        return False

# Used to define hits from melee attacks
def melee_hit_rect(one, two):
    if one.mid_weapon_melee_rect.colliderect(two.hit_rect) or one.weapon_melee_rect.colliderect(two.hit_rect) or one.melee_rect.colliderect(two.hit_rect): #checks for either the fist hitting a mob or the cente or tip of weapon.
        if one.mother.weapon_hand == 'weapons':
            if one.swing_weapon1: # This differentiates between weapons that are being swung and those that are thrusted.
                if one.frame > 3:
                    return True
            else:
                if one.frame < 3:
                    return True
        else:
            return False
    elif one.mid_weapon2_melee_rect.colliderect(two.hit_rect) or one.weapon2_melee_rect.colliderect(two.hit_rect) or one.melee2_rect.colliderect(two.hit_rect): #checks for either the fist hitting a mob or the cente or tip of weapon.
        if one.mother.weapon_hand == 'weapons2':
            if one.swing_weapon2:
                if one.frame > 3:
                    return True
            else:
                if one.frame < 3:
                    return True
        else:
            return False
    else:
        return False

def breakable_melee_hit_rect(one, two):
    if one.mid_weapon_melee_rect.colliderect(two.trunk.hit_rect) or one.weapon_melee_rect.colliderect(two.trunk.hit_rect) or one.melee_rect.colliderect(two.trunk.hit_rect):
        if one.mother.weapon_hand == 'weapons':
            if one.swing_weapon1: # This differentiates between weapons that are being swung and those that are thrusted.
                if one.frame > 3:
                    return True
            else:
                if one.frame < 6:
                    return True
        else:
            return False

    elif one.mid_weapon2_melee_rect.colliderect(two.trunk.hit_rect) or one.weapon2_melee_rect.colliderect(two.trunk.hit_rect) or one.melee2_rect.colliderect(two.trunk.hit_rect):
        if one.mother.weapon_hand == 'weapons2':
            if one.swing_weapon2:
                if one.frame > 3:
                    return True
            else:
                if one.frame < 6:
                    return True
        else:
            return False
    else:
        return False

# Used to define fireball hits
def fire_collide(one, two):
    if one.hit_rect.colliderect(two.hit_rect):
        return True
    else:
        return False

def entryway_collide(one, two):
    if one.rect.colliderect(two.hit_rect):
        return True
    else:
        return False

class Game:
    def __init__(self):
        self.window_ratio = .97
        self.screen_width = WIDTH
        self.screen_height = int(HEIGHT * self.window_ratio)
        self.flags = pg.NOFRAME
        #self.screen = pg.display.set_mode((self.screen_width, HEIGHT), pg.FULLSCREEN)
        icon_image = pg.image.load(path.join(img_folder, ICON_IMG))
        pg.display.set_icon(icon_image)
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height), self.flags)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.dt = 0.0001
        # Loads Mutant Python Logo Faid in/out.
        mpy_logo_image = pg.image.load(path.join(img_folder, LOGO_IMAGE)).convert_alpha()
        mpy_logo_image = pg.transform.scale(mpy_logo_image, (int(self.screen_height/4), int(self.screen_height/4)))
        logo_width = mpy_logo_image.get_width()
        logo_placement = ((self.screen_width - logo_width)/2, (self.screen_height - logo_width)/2)
        mpy_words_image = pg.image.load(path.join(img_folder, MPY_WORDS)).convert_alpha()
        mpy_words_image = pg.transform.scale(mpy_words_image, (int(self.screen_width/4), int(self.screen_height/8)))
        words_height = mpy_words_image.get_height()
        words_width = mpy_words_image.get_width()
        words_placement = ((self.screen_width - words_width)/2, (self.screen_height - words_height)/2)
        for i in range(0, 256):
            #self.clock.tick(120)
            self.screen.fill(BLACK)
            mpy_logo_image.set_alpha(i)
            self.screen.blit(mpy_logo_image, logo_placement)
            pg.display.flip()
        for i in range(255, 0, -1):
            #self.clock.tick(120)
            self.screen.fill(BLACK)
            mpy_logo_image.set_alpha(i)
            self.screen.blit(mpy_logo_image, logo_placement)
            pg.display.flip()
        for i in range(0, 256):
            #self.clock.tick(120)
            self.screen.fill(BLACK)
            mpy_words_image.set_alpha(i)
            self.screen.blit(mpy_words_image, words_placement)
            pg.display.flip()
        self.load_data()
        for i in range(255, 0, -1):
            #self.clock.tick(120)
            self.screen.fill(BLACK)
            mpy_words_image.set_alpha(i)
            self.screen.blit(mpy_words_image, words_placement)
            pg.display.flip()
        self.channel3 = pg.mixer.Channel(2)
        self.channel4 = pg.mixer.Channel(3) # Fire, water fall
        self.channel5 = pg.mixer.Channel(4) # breaking sounds and other effects
        self.channel6 = pg.mixer.Channel(5) # vehicle sounds
        self.channel7 = pg.mixer.Channel(6) # explosions

    def on_screen(self, sprite, threshold = 50):
        rect = self.camera.apply(sprite)
        if rect.right < -threshold or rect.bottom < -threshold or rect.left > self.screen_width + threshold or rect.top > self.screen_height + threshold:
            return False
        else:
            return True

    def on_screen_no_edge(self, sprite): #no threashold for slightly faster draw.
        rect = self.camera.apply(sprite)
        if rect.right < 0 or rect.bottom < 0 or rect.left > self.screen_width or rect.top > self.screen_height:
            return False
        else:
            return True

    def is_living(self, npc_kind):
        if 'dead' in self.people[npc_kind]:
            if self.people[npc_kind]['dead']:
                return False
            else:
                return True
        else:
            return True

    def format_date(self):
        directive = "%m-%d-%Y_%H-%M-%S"
        return datetime.datetime.now().strftime(directive)

    def save_sprite_locs(self):
        # This block stores all sprite locations and their health/inventories in the map_sprite_data_list so the game remembers where everything is.
        npc_list = []
        animal_list = []
        item_list = []
        vehicle_list = []
        breakable_list = []
        if not self.underworld:
            for npc in self.npcs:
                if npc not in self.companions:
                    npc_list.append({'name': npc.species, 'location': npc.pos, 'health': npc.stats['health'], 'inventory': npc.inventory, 'colors': npc.colors})
                    self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].npcs = npc_list
            for animal in self.animals:
                if animal not in self.companions:
                    if animal != self.player.vehicle:
                        animal_list.append({'name': animal.species, 'location': animal.pos, 'health': animal.stats['health']})
                        self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].animals = animal_list
            for item in self.dropped_items:
                item_list.append({'name': item.name, 'location': item.pos, 'rotation': item.rot})
                self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].items = item_list
            for vehicle in self.vehicles:
                if vehicle.driver != self.player:
                    vehicle_list.append({'name': vehicle.species, 'location': vehicle.pos, 'health': vehicle.stats['health']})
                    self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].vehicles = vehicle_list
            for breakable in self.breakable:
                breakable_list.append({'name': breakable.name, 'location': breakable.center, 'w': breakable.w, 'h': breakable.h,  'rotation': breakable.rot})
                self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].breakable = breakable_list
        else:
            for npc in self.npcs:
                if npc not in self.companions:
                    npc_list.append({'name': npc.species, 'location': npc.pos, 'health': npc.stats['health'], 'inventory': npc.inventory, 'colors': npc.colors})
                    self.underworld_sprite_data_dict[self.previous_map].npcs = npc_list
            for animal in self.animals:
                if animal not in self.companions:
                    if animal != self.player.vehicle:
                        animal_list.append({'name': animal.species, 'location': animal.pos, 'health': animal.stats['health']})
                        self.underworld_sprite_data_dict[self.previous_map].animals = animal_list
            for item in self.dropped_items:
                item_list.append({'name': item.name, 'location': item.pos, 'rotation': item.rot})
                self.underworld_sprite_data_dict[self.previous_map].items = item_list
            for vehicle in self.vehicles:
                vehicle_list.append({'name': vehicle.species, 'location': vehicle.pos, 'health': vehicle.stats['health']})
                self.underworld_sprite_data_dict[self.previous_map].vehicles = vehicle_list
            for breakable in self.breakable:
                breakable_list.append({'name': breakable.name, 'location': breakable.center, 'w': breakable.w, 'h': breakable.h,  'rotation': breakable.rot})
                self.underworld_sprite_data_dict[self.previous_map].breakable = breakable_list

    def save(self):
        self.screen.fill(BLACK)
        self.save_sprite_locs()
        possessing = self.player.possessing
        if self.player.possessing:
            self.player.possessing.depossess()
        self.player.dragon = False
        if 'dragon' in self.player.equipped['race']: # Makes it so you aren't a dragon when you load a game.
            self.player.equipped['race'] = self.player.equipped['race'].replace('dragon', '')
            self.player.body.update_animations()
        self.draw_text('Saving....', self.script_font, 50, WHITE, self.screen_width / 2, self.screen_height / 2, align="topright")
        pg.display.flip()
        sleep(0.5)
        companion_list = []
        for companion in self.companions:
            companion_list.append(companion.species)
        vehicle_name = None
        if self.player.in_vehicle:
            vehicle_name = self.player.vehicle.species

        updated_equipment = [UPGRADED_WEAPONS, UPGRADED_HATS, UPGRADED_TOPS, UPGRADED_GLOVES, UPGRADED_BOTTOMS, UPGRADED_SHOES, UPGRADED_ITEMS]
        save_list = [self.player.inventory, self.player.equipped, self.player.stats, [self.player.pos.x, self.player.pos.y], self.previous_map, [self.world_location.x, self.world_location.y], self.chests, self.overworld_map, updated_equipment, self.people, self.quests, self.player.colors, vehicle_name, companion_list, self.map_sprite_data_list, self.underworld_sprite_data_dict, self.key_map]
        if not path.isdir(saves_folder): makedirs(saves_folder)

        with open(path.join(saves_folder, self.player.race + "_" + self.format_date() + ".sav"), "wb", -1) as FILE:
            pickle.dump(save_list, FILE)
        if possessing:
            possessing.possess(self.player)

    def load_save(self, file_name):
        load_file = []
        with open(file_name, "rb", -1) as FILE:
            load_file = pickle.load(FILE)
        # Loads saved upgraded equipment:
        self.people = load_file[9] # Updates NPCs
        self.quests = load_file[10] # Updates Quests from save
        self.saved_vehicle = load_file[12]
        self.chests = load_file[6] # Updates chests from dave
        self.saved_companions = load_file[13]
        self.map_sprite_data_list = load_file[14]
        self.underworld_sprite_data_dict = load_file[15]
        self.key_map = load_file[16]
        updated_equipment = load_file[8]
        UPGRADED_WEAPONS.update(updated_equipment[0])
        UPGRADED_HATS.update(updated_equipment[1])
        UPGRADED_TOPS.update(updated_equipment[2])
        UPGRADED_GLOVES.update(updated_equipment[3])
        UPGRADED_BOTTOMS.update(updated_equipment[4])
        UPGRADED_SHOES.update(updated_equipment[5])
        UPGRADED_ITEMS.update(updated_equipment[6])
        WEAPONS.update(UPGRADED_WEAPONS)
        HATS.update(UPGRADED_HATS)
        TOPS.update(UPGRADED_TOPS)
        BOTTOMS.update(UPGRADED_BOTTOMS)
        GLOVES.update(UPGRADED_GLOVES)
        SHOES.update(UPGRADED_SHOES)
        ITEMS.update(UPGRADED_ITEMS)
        self.player.inventory = load_file[0]
        self.player.equipped = load_file[1]
        self.player.race = self.player.equipped['race']
        self.player.stats = load_file[2]
        self.player.colors = load_file[11]
        self.previous_map = load_file[4]
        self.world_location = vec(load_file[5])
        self.load_map(self.previous_map)
        self.player.pos = vec(load_file[3])
        self.player.human_body.update_animations()
        self.player.dragon_body.update_animations()
        self.player.calculate_fire_power()
        self.player.calculate_perks()
        self.overworld_map = load_file[7]
        # Loads saved companions
        for companion in self.saved_companions:
            for npc_type in NPC_TYPE_LIST:
                if companion in eval(npc_type.upper()):
                    rand_angle = randrange(0, 360)
                    random_vec = vec(170, 0).rotate(-rand_angle)
                    follower_center = vec(self.player.pos + random_vec)
                    if npc_type == 'animals':
                        if companion != self.saved_vehicle: #Makes it so it doesn't double load companions you are riding.
                            follower = Animal(self, follower_center.x, follower_center.y, self.map, companion)
                            follower.offensive = False
                            follower.make_companion()
                    else:
                        follower = Npc(self, follower_center.x, follower_center.y, self.map, companion)
                        follower.offensive = False
                        follower.make_companion()
        self.saved_companions = []
        # Enters vehicle if you saved it inside a vehicle
        for vehicle in self.vehicles:
            if vehicle.kind == self.saved_vehicle:
                vehicle.enter_vehicle(self.player)
        for vehicle in self.flying_vehicles:
            if vehicle.kind == self.saved_vehicle:
                vehicle.enter_vehicle(self.player)
        if self.saved_vehicle in ANIMALS:
            mount = Animal(self, self.player.pos.x, self.player.pos.y, self.map, self.saved_vehicle)
            mount.mount(self.player)

        self.load_over_map(self.overworld_map)

    def update_old_save(self, file_name):
        load_file = []
        with open(file_name, "rb", -1) as FILE:
            load_file = pickle.load(FILE)
        # Loads saved upgraded equipment:
        self.people = PEOPLE # Updates NPCs
        self.quests = QUESTS # Updates Quests from save
        self.chests = CHESTS # Updates chests from dave
        self.key_map = KEY_MAP
        updated_equipment = load_file[8]
        UPGRADED_WEAPONS.update(updated_equipment[0])
        UPGRADED_HATS.update(updated_equipment[1])
        UPGRADED_TOPS.update(updated_equipment[2])
        UPGRADED_GLOVES.update(updated_equipment[3])
        UPGRADED_BOTTOMS.update(updated_equipment[4])
        UPGRADED_SHOES.update(updated_equipment[5])
        UPGRADED_ITEMS.update(updated_equipment[6])
        WEAPONS.update(UPGRADED_WEAPONS)
        HATS.update(UPGRADED_HATS)
        TOPS.update(UPGRADED_TOPS)
        BOTTOMS.update(UPGRADED_BOTTOMS)
        GLOVES.update(UPGRADED_GLOVES)
        SHOES.update(UPGRADED_SHOES)
        ITEMS.update(UPGRADED_ITEMS)
        self.player.inventory = load_file[0]
        self.player.equipped = load_file[1]
        self.player.race = self.player.equipped['race']
        self.player.stats = load_file[2]
        self.previous_map = load_file[4]
        self.world_location = vec(load_file[5])
        self.load_map(self.previous_map)
        self.player.pos = vec(load_file[3])
        self.player.human_body.update_animations()
        self.player.dragon_body.update_animations()
        self.player.calculate_fire_power()
        self.player.calculate_perks()
        self.overworld_map = load_file[7]
        self.load_over_map(self.overworld_map)

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)


    def load_data(self):
        self.title_font = HEADING_FONT
        self.hud_font = HUD_FONT
        self.script_font = SCRIPT_FONT
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((SHADOW))
        self.body_surface = pg.Surface((64, 64)).convert()
        self.body_surface.set_colorkey(BLACK)
        self.open_book_image = pg.image.load(path.join(img_folder, 'open_book.png')).convert()
        self.open_book_image = pg.transform.scale(self.open_book_image, (self.screen_width, self.screen_height - 30))
        self.open_letter_image = pg.image.load(path.join(img_folder, 'open_letter.png')).convert()
        self.open_letter_image = pg.transform.scale(self.open_letter_image, (self.screen_width, self.screen_height - 30))
        self.over_minimap_image = pg.image.load(path.join(img_folder, OVERWORLD_MAP_IMAGE)).convert()
        self.over_minimap_image = pg.transform.scale(self.over_minimap_image, (self.screen_width, self.screen_height))
        self.compass_image = pg.image.load(path.join(img_folder, 'compass.png')).convert_alpha()
        self.player_tur = pg.image.load(path.join(img_folder, PLAYER_TUR)).convert_alpha()
        #self.player_tank = pg.image.load(path.join(img_folder, PLAYER_TANK)).convert_alpha()
        #self.tank_in_water = pg.image.load(path.join(img_folder, TANK_IN_WATER)).convert_alpha()
        #self.sunken_tank = pg.image.load(path.join(img_folder, SUNKEN_TANK)).convert_alpha()
        self.lock_image = pg.image.load(path.join(img_folder, 'lock.png')).convert_alpha()
        self.lock_keyway_image = pg.image.load(path.join(img_folder, 'lock_keyway.png')).convert_alpha()
        self.keyed_keyway_image = pg.image.load(path.join(img_folder, 'keyed_keyway.png')).convert_alpha()
        self.lock_pick_image = pg.image.load(path.join(img_folder, 'lock_pick.png')).convert_alpha()
        self.swim_shadow_image = pg.image.load(path.join(img_folder, 'swim_shadow.png')).convert_alpha()
        self.mech_back_image = pg.image.load(path.join(img_folder, 'mech_back_lights.png')).convert_alpha()
        #self.rock_shadow_image = pg.image.load(path.join(img_folder, 'rock_shadow.png')).convert_alpha()
        self.invisible_image = pg.image.load(path.join(img_folder, 'invisible.png')).convert_alpha()
        # creates a dictionary of animal images. This is not in the settings file like the others because of the order it needs to import info.
        ANIMAL_IMAGES = {}
        for animal in ANIMAL_ANIMATIONS:
            temp_list = []
            number_of_files = len([name for name in os.listdir(animals_folder) if animal == name[:-5] if os.path.isfile(os.path.join(animals_folder, name))])
            for i in range(1, number_of_files + 1):
                filename = animal + '{}.png'.format(i)
                temp_list.append(filename)
            ANIMAL_IMAGES[animal] = temp_list
        # Loads animal images
        self.animal_images = {}
        for kind in ANIMAL_IMAGES:
            temp_list = []
            for i, picture in enumerate(ANIMAL_IMAGES[kind]):
                img = pg.image.load(path.join(animals_folder, ANIMAL_IMAGES[kind][i])).convert_alpha()
                temp_list.append(img)
            self.animal_images[kind] = temp_list
        # associates the animation frames with the animal images
        self.animal_animations = {}
        for kind in ANIMAL_ANIMATIONS:
            temp_dict = {}
            for animation in ANIMAL_ANIMATIONS[kind]:
                temp_list = []
                for frame in ANIMAL_ANIMATIONS[kind][animation]:
                    temp_list.append(self.animal_images[kind][frame - 1])
                temp_dict[animation] = temp_list
            self.animal_animations[kind] = temp_dict
        self.bullet_images = {}
        for x, size in enumerate(BULLET_SIZES):
            for i, item in enumerate(BULLET_IMAGES):
                bullet_img = pg.image.load(path.join(bullets_folder, BULLET_IMAGES[i])).convert_alpha()
                if size != 'ar':
                    if i != 0:
                        img = pg.transform.scale(bullet_img, (6*(x + 1), 4*(x + 1)))
                    else:
                        img = pg.transform.scale(bullet_img, (12 * (x + 1), 4 * (x + 1)))
                else:
                    img = pg.transform.scale(bullet_img, (80, 10))
                bullet_name = size + str(i)
                self.bullet_images[bullet_name] = img

        self.door_images = []
        for i, item in enumerate(DOOR_IMAGES):
            img = pg.image.load(path.join(doors_folder, DOOR_IMAGES[i])).convert_alpha()
            self.door_images.append(img)
        self.door_break_images = []
        for i, item in enumerate(DOOR_BREAK_IMAGES):
            img = pg.image.load(path.join(door_break_folder, DOOR_BREAK_IMAGES[i])).convert_alpha()
            self.door_break_images.append(img)
        self.item_images = []
        for i, item in enumerate(ITEM_IMAGES):
            img = pg.image.load(path.join(items_folder, ITEM_IMAGES[i])).convert_alpha()
            self.item_images.append(img)
        self.enchantment_images = []
        for i, item in enumerate(ENCHANTMENT_IMAGES):
            img = pg.image.load(path.join(enchantments_folder, ENCHANTMENT_IMAGES[i])).convert_alpha()
            self.enchantment_images.append(img)
        self.weapon_images = []
        for i, weapon in enumerate(WEAPON_IMAGES):
            img = pg.image.load(path.join(weapons_folder, WEAPON_IMAGES[i])).convert_alpha()
            self.weapon_images.append(img)
        self.hat_images = []
        for i, hat in enumerate(HAT_IMAGES):
            img = pg.image.load(path.join(hats_folder, HAT_IMAGES[i])).convert_alpha()
            self.hat_images.append(img)
        self.hair_images = []
        for i, hair in enumerate(HAIR_IMAGES):
            img = pg.image.load(path.join(hair_folder, HAIR_IMAGES[i])).convert_alpha()
            self.hair_images.append(img)
        self.top_images = []
        for i, top in enumerate(TOP_IMAGES):
            img = pg.image.load(path.join(tops_folder, TOP_IMAGES[i])).convert_alpha()
            self.top_images.append(img)
        self.bottom_images = []
        for i, bottom in enumerate(BOTTOM_IMAGES):
            img = pg.image.load(path.join(bottoms_folder, BOTTOM_IMAGES[i])).convert_alpha()
            self.bottom_images.append(img)
        self.shoe_images = []
        for i, shoe in enumerate(SHOE_IMAGES):
            img = pg.image.load(path.join(shoes_folder, SHOE_IMAGES[i])).convert_alpha()
            self.shoe_images.append(img)
        self.glove_images = []
        for i, glove in enumerate(GLOVE_IMAGES):
            img = pg.image.load(path.join(gloves_folder, GLOVE_IMAGES[i])).convert_alpha()
            self.glove_images.append(img)
        self.magic_images = []
        for i, magic in enumerate(MAGIC_IMAGES):
            img = pg.image.load(path.join(magic_folder, MAGIC_IMAGES[i])).convert_alpha()
            self.magic_images.append(img)
        self.light_mask_images = []
        for i, val in enumerate(LIGHT_MASK_IMAGES):
            img = pg.image.load(path.join(light_masks_folder, LIGHT_MASK_IMAGES[i])).convert_alpha()
            self.light_mask_images.append(img)

        self.flashlight_masks = []
        temp_img = pg.transform.scale(self.light_mask_images[3], (int(600 * 2.8), 600))
        for rot in range(0, 120):
            new_image = pg.transform.rotate(temp_img, rot*3)
            self.flashlight_masks.append(new_image)

        self.magic_animation_images = []
        for image in self.magic_images:
            image_list = []
                # enlarge image animation
            for i in range(0, 5):
                new_image = pg.transform.scale(image, (25*i, 25*i))
                image_list.append(new_image)
            # shrink animation
            for i in range(1, 10):
                new_image = pg.transform.scale(image, (int(140/i), int(140/i)))
                image_list.append(new_image)
            self.magic_animation_images.append(image_list)

        self.gender_images = []
        for i, gender in enumerate(GENDER_IMAGES):
            img = pg.image.load(path.join(gender_folder, GENDER_IMAGES[i])).convert_alpha()
            self.gender_images.append(img)
        self.corpse_images = []
        for i, corpse in enumerate(CORPSE_IMAGES):
            img = pg.image.load(path.join(corpse_folder, CORPSE_IMAGES[i])).convert_alpha()
            self.corpse_images.append(img)
        self.vehicle_images = []
        for i, x in enumerate(VEHICLES_IMAGES):
            img = pg.image.load(path.join(vehicles_folder, VEHICLES_IMAGES[i])).convert_alpha()
            self.vehicle_images.append(img)
        self.color_swatch_images = []
        for i, x in enumerate(COLOR_SWATCH_IMAGES):
            img = pg.image.load(path.join(color_swatches_folder, COLOR_SWATCH_IMAGES[i])).convert()
            self.color_swatch_images.append(img)
        self.race_images = []
        for i, race in enumerate(RACE_IMAGES):
            img = pg.image.load(path.join(race_folder, RACE_IMAGES[i])).convert_alpha()
            self.race_images.append(img)
        self.fire_images = []
        for i, x in enumerate(FIRE_IMAGES):
            img = pg.image.load(path.join(fire_folder, FIRE_IMAGES[i])).convert_alpha()
            self.fire_images.append(img)
        self.shock_images = []
        for i, x in enumerate(SHOCK_IMAGES):
            img = pg.image.load(path.join(shock_folder, SHOCK_IMAGES[i])).convert_alpha()
            self.shock_images.append(img)
        self.electric_door_images = []
        for i, x in enumerate(ELECTRIC_DOOR_IMAGES):
            img = pg.image.load(path.join(electric_door_folder, ELECTRIC_DOOR_IMAGES[i])).convert_alpha()
            self.electric_door_images.append(img)
        self.loading_screen_images = []
        for i, screen in enumerate(LOADING_SCREEN_IMAGES):
            img = pg.image.load(path.join(loading_screen_folder, LOADING_SCREEN_IMAGES[i])).convert()
            self.loading_screen_images.append(img)
        self.tree_images = {}
        self.breakable_images = {}
        for kind in BREAKABLE_IMAGES:
            if 'tree' not in kind:
                temp_list = []
                for i, picture in enumerate(BREAKABLE_IMAGES[kind]):
                    img = pg.image.load(path.join(breakable_folder, BREAKABLE_IMAGES[kind][i])).convert_alpha()
                    temp_list.append(img)
                self.breakable_images[kind] = temp_list
            else:
                temp_list = []
                temp_list2 = []
                temp_list3 = []
                for i, picture in enumerate(BREAKABLE_IMAGES[kind]):
                    img = pg.image.load(path.join(breakable_folder, BREAKABLE_IMAGES[kind][i])).convert_alpha()
                    scaled_image = pg.transform.scale(img, (TREE_SIZES['sm'], TREE_SIZES['sm']))
                    temp_list.append(scaled_image)
                    scaled_image = pg.transform.scale(img, (TREE_SIZES['md'], TREE_SIZES['md']))
                    temp_list2.append(scaled_image)
                    scaled_image = pg.transform.scale(img, (TREE_SIZES['lg'], TREE_SIZES['lg']))
                    temp_list3.append(scaled_image)
                self.tree_images['sm' + kind] = temp_list
                self.tree_images['md' + kind] = temp_list2
                self.tree_images['lg' + kind] = temp_list3

        self.portal_sheet = pg.image.load(PORTAL_SHEET).convert_alpha()
        self.portal_images = load_spritesheet(self.portal_sheet, 256)

        self.fireball_images = []
        for i, x in enumerate(FIREBALL_IMAGES):
            img = pg.image.load(path.join(fireball_folder, FIREBALL_IMAGES[i])).convert_alpha()
            self.fireball_images.append(img)
        self.explosion_images = []
        for i, x in enumerate(EXPLOSION_IMAGES):
            img = pg.image.load(path.join(explosion_folder, EXPLOSION_IMAGES[i])).convert_alpha()
            self.explosion_images.append(img)

        self.humanoid_images = {}
        for kind in HUMANOID_IMAGES:
            temp_list = []
            for i, picture in enumerate(HUMANOID_IMAGES[kind]):
                temp_folder = kind.replace('images', 'parts_folder')
                img = pg.image.load(path.join(eval(temp_folder), HUMANOID_IMAGES[kind][i])).convert_alpha()
                temp_list.append(img)
            self.humanoid_images[kind] = temp_list

        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        # lighting effect
        self.fog = pg.Surface((self.screen_width, self.screen_height))
        self.fog.fill(NIGHT_COLOR)
        # Sound loading
        self.effects_sounds = {}
        for key in EFFECTS_SOUNDS:
            self.effects_sounds[key] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[key]))
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)
        self.weapon_hit_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_hit_sounds[weapon] = []
            for snd in WEAPON_HIT_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.3)
                self.weapon_hit_sounds[weapon].append(s)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.2)
            self.zombie_moan_sounds.append(s)
        self.wraith_sounds = []
        for snd in WRAITH_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.2)
            self.wraith_sounds.append(s)
        self.punch_sounds = []
        for snd in PUNCH_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.2)
            self.punch_sounds.append(s)
        self.male_player_hit_sounds = []
        for snd in MALE_PLAYER_HIT_SOUNDS:
            self.male_player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.female_player_hit_sounds = []
        for snd in FEMALE_PLAYER_HIT_SOUNDS:
            self.female_player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.female_player_voice = {}
        for key in FEMALE_PLAYER_VOICE:
            temp_list = []
            for i, snd in enumerate(FEMALE_PLAYER_VOICE[key]):
                temp_list.append(pg.mixer.Sound(path.join(female_player_sound_folder, FEMALE_PLAYER_VOICE[key][i])))
            self.female_player_voice[key] = temp_list
        self.male_player_voice = {}
        for key in MALE_PLAYER_VOICE:
            temp_list = []
            for i, snd in enumerate(MALE_PLAYER_VOICE[key]):
                temp_list.append(pg.mixer.Sound(path.join(female_player_sound_folder, MALE_PLAYER_VOICE[key][i])))
            self.male_player_voice[key] = temp_list
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.lock_picking_sounds = []
        for snd in LOCK_PICKING_SOUNDS:
            self.lock_picking_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))

    def new(self):
        pg.mixer.music.load(path.join(music_folder, TITLE_MUSIC))
        pg.mixer.music.play(loops=-1)
        title_image = pg.image.load(path.join(img_folder, TITLE_IMAGE)).convert()
        title_image = pg.transform.scale(title_image, (self.screen_width, self.screen_height))
        self.continued_game = False
        self.in_load_menu = False
        self.in_npc_menu = False
        self.in_settings_menu = False
        waiting = True
        i = 0
        while waiting:
            self.clock.tick(FPS)
            self.screen.fill(BLACK)
            title_image.set_alpha(i)
            self.screen.blit(title_image, (0, 0))
            if i > 240:
                self.draw_text('Press any key to begin or C to continue', self.script_font, 30, WHITE, self.screen_width / 2, self.screen_height - 120,
                               align="center")

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    waiting = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_c:
                        waiting = False
                        self.in_load_menu = True
                        self.continued_game = True
                    elif event.key == pg.K_n:  # Enters the NPC creation tool
                        if event.mod & pg.KMOD_CTRL:
                            waiting = False
                            self.in_npc_menu = True
                        else:
                            waiting = False

                    elif event.key != pg.K_n:
                        if not event.mod & pg.KMOD_CTRL:
                            waiting = False

            pg.display.flip()
            i += 1
            if i > 255:
                i = 255

        # initialize all variables and do all the setup for a new game

        # Used for controlling day and night
        self.darkness = 0
        self.dark_color = (255, 255, 255)
        self.time_of_day = 0
        self.nightfall = False
        self.sunrise = False
        self.night = False
        self.last_darkness_change = 0
        self.day_start_time = pg.time.get_ticks()

        self.map_sprite_data_list = []
        self._player_inside = False
        self.compass_rot = 0
        self.people = PEOPLE
        self.saved_vehicle = []
        self.saved_companions = []
        self.underworld = False
        self.quests = QUESTS
        self.chests = CHESTS
        self.key_map = KEY_MAP
        self.bg_music = BG_MUSIC
        self.previous_music = TITLE_MUSIC
        self.portal_location = vec(0, 0)
        self.portal_combo = ''
        self.load_menu = Load_Menu(self)
        self.settings_menu = Settings_Menu(self)
        self.guard_alerted = False
        self.hud_map = False
        self.hud_overmap = False

        self.message_text = True
        self.message = ''
        self.map_type = None
        self.group = PyscrollGroup()
        self.all_sprites = pg.sprite.LayeredUpdates() # Used for all non_static sprites
        self.all_static_sprites = pg.sprite.Group() # used for all static sprites
        self.sprites_on_screen = pg.sprite.Group()
        self.moving_targets = pg.sprite.Group() # Used for all moving things bullets interact with
        self.moving_targets_on_screen = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.mobs_on_screen = pg.sprite.Group()
        self.npc_bodies = pg.sprite.Group()
        self.npc_bodies_on_screen = pg.sprite.Group()
        self.npcs =  pg.sprite.Group()
        self.npcs_on_screen = pg.sprite.Group()
        self.animals = pg.sprite.Group()
        self.animals_on_screen = pg.sprite.Group()
        self.fires = pg.sprite.Group()
        self.fires_on_screen = pg.sprite.Group()
        self.electric_doors = pg.sprite.Group()
        self.electric_doors_on_screen = pg.sprite.Group()
        self.entryways = pg.sprite.Group()
        self.entryways_on_screen = pg.sprite.Group()
        self.breakable = pg.sprite.Group()
        self.breakable_on_screen = pg.sprite.Group()
        self.corpses = pg.sprite.Group()
        self.corpses_on_screen = pg.sprite.Group()
        self.dropped_items = pg.sprite.Group()
        self.dropped_items_on_screen = pg.sprite.Group()

        self.beds = pg.sprite.Group()
        self.beds_on_screen = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.obstacles_on_screen = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.walls_on_screen = pg.sprite.Group()
        self.barriers = pg.sprite.Group()
        self.barriers_on_screen = pg.sprite.Group()
        self.elevations = pg.sprite.Group()
        self.elevations_on_screen = pg.sprite.Group()
        self.water = pg.sprite.Group()
        self.water_on_screen = pg.sprite.Group()
        self.shallows = pg.sprite.Group()
        self.long_grass = pg.sprite.Group()
        self.long_grass_on_screen = pg.sprite.Group()
        self.shallows_on_screen = pg.sprite.Group()
        self.lava = pg.sprite.Group()
        self.lava_on_screen = pg.sprite.Group()
        self.inside = pg.sprite.Group()
        self.inside_on_screen = pg.sprite.Group()
        self.climbs = pg.sprite.Group()
        self.climbs_on_screen = pg.sprite.Group()
        self.vehicles = pg.sprite.Group()
        self.vehicles_on_screen = pg.sprite.Group()

        self.aipaths = pg.sprite.Group()
        self.lights = pg.sprite.Group()
        self.firepots = pg.sprite.Group()
        self.arrows = pg.sprite.Group()
        self.chargers = pg.sprite.Group()
        self.mechsuits = pg.sprite.Group()
        self.detectors = pg.sprite.Group()
        self.detectables = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        self.door_walls = pg.sprite.Group()
        self.nospawn = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.toilets = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.grabable_animals = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        self.shocks = pg.sprite.Group()
        self.fireballs = pg.sprite.Group()
        self.firepits = pg.sprite.Group()
        self.containers = pg.sprite.Group()
        self.chest_containers = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.enemy_bullets = pg.sprite.Group()
        self.enemy_fireballs = pg.sprite.Group()
        self.work_stations = pg.sprite.Group()
        self.climbables_and_jumpables = pg.sprite.Group()
        self.all_vehicles = pg.sprite.Group()
        self.companions = pg.sprite.Group()
        self.companion_bodies = pg.sprite.Group()
        self.boats = pg.sprite.Group()
        self.amphibious_vehicles  = pg.sprite.Group()
        self.flying_vehicles  = pg.sprite.Group()
        self.land_vehicles  = pg.sprite.Group()
        self.turrets = pg.sprite.Group()
        self.occupied_vehicles = pg.sprite.Group()
        self.random_targets = pg.sprite.Group()
        self.target_list = [self.random_targets, self.entryways, self.work_stations, self.moving_targets,  self.aipaths]
        self.new_game = True
        self.respawn = False
        self.previous_map = "1.tmx"
        self.world_location = vec(1, 1)
        self.underworld_sprite_data_dict = {}
        self.player = Player(self) # Creates initial player object
        if self.new_game:  # Why do I have to variables: new_game and conitnued_game
            self.in_character_menu = True
        self.character_menu = Character_Design_Menu(self)
        self.generic_npc = Npc(self, 0, 0, map, 'generic')  # Spawns a generic villager npc to be modified
        self.npc_menu = Npc_Design_Menu(self, self.generic_npc)
        if self.in_npc_menu:
            self.npc_menu.update()
        self.generic_npc.kill()
        if not self.continued_game:
            self.character_menu.update()
        self.in_character_menu = False
        self.overworld_map = START_WORLD
        if not self.continued_game:
            self.load_over_map(self.overworld_map) # Loads world map for first world. This will allow me to load other world maps later.
        if not self.continued_game:
            self.change_map(None, RACE[self.player.race]['start map'], RACE[self.player.race]['start pos'])
        self.menu = Inventory_Menu(self)
        self.stats_menu = Stats_Menu(self)
        self.quest_menu = None
        self.fly_menu = None
        self.in_menu = False
        self.in_inventory_menu = False
        self.store_menu = None
        self.in_store_menu = False
        self.in_stats_menu = False
        self.in_loot_menu = False
        self.in_lock_menu = False
        self.in_station_menu = False
        self.in_quest_menu = False
        self.in_dialogue_menu = False
        self.dialogue_menu = None
        self.dialogue_menu_npc = None
        self.last_hud_update = 0
        self.last_fire = 0
        self.last_dialogue = 0
        self.hud_health_stats = self.player.stats
        self.hud_health = self.hud_health_stats['health'] / self.hud_health_stats['max health']
        self.hud_stamina = self.hud_health_stats['stamina'] / self.hud_health_stats['max stamina']
        self.hud_magica = self.hud_health_stats['magica'] / self.hud_health_stats['max magica']
        self.hud_mobhp = 0
        self.show_mobhp = False
        self.last_mobhp_update = 0
        self.hud_hunger = 1
        self.hud_ammo1 = ''
        self.hud_ammo2 = ''
        self.e_down = False
        self.draw_debug = False
        self.paused = False
        self.effects_sounds['level_start'].play()
        if self.continued_game:
            self.load_menu.update()

    @property
    def portal_combo(self):  # This is the method that is called whenever you access portal_combo
        return self._portal_combo
    @portal_combo.setter # Runs whenever you set a value for portal_combo, it checks portal combos
    def portal_combo(self, value):
        self._portal_combo = value
        if value != '':
            if value in PORTAL_CODES:
                coordinate = vec(PORTAL_CODES[value][0], PORTAL_CODES[value][1])
                location = vec(PORTAL_CODES[value][2], PORTAL_CODES[value][3])
                self.portal_combo = ''
                Portal(self, self.portal_location, coordinate, location)
    @property
    def player_inside(self): #This is the method that is called whenever you access
        return self._player_inside
    @player_inside.setter #This is the method that is called whenever you set a value
    def player_inside(self, value):
        if value!=self._player_inside:
            self._player_inside = value
            self.map.toggle_visible_layers()
        else:
            pass

    def load_over_map(self, map):
        # Loads data from overworld tmx file
        file = open(path.join(map_folder, map), "r")
        map_data = file.readlines()
        self.overworld_map = map
        self.map_data_list = []
        for row in map_data:
            if '<' not in row: # Ignores all tags in tmx file
                row = row.replace(',\n', '') #gets rid of commas at the the end
                row = row.replace(' ', '') #gets rid of spaces between entries
                row = row.replace('\n', '') #gets rid of new lines
                row = row.split(',')
                self.map_data_list.append(row)
        for y, row in enumerate(self.map_data_list): # Randomizes select map elements based on settings.py
            for x, cell in enumerate(row):
                if cell in RANDOM_MAP_TILES:
                    map_list = eval(RANDOM_MAP_TILES[cell])
                    self.map_data_list[y][x] = choice(map_list)
        self.world_width = len(self.map_data_list[0])
        self.world_height = len(self.map_data_list)

        # This creates a map data object to store which sprites are on each map. This keeps track of where sprites are when they more around or when you drop things.
        if self.map_sprite_data_list == []:
            for x in range(0, self.world_width):
                row = []
                for y in range(0, self.world_height):
                    map_data_store = MapData(x, y)
                    row.append(map_data_store)
                self.map_sprite_data_list.append(row)

        #world_mini_map = WorldMiniMap(self, self.map_data_list) # Only uncomment this to create a new overworld map if you edit the old one. Otherwise it will take literally forever to load every time.
        #self.load_map(str(self.map_data_list[int(self.world_location.y)][int(self.world_location.x)]) + '.tmx')

    def in_surrounding_tiles(self, x, y, num, layer):
        if (x < self.map.tiles_wide-1) and (y < self.map.tiles_high-1):
            if 0 not in [x, y]:
                return num in [self.map.tmxdata.get_tile_gid(x - 1, y, layer), self.map.tmxdata.get_tile_gid(x + 1, y, layer), self.map.tmxdata.get_tile_gid(x + 1, y + 1, layer), self.map.tmxdata.get_tile_gid(x - 1, y - 1, layer), self.map.tmxdata.get_tile_gid(x, y + 1, layer), self.map.tmxdata.get_tile_gid(x, y - 1, layer), self.map.tmxdata.get_tile_gid(x - 1, y + 1, layer), self.map.tmxdata.get_tile_gid(x + 1, y - 1, layer)]
            elif x == 0 and y != 0:
                return num in [self.map.tmxdata.get_tile_gid(x + 1, y, layer), self.map.tmxdata.get_tile_gid(x + 1, y + 1, layer), self.map.tmxdata.get_tile_gid(x, y + 1, layer), self.map.tmxdata.get_tile_gid(x, y - 1, layer), self.map.tmxdata.get_tile_gid(x + 1, y - 1, layer)]
            elif x != 0 and y == 0:
                return num in [self.map.tmxdata.get_tile_gid(x - 1, y, layer), self.map.tmxdata.get_tile_gid(x + 1, y, layer), self.map.tmxdata.get_tile_gid(x + 1, y + 1, layer), self.map.tmxdata.get_tile_gid(x, y + 1, layer), self.map.tmxdata.get_tile_gid(x - 1, y + 1, layer)]
            else:
                return num in [self.map.tmxdata.get_tile_gid(x + 1, y, layer), self.map.tmxdata.get_tile_gid(x + 1, y + 1, layer), self.map.tmxdata.get_tile_gid(x, y + 1, layer)]
        elif (x == self.map.tiles_wide-1) and (y == self.map.tiles_high-1):
            if 0 not in [x, y]:
                return num in [self.map.tmxdata.get_tile_gid(x - 1, y, layer), self.map.tmxdata.get_tile_gid(x - 1, y - 1, layer), self.map.tmxdata.get_tile_gid(x, y - 1, layer)]
            elif x == 0 and y != 0:
                return num in [self.map.tmxdata.get_tile_gid(x, y - 1, layer)]
            elif x != 0 and y == 0:
                return num in [self.map.tmxdata.get_tile_gid(x - 1, y, layer)]
        elif (x == self.map.tiles_wide-1) and (y != self.map.tiles_high-1):
            if 0 not in [x, y]:
                return num in [self.map.tmxdata.get_tile_gid(x - 1, y, layer), self.map.tmxdata.get_tile_gid(x - 1, y - 1, layer), self.map.tmxdata.get_tile_gid(x, y + 1, layer), self.map.tmxdata.get_tile_gid(x, y - 1, layer), self.map.tmxdata.get_tile_gid(x - 1, y + 1, layer)]
            elif x == 0 and y != 0:
                return num in [self.map.tmxdata.get_tile_gid(x, y + 1, layer), self.map.tmxdata.get_tile_gid(x, y - 1, layer)]
            elif x != 0 and y == 0:
                return num in [self.map.tmxdata.get_tile_gid(x - 1, y, layer), self.map.tmxdata.get_tile_gid(x, y + 1, layer), self.map.tmxdata.get_tile_gid(x - 1, y + 1, layer)]
            else:
                return num in [self.map.tmxdata.get_tile_gid(x, y + 1, layer)]
        elif (x != self.map.tiles_wide-1) and (y == self.map.tiles_high-1):
            if 0 not in [x, y]:
                return num in [self.map.tmxdata.get_tile_gid(x - 1, y, layer), self.map.tmxdata.get_tile_gid(x + 1, y, layer), self.map.tmxdata.get_tile_gid(x - 1, y - 1, layer), self.map.tmxdata.get_tile_gid(x, y - 1, layer),
                               self.map.tmxdata.get_tile_gid(x + 1, y - 1, layer)]
            elif x == 0 and y != 0:
                return num in [self.map.tmxdata.get_tile_gid(x + 1, y, layer), self.map.tmxdata.get_tile_gid(x, y - 1, layer), self.map.tmxdata.get_tile_gid(x + 1, y - 1, layer)]
            elif x != 0 and y == 0:
                return num in [self.map.tmxdata.get_tile_gid(x - 1, y, layer), self.map.tmxdata.get_tile_gid(x + 1, y, layer)]
            else:
                return num in [self.map.tmxdata.get_tile_gid(x + 1, y, layer)]

    def on_map(self, sprite):
        offset = 0
        if sprite['location'].x <= 0:
            sprite['location'].x = self.map.width - offset
            return [False, -1, 0]
        if sprite['location'].y <= 0:
            sprite['location'].y = self.map.height - offset
            return [False, 0, -1]
        if sprite['location'].x >= self.map.width:
            sprite['location'].x = offset
            return [False, 1, 0]
        if sprite['location'].y >= self.map.height:
            sprite['location'].y = offset
            return [False, 0, 1]
        return [True, 0, 0]

    # Used for switching to the next map after you go north, south, east or west at the end of the current map.
    def change_map(self, cardinal = None, coordinate = None, location = None, undermap = None):
        self.save_sprite_locs()
        # This for loop moves npcs and animals to other maps when they go off the screen.
        if not self.underworld:
            for npc in self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].npcs:
                temp_loc = self.on_map(npc)
                if not temp_loc[0]:
                    if self.map_sprite_data_list[int(self.world_location.x) + temp_loc[1]][int(self.world_location.y) + temp_loc[2]].visited:
                        self.map_sprite_data_list[int(self.world_location.x) + temp_loc[1]][int(self.world_location.y) + temp_loc[2]].npcs.append(npc)
                    else:
                        self.map_sprite_data_list[int(self.world_location.x) + temp_loc[1]][int(self.world_location.y) + temp_loc[2]].moved_npcs.append(npc)
                    self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].npcs.remove(npc)
            for animal in self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].animals:
                temp_loc = self.on_map(animal)
                if not temp_loc[0]:
                    if self.map_sprite_data_list[int(self.world_location.x) + temp_loc[1]][int(self.world_location.y) + temp_loc[2]].visited:
                        self.map_sprite_data_list[int(self.world_location.x) + temp_loc[1]][int(self.world_location.y) + temp_loc[2]].animals.append(animal)
                    else:
                        self.map_sprite_data_list[int(self.world_location.x) + temp_loc[1]][int(self.world_location.y) + temp_loc[2]].moved_animals.append(animal)
                    self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].animals.remove(animal)
            for vehicle in self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].vehicles:
                temp_loc = self.on_map(vehicle)
                if not temp_loc[0]:
                    if self.map_sprite_data_list[int(self.world_location.x) + temp_loc[1]][int(self.world_location.y) + temp_loc[2]].visited:
                        self.map_sprite_data_list[int(self.world_location.x) + temp_loc[1]][int(self.world_location.y) + temp_loc[2]].vehicles.append(vehicle)
                    else:
                        self.map_sprite_data_list[int(self.world_location.x) + temp_loc[1]][int(self.world_location.y) + temp_loc[2]].moved_vehicles.append(vehicle)
                    self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].vehicles.remove(vehicle)

        self.guard_alerted = False # Makes it so guards stop attacking you after you change maps
        self.player.vel = vec(0, 0)
        self.player.acc = vec(0, 0)
        direction = cardinal
        offset = 64
        if cardinal:
            if direction == 'north':
                self.world_location -= vec(0, 1)
                self.player.rect.top = self.map.height - offset
                self.player.pos = vec(self.player.rect.center)
            elif direction == 'south':
                self.world_location += vec(0, 1)
                self.player.rect.bottom = offset
                self.player.pos = vec(self.player.rect.center)
            elif direction == 'east':
                self.world_location += vec(1, 0)
                self.player.rect.right = offset
                self.player.pos = vec(self.player.rect.center)
            elif direction == 'west':
                self.world_location -= vec(1, 0)
                self.player.rect.left = self.map.width - offset
                self.player.pos = vec(self.player.rect.center)
            # This part of the code wraps around creating a globe like world
            if self.world_location.x == self.world_width:
                self.world_location.x = 0
            if self.world_location.x < 0:
                self.world_location.x = self.world_width - 1
            if self.world_location.y == self.world_height:
                self.world_location.y = 0
            if self.world_location.y < 0:
                self.world_location.y = self.world_height - 1

        if coordinate:
            # Sets player's location of world map
            self.world_location = vec(coordinate)
            # Sets player's location on local map
            loc = vec(location)
            self.player.rect.center = (int(loc.x * 128), int(loc.y * 128))
            self.player.pos = vec(self.player.rect.center)
        if undermap == None:
            map = str(self.map_data_list[int(self.world_location.y)][int(self.world_location.x)]) + '.tmx'
        else:
            map = undermap

        # This block of code sets the positions of the player's followers so they are randomly arranged in a circular orientation around the player.
        for companion in self.companions:
            rand_angle = randrange(0, 360)
            random_vec = vec(170, 0).rotate(-rand_angle)
            companion.rect.center = self.player.rect.center + random_vec
            companion.pos = vec(companion.rect.center)
            companion.offensive = False
            companion.map = map
        self.load_map(map)

    def sleep_in_bed(self):
        self.screen.fill(BLACK)
        pg.mixer.music.stop()
        self.draw_text('Sweet dreams....', self.script_font, 50, WHITE, self.screen_width / 2, self.screen_height / 2, align="topright")
        pg.display.flip()
        self.player.add_health(50)
        self.player.add_stamina(50)
        self.player.add_magica(50)
        self.effects_sounds['snore'].play()
        sleep(10)
        self.beg = perf_counter() # resets dt
        pg.mixer.music.play(loops=-1)
        # Changes it to sunrise when you sleep.
        self.darkness = 225
        color_val = 255 - self.darkness
        self.dark_color = (color_val, color_val, color_val)
        self.night = True
        self.day_start_time = pg.time.get_ticks() - NIGHT_LENGTH

    def use_toilet(self):
        self.player.add_health(5)
        self.player.add_stamina(30)
        self.player.add_hunger(-4)
        toilet_sounds = ['fart', 'pee']
        self.effects_sounds[choice(toilet_sounds)].play()
        sleep(2)
        self.effects_sounds['toilet'].play()
        self.beg = perf_counter() # resets dt

    def garbage_collect(self): # This block of code removes everything in memory from previous maps
        for sprite in self.all_sprites:
            if self.player.possessing:
                if sprite in [self.player.possessing, self.player.possessing.body]:
                    continue
            if self.player.in_vehicle:
                if sprite in [self.player.vehicle]:
                    continue
            if sprite in self.companions:
                continue
            elif sprite in self.companion_bodies:
                continue
            elif sprite in [self.player, self.player.human_body, self.player.dragon_body, self.player.body]:
                continue
            else:
                sprite.kill()
                del sprite
        for sprite in self.turrets:
            if not sprite.mother.alive():
                sprite.kill()
                del sprite

        for sprite in self.all_static_sprites:
            sprite.kill()
            del sprite

        del self.map
        gc.collect()  # Forces garbage collection. Without this the game will quickly run out of memory.

    def layer_num_by_name(self, name):
        for i, layer in enumerate(self.map.tmxdata.visible_layers):
            if isinstance(layer, pytmx.TiledTileLayer):
                if layer.name == 'name':
                    return i
                else:
                    return None

    def load_map(self, temp_map):
        self.sprite_data = self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)]
        self.compass_rot = -math.atan2(49 - self.world_location.y, 89 - self.world_location.x)
        self.compass_rot = math.degrees(self.compass_rot)

        # Checks to see if the map is bellow the main world level
        map = temp_map
        self.underworld = False
        for kind in UNDERWORLD:
            if kind in map:
                self.underworld = True
        if self.underworld:
            if map in self.underworld_sprite_data_dict: # Checks to see if the map has bee visited and added to the data dictionary
                self.sprite_data = self.underworld_sprite_data_dict[map]
            else:
                self.sprite_data = MapData(int(self.world_location.x), int(self.world_location.y)) # Adds the map if it's never been visited as a MapData object to store sprite info in.
                self.underworld_sprite_data_dict[map] = self.sprite_data

        self.map_type = None
        self.screen.fill(BLACK)
        loading_screen = pg.transform.scale(choice(self.loading_screen_images), (self.screen_width, self.screen_height)) # Scales loading screen to resolution
        self.screen.blit(loading_screen, (0, 0))
        self.draw_text('Loading....', self.script_font, 50, WHITE, self.screen_width / 4, self.screen_height * 3/4, align="topright")
        pg.display.flip()
        if not self.new_game:
            self.garbage_collect()
        self.map = TiledMap(self, path.join(map_folder, map))
        self.group._map_layer = self.map.map_layer # Sets the map as the Pyscroll group base layer.
        self.camera = Camera(self, self.map.width, self.map.height)

        for i in range(0, 10): # Creates random targets for Npcs
            target = Target(self)
            hits = pg.sprite.spritecollide(target, self.walls, False)  # Kills targets that appear in walls.
            if hits:
                target.kill()


        if self.sprite_data.visited: # Loads stored map data for sprites if you have visited before.
            companion_names = []
            for companion in self.companions:
                companion_names.append(companion.species)
            for npc in self.sprite_data.npcs:
                if npc['name'] not in companion_names: # Makes it so it doesn't double load your companions.
                    Npc(self, npc['location'].x, npc['location'].y, map, npc['name'], npc['health'], npc['inventory'], npc['colors'])
            for animal in self.sprite_data.animals:
                Animal(self, animal['location'].x, animal['location'].y, map, animal['name'], animal['health'])
            for vehicle in self.sprite_data.vehicles:
                Vehicle(self, vehicle['location'], vehicle['name'], map, vehicle['health'])
            for breakable in self.sprite_data.breakable:
                Breakable(self, breakable['location'], breakable['w'], breakable['h'], breakable['name'], map, breakable['rotation'])
            for item in self.sprite_data.items:
                for item_type in ITEM_TYPE_LIST:
                    if item['name'] in eval(item_type.upper()):
                        Dropped_Item(self, item['location'], item_type, item['name'], item['rotation'])
        else: # Loads animals and NPCs that have moved onto unvisited maps.
            companion_names = []
            for companion in self.companions:
                companion_names.append(companion.species)
            for npc in self.sprite_data.moved_npcs:
                if npc['name'] not in companion_names: # Makes it so it doesn't double load your companions.
                    Npc(self, npc['location'].x, npc['location'].y, map, npc['name'], npc['health'], npc['inventory'], npc['colors'])
            self.sprite_data.moved_npcs = []
            for animal in self.sprite_data.moved_animals:
                Animal(self, animal['location'].x, animal['location'].y, map, animal['name'], animal['health'])
            self.sprite_data.moved_animals = []

        # Creates elevation objects if layers have EL in their names.
        for i, layer in enumerate(self.map.tmxdata.visible_layers):
            if 'EL' in layer.name:
                EL = layer.name
                EL = EL.replace('EL', '')
                EL = int(EL)
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, gid, in layer:
                        if gid != 0:
                            cliff = self.in_surrounding_tiles(x, y, 0, i)
                            elev = Elevation(self, x * self.map.tile_size, y * self.map.tile_size, self.map.tile_size, self.map.tile_size, EL, cliff)
                            hits = pg.sprite.spritecollide(elev, self.elevations, False)  # Kills redundant elevations on top of others.
                            for hit in hits:
                                if hit != elev:
                                    hit.kill()

        # Creates wall and ore block objects if layers have WALLS in their names.
        exception_tile = 0
        if self.map.tmxdata.get_tile_gid(0, 0, 0) != self.map.tmxdata.get_tile_gid(0, 1, 0): # Sees if there is a different tile in the upper left corner to use as a zero tile where no walls will spawn.
            exception_tile = self.map.tmxdata.get_tile_gid(0, 0, 0)  # Tile type to ignore and treat as a zero.
        if self.map.tmxdata.get_tile_gid(1, 0, 0) != self.map.tmxdata.get_tile_gid(0, 1, 0): # Sees if there is a different tile in the upper corner (2nd x pos) to use as an ore tile.
            block_tile = self.map.tmxdata.get_tile_gid(1, 0, 0)
        for i, layer in enumerate(self.map.tmxdata.visible_layers):
            if 'WALLS' in layer.name:
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, gid, in layer:
                        if gid != 0:
                            if gid == block_tile: # Makes ore block objects where the block_tile type tile is.
                                if not self.sprite_data.visited: # Only generates ores if you haven't been here before. Otherwise it generates the remaining ores from the map data object.
                                    block_type = choice(choices(BLOCK_LIST, BLOCK_PROB, k=10))
                                    center = vec(x * self.map.tile_size + self.map.tile_size / 2, y * self.map.tile_size + self.map.tile_size / 2)
                                    Breakable(self, center, self.map.tile_size, self.map.tile_size, block_type, map)
                            elif self.in_surrounding_tiles(x, y, 0, i):#Checks to see if surrounding tiles are zeros and spawns a wall if they are.
                                wall = Obstacle(self, x * self.map.tile_size, y * self.map.tile_size, self.map.tile_size, self.map.tile_size)
                                hits = pg.sprite.spritecollide(wall, self.walls, False)  # Kills redundant walls on top of others.
                                for hit in hits:
                                    if hit != wall:
                                        hit.kill()
                            elif (gid != exception_tile) and self.in_surrounding_tiles(x, y, exception_tile, i):#Checks to see if surrounding tiles are exceptions and spawns a wall if they are.
                                wall = Obstacle(self, x * self.map.tile_size, y * self.map.tile_size, self.map.tile_size, self.map.tile_size)
                                hits = pg.sprite.spritecollide(wall, self.walls, False)  # Kills redundant walls on top of others.
                                for hit in hits:
                                    if hit != wall:
                                        hit.kill()

        # This section creates ores based off of which tile is used in the map rather than having to create ore objects
        #if self.map_type:
        #    for type in UNDERWORLD:
        #        if type in self.map_type:
        #            # This section generates ore blocks to time in all the spaces with the tile specified in the position (0, 0).
        #            if not self.sprite_data.visited:
        #                block_tile = self.map.tmxdata.get_tile_gid(1, 0, 0)
        #                for location in self.map.tmxdata.get_tile_locations_by_gid(block_tile):
        #                    block_type = choice(choices(BLOCK_LIST, BLOCK_PROB, k = 10))
        #                    center = vec(location[0] * self.map.tile_size + self.map.tile_size/2, location[1] * self.map.tile_size + self.map.tile_size/2)
        #                    block = Breakable(self, center, self.map.tile_size, self.map.tile_size, block_type, map)
        #                    hits = pg.sprite.spritecollide(block, self.walls, False)  # Kills walls blocks spawn on top of.
        #                    for hit in hits:
        #                        if hit != hit.trunk:
        #                            hit.kill()

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name:
                obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
                # These are paths for the AIs to follow.
                if tile_object.name in AIPATHS:
                    AIPath(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.name)
                # It's super important that all elevations spawn before the player and mobs.
                if 'EL' in tile_object.name:
                    try:
                        _, elev, climb = tile_object.name.split('_')
                        climb = eval(climb)
                    except:
                        _, elev = tile_object.name.split('_')
                        climb = False
                    elev = int(elev)
                    Elevation(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, elev, climb)
                if tile_object.name == 'jumpable':
                    elev = Elevation(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height, 0, False, 'jumpable')
                if tile_object.name == 'climbable':
                    Elevation(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height, 0, False, 'climbable')
                if tile_object.name == 'player':
                    self.player.pos = vec(obj_center)
                    self.player.rect.center = self.player.pos

                if not self.sprite_data.visited: # Only executes if you have never been to this map before. Otherwise it pulls the data from the stored list.
                    # Loads NPCs from NPC_TYPE_LIST
                    for npc_type in NPC_TYPE_LIST:
                        if tile_object.name in eval(npc_type.upper()):
                            if npc_type == 'animals':
                                Animal(self, obj_center.x, obj_center.y, map, tile_object.name)
                            else:
                                if self.is_living(tile_object.name):
                                    Npc(self, obj_center.x, obj_center.y, map, tile_object.name)
                    # Loads vehicles
                    for vehicle in VEHICLES:
                        if vehicle == tile_object.name:
                            Vehicle(self, obj_center, vehicle, map)
                    # Loads items, weapons, and armor placed on the map
                    for item_type in ITEM_TYPE_LIST:
                        if tile_object.name in eval(item_type.upper()):
                            Dropped_Item(self, obj_center, item_type, tile_object.name)
                    # Loads fixed rotated items:
                    if '@' in tile_object.name:
                        item, rot = tile_object.name.split('@')
                        rot = int(rot)
                        for item_type in ITEM_TYPE_LIST:
                            if item in eval(item_type.upper()):
                                Dropped_Item(self, obj_center, item_type, item, rot)
                    # Used for destructable plants, rocks, ore veins, walls, etc
                    for item in BREAKABLES:
                        if item in tile_object.name:
                            size = None
                            if '@' in tile_object.name:
                                temp_item, rot = tile_object.name.split('@')
                                rot = int(rot)
                            else:
                                rot = None
                            if 'SZ' in tile_object.name:
                                size, temp_item = tile_object.name.split('SZ')
                            Breakable(self, obj_center, tile_object.width, tile_object.height, item, map, rot, size)

                # Loads detectors used to detect whether quest items have be delivered to the correct locations.
                if 'detector' in tile_object.name:  # These are invisible objects used to detect other objects touching them.
                    Detector(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.name)
                # Loads items/npcs that only appear after their corresponding quests are completed.
                if 'QC' in tile_object.name:
                    _, quest, quest_item = tile_object.name.split('_')
                    if self.quests[quest]['completed']:
                        if quest_item in VEHICLES:
                            Vehicle(self, obj_center, quest_item, map)
                        if quest_item in ANIMALS:
                            Animal(self, obj_center.x, obj_center.y, map, quest_item)
                        if quest_item in self.people:
                            if self.is_living(quest_item):
                                Npc(self, obj_center.x, obj_center.y, map, quest_item)
                        for item_type in ITEM_TYPE_LIST:
                            if quest_item in eval(item_type.upper()):
                                Dropped_Item(self, obj_center, item_type, quest_item)
                # Loads items/npcs that should only be there if a quest hasn't been completed
                if 'QU' in tile_object.name:
                    _, quest, quest_item = tile_object.name.split('_')
                    if not self.quests[quest]['completed']:
                        if quest_item in VEHICLES:
                            Vehicle(self, obj_center, quest_item, map)
                        if quest_item in ANIMALS:
                            Animal(self, obj_center.x, obj_center.y, map, quest_item)
                        if quest_item in self.people:
                            if self.is_living(quest_item):
                                Npc(self, obj_center.x, obj_center.y, map, quest_item)
                        for item_type in ITEM_TYPE_LIST:
                            if quest_item in eval(item_type.upper()):
                                Dropped_Item(self, obj_center, item_type, quest_item)
                # Loads items/npcs that only appear after a quest has been accepted.
                if 'QA' in tile_object.name:
                    _, quest, quest_item = tile_object.name.split('_')
                    if self.quests[quest]['accepted']:
                        if quest_item in VEHICLES:
                            Vehicle(self, obj_center, quest_item, map)
                        if quest_item in ANIMALS:
                            Animal(self, obj_center.x, obj_center.y, map, quest_item)
                        if quest_item in self.people:
                            if self.is_living(quest_item):
                                Npc(self, obj_center.x, obj_center.y, map, quest_item)
                        for item_type in ITEM_TYPE_LIST:
                            if quest_item in eval(item_type.upper()):
                                Dropped_Item(self, obj_center, item_type, quest_item)
                # Loads items/npcs that should only be there if a quest hasn't been accepted
                if 'QN' in tile_object.name:
                    _, quest, quest_item = tile_object.name.split('_')
                    if not self.quests[quest]['accepted']:
                        if quest_item in VEHICLES:
                            Vehicle(self, obj_center, quest_item, map)
                        if quest_item in ANIMALS:
                            Animal(self, obj_center.x, obj_center.y, map, quest_item)
                        if quest_item in self.people:
                            if self.is_living(quest_item):
                                Npc(self, obj_center.x, obj_center.y, map, quest_item)
                        for item_type in ITEM_TYPE_LIST:
                            if quest_item in eval(item_type.upper()):
                                Dropped_Item(self, obj_center, item_type, quest_item)
                if 'COMMAND' in tile_object.name: # I used this block of code for killing Alex's body: the character that the black wraith comes out of in the beginning.
                    _, command, npc = tile_object.name.split('_')
                    if npc != 'None':
                        if self.is_living(npc):
                            temp_npc = Npc(self, obj_center.x, obj_center.y, map, npc)
                            if command == 'kill':
                                temp_npc.death()
                if tile_object.name == 'fire':
                    Stationary_Animated(self, obj_center, 'fire')
                if tile_object.name == 'shock':
                    Stationary_Animated(self, obj_center, 'shock')
                if tile_object.name == 'charger':
                    Charger(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                if tile_object.name == 'portal':
                    self.portal_location = obj_center
                if 'firepot' in tile_object.name:
                    number = tile_object.name[-1:]
                    FirePot(self, obj_center, number)
                if tile_object.name == 'wall':
                    Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                if tile_object.name == 'light':
                    LightSource(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
                if 'lightsource' in tile_object.name:
                    numvars = tile_object.name.count('_')
                    if numvars == 2:
                        _, kind, rot = tile_object.name.split('_')
                    elif numvars == 1:
                        _, kind = tile_object.name.split('_')
                        rot = 0
                    kind = int(kind)
                    if rot == 'R':
                        rot = 0
                    elif rot == 'U':
                        rot = 90
                    elif rot == 'L':
                        rot = 180
                    elif rot == 'D':
                        rot = 270
                    else:
                        rot = int(rot)
                    LightSource(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height, kind, rot)
                if tile_object.name == 'inside':
                    Inside(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
                if tile_object.name == 'nospawn':
                    NoSpawn(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
                if tile_object.name == 'water':
                    Water(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
                if tile_object.name == 'shallows':
                    Shallows(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
                if tile_object.name == 'long grass':
                    LongGrass(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
                if tile_object.name == 'lava':
                    Lava(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
                if tile_object.name in ['grinder', 'forge', 'workbench', 'tanning rack', 'cooking fire', 'enchanter', 'alchemy lab', 'smelter']:
                    Work_Station(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.name)
                if 'chest' in tile_object.name:
                    spawn_chest = True
                    for container in self.containers:
                        if container.name == tile_object.name:
                            spawn_chest = False
                    if spawn_chest:
                        Chest(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.name)
                if 'bed' in tile_object.name:
                    Bed(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height, tile_object.name)
                if 'toilet' in tile_object.name:
                    Toilet(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
                if tile_object.name == 'electric entry':
                    ElectricDoor(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                if 'entryway' in tile_object.name:  # Used for animated doors that can be opened, closed or locked.
                    numvars = tile_object.name.count('_')
                    if numvars == 0:
                        entryway = Entryway(self, tile_object.x, tile_object.y)
                    elif numvars == 1:
                        _, orientation  = tile_object.name.split('_')
                        entryway = Entryway(self, tile_object.x, tile_object.y, orientation)
                    elif numvars == 2:
                        _, orientation, kind  = tile_object.name.split('_')
                        entryway = Entryway(self, tile_object.x, tile_object.y, orientation, kind)
                    elif numvars == 3:
                        _, orientation, kind, name = tile_object.name.split('_')
                        locked = eval(locked)
                        entryway = Entryway(self, tile_object.x, tile_object.y, orientation, kind, name)
                    elif numvars == 4:
                        _, orientation, kind, name, locked = tile_object.name.split('_')
                        locked = eval(locked)
                        entryway = Entryway(self, tile_object.x, tile_object.y, orientation, kind, name, locked)
                if 'door' in tile_object.name:  # This block of code positions the player at the correct door when changing maps
                    door = Door(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height, tile_object.name)
                    if self.previous_map[3:][:-4] == door.name[4:]:
                        # This sets up the direction vector which has x and y values of 1 but the signs tell what direction the player was last heading. So the player will appear on the correct side of the door.
                        direction_x = vec(self.player.direction.x, 0).normalize()
                        direction_y = vec(0, self.player.direction.y).normalize()
                        direction_vector = vec(direction_x.x, direction_y.y)
                        if door.rect.width > 512: # For wide doors/connection points to other maps. This makes it so the player appears in the correct x position on the map
                            self.player.pos.y = door.rect.y + (direction_vector.y * 128)
                            self.player.rect.center = self.player.pos
                        elif door.rect.height > 512: # For wide doors/connection points to other maps. This makes it so the player appears in the correct y position on the map
                            self.player.pos.x = door.rect.x + (direction_vector.x * 128)
                            self.player.rect.center = self.player.pos
                        else:
                            self.player.pos = vec(obj_center) + direction_vector * 64
                            self.player.rect.center = self.player.pos

                try:
                    if 'maptype' in tile_object.name:
                        self.map_type = tile_object.name[8:]
                except:
                    pass

        # Generates random drop items
        if self.map_type in ['mountain', 'forest', 'grassland', 'desert', 'beach']:
            for i in range(0, randrange(1, 15)):
                for item in ITEMS:
                    if 'random drop' in ITEMS[item].keys():
                        if randrange(0, ITEMS[item]['random drop']) < 2:
                            centerx = randrange(200, self.map.width - 200)
                            centery = randrange(200, self.map.height - 200)
                            center = vec(centerx, centery)
                            Dropped_Item(self, center, 'items', item)

        # Generates random animals/Npcs on maps that don't have existing animals on them. The type of animal depends on the maptype object in the tmx file.
        if (len(self.mobs) - len(self.companions)) < 4:
            if self.map_type:
                for i in range(0, randrange(10, 30)):
                    animal = choice(list(eval(self.map_type.upper() + '_ANIMALS')))
                    centerx = randrange(200, self.map.width - 200)
                    centery = randrange(200, self.map.height - 200)
                    if animal in self.people:
                        npc = Npc(self, centerx, centery, map, animal)
                        # check for NPCs that spawn in walls and kills them
                        hits = pg.sprite.spritecollide(npc, self.walls, False)
                        if hits:
                            npc.kill()

                    else:
                        anim = Animal(self, centerx, centery, map, animal)
                        # checks for animals that spawn in walls and kills them.
                        hits = pg.sprite.spritecollide(anim, self.walls, False)
                        if hits:
                            anim.kill()

        # Generates random ores, trees and plants
        if len(self.breakable) < 1:
            if self.map_type:
                if self.map_type in ['mountain', 'forest']:
                    if self.map_type == 'mountain':
                        rand_range = randrange(4, 7)
                        rand_trees = randrange(8, 12)
                    if self.map_type == 'forest':
                        rand_range = randrange(1, 3)
                        rand_trees = randrange(80, 160)
                    for i in range(0, rand_range):
                        vein = choice(VEIN_LIST)
                        centerx = randrange(200, self.map.width - 200)
                        centery = randrange(200, self.map.height - 200)
                        object_width = object_height = 100
                        objectx = int(centerx - object_width / 2)
                        objecty = int(centery - object_height / 2)
                        center = vec(centerx, centery)
                        Breakable(self, center, object_width, object_height, vein, map)
                    for i in range(0, rand_trees):
                        tree = choice(TREE_LIST)
                        centerx = randrange(200, self.map.width - 200)
                        centery = randrange(200, self.map.height - 200)
                        object_width = object_height = 100
                        objectx = int(centerx - object_width / 2)
                        objecty = int(centery - object_height / 2)
                        center = vec(centerx, centery)
                        Breakable(self, center, object_width, object_height, tree, map)
                if self.map_type in ['mountain', 'forest', 'grassland']:
                    if self.map_type == 'forest':
                        rand_plants = randrange(50, 200)
                    else:
                        rand_plants = randrange(15, 35)
                    for i in range(0, rand_plants):
                        plant = choice(PLANT_LIST)
                        centerx = randrange(200, self.map.width - 200)
                        centery = randrange(200, self.map.height - 200)
                        object_width = object_height = 100
                        objectx = int(centerx - object_width / 2)
                        objecty = int(centery - object_height / 2)
                        center = vec(centerx, centery)
                        Breakable(self, center, object_width, object_height, plant, map)
                if self.map_type in ['beach']:
                    rand_plants = randrange(15, 35)
                    for i in range(0, rand_plants):
                        tree = choice(BEACH_PLANT_LIST)
                        centerx = randrange(200, self.map.width - 200)
                        centery = randrange(200, self.map.height - 200)
                        object_width = object_height = 100
                        objectx = int(centerx - object_width / 2)
                        objecty = int(centery - object_height / 2)
                        center = vec(centerx, centery)
                        Breakable(self, center, object_width, object_height, tree, map)
                if self.map_type in ['tundra']:
                    rand_plants = randrange(10, 25)
                    for i in range(0, rand_plants):
                        tree = 'pine tree'
                        centerx = randrange(200, self.map.width - 200)
                        centery = randrange(200, self.map.height - 200)
                        object_width = object_height = 100
                        objectx = int(centerx - object_width / 2)
                        objecty = int(centery - object_height / 2)
                        center = vec(centerx, centery)
                        Breakable(self, center, object_width, object_height, tree, map)
        # Kills breakables that spawn in water or no spawn areas.
        hits = pg.sprite.groupcollide(self.breakable, self.water, False, False)
        for hit in hits:
            hit.trunk.kill()
            hit.kill()
        hits = pg.sprite.groupcollide(self.breakable, self.shallows, False, False)
        for hit in hits:
            hit.trunk.kill()
            hit.kill()
        hits = pg.sprite.groupcollide(self.breakable, self.nospawn, False, False)
        for hit in hits:
            hit.trunk.kill()
            hit.kill()
        hits = pg.sprite.groupcollide(self.breakable, self.long_grass, False, False)
        for hit in hits:
            hit.trunk.kill()
            hit.kill()


        # check for fish out of water and kills them
        hits = pg.sprite.groupcollide(self.animals, self.water, False, False)
        for animal in self.animals:
            if 'fish' in animal.kind['name']:
                if animal not in hits:
                    animal.death(True)
            if 'shark' in animal.kind['name']:
                if animal not in hits:
                    animal.death(True)

        # Adds all players and companions
        #self.group.add(self.player.body)
        #for sprite in self.companions:
        #    if sprite not in self.animals:
        #        self.group.add(sprite.body)
        #    else:
        #        self.group.add(sprite)
        # Adds vehicles back to group
        #if self.player.in_vehicle:
        #    self.group.add(self.player.vehicle)
        #    if self.player.vehicle.cat == 'tank':
        #        self.group.add(self.player.vehicle.turret)
        self.sprite_data.visited = True
        self.previous_map = map
        self.respawn = False
        if self.new_game:
            self.new_game = False

        # Starts music based on map
        if self.map_type == None:
            self.bg_music = BG_MUSIC
        else:
            self.bg_music = eval(self.map_type.upper() + '_MUSIC')
        if self.bg_music != self.previous_music: #Only starts new music if type of map changes
            self.previous_music = self.bg_music
            pg.mixer.music.fadeout(300)
            pg.mixer.music.load(path.join(music_folder, self.bg_music))
            pg.mixer.music.play(loops=-1)

        # sets up NPC target list for map
        self.target_list = [self.random_targets, self.entryways, self.work_stations, self.moving_targets, self.aipaths]
        for x in self.target_list:  # Replaces empty sprite groups with the random targets group.
            if list(x) == []:
                x = self.random_targets

        self.clock.tick(FPS)  # resets dt


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        self.beg = perf_counter()
        while self.playing:
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def night_transition(self):
        now = pg.time.get_ticks()
        if now - self.last_darkness_change > NIGHTFALL_SPEED:
            self.darkness += 1
            self.last_darkness_change = now
            if self.darkness > MAX_DARKNESS:
                self.darkness = MAX_DARKNESS
                self.day_start_time = now
                self.night = True
                self.nightfall = False
            #color_val = 255 - self.darkness
            self.dark_color = (self.darkness, self.darkness, self.darkness)

    def day_transition(self):
        now = pg.time.get_ticks()
        if now - self.last_darkness_change > NIGHTFALL_SPEED:
            self.darkness -= 1
            if self.darkness < 0:
                self.darkness = 0
                self.day_start_time = now
                self.night = False
                self.sunrise = False
            #color_val = 255 - self.darkness
            self.dark_color = (self.darkness, self.darkness, self.darkness)

    def update(self):
        # update portion of the game loop

        # Controls the day turning to night and vice versa
        now = pg.time.get_ticks()
        if self.night:
            if now - self.day_start_time > NIGHT_LENGTH:
                self.sunrise = True
                self.day_transition()
        elif now - self.day_start_time > DAY_LENGTH:
            self.nightfall = True
            self.night_transition()
        if now - self.last_mobhp_update > MOB_HEALTH_SHOW_TIME: # Turns off mob hp bar if when you aren't attacking the mob.
            self.show_mobhp = False

        # updates all sprites that are on screen and puts on screen sprites into groups for hit checks.
        self.message_text = False
        # finds static sprites (ones you don't see) on screen.
        self.obstacles_on_screen.empty()
        self.walls_on_screen.empty()
        self.barriers_on_screen.empty()
        self.water_on_screen.empty()
        self.shallows_on_screen.empty()
        self.long_grass_on_screen.empty()
        self.lava_on_screen.empty()
        self.elevations_on_screen.empty()
        self.climbs_on_screen.empty()
        self.beds_on_screen.empty()
        self.inside_on_screen.empty()
        for sprite in self.all_static_sprites:
            if self.on_screen(sprite, 400):
                if sprite in self.obstacles:
                    self.obstacles_on_screen.add(sprite)
                    if sprite in self.walls:
                        self.walls_on_screen.add(sprite)
                        self.barriers_on_screen.add(sprite)
                    elif sprite in self.water:
                        self.water_on_screen.add(sprite)
                    elif sprite in self.shallows:
                        self.shallows_on_screen.add(sprite)
                    elif sprite in self.lava:
                        self.lava_on_screen.add(sprite)
                elif sprite in self.elevations:
                    self.elevations_on_screen.add(sprite)
                    self.barriers_on_screen.add(sprite)
                    if sprite in self.beds:
                        self.beds_on_screen.add(sprite)
                    if sprite in self.climbs:
                        self.climbs_on_screen.add(sprite)
                elif sprite in self.inside:
                    self.inside_on_screen.add(sprite)
                elif sprite in self.long_grass:
                    self.long_grass_on_screen.add(sprite)


        # dynamic sprites on screen
        self.vehicles_on_screen.empty()
        self.entryways_on_screen.empty()
        self.electric_doors_on_screen.empty()
        self.breakable_on_screen.empty()
        self.corpses_on_screen.empty()
        self.dropped_items_on_screen.empty()
        self.fires_on_screen.empty()
        self.mobs_on_screen.empty()
        self.npcs_on_screen.empty()
        self.npc_bodies_on_screen.empty()
        self.animals_on_screen.empty()
        self.moving_targets_on_screen.empty()
        self.sprites_on_screen.empty()
        for sprite in self.all_sprites:
            if self.on_screen(sprite):
                self.sprites_on_screen.add(sprite)
                if sprite in self.entryways:
                    self.entryways_on_screen.add(sprite)
                    if sprite in self.electric_doors:
                        self.electric_doors_on_screen.add(sprite)
                elif sprite in self.vehicles:
                    self.vehicles_on_screen.add(sprite)
                    if sprite in self.walls:
                        self.walls_on_screen.add(sprite)
                elif sprite in self.fires:
                    self.fires_on_screen.add(sprite)
                elif sprite in self.breakable:
                        self.breakable_on_screen.add(sprite)
                elif sprite in self.corpses:
                        self.corpses_on_screen.add(sprite)
                elif sprite in self.dropped_items:
                        self.dropped_items_on_screen.add(sprite)
                elif sprite in self.npc_bodies:
                    self.npc_bodies_on_screen.add(sprite)
                elif sprite in self.moving_targets:
                    self.moving_targets_on_screen.add(sprite)
                    if sprite in self.mobs:
                        self.mobs_on_screen.add(sprite)
                        if sprite in self.animals:
                            self.animals_on_screen.add(sprite)
                        elif sprite in self.npcs:
                            self.npcs_on_screen.add(sprite)
            elif sprite in self.bullets: # Kills bullets not on screen.
                sprite.kill()
            elif sprite == self.player.vehicle:
                sprite.update()
            elif sprite in self.companions:
                sprite.update()
            elif sprite in self.companion_bodies:
                sprite.update()
        self.sprites_on_screen.update()
        self.camera.update(self.player)
        self.group.center(self.player.rect.center)

        # Used for playing fire sounds at set distances:
        closest_fire = None
        previous_distance = 30000
        for sprite in self.fires_on_screen:    # Finds the closest fire and ignores the others.
            player_dist = self.player.pos - sprite.pos
            player_dist = player_dist.length()
            if previous_distance > player_dist:
                closest_fire = sprite
                previous_distance = player_dist

        if closest_fire:
            if previous_distance < 400:  # This part makes it so the fire volume decreases as you walk away from it.
                volume = 150 / (previous_distance * 2 + 0.001)
                self.channel4.set_volume(volume)
                if not self.channel4.get_busy():
                    self.channel4.play(self.effects_sounds['fire crackle'], loops=-1)
            else:
                self.channel4.stop()
        else:
            self.channel4.stop()

        # These hit checks only happen if the player insn't in a flying vehicle.
        if self.player not in self.flying_vehicles:
            # player hits portal
            hits = pg.sprite.spritecollide(self.player, self.portals, False, pg.sprite.collide_circle_ratio(0.35))
            if hits:
                now = pg.time.get_ticks()
                if now - hits[0].spawn_time > 1500: # Makes it so you can see the portal appear before it transfers you to a new map
                    self.change_map(None, hits[0].coordinate, hits[0].location)

            # player hits door
            hits = pg.sprite.spritecollide(self.player, self.doors, False)
            if hits:
                # Sets player's location on local map
                loc = hits[0].loc
                self.player.rect.center = (int(loc.x * 128), int(loc.y * 128))
                self.player.pos = vec(self.player.rect.center)
                self.change_map(None, None, None, hits[0].map)

            # player hits charger
            hits = pg.sprite.spritecollide(self.player, self.chargers, False)
            if hits:
                if 'mechanima' in self.player.race:
                    hits[0].charge(self.player)

            # player hits bed
            hits = pg.sprite.spritecollide(self.player, self.beds_on_screen, False, pg.sprite.collide_rect_ratio(0.5))
            if hits:
                self.message_text = True
                if hits[0].name == 'bed':
                    if hits[0].cost > 0:
                        if self.player.inventory['gold'] >= hits[0].cost:
                            self.message = 'Press ' + pg.key.name(self.key_map['interact']).upper() + ' to pay ' + str(hits[0].cost) + ' gold to sleep in bed.'
                            if self.e_down:
                                self.player.inventory['gold'] -= hits[0].cost
                                self.effects_sounds['cashregister'].play()
                                self.sleep_in_bed()
                                self.message_text = False
                                self.e_down = False
                        else:
                            self.message = 'You cannot afford this bed.'
                    else:
                        self.message = 'Press ' + pg.key.name(self.key_map['interact']).upper() + ' to sleep in bed.'
                        if self.e_down:
                            self.sleep_in_bed()
                            self.message_text = False
                            self.e_down = False
                else:
                    self.message = 'You can not sleep in ' + hits[0].name + '.'

            # player hits toilet
            hits = pg.sprite.spritecollide(self.player, self.toilets, False, pg.sprite.collide_rect_ratio(0.40))
            if hits:
                self.message_text = True
                self.message = pg.key.name(self.key_map['interact']).upper() + ' to use toilet'
                if self.e_down:
                    self.use_toilet()
                    self.message_text = False
                    self.e_down = False

            # player hit corps
            hits = pg.sprite.spritecollide(self.player, self.corpses_on_screen, False)
            if hits:
                self.message_text = True
                self.message = pg.key.name(self.key_map['interact']).upper() + " to loot"
                if self.e_down:
                    if not self.in_loot_menu:
                        self.in_loot_menu = True
                        self.in_menu = True
                        self.loot_menu = Loot_Menu(self, hits[0])
                        self.message_text = False

            # player melee hits entryway (door)
            if self.player.melee_playing:
                hits = pg.sprite.spritecollide(self.player.body, self.entryways_on_screen, False, melee_hit_rect)
                if hits:
                    if hits[0] in self.electric_doors_on_screen:
                        hits[0].gets_hit(40, 0, 0, 100, self.player)
                    else:
                        self.player.does_melee_damage(hits[0])

            # player hits entryway (a door)
            hits = pg.sprite.spritecollide(self.player, self.entryways_on_screen, False, entryway_collide)
            if hits:
                self.message_text = True
                if hits[0].locked:
                    self.message = hits[0].name + ' is locked. ' + pg.key.name(self.key_map['interact']).upper() + ' to unlock'
                    if self.e_down:
                        if not self.in_lock_menu:
                            self.in_lock_menu = self.in_menu = True
                            self.lock_menu = Lock_Menu(self, hits[0])
                            self.message_text = False
                        self.e_down = False
                elif not hits[0].opened:
                    self.message = pg.key.name(self.key_map['interact']).upper() + ' to open'
                    if self.e_down:
                        hits[0].open = True
                        hits[0].close = False
                        self.message_text = False
                        self.e_down = False
                elif hits[0].opened:
                    self.message = pg.key.name(self.key_map['interact']).upper() + ' to close'
                    if self.e_down:
                        hits[0].close = True
                        hits[0].open = False
                        self.message_text = False
                        self.e_down = False

            # player hit container
            hits = pg.sprite.spritecollide(self.player, self.containers, False)
            if hits:
                if not hits[0].inventory['locked']:
                    self.message_text = True
                    self.message = pg.key.name(self.key_map['interact']).upper() + ' to open'
                    if self.e_down:
                        if not self.in_loot_menu:
                            if hits[0] in self.chest_containers:
                                self.effects_sounds['door open'].play()
                            self.in_loot_menu = True
                            self.loot_menu = Loot_Menu(self, hits[0])
                        self.message_text = False
                        self.e_down = False
                else:
                    self.message_text = True
                    self.message = pg.key.name(self.key_map['interact']).upper() + ' to unlock'
                    if self.e_down:
                        if not self.in_lock_menu:
                            self.in_lock_menu = self.in_menu = True
                            self.lock_menu = Lock_Menu(self, hits[0])
                        self.message_text = False
                        self.e_down = False


            # Player is in talking range of NPC
            if True not in [self.message_text, self.in_menu]:
                hits = pg.sprite.spritecollide(self.player, self.npcs_on_screen, False, npc_talk_rect)
                if hits:
                    if hits[0].dialogue:
                        if not self.in_dialogue_menu:
                            now = pg.time.get_ticks()
                            if now - self.last_dialogue > 2000:
                                self.message_text = True
                                self.message = pg.key.name(self.key_map['interact']).upper() + ' to talk'
                                if self.e_down:
                                    hits[0].target = self.player
                                    hits[0].talk_attempt = True
                                    self.message_text = False
                                    self.e_down = False
            if self.dialogue_menu_npc:
                self.dialogue_menu = Dialogue_Menu(self, self.dialogue_menu_npc)

            # player hits work station (forge, grinder, work bench, etc)
            hits = pg.sprite.spritecollide(self.player, self.work_stations, False)
            if hits:
                self.station_type = hits[0].kind
                self.message_text = True
                self.message = pg.key.name(self.key_map['interact']).upper() + ' to use ' + self.station_type
                if self.e_down:
                    self.in_station_menu = True
                    self.in_menu = True
                    self.station_menu = Work_Station_Menu(self, hits[0].kind)
                    self.message_text = False
                    self.e_down = False

            # player hits water
            hits = pg.sprite.spritecollide(self.player, self.water_on_screen, False)
            if hits:
                if not pg.sprite.spritecollide(self.player, self.long_grass_on_screen, False):
                    self.player.swimming = True
                else:
                    self.player.swimming = False
            else:
                self.player.swimming = False

            # player hits shallows
            hits = pg.sprite.spritecollide(self.player, self.shallows_on_screen, False)
            if hits:
                self.player.in_shallows = True
            else:
                self.player.in_shallows = False

            # player hits long grass
            hits = pg.sprite.spritecollide(self.player, self.long_grass_on_screen, False)
            if hits:
                self.player.in_grass = True
            else:
                self.player.in_grass = False

            # player hits elevation change
            hits = pg.sprite.spritecollide(self.player, self.elevations_on_screen, False)
            if hits:
                keys = pg.key.get_pressed()
                if keys[self.key_map['climb']]:
                    if self.player.stats['stamina'] > 10 and not self.player.in_vehicle:
                        self.player.climbing = True
                    else:
                        if self.player.in_vehicle:
                            if 'climbables' not in self.player.vehicle.collide_list:
                                if 'obstacles' not in self.player.vehicle.collide_list:
                                    self.player.climbing = True
            else:
                self.player.climbing = False
                if not self.player.jumping:
                    if self.player.elevation > 1:
                        self.player.falling = True
                        self.player.pre_jump()
                    self.player.elevation = 0


            # player hits dropped item
            hits = pg.sprite.spritecollide(self.player, self.dropped_items_on_screen, False, pg.sprite.collide_circle_ratio(0.75))
            for hit in hits:
                if hit.name not in ['fire pit']:
                    self.message_text = True
                    if self.message != "You are carrying too much weight.":
                        self.message = pg.key.name(self.key_map['interact']).upper() + 'to pick up'
                    if self.e_down:
                        self.player.inventory[hit.item_type].append(hit.item)
                        self.player.calculate_weight()
                        self.e_down = False
                        if self.player.stats['weight'] > self.player.stats['max weight']:
                            self.player.inventory[hit.item_type].remove(hit.item)
                            self.player.calculate_weight()
                            self.message = "You are carrying too much weight."
                        else:
                            self.message_text = False
                            hit.kill()

            # player melee hits breakable: a bush, tree, rock, ore vein, shell, glass, etc.
            if self.player.melee_playing:
                hits = pg.sprite.spritecollide(self.player.body, self.breakable_on_screen, False, breakable_melee_hit_rect)
                for bush in hits:
                    if self.player.equipped[self.player.weapon_hand] == None:
                        weapon_type = None
                    else:
                        weapon_type = WEAPONS[self.player.equipped[self.player.weapon_hand]]['type']
                        if not self.player.change_used_item('weapons', self.player.equipped[self.player.weapon_hand]): # Makes it so pickaxes and other items deplete their hp
                            weapon_type = None
                    bush.gets_hit(weapon_type)

            # moving target hits lava
            hits = pg.sprite.groupcollide(self.moving_targets_on_screen, self.lava_on_screen, False, False)
            for hit in hits:
                for lava in hits[hit]:
                    if not (hit.jumping or hit.flying):
                        hit.gets_hit(lava.damage, 0, 0)
                        now = pg.time.get_ticks()
                        if now - self.last_fire > 300:
                            pos = hit.pos + vec(-1, -1)
                            self.effects_sounds['fire blast'].play()
                            Stationary_Animated(self, hit.pos, 'fire', 3000)
                            Stationary_Animated(self, pos, 'fire', 1000)
                            self.last_fire = now

            # moving target hits electric door
            hits = pg.sprite.groupcollide(self.moving_targets_on_screen, self.electric_doors_on_screen, False, False)
            for hit in hits:
                if hit.race not in ['mechanima', 'mechanima dragon', 'mech_suit']:
                    for edoor in hits[hit]:
                        if not (hit.jumping or hit.flying):
                            hit.gets_hit(edoor.damage, 0, 50)
                            now = pg.time.get_ticks()
                            if now - self.last_fire > 300:
                                pos = hit.pos + vec(-1, -1)
                                self.effects_sounds['fire blast'].play()
                                Stationary_Animated(self, hit.pos, 'fire', 3000)
                                Stationary_Animated(self, pos, 'fire', 1000)
                                self.last_fire = now
                else:
                    hit.add_health(0.02)

            # NPC hit player
            hits = pg.sprite.spritecollide(self.player, self.npcs_on_screen, False, pg.sprite.collide_circle_ratio(0.7))
            for hit in hits:
                self.player.hit_rect.centerx = self.player.pos.x
                collide_with_walls(self.player, [hit], 'x')
                self.player.hit_rect.centery = self.player.pos.y
                collide_with_walls(self.player, [hit], 'y')
                self.player.rect.center = self.player.hit_rect.center
                if hit.touch_damage:
                    if random() < 0.7:
                        self.player.gets_hit(hit.damage, hit.knockback, hits[0].rot)

            # player hits empty vehicle or mech suit
            if not self.player.in_vehicle:
                if self.player.possessing == None:
                    hits = pg.sprite.spritecollide(self.player, self.mechsuits, False)
                    if hits:
                        if (hits[0].driver == None) and hits[0].living:
                            self.message_text = True
                            self.message = pg.key.name(self.key_map['interact']).upper() + " to enter, T to exit"
                        if self.e_down:
                            if hits[0].living:
                                hits[0].possess(self.player)
                            self.message_text = False
                            self.e_down = False

                hits = pg.sprite.spritecollide(self.player, self.vehicles_on_screen, False, pg.sprite.collide_circle_ratio(0.95))
                if hits:
                    if not hits[0].occupied and hits[0].living:
                        self.message_text = True
                        self.message = pg.key.name(self.key_map['interact']).upper() + ' to enter, ' + pg.key.name(self.key_map['dismount']).upper() + ' to exit'
                    if self.e_down:
                        if hits[0].living:
                            hits[0].enter_vehicle(self.player)
                        self.message_text = False
                        self.e_down = False
                hits = pg.sprite.spritecollide(self.player, self.flying_vehicles, False)
                if hits:
                    if not hits[0].occupied and hits[0].living:
                        self.message_text = True
                        if self.message != "You need a key to operate this vehicle.":
                            self.message = pg.key.name(self.key_map['interact']).upper() + ' to enter, ' + pg.key.name(self.key_map['dismount']).upper() + ' to exit'
                    if self.e_down:
                        self.e_down = False
                        if hits[0].living:
                            if hits[0].kind == 'airship':
                                if 'airship key' in self.player.inventory['items']:
                                    hits[0].enter_vehicle(self.player)
                                    self.message_text = False
                                elif len(self.companions.sprites()) > 0:
                                    self.message_text = False
                                    is_felius = False
                                    for companion in self.companions:
                                        if companion.name == 'Felius':
                                            is_felius = True
                                    if is_felius:
                                        hits[0].enter_vehicle(self.player)
                                else:
                                    self.message = "You need a key to operate this vehicle."
                            else:
                                hits[0].enter_vehicle(self.player)
        else:
            self.player.swimming = False
            self.player.in_shallows = False
            self.player.in_grass = False


        # These hit checks apply whether the player is in a flying vehicle or not.

        # Animal hit player
        hits = pg.sprite.spritecollide(self.player, self.animals, False, pg.sprite.collide_circle_ratio(0.7))
        if self.player not in self.flying_vehicles:
            for hit in hits:
                if not hit.occupied:
                    if hit in self.grabable_animals:
                        self.message_text = True
                        self.message = pg.key.name(self.key_map['interact']).upper() + ' to catch'
                        if self.e_down:
                            self.player.inventory[hit.item_type].append(hit.item)
                            hit.kill()
                            self.message_text = False
                            self.e_down = False
                    elif hit.mountable:
                        self.message_text = True
                        self.message = pg.key.name(self.key_map['interact']).upper() + ' to mount, ' + pg.key.name(self.key_map['dismount']).upper() + ' to dismount'
                        if self.e_down:
                            hit.mount(self.player)
                            self.message_text = False
                            self.e_down = False
                    elif hit.touch_damage:
                         hit.does_melee_damage(self.player)
                    else:
                        self.player.gets_hit(0, hit.knockback, hits[0].rot)

        else:  # Makes it so flying animals still interact with flying players
            for hit in hits:
                if hit.flying:
                    if not hit.occupied:
                        if hit in self.grabable_animals:
                            self.message_text = True
                            self.message = pg.key.name(self.key_map['interact']).upper() + ' to catch'
                            if self.e_down:
                                self.player.inventory[hit.item_type].append(hit.item)
                                hit.kill()
                                self.message_text = False
                                self.e_down = False
                        elif hit.mountable:
                            self.message_text = True
                            self.message = pg.key.name(self.key_map['interact']).upper() + ' to mount, ' + pg.key.name(self.key_map['dismount']).upper() + ' to dismount'
                            if self.e_down:
                                hit.mount(self.player)
                                self.message_text = False
                                self.e_down = False
                        if hit.touch_damage:
                            hit.does_melee_damage(self.player)
                        else:
                            self.player.gets_hit(0, hit.knockback, hits[0].rot)

        # animal hits mob
        hits = pg.sprite.groupcollide(self.animals, self.mobs_on_screen, False, False, pg.sprite.collide_circle_ratio(0.7))
        for animal in hits:
            for mob in hits[animal]:
                if mob != animal:
                    if animal.touch_damage:
                        if animal.kind != mob.kind:
                            animal.does_melee_damage(mob)

        # mob hit elevation object
        hits = pg.sprite.groupcollide(self.mobs_on_screen, self.elevations_on_screen, False, False)
        for mob in self.mobs_on_screen:
            if mob in hits:
                for elev in hits[mob]: # Makes it so NPCs can climb and jump.
                    if elev.elevation - mob.elevation > 2:
                        if (not mob.flying) and (mob in self.animals_on_screen):
                            mob.hit_wall = True
                            mob.last_wall_hit = pg.time.get_ticks()
                            mob.seek_random_target()
                        elif (mob in self.companions) or mob.target == self.player:
                            mob.running = False
                            mob.climbing = True
                            mob.last_climb = pg.time.get_ticks()
                        elif mob in self.npcs_on_screen:
                            chance = randrange(0, 600)
                            if chance == 1:
                                mob.climbing = True
                            else:
                                mob.hit_wall = True
                                mob.last_wall_hit = pg.time.get_ticks()
                                mob.seek_random_target()
                    elif elev.elevation - mob.elevation > 1:
                        if (not mob.flying) and (mob in self.animals_on_screen):
                            mob.hit_wall = True
                        elif (mob in self.companions) or mob.target == self.player:
                            mob.jumping = True
                            mob.last_climb = pg.time.get_ticks()
                        elif mob in self.npcs_on_screen:
                            chance = randrange(0, 200)
                            if chance == 1:
                                mob.jumping = True
                            else:
                                mob.hit_wall = True
                                mob.last_wall_hit = pg.time.get_ticks()
                                mob.seek_random_target()
            else:
                mob.climbing = False
                if not mob.jumping:
                    if mob.elevation > 1:
                        mob.falling = True
                        mob.pre_jump()
                    mob.elevation = 0

        # vehicle hit breakable
        hits = pg.sprite.groupcollide(self.breakable_on_screen, self.vehicles_on_screen, False, False, vehicle_collide_any)
        for breakable in hits:
           for vehicle in hits[breakable]:
               if not vehicle.flying:
                    breakable.gets_hit(vehicle.cat, 0, 0, 0)

        # explosion hit breakable
        hits = pg.sprite.groupcollide(self.breakable_on_screen, self.explosions, False, False, pg.sprite.collide_circle_ratio(0.5))
        for breakable in hits:
            for exp in hits[breakable]:
                if exp.damage > 200:
                    breakable.gets_hit('explosion', 0, 0, 0)

        # NPC hits charger
        hits = pg.sprite.groupcollide(self.npcs_on_screen, self.chargers, False, False)
        for npc in hits:
            if npc.race in ['mechanima', 'mech_suit']:
                hits[npc][0].charge(npc)

        # NPC or Player melee hits moving_target
        hits = pg.sprite.groupcollide(self.npc_bodies_on_screen, self.moving_targets_on_screen, False, False, melee_hit_rect)
        for body in hits:
            if body.mother.in_player_vehicle:
                pass
            for mob in hits[body]:
                if mob.immaterial:
                    if body.mother.equipped[body.mother.weapon_hand]:
                        if ('aetherial' not in body.mother.equipped[body.mother.weapon_hand]) or ('plasma' not in body.mother.equipped[body.mother.weapon_hand]):
                            continue
                if mob.in_player_vehicle:
                    continue
                elif body.mother == mob:
                    continue
                elif mob in self.flying_vehicles:
                    continue
                elif mob.in_vehicle:
                    continue
                elif body.mother.in_vehicle: # Makes it so you can't attack your own vehicle
                    if mob == body.mother.vehicle:
                        continue
                if body.mother.melee_playing:
                    if body.mother == self.player:
                        if mob not in self.companions:
                            mob.offensive = True
                            mob.provoked = True
                    if body.mother == self.player.possessing:
                        if mob not in self.companions:
                            mob.offensive = True
                            mob.provoked = True
                    body.mother.does_melee_damage(mob)

        # fire hit moving target
        hits = pg.sprite.groupcollide(self.moving_targets, self.fires_on_screen, False, False, pg.sprite.collide_circle_ratio(0.5))
        for mob in hits:
            if mob in self.occupied_vehicles:
                pass
            elif mob.in_vehicle:
                pass
            elif mob.in_player_vehicle:
                pass
            else:
                if 'dragon' not in mob.race:
                    if 'wyvern' not in mob.race:
                        for fire in hits[mob]:
                            mob.gets_hit(fire.damage, 0, mob.rot - 180)

        # explosion hit moving target
        hits = pg.sprite.groupcollide(self.moving_targets, self.explosions, False, False, pg.sprite.collide_circle_ratio(0.5))
        for mob in hits:
            if mob in self.occupied_vehicles:
                pass
            elif mob.in_vehicle:
                pass
            elif mob.in_player_vehicle:
                pass
            else:
                for fire in hits[mob]:
                    mob.gets_hit(fire.damage, 0, mob.rot - 180)


        # fireball hit moving target
        hits = pg.sprite.groupcollide(self.moving_targets, self.fireballs, False, False, fire_collide)
        for mob in hits:
            for bullet in hits[mob]:
                if mob in self.occupied_vehicles:
                    if bullet.mother == mob.driver: # Ignores fireballs from driver
                        pass
                    elif bullet.mother in self.companions:
                        pass
                    elif mob.driver == self.player:
                        if bullet.mother in self.player_group:
                            pass
                        else: # When enemy fireballs hit vehicle player is in.
                            mob.gets_hit(bullet.damage, 0, bullet.rot)
                            bullet.explode(mob)
                    else: # When fireball hits non player vehicle
                        mob.gets_hit(bullet.damage, 0, bullet.rot)
                        bullet.explode(mob)
                elif bullet.mother != mob:
                    if not mob.in_player_vehicle:
                        if bullet.mother == self.player:
                            mob.provoked = True
                        mob.gets_hit(bullet.damage, bullet.knockback, bullet.rot)
                        bullet.explode(mob)
                        if bullet.mother == self.player:
                            self.player.stats['marksmanship hits'] += 1

        # fireball hits firepit
        hits = pg.sprite.groupcollide(self.firepits, self.fireballs, False, False, fire_collide)
        for item in hits:
            for bullet in hits[item]:
                if not item.lit:
                    bullet.explode(item)
                    item.lit = True
                    center = vec(item.rect.center)
                    Stationary_Animated(self, center, 'fire')
                    Work_Station(self, center.x - 64, center.y - 64, 128, 128, 'cooking fire')
        # fire hits firepit
        hits = pg.sprite.groupcollide(self.firepits, self.fires_on_screen, False, False, pg.sprite.collide_circle_ratio(0.5))
        for item in hits:
            if not item.lit:
                item.lit = True
                center = vec(item.rect.center)
                Stationary_Animated(self, center, 'fire')
                Work_Station(self, center.x - 64, center.y - 64, 128, 128, 'cooking fire')


        # bullets hit moving_target
        hits = pg.sprite.groupcollide(self.moving_targets, self.bullets, False, False, pg.sprite.collide_circle_ratio(0.5))
        for mob in hits:
            for bullet in hits[mob]:
                if mob in self.occupied_vehicles:
                    if bullet.mother == mob.driver: # Ignores bullet from driver that hit vehicle
                        pass
                    elif bullet.mother in self.companions:
                        pass
                    elif bullet.mother in self.turrets: # Ignores bullets from turrets of vehicle that's shooting
                        if bullet.mother.mother == mob:
                            pass
                    elif mob.driver == self.player:
                        if bullet.mother in self.player_group:
                            pass
                        else: # When enemy bullet hit vehicle player is in.
                            mob.gets_hit(bullet.damage, 0, bullet.rot)
                            bullet.death(mob)
                    else: # When bullet hits non player vehicle
                        mob.gets_hit(bullet.damage, 0, bullet.rot)
                        bullet.death(mob)
                elif bullet.mother != mob:
                    if not mob.immaterial or bullet.energy:
                        if not mob.in_player_vehicle:
                            if mob != self.player:
                                if bullet.mother == self.player: # Makes it so NPCs attack you if you shoot them.
                                    if mob.aggression in ['awd', 'sap', 'fup']:
                                        mob.offensive = True
                                        mob.provoked = True
                                    mob.gets_hit(bullet.damage, bullet.knockback, bullet.rot)
                                    self.hud_mobhp = mob.stats['health'] / mob.stats['max health']
                                    self.show_mobhp = True
                                    self.last_mobhp_update = pg.time.get_ticks()
                                    bullet.death(mob)
                                else:
                                    mob.gets_hit(bullet.damage, bullet.knockback, bullet.rot)
                                    bullet.death(mob)
                            else:
                                if not mob.immaterial or bullet.energy or (self.player.stats['weight'] != 0):
                                    if not mob.immaterial or bullet.energy:
                                        mob.gets_hit(bullet.damage, bullet.knockback, bullet.rot)
                                    bullet.death(mob)
                            if bullet.mother == self.player:
                                mob.provoked = True
                                self.player.stats['marksmanship hits'] += 1

        # fireball hits firepot
        hits = pg.sprite.groupcollide(self.firepots, self.fireballs, False, False, fire_collide)
        for pot in hits:
            pot.hit = True
            for bullet in hits[pot]:
                bullet.explode()
            self.player.stats['marksmanship hits'] += 1

        # dropped item hit water
        hits = pg.sprite.groupcollide(self.dropped_items_on_screen, self.water_on_screen, False, False)
        for hit in hits:
            if 'dead' in hit.item and 'fish' in hit.item:
                if hit.dropped_fish:
                    animal_dict = ANIMALS[hit.item[5:]]
                    animal_name = animal_dict['name']
                    Animal(self, hit.pos.x, hit.pos.y, hit.map, animal_name)
                    hit.kill()
            elif not hit.floats:
                hit.kill()

        # detectable hit detector
        hits = pg.sprite.groupcollide(self.detectors, self.detectables, False, False)
        for detector in hits:
            if not detector.detected:
                for detectable in hits[detector]:
                    if detector.item in detectable.name:
                        detector.trigger(detectable)
                        if detector.kill_item:
                            detectable.kill()

        # npc hit water
        hits = pg.sprite.groupcollide(self.npcs_on_screen, self.water_on_screen, False, False)
        for npc in self.npcs_on_screen:
            if npc in hits:
                if not npc.in_player_vehicle:
                    if not pg.sprite.spritecollide(npc, self.long_grass_on_screen, False):
                        npc.swimming = True
                    else:
                        npc.swimming = False
            else:
                npc.swimming = False

        # npc hits doors and opens them
        hits = pg.sprite.groupcollide(self.npcs_on_screen, self.entryways_on_screen, False, False, entryway_collide)
        for npc in hits:
            for entryway in hits[npc]:
                if not entryway.locked:
                    if not entryway.opened:
                        entryway.open = True
                        entryway.close = False
                    elif npc.target in self.entryways_on_screen:
                        if not entryway.open:
                            entryway.close = True

        # land vehicle hits water
        hits = pg.sprite.groupcollide(self.land_vehicles, self.water_on_screen, False, False)
        for vcle in hits:
            vcle.gets_hit(2, 0, 0)

        # npc hit shallows
        hits = pg.sprite.groupcollide(self.npcs_on_screen, self.shallows_on_screen, False, False)
        for npc in self.npcs_on_screen:
            if npc in hits:
                npc.in_shallows = True
            else:
                npc.in_shallows = False

        # npc hit long grass
        hits = pg.sprite.groupcollide(self.npcs_on_screen, self.long_grass_on_screen, False, False)
        for npc in self.npcs_on_screen:
            if npc in hits:
                npc.in_grass = True
            else:
                npc.in_grass = False

        # npc hit AI path
        hits = pg.sprite.groupcollide(self.npcs_on_screen, self.aipaths, False, False)
        for npc in self.npcs_on_screen:
            if npc in hits:
                now = pg.time.get_ticks()
                if now - npc.last_path_change > 3000:
                    npc.aipath = hits[npc]  #sets aipath to list of paths hit
            else:
                npc.aipath = None

        # animal hit long grass
        hits = pg.sprite.groupcollide(self.animals_on_screen, self.long_grass_on_screen, False, False)
        for animal in self.animals_on_screen:
            if animal in hits:
                animal.in_grass = True
            else:
                animal.in_grass = False

        # mob hits player's moving vehicle
        #hits = pg.sprite.groupcollide(self.mobs_on_screen, self.occupied_vehicles, False, False, mob_hit_rect)
        #for mob in hits:
        #    for vehicle in hits[mob]:
        #        if vehicle not in self.flying_vehicles:
        #            if vehicle == self.player.vehicle:
        #                if not mob.in_player_vehicle:
        #                    keys = pg.key.get_pressed()
        #                    if keys[pg.K_w] or pg.mouse.get_pressed() == (0, 0, 1) or keys[pg.K_s] or keys[pg.K_RIGHT] or keys[pg.K_LEFT] or keys[pg.K_UP] or keys[pg.K_DOWN]:
        #                        try:
        #                            self.player.friction = -10/self.player.vel.length()
        #                        except:
        #                            self.player.friction = -.08
        #                        if self.player.friction < -.08:
        #                            self.player.friction = -.08
        #                        if vehicle in self.animals:
        #                            knockback = 20
        #                        else:
        #                            knockback = 0
        #                        mob.gets_hit(self.player.vel.length()/80, knockback, 0)
        #                    elif vehicle in self.animals:
        #                        mob.gets_hit(0, 20, 0)
        #                    mob.vel = vec(0, 0)

    def render_lighting(self, underworld = False):
        # draw the light mask (gradient) onto fog image
        if self.underworld:
            self.fog.fill((180, 180, 180))
        else:
            self.fog.fill(self.dark_color)
        if self.player_inside:
            for light in self.lights:
                if self.on_screen(light):
                    lightrect = self.camera.apply_rect(light.light_mask_rect)
                    self.fog.blit(light.light_mask, lightrect)
        else:
            for light in self.lights:
                if self.on_screen(light):
                    if not pg.sprite.spritecollide(light, self.inside_on_screen, False):
                        lightrect = self.camera.apply_rect(light.light_mask_rect)
                        self.fog.blit(light.light_mask, lightrect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_SUB)

    def rot_center(self, image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pg.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def draw_minimap(self):
        mini_rect = pg.Rect((self.screen_width - self.map.minimap.rect.width), 0, self.map.minimap.rect.width, self.map.minimap.rect.height)
        width = self.screen_width - self.map.minimap.rect.width
        scale = self.map.minimap.rect.width / self.map.width
        map_pos = vec(self.player.rect.center) * scale
        pos_rect = pg.Rect(0, 0, 20, 20)
        pos_rect.center = (int(map_pos.x + width), int(map_pos.y))
        temp_compass_img = self.rot_center(self.compass_image.copy(), self.compass_rot)
        self.screen.blit(self.map.minimap.image, (width, 0))
        self.screen.blit(temp_compass_img, (width - 128, 0))
        pg.draw.rect(self.screen, WHITE, mini_rect, 2)
        pg.draw.rect(self.screen, YELLOW, pos_rect, 1)

    def draw_overmap(self):
        cell_width = self.screen_width / len(self.map_data_list[0])
        cell_height = self.screen_height / len(self.map_data_list)
        offsetx = int(self.world_location.x * cell_width)
        offsety = int(self.world_location.y * cell_height)
        scalex = cell_width / self.map.width
        scaley = cell_height / self.map.height
        currentmap_rect = pg.Rect(0, 0, cell_width, cell_height)
        currentmap_rect.topleft = (offsetx, offsety)
        map_pos = vec(self.player.rect.centerx * scalex, self.player.rect.centery * scaley)
        pos_rect = pg.Rect(0, 0, 3, 3)
        pos_rect.center = (int(map_pos.x + offsetx), int(map_pos.y + offsety))
        self.screen.blit(self.over_minimap_image, (0, 0))
        pg.draw.rect(self.screen, YELLOW, currentmap_rect, 4)
        pg.draw.rect(self.screen, RED, pos_rect, 4)


    def draw(self):
        pg.display.set_caption("Legends of Zhara")
        self.group.draw(self.screen, self)
        if self.draw_debug:
            for wall in self.walls_on_screen:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
            for vehicle in self.vehicles_on_screen:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(vehicle.hit_rect), 1)
                pg.draw.rect(self.screen, GREEN, self.camera.apply_rect(vehicle.hit_rect2), 1)
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(vehicle.hit_rect3), 1)
            for mob in self.mobs_on_screen:
                pg.draw.rect(self.screen, YELLOW, self.camera.apply_rect(mob.hit_rect), 1)
            #for npc in self.npcs_on_screen:
            #    pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(npc.temp_target.hit_rect), 1)
            for target in self.random_targets:
                pg.draw.rect(self.screen, BLUE, self.camera.apply_rect(target.rect), 1)
            pg.draw.rect(self.screen, YELLOW, self.camera.apply_rect(self.player.hit_rect), 1)
            pg.draw.rect(self.screen, YELLOW, self.camera.apply_rect(self.player.body.mid_weapon_melee_rect), 1)
            pg.draw.rect(self.screen, YELLOW, self.camera.apply_rect(self.player.body.weapon_melee_rect), 1)
            pg.draw.rect(self.screen, YELLOW, self.camera.apply_rect(self.player.body.melee_rect), 1)
            #for elev in self.elevations_on_screen:
            #    pg.draw.rect(self.screen, BLUE, self.camera.apply_rect(elev.rect), 1)


        # Only draws roofs when outside of buildings
        hits = pg.sprite.spritecollide(self.player, self.inside_on_screen, False)
        if not hits:
            self.player_inside = False
        else:
            self.player_inside = True
            if self.player.in_vehicle:
                if self.player.vehicle in self.flying_vehicles:
                    self.player_inside = False

        # Draws flying vehicle sprites after roves.
        #for sprite in self.flying_vehicles:
        #    self.screen.blit(sprite.image, self.camera.apply(sprite))

        if self.underworld:
            self.render_lighting(True)
        elif True in [self.night, self.sunrise, self.nightfall]:
            self.render_lighting()
        if self.hud_map:
            self.draw_minimap()
        if self.hud_overmap:
            self.draw_overmap()

        # HUD functions
        draw_player_stats(self.screen, 10, 10, self.hud_health)
        draw_player_stats(self.screen, 10, 40, self.hud_stamina, BLUE)
        draw_player_stats(self.screen, 10, 70, self.hud_magica, CYAN)
        if self.show_mobhp:
            draw_player_stats(self.screen, int(self.screen_width/2 - 150), self.screen_height - 70, self.hud_mobhp, BLUE, 300)
        if self.player.hungers:
            draw_player_stats(self.screen, 10, 100, self.hud_hunger, BROWN)
            self.draw_text("HGR {:.0f}".format(self.player.stats['hunger']), self.hud_font, 20, WHITE, 120, 100, align="topleft")
        if self.hud_ammo1 != '':
            self.draw_text(self.hud_ammo1, self.hud_font, 20, WHITE, 50, self.screen_height - 100, align="topleft")
        if self.hud_ammo2 != '':
            self.draw_text(self.hud_ammo2, self.hud_font, 20, WHITE, 50, self.screen_height - 50, align="topleft")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, self.screen_width / 2, self.screen_height / 2, align="center")
        if self.message_text == True:
            self.draw_text(self.message, self.hud_font, 30, WHITE, self.screen_width / 2, self.screen_height / 2 + 100, align="center")
        self.draw_text("FPS {:.0f}".format(1/self.dt), self.hud_font, 20, WHITE, self.screen_width/2, 10, align="topleft")
        self.draw_text("HP {:.0f}".format(self.hud_health_stats['health']), self.hud_font, 20, WHITE, 120, 10, align="topleft")
        self.draw_text("ST {:.0f}".format(self.player.stats['stamina']), self.hud_font, 20, WHITE, 120, 40, align="topleft")
        self.draw_text("MP {:.0f}".format(self.player.stats['magica']), self.hud_font, 20, WHITE, 120, 70, align="topleft")

        pg.display.flip()
        self.wt = self.beg + (1 / FPS)
        while (perf_counter() < self.wt):
            pass
        self.dt = perf_counter() - self.beg
        if self.dt > 0.2: # Caps dt at 200 ms.
            self.dt = 0.2
        self.beg = perf_counter()
        if self.in_inventory_menu:
            self.menu.update()
        if self.in_quest_menu:
            self.quest_menu.update()
        if self.in_store_menu:
            self.store_menu.update()
        if self.in_stats_menu:
            self.stats_menu.update()
        if self.in_character_menu:
            self.character_menu.update()
        if self.in_npc_menu:
            self.npc_menu.update()
        if self.in_loot_menu:
            self.loot_menu.update()
        if self.in_lock_menu:
            self.lock_menu.update()
        if self.in_load_menu:
            self.load_menu.update()
        if self.in_settings_menu:
            self.settings_menu.update()
        if self.in_station_menu:
            self.station_menu.update()
        if self.in_dialogue_menu:
            self.dialogue_menu.update()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # Shooting/attacking
            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed() == (1, 0, 1):
                    self.player.dual_shoot()
                elif pg.mouse.get_pressed() == (0, 0, 1) or pg.mouse.get_pressed() == (0, 1, 1):
                    self.player.weapon_hand = 'weapons'
                    self.player.shoot()
                elif pg.mouse.get_pressed() == (1, 0, 0) or pg.mouse.get_pressed() == (1, 1, 0):
                    self.player.weapon_hand = 'weapons2'
                    self.player.shoot()
                else: # Prevents e_down from getting stuck on true
                    self.e_down = False
            if event.type == pg.MOUSEBUTTONUP: # Updates which hand should be attacking when mouse buttons change.
                if pg.mouse.get_pressed() == (0, 0, 1) or pg.mouse.get_pressed() == (0, 1, 1):
                    self.player.weapon_hand = 'weapons'
                elif pg.mouse.get_pressed() == (1, 0, 0) or pg.mouse.get_pressed() == (1, 1, 0):
                    self.player.weapon_hand = 'weapons2'
                else: # Prevents e_down from getting stuck on true
                    self.e_down = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.in_settings_menu = True
                    self.in_menu = True
                if event.key == self.key_map['inventory']:
                    self.player.empty_mags() # This makes sure the bullets in your clip don't transfer to the wrong weapons if you switch weapons in your inventory
                    self.in_inventory_menu = True
                    self.in_menu = True
                if event.key == self.key_map['interact']:
                    self.e_down = True
                else:
                    self.e_down = False
                #if event.key == pg.K_BACKQUOTE:  # Switches to last weapon
                #    self.player.toggle_previous_weapons()
                if event.key == self.key_map['skill']:
                    self.in_stats_menu = True
                if event.key == self.key_map['quest']:
                    self.in_quest_menu = self.in_menu = True
                    self.quest_menu = Quest_Menu(self)
                if event.key == self.key_map['reload']:
                    self.player.pre_reload()
                if event.key == self.key_map['hitbox']:
                    self.draw_debug = not self.draw_debug
                if event.key == self.key_map['pause']:
                    trace_mem()
                    if self.player.vehicle:
                        print(self.group.get_layer_of_sprite(self.player.vehicle))
                    self.paused = not self.paused
                    self.beg = perf_counter() # resets dt.
                if event.key == pg.K_EQUALS:
                    self.map.minimap.resize()
                if event.key == pg.K_MINUS:
                    self.map.minimap.resize(False)
                if event.key == self.key_map['minimap']: # Toggles hud mini map
                    self.hud_map = not self.hud_map
                if event.key == self.key_map['overmap']: # Toggles overworld map
                    self.hud_overmap = not self.hud_overmap
                if event.key == self.key_map['use']:
                    if not self.in_store_menu:
                        self.player.use_item()
                if event.key == self.key_map['place']:
                    self.player.place_item()
                if event.key == self.key_map['grenade']:
                    self.player.throw_grenade()
                if event.key == self.key_map['transform']:
                    if self.player.possessing == None:
                        self.player.transform()
                    else:
                        self.player.possessing.depossess()

                if event.key == self.key_map['fire']:
                    if self.player.dragon:
                        self.player.breathe_fire()
                if event.key == self.key_map['craft']:
                    self.in_station_menu = True
                    self.in_menu = True
                    self.station_menu = Work_Station_Menu(self, 'crafting')
                if event.key == self.key_map['lamp']:
                    self.player.light_on = not self.player.light_on
                if event.key == self.key_map['up']:
                    if self.player.in_vehicle:
                        if self.player.vehicle in self.flying_vehicles:
                            self.fly_menu = Fly_Menu(self)

                if event.key == self.key_map['cast']:
                    self.player.cast_spell()
                if event.key == pg.K_RETURN:   # Toggles fullscreen mode when you press ALT+ENTER
                    if event.mod & pg.KMOD_ALT:
                        self.flags ^=  pg.NOFRAME | pg.FULLSCREEN
                        if self.flags & pg.FULLSCREEN:
                            self.screen_height = HEIGHT
                        else:
                            self.screen_height = int(HEIGHT * self.window_ratio)
                        pg.display.set_mode((self.screen_width, self.screen_height), self.flags)
                if event.key ==  pg.K_s: # Saves game
                    if event.mod & pg.KMOD_CTRL:
                        self.save()
                if event.key ==  pg.K_l: # loads game
                    if event.mod & pg.KMOD_CTRL:
                        self.in_load_menu = True
                if event.key == self.key_map['jump']:
                    self.player.pre_jump()

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED,
                       self.screen_width / 2, self.screen_height / 2, align="center")
        self.draw_text("Press Escape to quit, C to continue or N to start a new game.", self.script_font, 16, WHITE,
                       self.screen_width / 2, self.screen_height * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_key()
        self.garbage_collect()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        waiting = False
                        self.quit()
                    elif event.key == pg.K_c:
                        waiting = False
                        self.player.stats['health'] = self.player.stats['max health']
                        self.in_load_menu = True
                        self.run()
                    elif event.key == pg.K_n:
                        waiting = False

# create the game object
g = Game()
while True:
    g.new()
    g.run()
    g.show_go_screen()
