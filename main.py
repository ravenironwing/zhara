# The Legend of Sky Realm by Raven Dewey (aka Ravenwing)

import tracemalloc
import gc
import pygame as pg
import sys
import pickle
from random import choice, random, choices
from os import path
from settings import *
from npcs import *
from quests import *
from menu import *
from sprites import *
from tilemap import *
import datetime
from time import sleep
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

    if game == None:
        for spr in self.sprites():
            new_rect = spr.rect.move(ox, oy)
            try:
                new_surfaces_append((spr.image, new_rect, gl(spr), spr.blendmode))
            except AttributeError:  # generally should only fail when no blendmode available
                new_surfaces_append((spr.image, new_rect, gl(spr)))
            spritedict[spr] = new_rect

    else:
        for spr in self.sprites(): # This modded version only adds the sprite images that are on screen using the game.camera and the on_screen method
            if game.on_screen(spr):
                new_rect = spr.rect.move(ox, oy)
                try:
                    new_surfaces_append((spr.image, new_rect, gl(spr), spr.blendmode))
                except AttributeError:  # generally should only fail when no blendmode available
                    new_surfaces_append((spr.image, new_rect, gl(spr)))
                spritedict[spr] = new_rect

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
def draw_player_stats(surf, x, y, pct, color = GREEN):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
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
                if one.frame < 3:
                    return True
        else:
            return False

    elif one.mid_weapon2_melee_rect.colliderect(two.trunk.hit_rect) or one.weapon2_melee_rect.colliderect(two.trunk.hit_rect) or one.melee2_rect.colliderect(two.trunk.hit_rect):
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

# Used to define fireball hits
def fire_collide(one, two):
    if one.hit_rect.colliderect(two.hit_rect):
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
        self.icon_image = pg.image.load(path.join(img_folder, ICON_IMG))
        pg.display.set_icon(self.icon_image)
        self.screen = pg.display.set_mode((self.screen_width, self.screen_height), self.flags)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.channel4 = pg.mixer.Channel(3)

    def on_screen(self, sprite):
        rect = self.camera.apply(sprite)
        threshold = 50
        if rect.right < -threshold or rect.bottom < -threshold or rect.left > self.screen_width + threshold or rect.top > self.screen_height + threshold:
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
        # This block stores all sprite locations and their health in the map_sprite_data_list so the game remembers where everything is.
        npc_list = []
        animal_list = []
        item_list = []
        vehicle_list = []
        breakable_list = []
        if not self.underworld:
            for npc in self.npcs:
                if npc not in self.companions:
                    npc_list.append({'name': npc.species, 'location': npc.pos, 'health': npc.health})
                    self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].npcs = npc_list
            for animal in self.animals:
                if animal not in self.companions:
                    if animal != self.player.vehicle:
                        animal_list.append({'name': animal.species, 'location': animal.pos, 'health': animal.health})
                        self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].animals = animal_list
            for item in self.dropped_items:
                item_list.append({'name': item.name, 'location': item.pos, 'rotation': item.rot})
                self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].items = item_list
            for vehicle in self.vehicles:
                vehicle_list.append({'name': vehicle.species, 'location': vehicle.pos, 'health': vehicle.health})
                self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].vehicles = vehicle_list
            for breakable in self.breakable:
                breakable_list.append({'name': breakable.name, 'location': breakable.center, 'w': breakable.w, 'h': breakable.h,  'rotation': breakable.rot})
                self.map_sprite_data_list[int(self.world_location.x)][int(self.world_location.y)].breakable = breakable_list
        else:
            for npc in self.npcs:
                if npc not in self.companions:
                    npc_list.append({'name': npc.species, 'location': npc.pos, 'health': npc.health})
                    self.underworld_sprite_data_dict[self.previous_map].npcs = npc_list
            for animal in self.animals:
                if animal not in self.companions:
                    if animal != self.player.vehicle:
                        animal_list.append({'name': animal.species, 'location': animal.pos, 'health': animal.health})
                        self.underworld_sprite_data_dict[self.previous_map].animals = animal_list
            for item in self.dropped_items:
                item_list.append({'name': item.name, 'location': item.pos, 'rotation': item.rot})
                self.underworld_sprite_data_dict[self.previous_map].items = item_list
            for vehicle in self.vehicles:
                vehicle_list.append({'name': vehicle.species, 'location': vehicle.pos, 'health': vehicle.health})
                self.underworld_sprite_data_dict[self.previous_map].vehicles = vehicle_list
            for breakable in self.breakable:
                breakable_list.append({'name': breakable.name, 'location': breakable.center, 'w': breakable.w, 'h': breakable.h,  'rotation': breakable.rot})
                self.underworld_sprite_data_dict[self.previous_map].breakable = breakable_list

    def save(self):
        self.save_sprite_locs()
        possessing = self.player.possessing
        if self.player.possessing != None:
            self.player.possessing.depossess()
        self.player.dragon = False
        if 'dragon' in self.player.equipped['race']: # Makes it so you aren't a dragon when you load a game.
            self.player.equipped['race'] = self.player.equipped['race'].replace('dragon', '')
            self.player.body.update_animations()
        self.draw_text('Saving....', self.script_font, 50, WHITE, self.screen_width / 2, self.screen_height / 2, align="topright")
        pg.display.flip()
        sleep(0.5)
        if self.player.in_vehicle:
            vehicle_name = self.player.vehicle.species
            if self.player.vehicle not in self.animals:
                self.vehicle_data[vehicle_name]['location'][0] = self.world_location.x
                self.vehicle_data[vehicle_name]['location'][1] = self.world_location.y
                self.vehicle_data[vehicle_name]['location'][2] = int(self.player.pos.x / self.map.tile_size)
                self.vehicle_data[vehicle_name]['location'][3] = int(self.player.pos.y / self.map.tile_size)
        else:
            vehicle_name = None
        companion_list = []
        for companion in self.companions:
            companion_list.append(companion.species)

        updated_equipment = [UPGRADED_WEAPONS, UPGRADED_HATS, UPGRADED_TOPS, UPGRADED_GLOVES, UPGRADED_BOTTOMS, UPGRADED_SHOES, UPGRADED_ITEMS]
        save_list = [self.player.inventory, self.player.equipped, self.player.stats, [self.player.pos.x, self.player.pos.y], self.previous_map, [self.world_location.x, self.world_location.y], self.chests, self.overworld_map, updated_equipment, self.people, self.quests, self.vehicle_data, vehicle_name, companion_list, self.map_sprite_data_list, self.underworld_sprite_data_dict, self.player.colors]
        with open(path.join(saves_folder, self.player.race + "_" + self.format_date() + ".sav"), "wb", -1) as FILE:
            pickle.dump(save_list, FILE)
        if possessing != None:
            possessing.possess(self.player)

    def load_save(self, file_name):
        load_file = []
        with open(file_name, "rb", -1) as FILE:
            load_file = pickle.load(FILE)
        # Loads saved upgraded equipment:
        self.people = load_file[9] # Updates NPCs
        self.quests = load_file[10] # Updates Quests from save
        self.vehicle_data = load_file[11]  # Updates Quests from save
        self.saved_vehicle = load_file[12]
        self.chests = load_file[6] # Updates chests from dave
        self.saved_companions = load_file[13]
        self.map_sprite_data_list = load_file[14]
        self.underworld_sprite_data_dict = load_file[15]
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
        self.player.colors = load_file[16]
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
            if self.world_location == (self.vehicle_data[vehicle.kind]['location'][0], self.vehicle_data[vehicle.kind]['location'][1]):
                if vehicle.kind == self.saved_vehicle:
                    vehicle.enter_vehicle(self.player)
        for vehicle in self.flying_vehicles:
            if self.world_location == (self.vehicle_data[vehicle.kind]['location'][0], self.vehicle_data[vehicle.kind]['location'][1]):
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
        self.vehicle_data = VEHICLES
        self.quests = QUESTS # Updates Quests from save
        self.chests = CHESTS # Updates chests from dave
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
        self.title_image = pg.image.load(path.join(img_folder, TITLE_IMAGE)).convert()
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
                    img = pg.transform.scale(bullet_img, (6*(x + 1), 4*(x + 1)))
                else:
                    img = pg.transform.scale(bullet_img, (80, 10))
                bullet_name = size + str(i + 1)
                self.bullet_images[bullet_name] = img

           # img = pg.transform.scale(bullet_img, (15, 15))
           # bullet_name = 'md' + str(i + 1)
           # self.bullet_images[bullet_name] = img

           # img = pg.transform.scale(bullet_img, (40, 40))
           # bullet_name = 'lg' + str(i + 1)
           # self.bullet_images[bullet_name] = img

        #self.bullet_images = {}
        #    for x in self.bullet_images_list:
        #self.bullet_images['lg'] = pg.image.load(BULLET_IMG).convert_alpha()
        #self.bullet_images['md'] = pg.transform.scale(self.bullet_images['lg'], (15, 15))
        #self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))
        #self.bullet_images['lglz'] = pg.image.load(BLUELASER_IMG).convert_alpha()
        #self.bullet_images['mdlz'] = pg.transform.scale(self.bullet_images['lglz'], (15, 15))
        #self.bullet_images['smlz'] = pg.transform.scale(self.bullet_images['lglz'], (10, 10))

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
        self.loading_screen_images = []
        for i, screen in enumerate(LOADING_SCREEN_IMAGES):
            img = pg.image.load(path.join(loading_screen_folder, LOADING_SCREEN_IMAGES[i])).convert()
            self.loading_screen_images.append(img)
        self.breakable_images = {}
        for kind in BREAKABLE_IMAGES:
            temp_list = []
            for i, picture in enumerate(BREAKABLE_IMAGES[kind]):
                img = pg.image.load(path.join(breakable_folder, BREAKABLE_IMAGES[kind][i])).convert_alpha()
                temp_list.append(img)
            self.breakable_images[kind] = temp_list

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
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
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
        self.title_image = pg.transform.scale(self.title_image, (self.screen_width, self.screen_height))

        self.continued_game = False
        self.in_load_menu = False
        self.in_npc_menu = False
        waiting = True
        i = 0
        while waiting:
            self.clock.tick(FPS)
            self.screen.fill(BLACK)
            self.title_image.set_alpha(i) 
            self.screen.blit(self.title_image, (0, 0))
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
        self.map_sprite_data_list = []
        self._player_inside = False
        self.compass_rot = 0
        self.people = PEOPLE
        self.vehicle_data = VEHICLES
        self.saved_vehicle = []
        self.saved_companions = []
        self.underworld = False
        self.quests = QUESTS
        self.chests = CHESTS
        self.bg_music = BG_MUSIC
        self.previous_music = TITLE_MUSIC
        self.portal_location = vec(0, 0)
        self.portal_combo = ''
        self.load_menu = Load_Menu(self)
        self.guard_alerted = False
        self.hud_map = False
        self.hud_overmap = False
        self.vehicle_text = False
        self.mechsuit_text = False
        self.vehicle_key_text = False
        self.talk_text = False
        self.station_type = ''
        self.station_text = False
        self.loot_text = False
        self.bed_message = ''
        self.lock_text = False
        self.bed_text = False
        self.toilet_text = False
        self.too_much_weight = False
        self.pick_up_text = False
        self.map_type = None
        self.group = PyscrollGroup()
        self.all_sprites = pg.sprite.LayeredUpdates() # Used for all non_static sprites
        self.all_static_sprites = pg.sprite.Group() # used for all static sprites
        self.firepots = pg.sprite.Group()
        self.arrows = pg.sprite.Group()
        self.chargers = pg.sprite.Group()
        self.mechsuits = pg.sprite.Group()
        self.detectors = pg.sprite.Group()
        self.detectables = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.inside = pg.sprite.Group()
        self.jumpables = pg.sprite.Group()
        self.climbables = pg.sprite.Group()
        self.climbables_and_jumpables = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.beds = pg.sprite.Group()
        self.toilets = pg.sprite.Group()
        self.water = pg.sprite.Group()
        self.shallows = pg.sprite.Group()
        self.lava = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.moving_targets = pg.sprite.Group() # Used for all moving things bullets interact with
        self.breakable = pg.sprite.Group()
        self.npc_bodies = pg.sprite.Group()
        self.npcs =  pg.sprite.Group()
        self.animals = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.grabable_animals = pg.sprite.Group()
        self.corpses = pg.sprite.Group()
        self.fires = pg.sprite.Group()
        self.explosions = pg.sprite.Group()
        self.shocks = pg.sprite.Group()
        self.fireballs = pg.sprite.Group()
        self.firepits = pg.sprite.Group()
        self.containers = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.enemy_bullets = pg.sprite.Group()
        self.enemy_fireballs = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.dropped_items = pg.sprite.Group()
        self.work_stations = pg.sprite.Group()
        self.vehicles = pg.sprite.Group()
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
        #self.tanks = pg.sprite.Group()
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
        self.last_hud_update = 0
        self.last_fire = 0
        self.last_dialogue = 0
        self.hud_health = 0
        self.hud_stamina = 0
        self.hud_ammo1 = 0
        self.hud_ammo2 = 0
        self.e_down = False
        self.draw_debug = False
        self.paused = False
        self.night = False
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
    def player_inside(self): #This is the method that is called whenever you access in_shallows
        return self._player_inside
    @player_inside.setter #This is the method that is called whenever you set a value for in_shallows
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

        self.guard_alerted = False # Makes it so guards stop attacking you after you change maps
        self.player.vel = vec(0, 0)
        self.player.acc = vec(0, 0)
        direction = cardinal
        offset = 64
        if cardinal != None:
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

        if coordinate != None:
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
        self.player.stats['health'] += 50
        if self.player.stats['health'] > self.player.stats['max health']:
            self.player.stats['health'] = self.player.stats['max health']
        self.player.stats['stamina'] = self.player.stats['max stamina']
        self.player.stats['magica'] += 50
        if self.player.stats['magica'] > self.player.stats['max magica']:
            self.player.stats['magica'] = self.player.stats['max magica']
        self.effects_sounds['snore'].play()
        sleep(10)
        self.clock.tick(FPS) # Characters randomly disappear without this for some reason. I have no clue why this fixes it
        pg.mixer.music.play(loops=-1)

    def use_toilet(self):
        self.player.stats['health'] += 5
        if self.player.stats['health'] > self.player.stats['max health']:
            self.player.stats['health'] = self.player.stats['max health']
        self.player.stats['stamina'] += 30
        if self.player.stats['stamina'] > self.player.stats['stamina']:
            self.player.stats['stamina'] = self.player.stats['stamina']
        toilet_sounds = ['fart', 'pee']
        self.effects_sounds[choice(toilet_sounds)].play()
        sleep(2)
        self.effects_sounds['toilet'].play()
        self.clock.tick(FPS) # Characters randomly disappear without this for some reason. I have no clue why this fixes it

    def garbage_collect(self): # This block of code removes everything in memory from previous maps
        for sprite in self.all_sprites:
            if self.player.possessing:
                if sprite in [self.player.possessing, self.player.possessing.body]:
                    continue
            if self.player.in_vehicle:
                try:
                    if sprite in [self.player.vehicle, self.player.vehicle.turret]:
                        continue
                except:
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

        for sprite in self.all_static_sprites:
            sprite.kill()
            del sprite
        del self.map
        gc.collect()  # Forces garbage collection. Without this the game will quickly run out of memory.

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
        self.camera = Camera(self.map.width, self.map.height)

        for i in range(0, 10): # Creates random targets for Npcs
            Random_Target(self)

        if not self.underworld:
            # Loads vehicles based off of their recorded locations in vehicles.py or the saved vehicle dictionary.... This while part should probably be taken out since the vehicle data should be stored in the MapData object
            for vehicle in self.vehicle_data:
                if self.world_location == (self.vehicle_data[vehicle]['location'][0], self.vehicle_data[vehicle]['location'][1]):
                    ship = Vehicle(self, (self.vehicle_data[vehicle]['location'][2] * self.map.tile_size, self.vehicle_data[vehicle]['location'][3] * self.map.tile_size), vehicle, map)

        if self.sprite_data.visited: # Loads stored map data for sprites if you have visited before.
            companion_names = []
            for companion in self.companions:
                companion_names.append(companion.species)
            for npc in self.sprite_data.npcs:
                if npc['name'] not in companion_names: # Makes it so it doesn't double load your companions.
                    Npc(self, npc['location'].x, npc['location'].y, map, npc['name'], npc['health'])
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
                    Npc(self, npc['location'].x, npc['location'].y, map, npc['name'], npc['health'])
            self.sprite_data.moved_npcs = []
            for animal in self.sprite_data.moved_animals:
                Animal(self, animal['location'].x, animal['location'].y, map, animal['name'], animal['health'])
            self.sprite_data.moved_animals = []

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name != None:
                obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
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

                    # Loads items, weapons, and armor placed on the map
                    for item_type in ITEM_TYPE_LIST:
                        if tile_object.name in eval(item_type.upper()):
                            Dropped_Item(self, obj_center, item_type, tile_object.name)
                    # Loads fixed roated items:
                    if '@' in tile_object.name:
                        item, rot = tile_object.name.split('@')
                        rot = int(rot)
                        for item_type in ITEM_TYPE_LIST:
                            if item in eval(item_type.upper()):
                                Dropped_Item(self, obj_center, item_type, item, rot)
                    # Used for destructable plants, rocks, ore veins, walls, etc
                    for item in BREAKABLES:
                        if item in tile_object.name:
                            if '@' in tile_object.name:
                                temp_item, rot = tile_object.name.split('@')
                                rot = int(rot)
                            else:
                                rot = None
                            Breakable(self, obj_center, tile_object.width, tile_object.height, item, map, rot)

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
                    Obstacle(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
                if tile_object.name == 'inside':
                    Inside(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
                if tile_object.name == 'jumpable':
                    Jumpable(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
                if tile_object.name == 'climbable':
                    Climbable(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
                if tile_object.name == 'water':
                    Water(self, tile_object.x, tile_object.y,
                             tile_object.width, tile_object.height)
                if tile_object.name == 'shallows':
                    Shallows(self, tile_object.x, tile_object.y,
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

        # This section creates walls based off of which tile is used in the map rather than having to create wall objects
        if self.map_type in ['ant_tunnel', 'cave']:
            wall_tile = self.map.tmxdata.get_tile_gid(0, 0, 0) # Uses whatever tile is in the upper left corner of the second layer as the wall tile.
            for location in self.map.tmxdata.get_tile_locations_by_gid(wall_tile):
                Obstacle(self, location[0] * self.map.tile_size, location[1] * self.map.tile_size, self.map.tile_size, self.map.tile_size)

            # This section generates ore blocks to time in all the spaces with the tile specified in the position (1, 0).
            if not self.sprite_data.visited:
                block_tile = self.map.tmxdata.get_tile_gid(1, 0, 0)
                for location in self.map.tmxdata.get_tile_locations_by_gid(block_tile):
                    block_type = choice(choices(BLOCK_LIST, BLOCK_PROB, k = 10))
                    center = vec(location[0] * self.map.tile_size + self.map.tile_size/2, location[1] * self.map.tile_size + self.map.tile_size/2)
                    Breakable(self, center, self.map.tile_size, self.map.tile_size, block_type, map)

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
            if self.map_type != None:
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
            if self.map_type != None:
                if self.map_type in ['mountain', 'forest']:
                    if self.map_type == 'mountain':
                        rand_range = randrange(4, 7)
                        rand_trees = randrange(8, 12)
                    if self.map_type == 'forest':
                        rand_range = randrange(1, 3)
                        rand_trees = randrange(30, 60)
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
        # Kills breakables that spawn in water
        hits = pg.sprite.groupcollide(self.breakable, self.water, True, False)
        hits = pg.sprite.groupcollide(self.breakable, self.shallows, True, False)


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

        self.clock.tick(FPS)  # I don't know why this fixes it, but without this the player can move while a new map is loading. I think it somehow interrupts the keyboard input in the sprite.update.


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        # updates all sprites that are on screen
        fires_on_screen = []
        for sprite in self.all_sprites:
            if self.on_screen(sprite):
                sprite.update()
                if sprite in self.fires:
                    fires_on_screen.append(sprite) # Creates a list of all fires on screen so I can calculate their distance and play fire sounds at correct volumes.
            elif sprite == self.player.vehicle:
                sprite.update()
            elif sprite in self.companions:
                sprite.update()
            elif sprite in self.companion_bodies:
                sprite.update()
        self.camera.update(self.player)
        self.group.center(self.player.rect.center)

        # Used for playing fire sounds at set distances:
        closest_fire = None
        previous_distance = 30000
        for sprite in fires_on_screen:    # Finds the closest fire and ignores the others.
            player_dist = self.player.pos - sprite.pos
            player_dist = player_dist.length()
            if previous_distance > player_dist:
                closest_fire = sprite
                previous_distance = player_dist

        if closest_fire != None:
            if previous_distance < 400:  # This part makes it so the fire volume decreases as you walk away from it.
                volume = 150 / (previous_distance * 2)
                self.channel4.set_volume(volume)
                if not self.channel4.get_busy():
                    self.channel4.play(self.effects_sounds['fire crackle'], loops=-1)
            else:
                self.channel4.stop()
        else:
            self.channel4.stop()

        #self.map.update()
        #self.camera.update(self.map)

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
            self.bed_text = False
            hits = pg.sprite.spritecollide(self.player, self.beds, False)
            if hits:
                if self.player.climbing:
                    self.bed_text = True
                    if hits[0].name == 'bed':
                        if hits[0].cost > 0:
                            if self.player.inventory['gold'] >= hits[0].cost:
                                self.bed_message = 'Press E to pay ' + str(hits[0].cost) + ' gold to sleep in bed.'
                                if self.e_down:
                                    self.player.inventory['gold'] -= hits[0].cost
                                    self.effects_sounds['cashregister'].play()
                                    self.sleep_in_bed()
                                    self.bed_text = False
                                    self.e_down = False
                            else:
                                self.bed_message = 'You cannot afford this bed.'
                        else:
                            self.bed_message = 'Press E to sleep in bed.'
                            if self.e_down:
                                self.sleep_in_bed()
                                self.bed_text = False
                                self.e_down = False
                    else:
                        self.bed_message = 'You can not sleep in ' + hits[0].name + '.'

            # player hits toilet
            self.toilet_text = False
            hits = pg.sprite.spritecollide(self.player, self.toilets, False)
            if hits:
                if self.player.climbing:
                    self.toilet_text = True
                    if self.e_down:
                        self.use_toilet()
                        self.toilet_text = False
                        self.e_down = False

            # player hit corps
            self.loot_text = False
            hits = pg.sprite.spritecollide(self.player, self.corpses, False)
            if hits:
                self.loot_text = True
                if self.e_down:
                    if not self.in_loot_menu:
                        self.in_loot_menu = True
                        self.in_menu = True
                        self.loot_menu = Loot_Menu(self, hits[0])

            # player hit container
            self.lock_text = False
            hits = pg.sprite.spritecollide(self.player, self.containers, False)
            if hits:
                if not hits[0].inventory['locked']:
                    self.loot_text = True
                    if self.e_down:
                        if not self.in_loot_menu:
                            self.in_loot_menu = True
                            self.loot_menu = Loot_Menu(self, hits[0])
                else:
                    self.lock_text = True
                    if self.e_down:
                        if not self.in_lock_menu:
                            self.in_lock_menu = self.in_menu = True
                            self.lock_menu = Lock_Menu(self, hits[0])


            # Player is in talking range of NPC
            self.talk_text = False
            if True not in [self.in_menu, self.vehicle_text, self.vehicle_key_text, self.loot_text, self.bed_text, self.lock_text, self.toilet_text, self.station_text, self.pick_up_text]:
                hits = pg.sprite.spritecollide(self.player, self.npcs, False, npc_talk_rect)
                if hits:
                    if hits[0].dialogue != None:
                        if not self.in_dialogue_menu:
                            now = pg.time.get_ticks()
                            if now - self.last_dialogue > 2000:
                                self.talk_text = True
                                if self.e_down:
                                    self.talk_text = False
                                    self.dialogue_menu = Dialogue_Menu(self, hits[0])

            # player hits work station (forge, grinder, work bench, etc)
            self.station_text = False
            hits = pg.sprite.spritecollide(self.player, self.work_stations, False)
            if hits:
                self.station_type = hits[0].kind
                self.station_text = True
                if self.e_down:
                    self.in_station_menu = True
                    self.in_menu = True
                    self.station_menu = Work_Station_Menu(self, hits[0].kind)
                    self.e_down = False

            # player hits water
            hits = pg.sprite.spritecollide(self.player, self.water, False)
            if hits:
                self.player.swimming = True
            else:
                self.player.swimming = False

            # player hits shallows
            hits = pg.sprite.spritecollide(self.player, self.shallows, False)
            if hits:
                self.player.in_shallows = True
            else:
                self.player.in_shallows = False

            # player hits climbable
            hits = pg.sprite.spritecollide(self.player, self.climbables_and_jumpables, False)
            if hits:
                keys = pg.key.get_pressed()
                if keys[pg.K_v]:
                    if self.player.stats['stamina'] > 10 and not self.player.in_vehicle:
                        self.player.climbing = True
                    else:
                        if self.player.in_vehicle:
                            if 'climbables' not in self.player.vehicle.collide_list:
                                if 'obstacles' not in self.player.vehicle.collide_list:
                                    self.player.climbing = True
            else:
                self.player.climbing = False

            # player hits dropped item
            self.pick_up_text = False
            self.too_much_weight = False
            hits = pg.sprite.spritecollide(self.player, self.dropped_items, False, pg.sprite.collide_circle_ratio(0.75))
            for hit in hits:
                if hit.name not in ['fire pit']:
                    self.pick_up_text = True
                    if self.e_down:
                        self.player.inventory[hit.item_type].append(hit.item)
                        self.player.calculate_weight()
                        if self.player.stats['weight'] > self.player.stats['max weight']:
                            self.player.inventory[hit.item_type].remove(hit.item)
                            self.player.calculate_weight()
                            self.too_much_weight = True
                        else:
                            hit.kill()

            # player melee hits breakable: a bush, tree, rock, ore vein, shell, glass, etc.
            if self.player.melee_playing:
                hits = pg.sprite.spritecollide(self.player.body, self.breakable, False, breakable_melee_hit_rect)
                for bush in hits:
                    if self.player.equipped[self.player.weapon_hand] == None:
                        weapon_type = None
                    else:
                        weapon_type = WEAPONS[self.player.equipped[self.player.weapon_hand]]['type']
                        if not self.player.change_used_item('weapons', self.player.equipped[self.player.weapon_hand]): # Makes it so pickaxes and other items deplete their hp
                            weapon_type = None
                    bush.gets_hit(weapon_type)

            # player hits lava
            hits = pg.sprite.spritecollide(self.player, self.lava, False)
            for hit in hits:
                if not self.player.jumping:
                    self.player.gets_hit(hit.damage, 0, 0)
                    now = pg.time.get_ticks()
                    if now - self.last_fire > 300:
                        pos = self.player.pos + vec(-1, -1)
                        self.effects_sounds['fire blast'].play()
                        Stationary_Animated(self, self.player.pos, 'fire', 3000)
                        Stationary_Animated(self, pos, 'fire', 1000)
                        self.last_fire = now

            # NPC hit player
            hits = pg.sprite.spritecollide(self.player, self.npcs, False, pg.sprite.collide_circle_ratio(0.7))
            for hit in hits:
                if hit.touch_damage:
                    if random() < 0.7:
                        self.player.gets_hit(hit.damage, hit.knockback, hits[0].rot)
                else:
                    self.player.hit_rect.centerx = self.player.pos.x
                    collide_with_walls(self.player, [hit], 'x')
                    self.player.hit_rect.centery = self.player.pos.y
                    collide_with_walls(self.player, [hit], 'y')
                    self.player.rect.center = self.player.hit_rect.center


            # player hits an empty vehicle or mech suit
            self.vehicle_text = False
            self.vehicle_key_text = False
            self.mechsuit_text = False
            if not self.player.in_vehicle:
                if self.player.possessing == None:
                    hits = pg.sprite.spritecollide(self.player, self.mechsuits, False)
                    if hits:
                        if (hits[0].driver == None) and hits[0].living:
                            self.mechsuit_text = True
                        if self.e_down:
                            if hits[0].living:
                                hits[0].possess(self.player)
                            self.mechsuit_text = False

                hits = pg.sprite.spritecollide(self.player, self.vehicles, False)
                if hits:
                    if not hits[0].occupied and hits[0].living:
                        self.vehicle_text = True
                    if self.e_down:
                        if hits[0].living:
                            hits[0].enter_vehicle(self.player)
                        self.vehicle_text = False
                hits = pg.sprite.spritecollide(self.player, self.flying_vehicles, False)
                if hits:
                    if not hits[0].occupied and hits[0].living:
                        self.vehicle_text = True
                    if self.e_down:
                        if hits[0].living:
                            if hits[0].kind == 'airship':
                                if 'airship key' in self.player.inventory['items']:
                                    hits[0].enter_vehicle(self.player)
                                elif len(self.companions.sprites()) > 0:
                                    is_felius = False
                                    for companion in self.companions:
                                        if companion.name == 'Felius':
                                            is_felius = True
                                    if is_felius:
                                        hits[0].enter_vehicle(self.player)
                                else:
                                    self.vehicle_key_text = True
                            else:
                                hits[0].enter_vehicle(self.player)
                        self.vehicle_text = False
        else:
            self.player.swimming = False
            self.player.in_shallows = False


        # Animal hit player
        if self.player not in self.flying_vehicles:
            hits = pg.sprite.spritecollide(self.player, self.animals, False, pg.sprite.collide_circle_ratio(0.7))
            for hit in hits:
                if not hit.occupied:
                    if hit in self.grabable_animals:
                        self.pick_up_text = True
                        if self.e_down:
                            self.player.inventory[hit.item_type].append(hit.item)
                            hit.kill()
                    elif hit.mountable:
                        if self.e_down:
                            hit.mount(self.player)
                    if hit.touch_damage:
                        if random() < 0.7:
                            self.player.gets_hit(hit.damage, hit.knockback, hits[0].rot)
                    else:
                        self.player.gets_hit(0, hit.knockback, hits[0].rot)
        else:  # Makes it so flying animals still interact with flying players
            hits = pg.sprite.spritecollide(self.player, self.animals, False, pg.sprite.collide_circle_ratio(0.7))
            for hit in hits:
                if hit.flying:
                    if not hit.occupied:
                        if hit in self.grabable_animals:
                            self.pick_up_text = True
                            if self.e_down:
                                self.player.inventory[hit.item_type].append(hit.item)
                                hit.kill()
                        elif hit.mountable:
                            if self.e_down:
                                hit.mount(self.player)
                        if hit.touch_damage:
                            if random() < 0.7:
                                self.player.gets_hit(hit.damage, hit.knockback, hits[0].rot)
                        else:
                            self.player.gets_hit(0, hit.knockback, hits[0].rot)

        # NPC hits charger
        hits = pg.sprite.groupcollide(self.npcs, self.chargers, False, False)
        for npc in hits:
            if npc.race in ['mechanima', 'mech_suit']:
                hits[npc][0].charge(npc)

        # NPC or Player melee hits moving_target
        hits = pg.sprite.groupcollide(self.npc_bodies, self.moving_targets, False, False, melee_hit_rect)
        for body in hits:
            if body.mother.in_player_vehicle:
                pass
            for mob in hits[body]:
                if mob.immaterial:
                    if body.mother.equipped[body.mother.weapon_hand] != None:
                        if 'aetherial' not in body.mother.equipped[body.mother.weapon_hand]:
                            continue
                if mob.in_player_vehicle:
                    pass
                elif body.mother == mob:
                    pass
                elif mob in self.flying_vehicles:
                    pass
                elif mob.in_vehicle:
                    pass
                elif body.mother.in_vehicle: # Makes it so you can't attack your own vehicle
                    if mob == body.mother.vehicle:
                        pass
                elif body.mother.melee_playing:
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
        hits = pg.sprite.groupcollide(self.moving_targets, self.fires, False, False, pg.sprite.collide_circle_ratio(0.5))
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
        hits = pg.sprite.groupcollide(self.firepits, self.fires, False, False, pg.sprite.collide_circle_ratio(0.5))
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
        hits = pg.sprite.groupcollide(self.dropped_items, self.water, False, False)
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
        hits = pg.sprite.groupcollide(self.npcs, self.water, False, False)
        for npc in hits:
            if not npc.in_player_vehicle:
                npc.swimming = True
        for npc in self.npcs:
            if not npc in hits:
                npc.swimming = False

        # companion hit climbable or jumpable
        hits = pg.sprite.groupcollide(self.companions, self.climbables_and_jumpables, False, False)
        for npc in hits:
            npc.climbing = True
        for npc in self.npcs:
            if not npc in hits:
                npc.climbing = False

        # land vehicle hits water
        hits = pg.sprite.groupcollide(self.land_vehicles, self.water, False, False)
        for vcle in hits:
            vcle.gets_hit(2, 0, 0)

        # npc hit shallows
        hits = pg.sprite.groupcollide(self.npcs, self.shallows, False, False)
        for npc in hits:
            npc.in_shallows = True
        for npc in self.npcs:
            if not npc in hits:
                npc.in_shallows = False

        # mob hits player's moving vehicle
        hits = pg.sprite.groupcollide(self.mobs, self.occupied_vehicles, False, False, mob_hit_rect)
        for mob in hits:
            for vehicle in hits[mob]:
                if vehicle not in self.flying_vehicles:
                    if vehicle == self.player.vehicle:
                        if not mob.in_player_vehicle:
                            keys = pg.key.get_pressed()
                            if keys[pg.K_w] or pg.mouse.get_pressed() == (0, 0, 1) or keys[pg.K_s] or keys[pg.K_RIGHT] or keys[pg.K_LEFT] or keys[pg.K_UP] or keys[pg.K_DOWN]:
                                try:
                                    self.player.friction = -10/self.player.vel.length()
                                except:
                                    self.player.friction = -.08
                                if self.player.friction < -.08:
                                    self.player.friction = -.08
                                if vehicle in self.animals:
                                    knockback = 20
                                else:
                                    knockback = 0
                                mob.gets_hit(self.player.vel.length()/80, knockback, 0)
                            elif vehicle in self.animals:
                                mob.gets_hit(0, 20, 0)
                            mob.vel = vec(0, 0)


    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

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
        pg.display.set_caption("Legends of Zhara  FPS: {:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        #self.screen.blit(self.map.image, self.camera.apply(self.map))
        #self.overlay_group.center(self.player.body.rect.center)
        self.group.draw(self.screen, self)
        #for sprite in self.all_sprites:
            #if isinstance(sprite, Mob):
            #    sprite.draw_health()
        #    if sprite not in self.group:
        #        if sprite not in self.flying_vehicles:
        #            if self.on_screen(sprite): # Only blits sprites if they are on screen.
        #                self.screen.blit(sprite.image, self.camera.apply(sprite))
        #            elif sprite == self.player.vehicle:
        #                if self.player.vehicle not in self.flying_vehicles:
        #                    self.screen.blit(sprite.image, self.camera.apply(sprite))
        #            elif sprite in self.companion_bodies:
        #                self.screen.blit(sprite.image, self.camera.apply(sprite))
        #            if self.draw_debug:
        #                try:
        #                    pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        #                except:
        #                    pass
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)

        # Only draws roofs when outside of buildings
        hits = pg.sprite.spritecollide(self.player, self.inside, False)
        if not hits:
            self.player_inside = False
            #self.overlay_group.draw(self.screen, self)
            #self.screen.blit(self.map.overlay.image, self.camera.apply(self.map))
        else:
            self.player_inside = True
            if self.player.in_vehicle:
                if self.player.vehicle in self.flying_vehicles:
                    self.player_inside = False
                    #self.overlay_group.draw(self.screen)
                    #self.screen.blit(self.map.overlay.image, self.camera.apply(self.map))

        # Draws flying vehicle sprites after roves.
        #for sprite in self.flying_vehicles:
        #    self.screen.blit(sprite.image, self.camera.apply(sprite))

        if self.hud_map:
            self.draw_minimap()
        if self.hud_overmap:
            self.draw_overmap()

        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        if self.night:
            self.render_fog()

        # HUD functions
        now = pg.time.get_ticks() # Only updates HUD info every 10 cycles to help reduce lag.
        if now - self.last_hud_update > FPS * 10:
            if self.player.in_vehicle:
                self.hud_health = self.player.vehicle.health / self.player.vehicle.max_health
                self.hud_health_num = self.player.vehicle.health
            elif self.player.possessing != None:
                self.hud_health = self.player.possessing.health / self.player.possessing.max_health
                self.hud_health_num = self.player.possessing.health
            else:
                self.hud_health = self.player.stats['health'] / self.player.stats['max health']
                self.hud_health_num = self.player.stats['health']
            self.hud_stamina = self.player.stats['stamina'] / self.player.stats['max stamina']
            self.hud_magica = self.player.stats['magica'] / self.player.stats['max magica']
            if self.player.ammo_cap1 + self.player.mag1 != 0:
                self.hud_ammo1 = "Right Ammo: " + str(self.player.mag1) + '/' + str(self.player.ammo_cap1)
            else:
                self.hud_ammo1 = ""
            if self.player.ammo_cap2 + self.player.mag2 != 0:
                self.hud_ammo2 = "Left Ammo: " + str(self.player.mag2) + '/' + str(self.player.ammo_cap2)
            else:
                self.hud_ammo2 = ""

            self.last_hud_update = now
        draw_player_stats(self.screen, 10, 10, self.hud_health)
        draw_player_stats(self.screen, 10, 40, self.hud_stamina, BLUE)
        draw_player_stats(self.screen, 10, 70, self.hud_magica, CYAN)
        self.draw_text(self.hud_ammo1, self.hud_font, 20, WHITE, 50, self.screen_height - 100, align="topleft")
        self.draw_text(self.hud_ammo2, self.hud_font, 20, WHITE, 50, self.screen_height - 50, align="topleft")
        #self.draw_text('Zombies: {}'.format(len(self.mobs)), self.hud_font, 30, WHITE, self.screen_width - 10, 10, align="topright")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, self.screen_width / 2, self.screen_height / 2, align="center")
        if self.vehicle_text == True:
            self.draw_text('E to enter, X to exit', self.hud_font, 30, WHITE, self.screen_width / 2, self.screen_height / 2 + 100,
                           align="center")
        if self.mechsuit_text == True:
            self.draw_text('E to enter, T to exit', self.hud_font, 30, WHITE, self.screen_width / 2, self.screen_height / 2 + 100,
                           align="center")
        if self.vehicle_key_text == True:
            self.draw_text('You need a key to operate this vehicle.', self.hud_font, 30, WHITE, self.screen_width / 2, self.screen_height / 2 + 100,
                           align="center")
        if self.talk_text == True:
            self.draw_text('E to Talk', self.hud_font, 30, WHITE, self.screen_width / 2, self.screen_height / 2 + 100,
                           align="center")
        if self.loot_text == True:
            self.draw_text('E to loot/store items', self.hud_font, 30, WHITE, self.screen_width / 2, self.screen_height / 2 + 100,
                           align="center")
        if self.bed_text == True:
            self.draw_text(self.bed_message, self.hud_font, 30, WHITE, self.screen_width / 2, self.screen_height / 2 + 160,
                           align="center")
        if self.toilet_text == True:
            self.draw_text('E to use toilet', self.hud_font, 30, WHITE, self.screen_width / 2, self.screen_height / 2 + 100,
                           align="center")
        if self.too_much_weight == True:
            self.draw_text('You can\'t carry any more weight', self.hud_font, 30, WHITE, self.screen_width / 2, self.screen_height / 2 + 100,
                           align="center")
        if self.lock_text == True:
            self.draw_text('E to pick lock', self.hud_font, 30, WHITE, self.screen_width / 2, self.screen_height / 2 + 100,
                           align="center")
        if self.pick_up_text == True:
            self.draw_text('E to pickup item', self.hud_font, 30, WHITE, self.screen_width / 2, self.screen_height / 2 + 150,
                           align="center")
        if self.station_text == True:
            self.draw_text('E to use ' + self.station_type, self.hud_font, 30, WHITE, self.screen_width / 2, self.screen_height / 2 + 150,
                           align="center")
        self.draw_text("FPS {:.0f}".format(self.clock.get_fps()), self.hud_font, 20, WHITE,
                       25, 100, align="topleft")
        self.draw_text("HP {:.0f}".format(self.hud_health_num), self.hud_font, 20, WHITE,
                       120, 10, align="topleft")
        self.draw_text("ST {:.0f}".format(self.player.stats['stamina']), self.hud_font, 20, WHITE,
                       120, 40, align="topleft")
        self.draw_text("MP {:.0f}".format(self.player.stats['magica']), self.hud_font, 20, WHITE,
                       120, 70, align="topleft")
        pg.display.flip()
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
                if event.key in  [pg.K_ESCAPE, pg.K_i]:
                    self.player.empty_mags() # This makes sure the bullets in your clip don't transfer to the wrong weapons if you switch weapons in your inventory
                    self.in_inventory_menu = True
                    self.in_menu = True
                if event.key == pg.K_e:
                    self.e_down = True
                else:
                    self.e_down = False
                #if event.key == pg.K_BACKQUOTE:  # Switches to last weapon
                #    self.player.toggle_previous_weapons()
                if event.key == pg.K_k:
                    self.in_stats_menu = True
                if event.key == pg.K_j:
                    self.in_quest_menu = self.in_menu = True
                    self.quest_menu = Quest_Menu(self)
                if event.key == pg.K_r:
                    self.player.pre_reload()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    trace_mem()
                    if self.player.vehicle != None:
                        print(self.group.get_layer_of_sprite(self.player.vehicle))
                    self.paused = not self.paused
                if event.key == pg.K_n:
                    self.night = not self.night
                if event.key == pg.K_EQUALS:
                    self.map.minimap.resize()
                if event.key == pg.K_MINUS:
                    self.map.minimap.resize(False)
                if event.key == pg.K_m: # Toggles hud mini map
                    self.hud_map = not self.hud_map
                if event.key == pg.K_o: # Toggles overworld map
                    self.hud_overmap = not self.hud_overmap
                if event.key == pg.K_b:
                    if not self.in_store_menu:
                        self.player.use_item()
                if event.key == pg.K_y:
                    self.player.place_item()
                if event.key == pg.K_g:
                    self.player.throw_grenade()
                if event.key == pg.K_t:
                    if self.player.possessing == None:
                        if self.player.stats['magica'] > 50 or self.player.dragon:
                            self.player.transform()
                    else:
                        self.player.possessing.depossess()

                if event.key == pg.K_f:
                    if self.player.dragon:
                        self.player.breathe_fire()
                if event.key == pg.K_l:
                    self.in_station_menu = True
                    self.in_menu = True
                    self.station_menu = Work_Station_Menu(self, 'crafting')
                if event.key == pg.K_u:
                    if self.player.in_vehicle:
                        if self.player.vehicle in self.flying_vehicles:
                            self.fly_menu = Fly_Menu(self)

                if event.key == pg.K_q:
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
                        self.screen.fill(BLACK)
                        self.save()
                if event.key ==  pg.K_l: # Saves game
                    if event.mod & pg.KMOD_CTRL:
                        self.in_load_menu = True
                if event.key == pg.K_SPACE:
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
