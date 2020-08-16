import pygame as pg
from random import uniform, choice, randint, random, randrange
from settings import *
from npcs import *
from os import path
import copy
from interactables import *
from collections import Counter
from menu import *
from vehicles import *
from math import ceil
from time import perf_counter

vec = pg.math.Vector2

def wall_check(sprite):  # Used for tile-based wall collisions
    if len(sprite.game.wall_tiles) > 0:
        proximity = sprite.game.map.tile_size / 3
        try:
            pdir = sprite.acc.normalize() * proximity
        except:
            pdir = vec(1, 0).rotate(-sprite.rot) * proximity
        x = int((sprite.pos.x + pdir.x) / sprite.game.map.tile_size)
        y = int((sprite.pos.y + pdir.y) / sprite.game.map.tile_size)
        if x < 0: return
        if y < 0: return
        if x > sprite.game.map.tiles_wide: return
        if y > sprite.game.map.tiles_high: return
        if sprite.game.map.tmxdata.get_tile_gid(x, y, sprite.game.wall_tile_layer) in sprite.game.wall_tiles:
            sprite.acc = sprite.acc.rotate(180)
            sprite.vel = sprite.vel.rotate(180)
            return True
        else:
            return False

def next_wall_check(sprite):  # Used for tile-based wall collisions
    if len(sprite.game.wall_tiles) > 0:
        try:
            pdir = sprite.acc.normalize()
        except:
            pdir = vec(1, 0).rotate(-sprite.rot)
        x = int(sprite.pos.x / sprite.game.map.tile_size + pdir.x)
        y = int(sprite.pos.y / sprite.game.map.tile_size + pdir.y)
        if x < 0: return
        if y < 0: return
        if x > sprite.game.map.tiles_wide: return
        if y > sprite.game.map.tiles_high: return
        if sprite.game.map.tmxdata.get_tile_gid(x, y, sprite.game.wall_tile_layer) in sprite.game.wall_tiles:
            return True
        else:
            return False

def in_wall(game, group, pos):
    for wall in group:
        if wall not in game.door_walls:
            if wall.rect.left < pos.x < wall.rect.right:
                if wall.rect.top < pos.y < wall.rect.bottom:
                    return wall
    else:
        return False

def set_elevation(sprite):
    # Sets elevation to the highest elevation you hit.
    hit_level = sprite
    hits = pg.sprite.spritecollide(sprite, sprite.game.elevations, False)
    if hits:
        for hit in hits:  # Uses only the highest elevation you hit.
            if hit not in sprite.game.climbables_and_jumpables:
                if hit.elevation > hit_level.elevation:
                    hit_level = hit
        sprite.elevation = hit_level.elevation

def color_image(image, color):
    temp_image = image.copy()
    color_image = pg.Surface(temp_image.get_size()).convert_alpha()
    color_image.fill(color)
    temp_image.blit(color_image, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
    return temp_image

def collide(sprite):
    sprite.hit_rect.centerx = sprite.pos.x
    for item in sprite.collide_list:
            collide_with_walls(sprite, item, 'x')
    if not (sprite.immaterial or sprite.flying):
        collide_with_elevations(sprite, 'x')
        collide_with_vehicles(sprite, 'x')

    sprite.hit_rect.centery = sprite.pos.y
    for item in sprite.collide_list:
            collide_with_walls(sprite, item, 'y')
    if not (sprite.immaterial or sprite.flying):
        collide_with_elevations(sprite, 'y')
        collide_with_vehicles(sprite, 'y')
    sprite.rect.center = sprite.hit_rect.center

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, dir):
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        if dir == 'x':
            if hits[0].rect.centerx > sprite.hit_rect.centerx: # going right
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx: # going left
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
        elif dir == 'y':
            if hits[0].rect.centery > sprite.hit_rect.centery: # going down
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery: # going up
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

    """
    if sprite in sprite.game.vehicles_on_screen:
        hits = pg.sprite.spritecollide(sprite, group, False, wall_vehicle_collide_hit2_rect)
        if hits:
            if dir == 'x':
                if hits[0].rect.centerx > sprite.hit_rect2.centerx: # Heading Right
                    sprite.pos.x = hits[0].rect.left - (sprite.hit_rect2.width / 2 + sprite.hrect_offset2.rotate(-sprite.rot).x)
                if hits[0].rect.centerx < sprite.hit_rect2.centerx: # Heading Left
                    sprite.pos.x = hits[0].rect.right + sprite.hit_rect2.width / 2 + sprite.hrect_offset2.rotate(-sprite.rot).x
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x
                sprite.hit_rect2.centerx = sprite.pos.x + sprite.hrect_offset2.rotate(-sprite.rot).x
            if dir == 'y':
                if hits[0].rect.centery > sprite.hit_rect2.centery: # Heading down
                    sprite.pos.y = hits[0].rect.top - (sprite.hit_rect2.height / 2 + sprite.hrect_offset2.rotate(-sprite.rot).y)
                if hits[0].rect.centery < sprite.hit_rect2.centery: # Heading up
                    sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect2.height / 2  + sprite.hrect_offset2.rotate(-sprite.rot).y
                sprite.vel.y = 0
                sprite.hit_rect.centery = sprite.pos.y
                sprite.hit_rect2.centery = sprite.pos.y + sprite.hrect_offset2.rotate(-sprite.rot).y
        hits = pg.sprite.spritecollide(sprite, group, False, wall_vehicle_collide_hit3_rect)
        if hits:
            if dir == 'x':
                if hits[0].rect.centerx > sprite.hit_rect3.centerx:  # Heading Right
                    sprite.pos.x = hits[0].rect.left - (sprite.hit_rect3.width / 2 + sprite.hrect_offset3.rotate(-sprite.rot).x)
                if hits[0].rect.centerx < sprite.hit_rect3.centerx:  # Heading Left
                    sprite.pos.x = hits[0].rect.right + sprite.hit_rect3.width / 2 + sprite.hrect_offset3.rotate(-sprite.rot).x
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x
                sprite.hit_rect3.centerx = sprite.pos.x + sprite.hrect_offset3.rotate(-sprite.rot).x
            if dir == 'y':
                if hits[0].rect.centery > sprite.hit_rect3.centery:  # Heading down
                    sprite.pos.y = hits[0].rect.top - (sprite.hit_rect3.height / 2 + sprite.hrect_offset3.rotate(-sprite.rot).y)
                if hits[0].rect.centery < sprite.hit_rect3.centery:  # Heading up
                    sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect3.height / 2 + sprite.hrect_offset3.rotate(-sprite.rot).y
                sprite.vel.y = 0
                sprite.hit_rect.centery = sprite.pos.y
                sprite.hit_rect3.centery = sprite.pos.y + sprite.hrect_offset3.rotate(-sprite.rot).y
        """

def vehicle_collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.hit_rect)
def vehicle_collide_hit2_rect(one, two):
    return one.hit_rect.colliderect(two.hit_rect2)
def vehicle_collide_hit3_rect(one, two):
    return one.hit_rect.colliderect(two.hit_rect3)
def vehicle_collide_any(one, two):
    return (one.hit_rect.colliderect(two.hit_rect) or one.hit_rect.colliderect(two.hit_rect2) or one.hit_rect.colliderect(two.hit_rect3))
def wall_vehicle_collide_hit2_rect(one, two):
    return one.hit_rect2.colliderect(two.rect)
def wall_vehicle_collide_hit3_rect(one, two):
    return one.hit_rect3.colliderect(two.rect)

def collide_with_vehicles(sprite, dir):
    forward = False
    hits = pg.sprite.spritecollide(sprite, sprite.game.vehicles_on_screen, False, vehicle_collide_any)
    if hits:
        if sprite != hits[0]:
            if hits[0].forward:
                forward = True
                sprite.gets_hit(hits[0].damage, 10, sprite.rot -180, 80)

    if not forward:
        hits = pg.sprite.spritecollide(sprite, sprite.game.vehicles_on_screen, False, vehicle_collide_hit_rect)
        if hits:
            if sprite != hits[0]:
                if dir == 'x':
                    if hits[0].rect.centerx > sprite.hit_rect.centerx:
                        sprite.pos.x = hits[0].hit_rect.left - sprite.hit_rect.width / 2
                    if hits[0].rect.centerx < sprite.hit_rect.centerx:
                        sprite.pos.x = hits[0].hit_rect.right + sprite.hit_rect.width / 2
                    sprite.vel.x = 0
                    sprite.hit_rect.centerx = sprite.pos.x
                elif dir == 'y':
                    if hits[0].rect.centery > sprite.hit_rect.centery:
                        sprite.pos.y = hits[0].hit_rect.top - sprite.hit_rect.height / 2
                    if hits[0].rect.centery < sprite.hit_rect.centery:
                        sprite.pos.y = hits[0].hit_rect.bottom + sprite.hit_rect.height / 2
                    sprite.vel.y = 0
                    sprite.hit_rect.centery = sprite.pos.y
        hits = pg.sprite.spritecollide(sprite, sprite.game.vehicles_on_screen, False, vehicle_collide_hit2_rect)
        if hits:
            if sprite != hits[0]:
                if dir == 'x':
                    if hits[0].rect.centerx > sprite.hit_rect.centerx:
                        sprite.pos.x = hits[0].hit_rect2.left - sprite.hit_rect.width / 2
                    if hits[0].rect.centerx < sprite.hit_rect.centerx:
                        sprite.pos.x = hits[0].hit_rect2.right + sprite.hit_rect.width / 2
                    sprite.vel.x = 0
                    sprite.hit_rect.centerx = sprite.pos.x
                elif dir == 'y':
                    if hits[0].rect.centery > sprite.hit_rect.centery:
                        sprite.pos.y = hits[0].hit_rect2.top - sprite.hit_rect.height / 2
                    if hits[0].rect.centery < sprite.hit_rect.centery:
                        sprite.pos.y = hits[0].hit_rect2.bottom + sprite.hit_rect.height / 2
                    sprite.vel.y = 0
                    sprite.hit_rect.centery = sprite.pos.y
        hits = pg.sprite.spritecollide(sprite, sprite.game.vehicles_on_screen, False, vehicle_collide_hit3_rect)
        if hits:
            if sprite != hits[0]:
                if dir == 'x':
                    if hits[0].rect.centerx > sprite.hit_rect.centerx:
                        sprite.pos.x = hits[0].hit_rect3.left - sprite.hit_rect.width / 2
                    if hits[0].rect.centerx < sprite.hit_rect.centerx:
                        sprite.pos.x = hits[0].hit_rect3.right + sprite.hit_rect.width / 2
                    sprite.vel.x = 0
                    sprite.hit_rect.centerx = sprite.pos.x
                elif dir == 'y':
                    if hits[0].rect.centery > sprite.hit_rect.centery:
                        sprite.pos.y = hits[0].hit_rect3.top - sprite.hit_rect.height / 2
                    if hits[0].rect.centery < sprite.hit_rect.centery:
                        sprite.pos.y = hits[0].hit_rect3.bottom + sprite.hit_rect.height / 2
                    sprite.vel.y = 0
                    sprite.hit_rect.centery = sprite.pos.y

def collide_with_elevations(sprite, dir):
    xwall = False
    ywall = False
    hits = pg.sprite.spritecollide(sprite, sprite.game.elevations_on_screen, False, collide_hit_rect)
    if hits:
        hit_level = hits[0]
        for hit in hits: # Uses only the highest elevation you hit.
            if hit.elevation > hit_level.elevation:
                hit_level = hit
        if dir == 'x':
            if hit_level.elevation - sprite.elevation > 3:
                xwall = True
                sprite.climbing = False
            elif hit_level.elevation - sprite.elevation == 3:
                if not sprite.climbing:
                    xwall = True
            elif hit_level.elevation - sprite.elevation == 2:
                if True not in [sprite.jumping, sprite.climbing]:
                    xwall = True
            elif hit_level.elevation - sprite.elevation <= 1:
                if hit_level.elevation - sprite.elevation < -1:
                    sprite.falling = True
                    sprite.pre_jump()
                sprite.elevation = hit_level.elevation
            if xwall:
                if hit_level.rect.centerx > sprite.hit_rect.centerx:
                    sprite.pos.x = hit_level.rect.left - sprite.hit_rect.width / 2
                if hit_level.rect.centerx < sprite.hit_rect.centerx:
                    sprite.pos.x = hit_level.rect.right + sprite.hit_rect.width / 2
                sprite.vel.x = 0
                sprite.hit_rect.centerx = sprite.pos.x
        elif dir == 'y':
            if hit_level.elevation - sprite.elevation > 3:
                ywall = True
                sprite.climbing = False
            elif hit_level.elevation - sprite.elevation == 3:
                if not sprite.climbing:
                    ywall = True
                else:
                    sprite.elevation = hit_level.elevation
            elif hit_level.elevation - sprite.elevation == 2:
                if True not in [sprite.jumping, sprite.climbing]:
                    ywall = True
                else:
                    sprite.elevation = hit_level.elevation
            elif hit_level.elevation - sprite.elevation <= 1:
                if hit_level.elevation - sprite.elevation < -1:
                    sprite.falling = True
                    sprite.pre_jump()
                sprite.elevation = hit_level.elevation
            if ywall:
                if hit_level.rect.centery > sprite.hit_rect.centery:
                    sprite.pos.y = hit_level.rect.top - sprite.hit_rect.height / 2
                if hit_level.rect.centery < sprite.hit_rect.centery:
                    sprite.pos.y = hit_level.rect.bottom + sprite.hit_rect.height / 2
                sprite.vel.y = 0
                sprite.hit_rect.centery = sprite.pos.y


# Used for detecting when a fireball hits an obstacle
def fire_collide(one, two):
    if one.hit_rect.colliderect(two.rect):
        return True
    else:
        return False


def random_inventory(character):
    tops = []
    bottoms = []
    character.inventory = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': [None], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'gloves': [None], 'shoes': [None], 'items': [None], 'gold': 0}

    # Separates out items to match character's gender
    if character.gender == 'male':
        random_hair = choice(SHORT_HAIR_LIST)
        tops = MALE_TOPS
        bottoms = MALE_BOTTOMS
    else:
        random_hair = choice(LONG_HAIR_LIST)
        tops = FEMALE_TOPS
        bottoms = FEMALE_BOTTOMS
    # Adds random items to inventory
    if character.armed:
        character.inventory['weapons'].append(choice(list(WEAPONS.keys())))
    character.inventory['tops'].append(choice(tops))
    character.inventory['bottoms'].append(choice(bottoms))
    character.inventory['gloves'].append(choice(list(GLOVES.keys())))
    character.inventory['shoes'].append(choice(list(SHOES.keys())))
    character.inventory['items'].append(choice(list(ITEMS.keys())))
    character.inventory['hair'].append(random_hair)
    change_clothing(character)

def random_inventory_item(container, temp_inventory):
    try:
        gender = container.gender
    except:
        gender = None

    for item_type in ITEM_TYPE_LIST:
        for i, value in enumerate(temp_inventory[item_type]):
            if value:
                if 'random ' in value:
                    temp_value = value.replace('random ', '')
                    temp_list = eval(temp_value + item_type.upper())
                    if 'gender' in (list(eval(item_type.upper()).values())[0]).keys():
                        female_list = []
                        male_list = []
                        for x in temp_list:
                            if x:
                                if eval(item_type.upper())[x]['gender'] in ['female', 'other']:
                                    female_list.append(x)
                            else:
                                female_list.append(x)
                            if x:
                                if eval(item_type.upper())[x]['gender'] in ['male', 'other']:
                                    male_list.append(x)
                            else:
                                male_list.append(x)
                        if gender == 'female':
                            if len(female_list) > 0:
                                container.inventory[item_type][i] = choice(female_list)
                            else:
                                container.inventory[item_type][i] = choice(temp_list)
                        else:
                            if len(male_list) > 0:
                                container.inventory[item_type][i] = choice(male_list)
                            else:
                                container.inventory[item_type][i] = choice(temp_list)
                    else:
                        container.inventory[item_type][i] = choice(temp_list)
                elif value == 'random':
                    if item_type == 'tops':
                        if gender == 'female':
                            container.inventory[item_type][i] = choice(FEMALE_TOPS)
                        elif gender in ['male', 'other']:
                            container.inventory[item_type][i] = choice(MALE_TOPS)
                        else:
                            container.inventory[item_type][i] = choice(list(TOPS.keys()))
                    elif item_type == 'bottoms':
                        if gender == 'male':
                            container.inventory[item_type][i] = choice(MALE_BOTTOMS)
                        elif gender in ['female', 'other']:
                            container.inventory[item_type][i] = choice(FEMALE_BOTTOMS)
                        else:
                            container.inventory[item_type][i] = choice(list(BOTTOMS.keys()))
                    elif item_type == 'hair':
                        if gender == 'male':
                            container.inventory[item_type][i] = choice(SHORT_HAIR_LIST)
                        elif gender in ['female', 'other']:
                            container.inventory[item_type][i] = choice(LONG_HAIR_LIST)
                        else:
                            container.inventory[item_type][i] = choice(list(HAIR.keys()))
                    else:
                        container.inventory[item_type][i] = choice(list(eval(item_type.upper()).keys()))
                else:
                    container.inventory[item_type][i] = temp_inventory[item_type][i]

def drop_all_items(sprite, delete_items = False):
    for item_type in ITEM_TYPE_LIST:
        if item_type != 'magic':
            if not delete_items:
                for item in sprite.inventory[item_type]:
                    if item:
                        Dropped_Item(sprite.game, sprite.pos + vec(randrange(-50, 50), randrange(-100, 100)), item_type, item)
            sprite.inventory[item_type] = [None]
            sprite.equipped[item_type] = None

def change_clothing(character, best = False, naked = False):
    # Adds items to equipped list
    remove_nones(character.inventory['tops'], character.inventory['bottoms'], character.inventory['hair'], character.inventory['weapons'], character.inventory['shoes'], character.inventory['gloves'], character.inventory['hats'])
    for item_type in ITEM_TYPE_LIST:
        if naked:
            character.equipped[item_type] = None
        elif not best:
            if item_type == 'weapons':
                not_lamps = list(set(character.inventory[item_type]) - set(NON_GUN_LIGHTS))
                if len(not_lamps) == 0:
                    not_lamps = [None]
                character.equipped[item_type] = choice(not_lamps)
            else:
                character.equipped[item_type] = choice(character.inventory[item_type])
        if best: # Changest into clothes with best ratings
            stat = 0
            best_item = None
            for item in character.inventory[item_type]:
                if item:
                    if item_type == 'weapons':
                        if WEAPONS[item]['gun']:
                            if WEAPONS[item]['damage'] > stat:
                                stat = WEAPONS[item]['damage']
                                best_item = item
                        elif WEAPONS[item]['melee damage'] > stat:
                            stat = WEAPONS[item]['melee damage']
                            best_item = item
                    elif item_type in ['tops', 'bottoms', 'gloves', 'shoes', 'hats']:
                        if eval(item_type.upper())[item]['armor'] > stat:
                            stat = eval(item_type.upper())[item]['armor']
                            best_item = item
                    else:
                        best_item = choice(character.inventory[item_type])
                else:
                    best_item = None
            character.equipped[item_type] = best_item
    character.set_gun_vars()

def lamp_check(character):
    if character.game.night:
        # checks for lamps
        add_light = False
        light_reach = 1
        for item in character.inventory['weapons']:
            if item in LIGHTS_LIST:
                if WEAPONS[item]['gun']:
                    character.equipped['weapons'] = item
                    character.lamp_hand = 'weapons'
                else:
                    character.equipped['weapons2'] = item
                    character.lamp_hand = 'weapons2'
                character.brightness = WEAPONS[item]['brightness']
                character.mask_kind = WEAPONS[item]['light mask']
                if 'light reach' in WEAPONS[item]:
                    light_reach = WEAPONS[item]['light reach']
                character.game.lights.add(character)
                character.light_mask_orig = pg.transform.scale(character.game.light_mask_images[character.mask_kind], (int(character.brightness * light_reach), character.brightness))
                character.light_mask = character.light_mask_orig.copy()
                character.light_mask_rect = character.light_mask.get_rect()
                if WEAPONS[item]['gun']:
                    character.light_mask_rect.center = character.body.melee_rect.center
                else:
                    character.light_mask_rect.center = character.body.melee2_rect.center
                character.body.update_animations()
                add_light = True
                break
        if not add_light:
            if character in character.game.lights:
                character.game.lights.remove(character)
    elif character.equipped['weapons2'] in LIGHTS_LIST:
        character.equipped['weapons2'] = None
        if character in character.game.lights:
            character.game.lights.remove(character)
        character.body.update_animations()

def remove_nones(*my_lists):
    for my_list in my_lists:
        while True:
            if None in my_list and len(my_list)!=1:
                my_list.remove(None)
            elif len(my_list)==1 and None in my_list:
                break
            if None not in my_list:
                break

def toggle_equip(character, var): # Toggles whether weapons are equipped/drawn or not
    if var:  # Unequips weapons
        if character.equipped['weapons']:
            character.current_weapon = character.equipped['weapons']
            character.equipped['weapons'] = None
        if character.equipped['weapons2']:
            character.current_weapon2 = character.equipped['weapons2']
            character.equipped['weapons2'] = None
    else:  # Equips weapons
        character.equipped['weapons'] = character.current_weapon
        character.equipped['weapons2'] = character.current_weapon2

def fix_angle(ang): #fixes angle measures so they are never greater than abs(180) which makes it easier to work with quadrants.
    angle = ang
    if angle > 180:
        angle = angle - 360
    if angle < -180:
        angle = angle + 360
    return angle

class Turret(pg.sprite.Sprite):
    def __init__(self, game, mother):
        self.mother = mother
        self._layer = BULLET_LAYER
        self.groups = game.turrets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.game.group.add(self)
        self.image_orig = self.game.player_tur
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        #self.rect = self.rect.inflate(100, 100)
        self.rect.center = self.mother.rect.center
        self.hit_rect = SMALL_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.light_mask = pg.transform.scale(self.game.light_mask_images[2], (600, 600))
        self.light_mask_rect = self.light_mask.get_rect()
        self.light_mask_rect.center = self.rect.center
        self.rot = 0
        self.rot_rel = 0
        self.rot_speed = 0
        self.last_shot = 0
        self.occupied = False
        self.equipped = 'tank turret'
        self.vel = vec(0, 0)
        self.max_rot_speed = 20
        self.direction = vec(1, 0)

    def rotate_to(self, vec):
        vector = vec
        angle = fix_angle(vector.angle_to(self.direction))
        if angle < -1:
            self.rot_speed = -self.max_rot_speed * 10 * abs(angle) / 180
        elif angle > 1:
            self.rot_speed = self.max_rot_speed * 10 * abs(angle) / 180
        else:
            self.rot_speed = 0

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.equipped]['rate']:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.game.player.pos + WEAPONS[self.equipped]['offset'].rotate(-self.rot)
            for i in range(WEAPONS[self.equipped]['bullet_count']):
                Bullet(self, self.game, pos, dir, self.rot, self.equipped)
                snd = choice(self.game.weapon_sounds[WEAPONS[self.equipped]['type']])
                if snd.get_num_channels() > 2:
                    snd.stop()
                snd.play()
            if WEAPONS[self.equipped]['gun']:
                MuzzleFlash(self.game, pos)

    def update(self):
        if self.occupied == True:
            if self.mother.driver == self.game.player:
                self.rotate_to(self.game.player.mouse_direction)
                if pg.mouse.get_pressed() in [(1, 0, 1), (1, 1, 1), (1, 0, 0), (1, 1, 0)]:
                    self.shoot()
            self.rect.center = self.mother.rect.center
            self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
            self.direction = vec(1, 0).rotate(-self.rot)
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            self.rect.center = self.mother.rect.center
            self.hit_rect.center = self.rect.center
            self.light_mask_rect.center = self.rect.center
        if not self.mother.alive():
            self.kill()

class Vehicle(pg.sprite.Sprite):
    def __init__(self, game, center, kind, map, health = None):
        self.kind = self.race = self.species = kind
        self.data = VEHICLES[kind]
        self._layer = self.data['layer']
        self.mountable = self.data['mountable']
        self.veh_acc = self.data['acceleration']
        self.rot_speed = self.data['rot speed']
        self.forward_sound_playing = False
        if 'run sound' in self.data.keys():
            self.run_sound = self.data['run sound']
        else:
            self.run_sound = None
        if 'drive sound' in self.data.keys():
            self.drive_sound = self.data['drive sound']
        else:
            self.drive_sound = None
        if 'fuel' in self.data.keys():
            self.fuel = self.data['fuel']
        else:
            self.fuel = None
        self.cat = self.data['cat']
        if self.cat in BOATS:
            self.flying = False
            self.groups = game.all_sprites, game.vehicles, game.boats, game.all_vehicles
        elif self.cat in AMPHIBIOUS_VEHICLES:
            self.flying = False
            self.groups = game.all_sprites, game.vehicles, game.amphibious_vehicles, game.all_vehicles
        elif self.cat in FLYING_VEHICLES:
            self.groups = game.all_sprites, game.flying_vehicles, game.all_vehicles
            self.flying = True
        else:
            self.flying = False
            self.groups = game.all_sprites, game.vehicles, game.land_vehicles, game.all_vehicles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.game.group.add(self)
        self.image_orig = self.game.vehicle_images[self.data['image']]
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.hit_rect = self.data['hit rect'].copy()
        self.hit_rect2 = pg.Rect(0, 0, int(self.hit_rect.width*(5/6)), int(self.hit_rect.width*(5/6)))
        self.hit_rect3 = self.hit_rect2.copy()
        self.hrect_offset2 = vec(self.hit_rect2.width/2, 0)
        self.hrect_offset3 = vec(-self.hit_rect3.width/2, 0)
        self.hit_rect2.center = self.rect.center + self.hrect_offset2
        self.hit_rect3.center = self.rect.center + self.hrect_offset3
        self.hit_rect.center = self.rect.center
        self.transparency = 255 # Used to make vehicles look like they are sinking
        self.player_walk_anim = self.data['walk animation']
        self.player_rattack_anim = self.data['rattack animation']
        self.player_lattack_anim = self.data['lattack animation']
        self.damage = self.data['damage']
        self.light_mask = None
        self.vel = vec(0, 0)
        self.pos = vec(center)
        self.rot = 0
        self.prev_rot = 0
        self.occupied = False
        self.damaged = False
        self.jumping = False
        self.climbing = False
        self.immaterial = False
        self.invisible = False
        self.protected = False
        self.offensive = False
        self.aggression = "vehicle"
        self._forward = False
        self.elevation = 0
        self.in_vehicle = self.in_player_vehicle = False
        if not health:
            self.stats = {'health': self.data['hp'], 'max health': self.data['hp']}
        else:
            self.stats = {'health': health, 'max health': self.data['hp']}
        self.last_hit = 0
        self.last_drain = 0
        self.living = True
        self.driver = None
        self.turret = None
        if self.cat == 'tank':
            self.turret = Turret(game, self)
            collide_list = ['walls']
        elif self.cat == 'boat':
            collide_list = ['walls', 'shallows']
        elif self.cat == 'airship':
            collide_list = []
        else:
            collide_list = ['walls', 'water']
        self.collide_list = []
        for item in collide_list:
            self.collide_list.append(eval("self.game." + item + "_on_screen"))

    @property
    def forward(self): #This is the method that is called whenever you access
        return self._forward
    @forward.setter #This is the method that is called whenever you set a value
    def forward(self, value):
        if value!=self._forward:
            self._forward = value
            if self.occupied:
                if value:
                    if self.drive_sound:
                        if not self.forward_sound_playing:
                            self.forward_sound_playing = True
                            self.game.channel6.stop()
                            self.game.channel6.play(self.game.effects_sounds[self.drive_sound], loops=-1)
                else:
                    if self.run_sound:
                        if self.forward_sound_playing:
                            self.game.channel6.stop()
                            self.game.channel6.play(self.game.effects_sounds[self.run_sound], loops=-1)
                            self.forward_sound_playing = False

    def add_health(self, amount):
        self.stats['health']+= amount
        if self.stats['health']> self.stats['max health']:
            self.stats['health']= self.stats['max health']
        if self.stats['health'] <= 0:
            self.living = False
            self.exit_vehicle()
        if self.game.hud_health_stats == self.stats:
            self.game.hud_health = self.stats['health'] / self.stats['max health']

    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[self.game.key_map['dismount']]:
            self.exit_vehicle()

    def reequip(self):
        if self.data['weapons']:
            self.driver.equipped['weapons'] = self.driver.current_weapon = self.data['weapons']
        if self.data['weapons2']:
            self.driver.equipped['weapons2'] = self.driver.current_weapon2 = self.data['weapons2']

    def enter_vehicle(self, driver):
        if driver == self.game.player:
            self.game.hud_health_stats = self.stats
        if self.run_sound:
            self.game.channel6.play(self.game.effects_sounds[self.run_sound], loops=-1)
        self.driver = driver
        self.driver.pos = vec(self.rect.center)# centers the driver in the vehicle.
        self.driver.rect.center = self.driver.hit_rect.center = self.rect.center
        self.driver.rot = self.rot # rotates the driver to fit the vehicle's rotation.
        self.occupied = True
        self.driver.in_vehicle = True
        self.driver.vehicle = self
        if self.data['weapons']:
            self.driver.last_weapon = self.driver.current_weapon
            self.driver.inventory['weapons'].append(self.data['weapons'])
            self.driver.equipped['weapons'] = self.driver.current_weapon = self.data['weapons']
        if self.data['weapons2'] or self.cat == 'tank':
            self.driver.last_weapon2 = self.driver.current_weapon2
            self.driver.inventory['weapons'].append(self.data['weapons2'])
            self.driver.equipped['weapons2'] = self.driver.current_weapon2 = self.data['weapons2']
        if self.data['weapons'] or self.data['weapons2']:
            self.driver.pre_reload()
        if self.cat == 'airship':
            self.light_mask = pg.transform.scale(self.game.light_mask_images[6], (800, 800))
            self.light_mask_rect = self.light_mask.get_rect()
            self.light_mask_rect.center = self.rect.center
            self.game.lights.add(self)
            self.game.flying_vehicles.add(self.driver)
            if self.driver == self.game.player:
                self.driver.in_flying_vehicle = True
                for companion in self.game.companions:
                    companion.in_player_vehicle = True
                    companion.in_flying_vehicle = True
        self.add(self.game.occupied_vehicles)
        self.add(self.game.moving_targets)
        self.driver.human_body.update_animations()
        if self.driver.has_dragon_body:
            self.driver.dragon_body.update_animations()
        if self.cat == 'tank':
            self.light_mask = self.game.flashlight_masks[int(self.rot/3)]
            self.light_mask_rect = self.light_mask.get_rect()
            self.light_mask_rect.center = self.rect.center
            self.game.lights.add(self)
            if self.driver == self.game.player:
                for companion in self.game.companions:
                    companion.in_player_vehicle = True
            self.turret.add(self.game.occupied_vehicles)
            self.turret.add(self.game.lights)
            self.turret.occupied = True
            self.driver.pre_reload()
        if self.kind == 'skiff':
            if self.driver == self.game.player:
                for companion in self.game.companions:
                    companion.in_player_vehicle = True
        self.game.beg = perf_counter()  # resets dt

    def exit_vehicle(self):
        if self.driver == self.game.player:
            self.game.hud_health_stats = self.driver.stats
        self.game.channel6.stop()
        self.forward_sound_playing = False
        self.pos = vec(self.rect.center)
        self.occupied = False
        self.driver.in_vehicle = False
        self.driver.friction = PLAYER_FRIC
        self.driver.acceleration = PLAYER_ACC
        if self.data['weapons']:
            self.driver.inventory['weapons'].remove(self.data['weapons'])
            if self.driver.last_weapon != self.data['weapons']:
                self.driver.equipped['weapons'] = self.driver.current_weapon = self.driver.last_weapon
            else:
                self.driver.equipped['weapons'] = None
        if self.data['weapons2']:
            self.driver.inventory['weapons'].remove(self.data['weapons2'])
            if self.driver.last_weapon2 != self.data['weapons2']:
                self.driver.equipped['weapons2'] = self.driver.current_weapon2 = self.driver.last_weapon2
            else:
                self.driver.equipped['weapons2'] = None
        self.driver.vehicle = None
        if self.cat == 'tank':
            self.light_mask = None
            self.game.lights.remove(self)
            self.turret.remove(self.game.occupied_vehicles)
            self.turret.remove (self.game.lights)
            self.turret.occupied = False
            if self.driver == self.game.player:
                for companion in self.game.companions:
                    companion.in_player_vehicle = False
        elif self.cat == 'airship':
            self.light_mask = None
            self.game.lights.remove(self)
            self.driver.remove(self.game.flying_vehicles)
            if self.driver == self.game.player:
                for companion in self.game.companions:
                    companion.in_player_vehicle = False
                    companion.in_flying_vehicle = False
        if self.kind == 'skiff':
            if self.driver == self.game.player:
                for companion in self.game.companions:
                    companion.in_player_vehicle = False
        self.remove(self.game.occupied_vehicles)
        self.remove(self.game.moving_targets)
        if self.driver == self.game.player:
            self.driver.empty_mags()
        self.driver.human_body.update_animations()
        if self.driver.has_dragon_body:
            self.driver.dragon_body.update_animations()
        self.driver.in_flying_vehicle = False
        self.driver = None
        self.game.beg = perf_counter()  # resets dt
    

    def gets_hit(self, damage, knockback = 0, rot = 0, dam_rate = DAMAGE_RATE):
        if self.living:
            now = pg.time.get_ticks()
            if now - self.last_hit > dam_rate * 2:
                self.game.effects_sounds[self.data['hit sound']].play()
                self.last_hit = now
                self.add_health(-damage)
                self.transparency -= 2
                if self.transparency < 30:
                    self.transparency = 30

    def update(self):
        if self.occupied == True:
            now = pg.time.get_ticks()
            # Increases vehicle friction when not accelerating
            if self.cat == 'airship':
                self.driver.friction = -.03
            elif self.driver.is_moving():
                # Makes the friction greater when the vehicle is sliding in a direction that is not straight forward.
                angle_difference = abs(fix_angle(self.driver.vel.angle_to(self.driver.direction)))
                if angle_difference > 350:
                    angle_difference = 0
                if angle_difference < 0.1:
                    angle_difference = 0
                self.driver.friction = -(angle_difference/1000 + .015)
            else:
                self.driver.friction = -.28
            if self.driver.swimming:
                self.image = pg.transform.rotate(self.image_orig, self.rot)
                self.image.fill((255, 255, 255, self.transparency), None, pg.BLEND_RGBA_MULT)
            else:
                self.image = pg.transform.rotate(self.image_orig, self.rot)
                if now - self.last_drain > 50:
                    self.last_drain = now
                    self.transparency += 1
                    if self.transparency > 255:
                        self.transparency = 255
            self.driver.acceleration = self.veh_acc
            self.rot = self.driver.rot
            if self.turret: # Rotates the turret if you rotate the vehicle.
                delta_rot = self.prev_rot - self.rot
                if delta_rot != 0:
                    self.turret.rot -= delta_rot
                self.prev_rot = self.rot
            self.rect = self.image.get_rect()
            self.pos = self.driver.pos #vec(self.driver.rect.center)
            self.rect.center = self.pos
            self.hit_rect2.center = self.pos + self.hrect_offset2.rotate(-self.rot)
            self.hit_rect3.center = self.pos + self.hrect_offset3.rotate(-self.rot)
            # This puts the companions in the vehicle with the player
            if self.driver == self.game.player:
                offset_vec = vec(80, 0).rotate(-(self.rot + 180))
                for companion in self.game.companions:
                    if companion.in_player_vehicle:
                        if companion in self.game.npcs:
                            companion.pos = companion.rect.center = companion.talk_rect.center = self.driver.pos + offset_vec
            collide(self)
            self.get_keys() # this needs to be last in this method to avoid executing the rest of the update section if you exit
            if self.turret:
                self.turret.update()
            if self.light_mask:
                if self.cat == 'tank':
                    self.light_mask = self.game.flashlight_masks[int(self.turret.rot/3)]
                    self.light_mask_rect = self.light_mask.get_rect()
                self.light_mask_rect.center = self.rect.center


class Character(pg.sprite.Sprite):
    def __init__(self, game, mother, dragon = False):
        self.mother = mother
        self.game = game
        self.dragon = dragon
        if not self.dragon:
            self.race = self.mother.equipped['race']
        else:
            self.race = self.mother.equipped['race'] + 'dragon'
        if self.mother in self.game.npcs:
            self._layer = MOB_LAYER
        else:
            self._layer = PLAYER_LAYER
        self.groups = game.all_sprites, game.npc_bodies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game.group.add(self)
        self.surface_width = self.surface_height = 250
        self.body_surface = pg.Surface((self.surface_width, self.surface_height)).convert()
        self.body_surface.fill(TRANSPARENT)
        self.image = self.body_surface
        self.image.set_colorkey(TRANSPARENT) #makes transparent
        self.rect = self.image.get_rect()
        self.rect.center = self.mother.pos
        # Collission rects for left and right hands/weapons.
        self.melee_rect = pg.Rect(0, 0, MELEE_SIZE, MELEE_SIZE)
        self.weapon_melee_rect = pg.Rect(0, 0, MELEE_SIZE, MELEE_SIZE)
        self.mid_weapon_melee_rect = pg.Rect(0, 0, MELEE_SIZE, MELEE_SIZE)
        self.melee2_rect = pg.Rect(0, 0, MELEE_SIZE, MELEE_SIZE)
        self.weapon2_melee_rect = pg.Rect(0, 0, MELEE_SIZE, MELEE_SIZE)
        self.mid_weapon2_melee_rect = pg.Rect(0, 0, MELEE_SIZE, MELEE_SIZE)
        self.swing_weapon1 = False # Used for timing melee attacks for stinging vs stabbing weapons.
        self.swing_weapon2 = False  # Used for timing melee attacks for stinging vs stabbing weapons.
        # Default Animation lists
        if self.mother not in self.game.npcs:
            self.climbing_shoot_anim = self.render_animation([CP_CLIMB0])
            self.climbing_weapon_anim = self.render_animation(CLIMB)
            self.climbing_weapon_melee_anim = self.render_animation(CLIMB_MELEE)
            self.climbing_l_weapon_melee_anim = self.render_animation(L_CLIMB_MELEE)
            self.walk_melee_anim = self.render_animation(WALK_PUNCH)
            self.walk_l_melee_anim = self.render_animation(L_WALK_PUNCH)
            self.dual_melee_anim = self.render_animation(D_PUNCH)
            self.dual_reload_anim = self.render_animation(RELOAD + L_RELOAD)
            self.walk_reload_anim = self.render_animation(WALK_RELOAD)
            self.l_walk_reload_anim = self.render_animation(L_WALK_RELOAD)
            self.walk_dual_reload_anim = self.render_animation(WALK_RELOAD + L_WALK_RELOAD)
            self.l_shoot_anim = self.render_animation(L_SHOOT)
            self.l_reload_anim = self.render_animation(L_RELOAD)

        if self.mother.gun:
            self.shoot_anim = self.render_animation(SHOOT)
            self.reload_anim = self.render_animation(RELOAD)

        self.jump_anim = self.render_animation(JUMP)
        self.stand_anim = self.render_animation(STAND)
        self.run_anim = self.render_animation(RUNNING)
        self.walk_anim = self.render_animation(WALK)
        self.melee_anim = self.render_animation(PUNCH)
        self.l_melee_anim = self.render_animation(L_PUNCH)
        self.shallows_anim = self.render_animation(SHALLOWS_WALK)
        # These animations never have weapons
        toggle_equip(self.mother, True) # This makes it so these animations are not ever created with weapons
        if self.mother not in self.game.npcs:
            self.swim_jump_anim = self.render_animation(WATER_JUMP)
            self.climb_jump_anim = self.render_animation(CLIMB_JUMP)
            self.climbing_melee_anim = self.render_animation(CLIMB_MELEE)
            self.climbing_l_melee_anim = self.render_animation(L_CLIMB_MELEE)

        self.climbing_anim = self.render_animation(CLIMB)
        self.swim_anim = self.render_animation(SWIM, True)
        self.swim_melee_anim = self.render_animation(WATER_PUNCH, True)
        #self.animations_cache_list = [self.stand_anim, self.shoot_anim, self.climbing_shoot_anim, self.climbing_weapon_anim, self.climbing_weapon_melee_anim, self.climbing_l_weapon_melee_anim, self.run_anim, self.walk_anim, self.melee_anim, self.walk_melee_anim, self.walk_l_melee_anim, self.dual_melee_anim,  self.l_melee_anim,  self.jump_anim, self.shallows_anim, self.reload_anim, self.l_reload_anim, self.dual_reload_anim, self.swim_anim, self.swim_jump_anim, self.swim_melee_anim, self.climb_jump_anim, self.climbing_anim, self.climbing_melee_anim, self.climbing_l_melee_anim]
        toggle_equip(self.mother, False)
        self.frame = 0
        self.last_step = 0

        self.weapon_pos = vec(0, 0)
        self.weapon2_pos = vec(0, 0)
        self.update_weapon_width()
        self.weapon_angle = 0
        self.weapon2_angle = 0
        # Must be last line in init.
        self.body_surface = self.stand_anim[0][0]

    def render_animation(self, animation_list, swimming = False):
        if not self.mother.possessing:
            self.colors = self.mother.colors
        else:
            self.colors = self.mother.possessing.colors
        if not self.dragon:
            self.race = self.mother.equipped['race'].replace('dragon', '')
        else:
            if 'dragon' not in self.mother.equipped['race']:
                self.race = self.mother.equipped['race'] + 'dragon'
            else:
                self.race = self.mother.equipped['race']
        animation_images = []
        weapons_positions = []
        weapons2_positions = []
        torso_pos = []
        for part_placement in animation_list:
            surface_width = self.surface_width
            surface_height = self.surface_height
            body_surface = pg.Surface((surface_width, surface_height), pg.SRCALPHA).convert_alpha()
            rect = self.body_surface.get_rect()

            if self.mother.equipped['gender'] == 'other':
                body_part_images_list = 'male' + '_' + self.race + '_' + 'images'  # Used male images by default for 'other'
            else:
                body_part_images_list = self.mother.equipped['gender'] + '_' + self.race + '_' + 'images'
            part_image_dict = {0: 0, 1: 0, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 5, 9: 6, 10: 6}
            reverse_list = [1, 4, 6, 10]
            i = 0
            for part in part_placement:
                if i in range(0, 9):
                    if i == 0 and swimming: # draws swimming shadow (the part of the body that's under water).
                        temp_img = self.game.swim_shadow_image
                        colored_img = color_image(temp_img, self.colors['skin'])
                        temp_rect = colored_img.get_rect()
                        body_surface.blit(colored_img, (rect.centerx - (temp_rect.centerx + 40), rect.centery - (temp_rect.centery)))
                    temp_img = self.game.humanoid_images[body_part_images_list][part_image_dict[i]]
                    if i in reverse_list:
                        temp_img = pg.transform.flip(temp_img, False, True)
                    colored_img = color_image(temp_img, self.colors['skin'])
                    image = pg.transform.rotate(colored_img, part[2])
                    temp_rect = image.get_rect()
                    body_surface.blit(image, (rect.centerx - (temp_rect.centerx - part[0]), rect.centery - (temp_rect.centery - part[1])))
                    if i == 7 and 'mechanima' in self.mother.equipped['race']: # draws back lights on mechs.
                        temp_img = self.game.mech_back_image
                        colored_img = color_image(temp_img, self.colors['hair'])
                        temp_rect = colored_img.get_rect()
                        body_surface.blit(colored_img, (rect.centerx - (temp_rect.centerx - part[0]), rect.centery - (temp_rect.centery - part[1])))

                if i in [0, 1, 2, 3, 4, 7]: #Adds all clothing except weapons and hats.
                    if self.mother.equipped[EQUIP_DRAW_LIST[i]]:
                        dict = eval(EQUIP_DRAW_LIST[i].upper())
                        imgpath = eval('self.game.' + EQUIP_IMG_LIST[i] + '_images')
                        temp_img = imgpath[dict[self.mother.equipped[EQUIP_DRAW_LIST[i]]]['image']]
                        if 'color' in dict[self.mother.equipped[EQUIP_DRAW_LIST[i]]]:
                            temp_img = color_image(temp_img, dict[self.mother.equipped[EQUIP_DRAW_LIST[i]]]['color'])
                        image = pg.transform.rotate(temp_img, part[2])
                        temp_rect = image.get_rect()
                        body_surface.blit(image, (rect.centerx - (temp_rect.centerx - part[0]), rect.centery - (temp_rect.centery - part[1])))
                    if i == 7: #Adds shirt/top
                        torso_pos = part  # used to place the wings on at the correct location/angle

                elif i == 9:
                    weapon_pos = vec(part[0], part[1])
                    weapon_angle = part[2]
                    if self.mother.equipped['weapons']:
                        temp_img = self.game.weapon_images[WEAPONS[self.mother.equipped['weapons']]['image']]
                        if 'color' in WEAPONS[self.mother.equipped['weapons']]:
                            temp_img = color_image(temp_img, WEAPONS[self.mother.equipped['weapons']]['color'])
                        image = pg.transform.rotate(temp_img, part[2])
                        temp_rect = image.get_rect()
                        body_surface.blit(image, (rect.centerx - (temp_rect.centerx - part[0]), rect.centery - (temp_rect.centery - part[1])))
                elif i == 10:
                    weapon2_pos = vec(part[0], part[1])
                    weapon2_angle = part[2]
                    if self.mother.equipped['weapons2']:
                        temp_img = self.game.weapon_images[WEAPONS[self.mother.equipped['weapons2']]['image']]
                        if 'color' in WEAPONS[self.mother.equipped['weapons2']]:
                            temp_img = color_image(temp_img, WEAPONS[self.mother.equipped['weapons2']]['color'])
                        image = pg.transform.rotate(temp_img, part[2])
                        temp_rect = image.get_rect()
                        body_surface.blit(image, (rect.centerx - (temp_rect.centerx - part[0]), rect.centery - (temp_rect.centery - part[1])))
                    if 'dragon' not in self.race:
                        if self.mother.equipped['hair']:
                            temp_img = self.game.hair_images[HAIR[self.mother.equipped['hair']]['image']]
                            colored_img = color_image(temp_img, self.colors['hair'])
                            image = pg.transform.rotate(colored_img, part_placement[8][2])
                            temp_rect = image.get_rect()
                            body_surface.blit(image, (rect.centerx - (temp_rect.centerx - part_placement[8][0]), rect.centery - (temp_rect.centery - part_placement[8][1])))
                        if self.mother.equipped['hats']:
                            temp_img = self.game.hat_images[HATS[self.mother.equipped['hats']]['image']]
                            if 'color' in HATS[self.mother.equipped['hats']]:
                                temp_img = color_image(temp_img, HATS[self.mother.equipped['hats']]['color'])
                            image = pg.transform.rotate(temp_img, part_placement[8][2])
                            temp_rect = image.get_rect()
                            body_surface.blit(image, (rect.centerx - (temp_rect.centerx - part_placement[8][0]), rect.centery - (temp_rect.centery - part_placement[8][1])))
                # Places wings
                elif 'dragon' in self.race and i == 11:
                    wing1_pos = vec(WING1_OFFSET).rotate(-torso_pos[2])
                    wing2_pos = vec(WING2_OFFSET).rotate(-torso_pos[2])
                    temp_img = self.game.humanoid_images[body_part_images_list][6]
                    colored_img = color_image(temp_img, self.colors['skin'])
                    image = pg.transform.rotate(colored_img, part[0] + torso_pos[2])
                    temp_rect = image.get_rect()
                    body_surface.blit(image, (rect.centerx - (temp_rect.centerx - (torso_pos[0] + wing1_pos.x)), rect.centery - (temp_rect.centery - (torso_pos[1] + wing1_pos.y))))
                    temp_img = self.game.humanoid_images[body_part_images_list][6]
                    colored_img = color_image(temp_img, self.colors['skin'])
                    temp_img = pg.transform.flip(colored_img, False, True)
                    image = pg.transform.rotate(temp_img, part[1] + torso_pos[2])
                    temp_rect = image.get_rect()
                    body_surface.blit(image, (rect.centerx - (temp_rect.centerx - (torso_pos[0] + wing2_pos.x)), rect.centery - (temp_rect.centery - (torso_pos[1] + wing2_pos.y))))
                    if not self.mother.equipped['hats'] == None:  # This makes it so horns on helmets are drawn over wings, not under them.
                        image = pg.transform.rotate(self.game.hat_images[HATS[self.mother.equipped['hats']]['image']], part_placement[8][2])
                        temp_rect = image.get_rect()
                        body_surface.blit(image, (rect.centerx - (temp_rect.centerx - part_placement[8][0]), rect.centery - (temp_rect.centery - part_placement[8][1])))
                i += 1
            animation_images.append(body_surface)
            weapons_positions.append([weapon_pos, weapon_angle])
            weapons2_positions.append([weapon2_pos, weapon2_angle])
        return [animation_images, weapons_positions, weapons2_positions]

    def animate(self, animation_info, speed):
        animation_images = animation_info[0]
        weapon_info = animation_info[1]
        weapon2_info = animation_info[2]
        now = pg.time.get_ticks()
        if self.frame > len(animation_images) - 1: # Makes sure the frame isn't greater than current animation
            self.frame = 0
        if now - self.last_step > speed:
            self.body_surface = animation_images[self.frame]
            self.weapon_pos = weapon_info[self.frame][0]
            self.weapon_angle = weapon_info[self.frame][1]/2
            self.weapon2_pos = weapon2_info[self.frame][0]
            self.weapon2_angle = weapon2_info[self.frame][1]/2
            self.last_step = now
            self.frame += 1

    def update_animations(self): # This needs to be done whenever the player or an NPC switches a weapon or other animation dependent equipment
        if self.dragon and (self.mother.equipped['race'] not in list(RACE.keys())):
            return
        else:
            #Default animaitons if no weapons
            self.stand_anim = self.render_animation(STAND)
            if not self.game.in_character_menu:
                if (self.mother not in self.game.npcs) or (self.mother in self.game.companions):
                    if self.mother.bow:
                        self.l_reload_anim = self.render_animation(L_BOW_RELOAD)
                        self.l_shoot_anim = self.render_animation(L_BOW_SHOOT)
                    else:
                        self.l_reload_anim = self.render_animation(L_RELOAD)
                        self.l_shoot_anim = self.render_animation(L_SHOOT)
                    self.walk_reload_anim = self.render_animation(WALK_RELOAD)
                    self.l_walk_reload_anim = self.render_animation(L_WALK_RELOAD)
                    self.walk_dual_reload_anim = self.render_animation(WALK_RELOAD + L_WALK_RELOAD)
                    self.climbing_shoot_anim = self.render_animation(CLIMB_SHOOT)
                    self.climbing_weapon_anim = self.render_animation(CLIMB)
                    self.climbing_weapon_melee_anim = self.render_animation(CLIMB_MELEE)
                    self.climbing_l_weapon_melee_anim = self.render_animation(L_CLIMB_MELEE)
                    self.dual_melee_anim = self.render_animation(D_PUNCH)
                    self.walk_melee_anim = self.render_animation(WALK_PUNCH)
                    self.walk_l_melee_anim = self.render_animation(L_WALK_PUNCH)

                if self.mother.bow:
                    self.reload_anim = self.render_animation(BOW_RELOAD)
                    self.shoot_anim = self.render_animation(BOW_SHOOT)
                elif self.mother.gun:
                    self.reload_anim = self.render_animation(RELOAD)
                    self.shoot_anim = self.render_animation(SHOOT)

                self.jump_anim = self.render_animation(JUMP)
                self.run_anim = self.render_animation(RUNNING)
                self.walk_anim = self.render_animation(WALK)
                self.melee_anim = self.render_animation(PUNCH)
                self.l_melee_anim = self.render_animation(L_PUNCH)
                self.shallows_anim = self.render_animation(SHALLOWS_WALK)

                # These animations never have weapons
                self.mother.current_weapon = self.mother.equipped['weapons']
                self.mother.current_weapon2 = self.mother.equipped['weapons2']
                toggle_equip(self.mother, True) # This makes it so these animations are not ever created with weapons
                if (self.mother not in self.game.npcs) or (self.mother in self.game.companions):
                    self.swim_jump_anim = self.render_animation(WATER_JUMP)
                    self.climb_jump_anim = self.render_animation(CLIMB_JUMP)
                    self.climbing_melee_anim = self.render_animation(CLIMB_MELEE)
                    self.climbing_l_melee_anim = self.render_animation(L_CLIMB_MELEE)

                self.climbing_anim = self.render_animation(CLIMB)
                self.swim_anim = self.render_animation(SWIM, True)
                self.swim_melee_anim = self.render_animation(WATER_PUNCH, True)
                toggle_equip(self.mother, False)

                # Default animations if right equipped
                if self.mother.equipped['weapons']:
                    #self.reload_anim = self.render_animation(eval(WEAPONS[self.mother.equipped['weapons']]['reload animation']))
                    self.stand_anim = self.render_animation([eval(WEAPONS[self.mother.equipped['weapons']]['grip'])])  # Change after animations are created
                    self.shoot_anim = self.render_animation([eval(WEAPONS[self.mother.equipped['weapons']]['grip'])])
                    self.walk_anim = self.render_animation(eval(WEAPONS[self.mother.equipped['weapons']]['walk']))
                    self.melee_anim = self.render_animation(eval(WEAPONS[self.mother.equipped['weapons']]['melee animation']))
                    if WEAPONS[self.mother.equipped['weapons']]['melee animation'] == 'SWIPE':
                        self.swing_weapon1 = True
                        self.walk_melee_anim = self.render_animation(WALK_SWIPE)
                    else:
                        self.swing_weapon1 = False
                # Default animations if left equipped
                if self.mother.equipped['weapons2']:
                    #self.l_reload_anim = self.render_animation(eval('L_' + WEAPONS[self.mother.equipped['weapons2']]['reload animation']))
                    self.l_shoot_anim = self.render_animation([eval('L_' + WEAPONS[self.mother.equipped['weapons2']]['grip'])])
                    self.l_melee_anim = self.render_animation(eval('L_' + WEAPONS[self.mother.equipped['weapons2']]['melee animation']))
                    self.stand_anim = self.render_animation([eval('L_' + WEAPONS[self.mother.equipped['weapons2']]['grip'])])  # Change after animations are created
                    self.walk_anim = self.render_animation(eval('L_' + WEAPONS[self.mother.equipped['weapons2']]['walk']))
                    if WEAPONS[self.mother.equipped['weapons2']]['melee animation'] == 'SWIPE':
                        self.swing_weapon2 = True
                        self.walk_l_melee_anim = self.render_animation(L_WALK_SWIPE)
                    else:
                        self.swing_weapon2 = False
                # Default animaitons for duel wielding
                if self.mother.equipped['weapons'] and self.mother.equipped['weapons2']:
                    self.dual_reload_anim = self.render_animation(RELOAD + L_RELOAD)
                    self.stand_anim = self.render_animation(STAND)
                    self.shoot_anim = self.render_animation([CP_STANDING_ARMS_OUT0])
                    self.l_shoot_anim = self.render_animation([CP_STANDING_ARMS_OUT0])
                    self.walk_anim = self.render_animation(WALK)
                if self.mother.in_vehicle:
                    if self.mother.vehicle.mountable:
                        self.walk_anim = self.run_anim = self.shallows_anim = self.swim_anim = self.shallows_anim = self.climbing_anim = self.climb_jump_anim = self.render_animation(RIDE)
                        self.melee_anim = self.walk_melee_anim = self.climbing_melee_anim = self.climbing_shoot_anim = self.climbing_weapon_anim = self.climbing_weapon_melee_anim = self.render_animation(SWIPE)
                        self.l_melee_anim = self.walk_l_melee_anim = self.climbing_l_melee_anim = self.climbing_l_weapon_melee_anim = self.render_animation(L_SWIPE)
                    else:
                        self.walk_anim = self.swim_anim = self.run_anim = self.shallows_anim = self.render_animation(self.mother.vehicle.player_walk_anim)
                        self.melee_anim = self.walk_melee_anim = self.render_animation(self.mother.vehicle.player_rattack_anim)
                        self.l_melee_anim = self.walk_l_melee_anim = self.render_animation(self.mother.vehicle.player_lattack_anim)

            self.update_weapon_width()
            self.animate(self.stand_anim, 1) #Calling this automatically updates the image

    def update_weapon_width(self): #Gets the widths of the currently equipped weapons for melee attacks and bullet spawning locations.
        if self.mother.equipped['weapons'] == None:
            self.weapon_width = 0
        else:
            self.weapon_width = self.game.weapon_images[WEAPONS[self.mother.equipped['weapons']]['image']].get_width() / 2
        if self.mother.equipped['weapons2'] == None:
            self.weapon2_width = 0
        else:
            self.weapon2_width = self.game.weapon_images[WEAPONS[self.mother.equipped['weapons2']]['image']].get_width() / 2

    def update(self):
        self.rect.center = self.mother.pos

        # Sets up three collision points for melee attacks: the fist, the center and the tip of the weapon.
        self.weapon_offset_temp = self.weapon_pos.rotate(-self.mother.rot)
        self.melee_rect.center = self.mother.pos + self.weapon_offset_temp
        self.weapon2_offset_temp = self.weapon2_pos.rotate(-self.mother.rot)
        self.melee2_rect.center = self.mother.pos + self.weapon2_offset_temp
        if self.mother.equipped['weapons']:
            self.weapon_offset_temp = (self.weapon_pos + vec(self.weapon_width/2, 0)).rotate(-(self.mother.rot + self.weapon_angle))
            self.mid_weapon_melee_rect.center = self.mother.pos + self.weapon_offset_temp
            self.weapon_offset_temp = (self.weapon_pos + vec(self.weapon_width, 0)).rotate(-(self.mother.rot + self.weapon_angle))
            self.weapon_melee_rect.center = self.mother.pos + self.weapon_offset_temp
        else:
            self.mid_weapon_melee_rect.center = self.weapon_melee_rect.center = self.melee_rect.center
        if self.mother.equipped['weapons2']:
            self.weapon2_offset_temp = (self.weapon2_pos + vec(self.weapon2_width/2, 0)).rotate(-(self.mother.rot + self.weapon2_angle))
            self.mid_weapon2_melee_rect.center = self.mother.pos + self.weapon2_offset_temp
            self.weapon2_offset_temp = (self.weapon2_pos + vec(self.weapon2_width, 0)).rotate(-(self.mother.rot + self.weapon2_angle))
            self.weapon2_melee_rect.center = self.mother.pos + self.weapon2_offset_temp
        else:
            self.mid_weapon2_melee_rect.center = self.weapon2_melee_rect.center = self.melee2_rect.center

        if not self.mother.alive():
            self.kill()

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        #Graphics and motion setup
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.players, game.player_group, game.moving_targets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.has_dragon_body = True # Used to define whether or not a character can transform into a dragon.
        self.image = self.game.body_surface
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.brightness = 1
        self.mask_kind = 0
        self.light_on = False
        self.light_mask_orig = pg.transform.scale(self.game.light_mask_images[0], (self.brightness, self.brightness))
        self.light_mask = self.light_mask_orig.copy()
        self.light_mask_rect = self.light_mask.get_rect()
        self.light_mask_rect.center = self.rect.center
        self.lamp_hand = 'weapons'
        self.elevation = 0
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(0, 0)
        self.direction = vec(1, 0) # A unit vector that represents the direction the player is facing.
        self.mouse_direction = vec(0, 0)
        self.mouse_pos = vec(0, 0)
        self.acceleration = PLAYER_ACC
        self.friction = PLAYER_FRIC
        self.rot = 0
        #time vars
        self.last_hit = 0 # Used for the time between mob hits to make it so you only get damaged based on the DAMAGE_RATE
        self.last_stat_update = 0 # Used to level stats periodically based on activities
        self.stat_update_delay = 50000
        self.last_voice = 0
        self.last_shot = 0
        self.last_shot2 = 0
        self.last_shift = 0
        self.last_stam_regen = 0
        self.last_move = 0
        self.last_damage = 0
        self.last_magica_drain = 0
        self.last_hunger = 0
        self.last_fireball = 0
        self.melee_playing = False
        self.dual_melee = False
        self.is_reloading = False
        self.gun = True # Says that the player needs reloading animations
        self.bow = False
        self.melee_rate = 0
        self.last_melee_sound = 0
        self.last_throw = 0
        self.last_climb = 0
        # Player state variables
        self.dragon = False
        self.temp_equipped = None # Used for switching your body to a mech suit or for Wraith possession.
        self.possessing = None
        self.transformable = False
        self.weapon_hand = 'weapons'
        self.flying = False
        self.jumping = False
        self.jump_count = 0
        self._climbing = False
        self._swimming = False
        self.in_shallows = False
        self.in_grass = False
        self.driver = None
        self.falling = False
        self.in_vehicle = self.in_player_vehicle = False
        self.in_flying_vehicle = False
        self.vehicle = None
        self.moving_melee = False
        self.living = True
        # player stats. You gain skill according to the activities the player does.
        self.stats = {'health': 100, 'max health': 100, 'stamina': 100, 'max stamina': 100, 'magica': 100, 'max magica': 100, 'hunger': 100, 'max hunger': 100, 'weight': 0, 'max weight': 100, 'strength': 1, 'agility': 1, 'armor': 0, 'kills': 0, 'marksmanship hits': 0, 'marksmanship shots fired': 0, 'marksmanship accuracy': 0, 'melee': 0, 'hits taken': 0, 'exercise': 0, 'healing': 0, 'stamina regen': 0, 'magica regen': 0, 'looting': 0, 'casting': 0, 'lock picking': 0, 'level': 0}
        self.fire_damage = self.start_fire_damage = 20
        self.after_effect = None
        # Used for equipment perks
        self.equipped_after_effect = False
        self.fireball_rate = self.original_fireball_rate = 400
        self.fireball_rate_perk = 0
        self.health_perk = self.old_health_perk = 0
        self.stamina_perk = self.old_stamina_perk = 0
        self.magica_perk = self.old_magica_perk = 0
        self.invisible = False
        self.arrow = None
        # vars for leveling
        self.last_kills = 0
        self.last_exercise = 0
        self.last_hits_taken = 0
        self.last_melee = 0
        self.last_stamina_regen = 0
        self.last_healing = 0
        self.last_casting = 0
        self.last_magica_regen = 0
        self.last_cast = 0
        # Player Body Customizations/Equipped
        self.inventory = {'gender': list(GENDER.keys()), 'hair': list(HAIR.keys()), 'race': list(RACE.keys()), 'weapons': [None], 'hats': [None], 'tops': [None], 'bottoms': [None], 'gloves': [None], 'shoes': [None], 'gold': 0, 'items': [None], 'magic': [None]}
        self.equipped = {'gender': 'female', 'race': 'osidine', 'weapons': None, 'weapons2': None, 'hair': None, 'hats': None, 'tops': None, 'bottoms': None, 'shoes': None, 'gloves': None, 'items': None, 'magic': None}
        self.race = self.kind = self.equipped['race']
        self.colors = {'hair': DEFAULT_HAIR_COLOR, 'skin': DEFAULT_SKIN_COLOR}
        self.ammo = {'pistol': 100, 'submachine gun': 100, 'shotgun': 100, 'rifle': 100, 'sniper rifle': 100, 'rocket launcher': 100, 'grenades': 100, 'turret': 1000, 'laser': 100, 'crystals': 100, 'bow': 100}
        self.mag1 = 0
        self.mag2 = 0
        self.ammo_cap1 = 0
        self.ammo_cap2 = 0
        self.last_weapon = self.equipped['weapons'] # This string is used to keep track of what the player's last weapon was for equipping and unequipping toggling weapons and keeping track of bullets from old weapons
        self.last_weapon2 = self.equipped['weapons2']
        self.current_weapon = self.equipped['weapons']# weapon you had for autoequipping when your weapon is sheathed.
        self.current_weapon2 = self.equipped['weapons2']  # weapon you had for autoequipping when your weapon is sheathed.
        # Create Body object (keep this as the last attribute.
        self.human_body = Character(self.game, self)
        self.dragon_body = Character(self.game, self, True)
        self.dragon_body.remove(self.game.all_sprites)
        self.body = self.human_body
        self.animation_playing = self.body.stand_anim
        # Redefined in character menu
        self.hungers = True
        self.immaterial = False
        self.magical_being = False
        # Needed for congruency with other Npc sprites, but only used to avoid errors.
        self.provoked = False
        self.offensive = False
        self.aggression = 'player'
        set_elevation(self)

    @property
    def swimming(self):
        return self._swimming
    @swimming.setter
    def swimming(self, value):
        if value!=self._swimming:
            if not self.in_vehicle:
                toggle_equip(self, value)
            self._swimming = value
        else:
            pass

    @property
    def climbing(self):
        return self._climbing
    @climbing.setter
    def climbing(self, value):
        if value!=self._climbing:
            if value:
                self.last_climb = pg.time.get_ticks()
                self.pre_jump()
            toggle_equip(self, value)
            self._climbing = value
        else:
            pass

    def get_keys(self):
        self.rot_speed = 0
        self.acc = vec(0, 0) # Makes it so the player doesn't accelerate when no key is pressed.

        # Controlls shooting/automatic shooting
        mouse_buttons_down = pg.mouse.get_pressed()
        if self.equipped[self.weapon_hand]:
            if WEAPONS[self.equipped[self.weapon_hand]]['bullet_count'] > 0:
                if WEAPONS[self.equipped[self.weapon_hand]]['auto']:
                    if mouse_buttons_down == (0, 0, 1) or mouse_buttons_down == (0, 1, 1):
                        self.weapon_hand = 'weapons'
                        self.shoot()
                    if mouse_buttons_down == mouse_buttons_down == (1, 0, 0) or mouse_buttons_down == (1, 1, 0):
                        self.weapon_hand = 'weapons2'
                        self.shoot()
                if mouse_buttons_down == (1, 0, 1) or mouse_buttons_down == (1, 1, 1):
                    self.dual_shoot(True)

        keys = pg.key.get_pressed()
        if keys[self.game.key_map['melee']]:
            self.pre_melee()

        # WASD keys for forward/rev and rotation
        if self.in_vehicle == False:
            if keys[self.game.key_map['strafe left']] and (keys[self.game.key_map['forward']] or mouse_buttons_down == (0, 1, 0) or mouse_buttons_down == (0, 1, 1) or mouse_buttons_down == (1, 1, 0)):
                self.accelerate(0.8, "diagonal left")
            elif keys[self.game.key_map['strafe right']] and (keys[self.game.key_map['forward']] or mouse_buttons_down == (0, 1, 0) or mouse_buttons_down == (0, 1, 1) or mouse_buttons_down == (1, 1, 0)):
                self.accelerate(0.8, "diagonal right")
            elif keys[self.game.key_map['strafe left']]:
                self.accelerate(0.8, "left")
            elif keys[self.game.key_map['strafe right']]:
                self.accelerate(0.8, "right")
            elif keys[self.game.key_map['forward']] or (mouse_buttons_down == (0, 1, 0) or mouse_buttons_down == (0, 1, 1) or mouse_buttons_down == (1, 1, 0)):
                self.accelerate()
            elif keys[self.game.key_map['back']]:
                self.accelerate(0.5, "rev")
            if keys[self.game.key_map['rot left']]:
                self.rot_speed = PLAYER_ROT_SPEED
            if keys[self.game.key_map['rot right']]:
                self.rot_speed = -PLAYER_ROT_SPEED
        else:
            if keys[self.game.key_map['rot left']]:
                self.rot_speed = self.vehicle.rot_speed
            if keys[self.game.key_map['rot right']]:
                self.rot_speed = -self.vehicle.rot_speed
            if keys[self.game.key_map['forward']] or (mouse_buttons_down == (0, 1, 0) or mouse_buttons_down == (0, 1, 1) or mouse_buttons_down == (1, 1, 0)):
                self.accelerate()
                self.vehicle.forward = True
            else:
                self.vehicle.forward = False
            if keys[self.game.key_map['back']]:
                self.accelerate(0.5, "rev")
        now = pg.time.get_ticks()

        # Running
        if keys[self.game.key_map['sprint']] and self.is_moving():
            if self.stats['stamina'] > 10 and not self.in_vehicle:
                if self.arrow == None:
                    if now - self.last_shift > 100:
                        if self.possessing == None:
                            self.acceleration = PLAYER_RUN + self.stats['agility']/4
                            if self.acceleration > MAX_RUN:
                                self.acceleration = MAX_RUN
                            self.add_stamina(-0.8)
                            self.last_shift = now
                        else:
                            self.acceleration = self.possessing.run_speed / 6
                            if 'mech_suit' not in self.equipped['race']:
                                self.add_stamina(-0.8)
                                self.last_shift = now
                else:
                    self.acceleration = PLAYER_ACC
            else:
                self.acceleration = PLAYER_ACC
        else:
            self.acceleration = PLAYER_ACC

        #Arrow keys auto rotate and move the player in the right/left, up/down directions
        #if keys[pg.K_UP] and keys[pg.K_RIGHT]:
        #    self.rotate_and_move(vec(1, -1))
        #elif keys[pg.K_DOWN] and keys[pg.K_LEFT]:
        #    self.rotate_and_move(vec(-1, 1))
        #elif keys[pg.K_UP] and keys[pg.K_LEFT]:
        #    self.rotate_and_move(vec(-1, -1))
        #elif keys[pg.K_DOWN] and keys[pg.K_RIGHT]:
        #    self.rotate_and_move(vec(1, 1))
        #else:
        #    if keys[pg.K_LEFT]:
        #        self.rotate_and_move(vec(-1, 0))
        #    if keys[pg.K_RIGHT]:
        #        self.rotate_and_move(vec(1, 0))
        #    if keys[pg.K_UP]:
        #        self.rotate_and_move(vec(0, -1))
        #    if keys[pg.K_DOWN]:
        #        self.rotate_and_move(vec(0, 1))

        #Mouse aiming
        mouse_movement = vec(pg.mouse.get_rel()).length()
        if mouse_movement > 0:
            self.rotate_to(self.mouse_direction)

    def rotate_to(self, vec):
        vector = vec
        angle = fix_angle(vector.angle_to(self.direction))
        if self.in_vehicle:
            rot_speed = self.vehicle.rot_speed/3
            if self.vehicle.turret == None:
                self.set_rot_speed(rot_speed, vector, angle)
        else:
            rot_speed = PLAYER_ROT_SPEED
            self.set_rot_speed(rot_speed, vector, angle)

    def set_rot_speed(self, rot_speed, vector, angle):
        if angle < 0:
            self.rot_speed = -rot_speed * 10 * abs(angle) / 180
        else:
            self.rot_speed = rot_speed * 10 * abs(angle) / 180

    #def rotate_and_move(self, vec):
    #    if self.in_vehicle:
    #        rot_speed = self.vehicle.rot_speed
    #    else:
    #        rot_speed = PLAYER_ROT_SPEED
    #    vector = vec
    #    angle = fix_angle(vector.angle_to(self.direction))
    #    if abs(angle) < 1:
    #        self.accelerate()
    #    elif angle < 0:
    #        self.rot_speed = -rot_speed * 10 * abs(angle) / 180
    #    else:
    #        self.rot_speed = rot_speed * 10 * abs(angle) / 180

    def accelerate(self, power = 1, direction = "forward"):
        perp = 0
        if self.melee_playing:
            self.moving_melee = True
        elif self.jumping:
            if self.climbing:
                self.acceleration = PLAYER_CLIMB
            elif self.possessing:
                self.acceleration = self.possessing.run_speed / 6
            else:
                self.acceleration = PLAYER_RUN
        else:
            self.moving_melee = False
            #Chooses Character's Walking and Running Animations
            now = pg.time.get_ticks()
            keys = pg.key.get_pressed()
            if self.swimming:
                self.animation_playing = self.body.swim_anim
                animate_speed = 120
            elif self.in_shallows or self.in_grass:
                self.animation_playing = self.body.shallows_anim
                animate_speed = 120
            elif self.climbing:
                if self.equipped['weapons2'] or self.equipped['weapons']:
                    self.animation_playing = self.body.climbing_weapon_anim
                else:
                    self.animation_playing = self.body.climbing_anim
                animate_speed = 250
            elif self.is_reloading:
                animate_speed = 120 # This animation is set up in the reload method
            elif keys[self.game.key_map['sprint']] and self.stats['stamina'] > 10:
                if self.arrow == None:
                    self.animation_playing = self.body.run_anim
                    animate_speed = 80
                else:
                    self.animation_playing = self.body.walk_anim
                    animate_speed = 120
            else:
                self.animation_playing = self.body.walk_anim
                animate_speed = 120

            if self.in_vehicle:
                if self.vehicle.mountable:
                    animate_speed = 200

            # Animates character
            if not self.is_reloading:
                self.body.animate(self.animation_playing, animate_speed)
            # Plays sounds based on what you are walking on or swimming in
            if self.swimming:
                if now - self.last_move > self.game.effects_sounds['swim'].get_length() * 1000:
                    self.last_move = now
                    self.game.effects_sounds['swim'].play()
                    if not self.in_vehicle:
                        self.add_stamina(-1)
            elif self.in_shallows:
                if now - self.last_move > self.game.effects_sounds['shallows'].get_length() * 1000:
                    self.last_move = now
                    self.game.effects_sounds['shallows'].play()

            elif self.in_grass:
                if now - self.last_move > self.game.effects_sounds['grass'].get_length() * 1000:
                    self.last_move = now
                    self.game.effects_sounds['grass'].play()

            elif self.climbing:
                self.acceleration = PLAYER_CLIMB
                if now - self.last_move > self.game.effects_sounds['climb'].get_length() * 1000: # I really should reuse this code for parts where I need to end the sound before playing another.
                    self.last_move = now
                    self.game.effects_sounds['climb'].play()
                    if not self.in_vehicle:
                        self.add_stamina(-8)

        if not ((self.melee_playing and (self.climbing or self.swimming)) or self.dual_melee):
            if direction == "rev":
                speed = -self.acceleration
            elif direction == "forward":
                speed = self.acceleration
            elif direction == "right":
                speed = 0
                perp = self.acceleration
            elif direction == "left":
                speed = 0
                perp = -self.acceleration
            elif direction == "diagonal right":
                speed = self.acceleration
                perp = self.acceleration
            elif direction == "diagonal left":
                speed = self.acceleration
                perp = -self.acceleration
            self.acc = vec(speed * power, perp * power).rotate(-self.rot)
        wall_check(self)

    def update(self):
        # This parts synchs the body sprite with the player's soul.
        self.body.rot = self.rot
        self.body.image = pg.transform.rotate(self.body.body_surface, self.rot)
        self.body.rect = self.body.image.get_rect()
        self.body.rect.center = self.rect.center

        if self.melee_playing:
            self.melee()
        if self.jumping:
            self.jump()
        if self.is_reloading:
            self.reload()

        now = pg.time.get_ticks()
        # Stops you from climbing after a certain time if you aren't on an object that requires you climb on it.
        if self.climbing:
            if now - self.last_climb > CLIMB_TIME:
                if not pg.sprite.spritecollide(self, self.game.climbs, False):
                    self.climbing = False
        # makes you more hungry if you are a race that eats
        if self.hungers:
            if now - self.last_hunger > GAME_HOUR:
                self.add_hunger(-5)
                self.last_hunger = now
        # drains magica if you are a dragon
        if self.dragon:
            if now - self.last_magica_drain > 2000:
                self.stats['magica'] -= 5
                if self.stats['magica'] < 0:
                    self.stats['magica'] = 0
                    self.transform()
                self.last_magica_drain = now
        # recharges magica when not a dragon
        else:
            time_delay = 3000
            time_reduction_factor = time_delay / (time_delay + self.stats['magica regen'])
            regen_delay = time_delay * time_reduction_factor + time_delay / 6
            if now - self.last_magica_drain > regen_delay:
                self.add_magica(4 + self.stats['magica regen']/50)
                self.last_magica_drain = pg.time.get_ticks()
        #recharge stamina and health
        if not (self.swimming or self.climbing):
            if self.stats['stamina'] < self.stats['max stamina']:
                time_delay = 3000
                time_reduction_factor = time_delay / (time_delay + self.stats['stamina regen'])
                regen_delay = time_delay * time_reduction_factor + time_delay/6
                if now - self.last_stam_regen > regen_delay:
                    keys = pg.key.get_pressed()
                    if not (keys[self.game.key_map['climb']] or self.is_attacking()):
                        if not (keys[self.game.key_map['sprint']] and self.is_moving()):
                            self.add_stamina((6 + self.stats['stamina regen']/50) * self.stats['hunger']/self.stats['max hunger']) # Stamina regenerates based off of your hunger level
                            if (self.stats['hunger'] > 75) or not self.hungers:  # You only heal when you're not too hungry.
                                self.add_health(self.stats['healing'] / 150)
                            self.last_stam_regen = pg.time.get_ticks()
        # Upgrades stats
        if now - self.last_stat_update > self.stat_update_delay:
            self.level_stats()
            self.last_stat_update = now

        # Mouse aiming vectors
        mouse_loc = vec(pg.mouse.get_pos())
        self.mouse_pos = vec(mouse_loc.x -self.game.camera.x, mouse_loc.y - self.game.camera.y)
        self.mouse_direction = vec(self.mouse_pos.x - self.pos.x, self.mouse_pos.y - self.pos.y) #gets the direciton from the character to mouse cursor.
        # Process key events and move character
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.direction = vec(1, 0).rotate(-self.rot)
        self.rect.center = self.pos
        self.acc += self.vel * self.friction
        self.vel += self.acc
        self.pos += (self.vel +0.5 * self.acc) * self.game.dt
        if not self.in_vehicle:
            if ('wraith' not in self.race) or self.stats['weight'] !=0:
                self.hit_rect.centerx = self.pos.x
                collide_with_walls(self, self.game.walls_on_screen, 'x')
                collide_with_elevations(self, 'x')
                collide_with_vehicles(self, 'x')
                self.hit_rect.centery = self.pos.y
                collide_with_walls(self, self.game.walls_on_screen, 'y')
                collide_with_elevations(self, 'y')
                collide_with_vehicles(self, 'y')
                self.rect.center = self.hit_rect.center
        if self.light_on:
            if self in self.game.lights:
                if self.race == 'mechanima':
                    self.light_mask_rect.center = self.rect.center
                elif self.lamp_hand == 'weapons':
                    self.light_mask_rect.center = self.body.melee_rect.center
                else:
                    self.light_mask_rect.center = self.body.melee2_rect.center
                if self.mask_kind in DIRECTIONAL_LIGHTS:
                    new_image = self.game.flashlight_masks[int(self.rot/3)] # Uses preloaded rotated images to save on CPU usage.
                    old_center = self.light_mask_rect.center
                    self.light_mask = new_image
                    self.light_mask_rect = self.light_mask.get_rect()
                    self.light_mask_rect.center = old_center
        else:
            self.light_mask_rect.center = (-2000, -2000) # Moves light off screen when off
        self.check_map_pos()

    def transform(self):
        self.invisible = False
        self.stats['casting'] += 0.5
        if 'dragon' not in self.equipped['race']:
            if self.stats['magica'] > 50:
                if self.transformable:
                    self.equipped['race'] = self.race + 'dragon'
                    explosion = Explosion(self.game, self)
                    self.human_body.remove(self.game.all_sprites)
                    self.human_body.remove(self.game.npc_bodies)
                    self.dragon_body.add(self.game.all_sprites)
                    self.dragon_body.add(self.game.npc_bodies)
                    self.game.group.add(self.dragon_body)
                    self.game.group.remove(self.human_body)
                    self.body = self.dragon_body
                    self.body.update()
                    self.stats['magica'] -= 10
                    self.dragon = True
        else:
            self.equipped['race'] = self.race
            explosion = Explosion(self.game, self)
            self.dragon_body.remove(self.game.all_sprites)
            self.dragon_body.remove(self.game.npc_bodies)
            self.human_body.add(self.game.all_sprites)
            self.human_body.add(self.game.npc_bodies)
            self.game.group.add(self.human_body)
            self.game.group.remove(self.dragon_body)
            self.body = self.human_body
            self.body.update()
            self.dragon = False

    def throw_grenade(self):
        now = pg.time.get_ticks()
        if now - self.last_throw > 1000:
            if self.equipped['weapons'] == None:
                body_pos = self.body.weapon_pos
                self.weapon_hand = 'weapons'
            else:
                body_pos = self.body.weapon2_pos
                self.weapon_hand = 'weapons2'
            if not self.is_moving() and not self.melee_playing:
                self.pre_melee()
            dir = vec(1, 0).rotate(-(self.rot))

            pos = self.pos + (body_pos + WEAPONS['grenade']['offset']).rotate(-(self.rot))
            Bullet(self, self.game, pos, dir, self.rot, 'grenade', False, self.in_flying_vehicle)
            self.ammo['grenades'] -= 1
            self.last_throw = now

    def shoot(self):
        if not self.is_moving():
            if self.weapon_hand == 'weapons2':
                self.animation_playing = self.body.l_shoot_anim
            else:
                self.animation_playing = self.body.shoot_anim
            if self.climbing:
                self.animation_playing = self.body.climbing_shoot_anim

        if self.equipped[self.weapon_hand]:
            if WEAPONS[self.equipped[self.weapon_hand]]['bullet_count'] > 0:
                if not WEAPONS[self.equipped[self.weapon_hand]]['gun']: # Makes it so you attack with melee weapons that also shoot things (enchanted weapons, slings, etc.)
                    self.pre_melee(True)
                    return
                keys = pg.key.get_pressed()
                if not self.is_moving() and not self.melee_playing:
                    self.body.animate(self.animation_playing, 120)
                if WEAPONS[self.equipped[self.weapon_hand]]['gun']:
                    now = pg.time.get_ticks()
                    if now - self.last_shot > WEAPONS[self.equipped[self.weapon_hand]]['rate']:
                        self.last_shot = now
                        self.fire_bullets()
            else:
                self.game.hud_ammo1 = ""
                self.game.hud_ammo2 = ""
                self.pre_melee()
        else:
            self.game.hud_ammo1 = ""
            self.game.hud_ammo2 = ""
            self.pre_melee()

    def dual_shoot(self, auto = False):
        if self.equipped['weapons'] and self.equipped['weapons2']:
            if WEAPONS[self.equipped['weapons']]['bullet_count'] > 0 and WEAPONS[self.equipped['weapons2']]['bullet_count'] > 0:
                temp_list = ['weapons', 'weapons2']
                now = pg.time.get_ticks()
                for weapon_hand in temp_list:
                    self.weapon_hand = weapon_hand
                    if auto:
                        if WEAPONS[self.equipped[self.weapon_hand]]['auto']:
                            if weapon_hand == 'weapons':
                                if now - self.last_shot > WEAPONS[self.equipped[weapon_hand]]['rate']:
                                    self.last_shot = now
                                    self.fire_bullets()
                            else:
                                if now - self.last_shot2 > WEAPONS[self.equipped[weapon_hand]]['rate']:
                                    self.last_shot2 = now
                                    self.fire_bullets()
                    else:
                        if weapon_hand == 'weapons':
                            if now - self.last_shot > WEAPONS[self.equipped[weapon_hand]]['rate']:
                                self.last_shot = now
                                self.fire_bullets()
                        else:
                            if now - self.last_shot2 > WEAPONS[self.equipped[weapon_hand]]['rate']:
                                self.last_shot2 = now
                                self.fire_bullets()
            else:
                self.dual_melee = True
                self.pre_melee()

        else:
            self.dual_melee = True
            self.pre_melee()

    def fire_bullets(self):
        if self.arrow: # Gets rid of arrow shown in bow before firing.
            self.arrow.kill()
            self.arrow = None

        if self.weapon_hand == 'weapons':
            angle = self.body.weapon_angle
            mag_selected = self.mag1
        else:
            angle = self.body.weapon2_angle
            mag_selected = self.mag2
        if mag_selected > 0:
            if not self.in_vehicle:
                self.vel += vec(-WEAPONS[self.equipped[self.weapon_hand]]['kickback'], 0).rotate(-self.rot)
            dir = vec(1, 0).rotate(-(self.rot + angle))
            if self.weapon_hand == 'weapons':
                pos = self.pos + (self.body.weapon_pos + WEAPONS[self.equipped['weapons']]['offset']).rotate(-(self.rot + angle))
            else:
                pos = self.pos + (self.body.weapon2_pos + vec(WEAPONS[self.equipped['weapons2']]['offset'].x, -WEAPONS[self.equipped['weapons2']]['offset'].y)).rotate(-(self.rot + angle))
            for i in range(WEAPONS[self.equipped[self.weapon_hand]]['bullet_count']):
                Bullet(self, self.game, pos, dir, self.rot, self.equipped[self.weapon_hand], False, self.in_flying_vehicle)
                if self.weapon_hand == 'weapons':
                    self.use_ammo(1)
                else:
                    self.use_ammo(2)
                self.play_weapon_sound()
                self.stats['marksmanship shots fired'] += 1
                self.stats['marksmanship accuracy'] = self.stats['marksmanship hits'] / self.stats['marksmanship shots fired']
            if WEAPONS[self.equipped[self.weapon_hand]]['gun']:
                MuzzleFlash(self.game, pos)
        else:
            self.out_of_ammo()

    def use_ammo(self, mag):
        if mag == 1:
            self.mag1 -= 1
            if self.mag1 < 0:
                self.mag1 = 0
        if mag == 2:
            self.mag2 -= 1
            if self.mag2 < 0:
                self.mag2 = 0
        self.update_hud_amo()

    def update_hud_amo(self):
        if self.ammo_cap1 + self.mag1 != 0:
            self.game.hud_ammo1 = "Right Ammo: " + str(self.mag1) + '/' + str(self.ammo_cap1)
        else:
            self.game.hud_ammo1 = ""
        if self.ammo_cap2 + self.mag2 != 0:
            self.game.hud_ammo2 = "Left Ammo: " + str(self.mag2) + '/' + str(self.ammo_cap2)
        else:
            self.game.hud_ammo2 = ""

    def out_of_ammo(self):
        now = pg.time.get_ticks()
        if now - self.last_voice > 3000:
            if WEAPONS[self.equipped[self.weapon_hand]]['gun']:
                if self.ammo[WEAPONS[self.equipped[self.weapon_hand]]['type']] == 0:
                    if self.equipped['gender'] == 'male':
                        choice(self.game.male_player_voice['out of ammo']).play()
                    else:
                        choice(self.game.female_player_voice['out of ammo']).play()
                else:
                    if self.equipped['gender'] == 'male':
                        choice(self.game.male_player_voice['empty clip']).play()
                    else:
                        choice(self.game.female_player_voice['empty clip']).play()
                self.last_voice = now
        if not self.is_moving():
            self.pre_melee()
        else:
            self.moving_melee = True
            self.pre_melee()

    def pre_reload(self):
        if not (self.melee_playing or self.jumping or self.swimming):
            if self.arrow:  # Gets rid of arrow shown in bow before reloading them.
                self.arrow.kill()
                self.arrow = None
            if self.equipped['weapons']:
                if WEAPONS[self.equipped['weapons']]['type'] == 'bow':
                    self.game.effects_sounds['bow reload'].play()
            if self.equipped['weapons2']:
                if WEAPONS[self.equipped['weapons2']]['type'] == 'bow':
                    self.game.effects_sounds['bow reload'].play()
            self.is_reloading = True
            self.body.frame = 0
            self.reload()

    def reload(self):
        speed = 100
        speed1 = 0
        speed2 = 0
        delay = 500
        if self.equipped['weapons'] and WEAPONS[self.equipped['weapons']]['bullet_count'] > 0: # checks if you are holding a gun
            if self.is_moving():
                self.animation_playing = self.body.walk_reload_anim
            else:
                self.animation_playing = self.body.reload_anim
            speed1 = WEAPONS[self.equipped['weapons']]['reload speed']
            speed = speed1
            right = True
        else:
            right = False
        if self.equipped['weapons2'] and WEAPONS[self.equipped['weapons2']]['bullet_count'] > 0: # checks if you are holding a gun
            if self.is_moving():
                self.animation_playing = self.body.l_walk_reload_anim
            else:
                self.animation_playing = self.body.l_reload_anim
            speed2 = WEAPONS[self.equipped['weapons2']]['reload speed']
            speed = speed2
            left = True
        else:
            left = False

        if left and right:
            if self.is_moving():
                self.animation_playing = self.body.walk_dual_reload_anim
            else:
                self.animation_playing = self.body.dual_reload_anim
            speed = speed1 + speed2

        if not(left or right):
            self.animation_playing = self.body.stand_anim

        now = pg.time.get_ticks()
        if now - self.last_shot > delay:
            if self.is_reloading:
                self.body.animate(self.animation_playing, speed)
                if self.body.frame > len(self.animation_playing[0]) - 1:
                    # Reloads magazines
                    if self.equipped['weapons']:
                        if 'enchanted' in self.equipped['weapons'] and WEAPONS[self.equipped['weapons']]['gun']:
                            if self.ammo['crystals'] - (WEAPONS[self.equipped['weapons']]['magazine size'] - self.mag1) < 0:
                                self.ammo['crystals'] = 0
                            else:
                                self.ammo['crystals'] -= (WEAPONS[self.equipped['weapons']]['magazine size'] - self.mag1)
                            if self.ammo[WEAPONS[self.equipped['weapons']]['type']] - (WEAPONS[self.equipped['weapons']]['magazine size'] - self.mag1) < 0:
                                self.mag1 = self.mag1 + self.ammo[WEAPONS[self.equipped['weapons']]['type']]
                                self.ammo[WEAPONS[self.equipped['weapons']]['type']] = 0
                            else:
                                self.ammo[WEAPONS[self.equipped['weapons']]['type']] -= (WEAPONS[self.equipped['weapons']]['magazine size'] - self.mag1)
                                self.mag1 = WEAPONS[self.equipped['weapons']]['magazine size']
                            self.ammo_cap1 = self.ammo[WEAPONS[self.equipped['weapons']]['type']]  # Used for HUD display value to improve frame rate by not looking up the value every cycle
                        else:
                            if 'enchanted' in self.equipped['weapons'] and WEAPONS[self.equipped['weapons']]['bullet_count'] > 0:
                                if self.ammo['crystals'] - (WEAPONS[self.equipped['weapons']]['magazine size'] - self.mag1) < 0:
                                    self.mag1 = self.mag1 + self.ammo['crystals']
                                    self.ammo['crystals'] = 0
                                else:
                                    self.ammo['crystals'] -= (WEAPONS[self.equipped['weapons']]['magazine size'] - self.mag1)
                                    self.mag1 = WEAPONS[self.equipped['weapons']]['magazine size']
                                self.ammo_cap1 = self.ammo['crystals'] # Used for HUD display value to improve frame rate by not looking up the value every cycle

                            if WEAPONS[self.equipped['weapons']]['gun']:
                                if self.ammo[WEAPONS[self.equipped['weapons']]['type']] - (WEAPONS[self.equipped['weapons']]['magazine size'] - self.mag1) < 0:
                                    self.mag1 = self.mag1 + self.ammo[WEAPONS[self.equipped['weapons']]['type']]
                                    self.ammo[WEAPONS[self.equipped['weapons']]['type']] = 0
                                else:
                                    self.ammo[WEAPONS[self.equipped['weapons']]['type']] -= (WEAPONS[self.equipped['weapons']]['magazine size'] - self.mag1)
                                    self.mag1 = WEAPONS[self.equipped['weapons']]['magazine size']
                                self.ammo_cap1 = self.ammo[WEAPONS[self.equipped['weapons']]['type']]  # Used for HUD display value to improve frame rate by not looking up the value every cycle
                        if WEAPONS[self.equipped['weapons']]['type'] != 'bow':
                            self.game.effects_sounds['gun_pickup'].play()
                        else:
                            if self.mag1 > 0:
                                Arrow(self.game, self, self.equipped['weapons'])
                    else:
                        self.mag1 = self.ammo_cap1 = 0

                    if self.equipped['weapons2']:
                        if 'enchanted' in self.equipped['weapons2'] and WEAPONS[self.equipped['weapons2']]['gun']:
                            if self.ammo['crystals'] - (WEAPONS[self.equipped['weapons2']]['magazine size'] - self.mag2) < 0:
                                self.ammo['crystals'] = 0
                            else:
                                self.ammo['crystals'] -= (WEAPONS[self.equipped['weapons2']]['magazine size'] - self.mag2)
                            if self.ammo[WEAPONS[self.equipped['weapons2']]['type']] - (WEAPONS[self.equipped['weapons2']]['magazine size'] - self.mag2) < 0:
                                self.mag2 = self.mag2 + self.ammo[WEAPONS[self.equipped['weapons2']]['type']]
                                self.ammo[WEAPONS[self.equipped['weapons2']]['type']] = 0
                            else:
                                self.ammo[WEAPONS[self.equipped['weapons2']]['type']] -= (WEAPONS[self.equipped['weapons2']]['magazine size'] - self.mag2)
                                self.mag2 = WEAPONS[self.equipped['weapons2']]['magazine size']
                            self.ammo_cap2 = self.ammo[WEAPONS[self.equipped['weapons2']]['type']]  # Used for HUD display value to improve frame rate by not looking up the value every cycle
                        else:
                            if 'enchanted' in self.equipped['weapons2'] and WEAPONS[self.equipped['weapons2']]['bullet_count'] > 0:
                                if self.ammo['crystals'] - (WEAPONS[self.equipped['weapons2']]['magazine size'] - self.mag2) < 0:
                                    self.mag2 = self.mag2 + self.ammo['crystals']
                                    self.ammo['crystals'] = 0
                                else:
                                    self.ammo['crystals'] -= (WEAPONS[self.equipped['weapons2']]['magazine size'] - self.mag2)
                                    self.mag2 = WEAPONS[self.equipped['weapons2']]['magazine size']
                                self.ammo_cap2 = self.ammo['crystals'] # Used for HUD display value to improve frame rate by not looking up the value every cycle
                            if WEAPONS[self.equipped['weapons2']]['bullet_count'] > 0:
                                if self.equipped['weapons']:
                                    if 'enchanted' in self.equipped['weapons'] and 'enchanted' in self.equipped['weapons2']:
                                        self.ammo_cap1 = self.ammo_cap2 # Makes sure if both your weapons use the same ammo they display the same ammo capacity.

                            if WEAPONS[self.equipped['weapons2']]['gun']:
                                if self.ammo[WEAPONS[self.equipped['weapons2']]['type']] - (WEAPONS[self.equipped['weapons2']]['magazine size'] - self.mag2) < 0:
                                    self.mag2 = self.mag2 + self.ammo[WEAPONS[self.equipped['weapons2']]['type']]
                                    self.ammo[WEAPONS[self.equipped['weapons2']]['type']] = 0
                                else:
                                    self.ammo[WEAPONS[self.equipped['weapons2']]['type']] -= (WEAPONS[self.equipped['weapons2']]['magazine size'] - self.mag2)
                                    self.mag2 = WEAPONS[self.equipped['weapons2']]['magazine size']
                                self.ammo_cap2 = self.ammo[WEAPONS[self.equipped['weapons2']]['type']] # Used for HUD display value to improve frame rate by not looking up the value every cycle
                        if self.equipped['weapons']:
                            if not 'enchanted' in self.equipped['weapons'] or not 'enchanted' in self.equipped['weapons2']:
                                if WEAPONS[self.equipped['weapons']]['bullet_count'] > 0 and WEAPONS[self.equipped['weapons2']]['bullet_count'] > 0:
                                    if self.ammo[WEAPONS[self.equipped['weapons']]['type']] == self.ammo[WEAPONS[self.equipped['weapons2']]['type']]:
                                        self.ammo_cap1 = self.ammo_cap2 # Makes sure if both your weapons use the same ammo they display the same ammo capacity.
                        if WEAPONS[self.equipped['weapons2']]['type'] != 'bow':
                            self.game.effects_sounds['gun_pickup'].play()
                        else:
                            if self.mag2 > 0:
                                Arrow(self.game, self, self.equipped['weapons2'])
                    else:
                        self.mag2 = self.ammo_cap2 = 0
                    self.is_reloading = False
                    self.last_shot = pg.time.get_ticks()
        self.update_hud_amo()

    def empty_mags(self):
        # Empties previous weapon mags back into ammo inventory:
        if self.equipped['weapons']:
            if 'enchanted' in self.equipped['weapons'] and not WEAPONS[self.equipped['weapons']]['gun']:
                if self.equipped['weapons'] and WEAPONS[self.equipped['weapons']]['bullet_count'] > 0:
                    self.ammo['crystals'] += self.mag1
                    self.mag1 = 0
        if self.equipped['weapons2']:
            if 'enchanted' in self.equipped['weapons2'] and not WEAPONS[self.equipped['weapons2']]['gun']:
                if self.equipped['weapons2'] and WEAPONS[self.equipped['weapons2']]['bullet_count'] > 0:
                    self.ammo['crystals'] += self.mag2
                    self.mag2 = 0
        if self.equipped['weapons'] and WEAPONS[self.equipped['weapons']]['gun']:
                self.ammo[WEAPONS[self.equipped['weapons']]['type']] += self.mag1
                self.mag1 = 0
        if self.equipped['weapons2'] and WEAPONS[self.equipped['weapons2']]['gun']:
                self.ammo[WEAPONS[self.equipped['weapons2']]['type']] += self.mag2
                self.mag2 = 0
        self.update_hud_amo()

    def play_weapon_sound(self, default = None):
        if default == None:
            snd = choice(self.game.weapon_sounds[WEAPONS[self.equipped[self.weapon_hand]]['type']])
        else:
            snd = choice(self.game.weapon_sounds['mace'])
        if snd.get_num_channels() > 2:
            snd.stop()
        snd.play()

    def play_weapon_hit_sound(self):
        snd = choice(self.game.weapon_hit_sounds[WEAPONS[self.equipped[self.weapon_hand]]['type']])
        if snd.get_num_channels() > 2:
            snd.stop()
        snd.play()

    def pre_melee(self, shot = False): # Used to get the timing correct between each melee strike, and for the sounds
        if True not in [self.jumping, self.is_reloading, self.arrow]:
            if not self.melee_playing:
                # Subtracts stamina
                if self.equipped[self.weapon_hand]:
                    self.add_stamina(-WEAPONS[self.equipped[self.weapon_hand]]['weight']/50, 100)
                else:
                    self.add_stamina(-0.04, 100)

                now = pg.time.get_ticks()
                if self.equipped[self.weapon_hand]:
                    rate =  WEAPONS[self.equipped[self.weapon_hand]]['rate']
                    if now - self.last_melee_sound > rate:
                        self.last_melee_sound = now
                        if shot:  # Used for weapons that shoot and attack at the same time.
                            self.fire_bullets()
                        if not WEAPONS[self.equipped[self.weapon_hand]]['gun']:
                            self.play_weapon_sound()
                        else:
                            self.play_weapon_sound('gun')
                else:
                    if now - self.last_melee_sound > 100:
                        self.last_melee_sound = now
                self.melee_playing = True
                self.body.frame = 0
                self.melee()

    def melee(self): # Used for the melee animations
        # Default values if no weapons
        rate = 200 #default timing between melee attacks if no agility. Reduces with higher agility
        rate_reduction_factor = rate/(rate + self.stats['agility'])
        def_speed = 60 #default speed of melee attacks
        speed_reduction_factor = def_speed/(def_speed + self.stats['agility'])
        self.melee_rate = rate * rate_reduction_factor + 90 # Makes it so the timing can't drop bellow 90
        speed = def_speed * speed_reduction_factor + 10 # Makes it so the timing can't drop bellow 10

        if self.weapon_hand == 'weapons':
            climbing_anim = self.body.climbing_melee_anim
            climbing_weapon_anim = self.body.climbing_weapon_melee_anim
            if self.moving_melee:
                melee_anim = self.body.walk_melee_anim
            else:
                melee_anim = self.body.melee_anim
        else:
            climbing_anim = self.body.climbing_l_melee_anim
            climbing_weapon_anim = self.body.climbing_l_weapon_melee_anim
            if self.moving_melee:
                melee_anim = self.body.walk_l_melee_anim
            else:
                melee_anim = self.body.l_melee_anim

        if self.climbing:
            self.animation_playing = climbing_anim
        else:
            self.animation_playing = melee_anim
        if self.equipped[self.weapon_hand]:
            if WEAPONS[self.equipped[self.weapon_hand]]['type'] == 'shield':
                self.melee_rate = self.melee_rate + WEAPONS[self.equipped[self.weapon_hand]]['weight'] * 2
                speed = WEAPONS[self.equipped[self.weapon_hand]]['weight'] * 4
            else:
                self.melee_rate = self.melee_rate + WEAPONS[self.equipped[self.weapon_hand]]['weight'] * 20
                speed = speed + WEAPONS[self.equipped[self.weapon_hand]]['weight'] * 5
                if self.climbing:
                    self.animation_playing = climbing_weapon_anim

        if self.dual_melee:
            if self.climbing and (self.equipped['weapons'] or self.equipped['weapons2']):
                self.animation_playing = choice([self.body.climbing_l_weapon_melee_anim, self.body.climbing_weapon_melee_anim])
            elif self.climbing:
                self.animation_playing = choice([self.body.climbing_l_melee_anim, self.body.climbing_melee_anim])
            else:
                self.animation_playing = self.body.dual_melee_anim
            if self.equipped['weapons'] and self.equipped['weapons2']:
                self.melee_rate = self.melee_rate + (WEAPONS[self.equipped['weapons']]['weight'] + WEAPONS[self.equipped['weapons2']]['weight'])/2 * 30
                speed = speed + (WEAPONS[self.equipped['weapons']]['weight'] + WEAPONS[self.equipped['weapons2']]['weight'])/2
            elif self.equipped['weapons']:
                self.melee_rate = self.melee_rate + WEAPONS[self.equipped['weapons']]['weight'] * 20
                speed = speed + WEAPONS[self.equipped['weapons']]['weight']/2 * 5
            elif self.equipped['weapons2']:
                self.melee_rate = self.melee_rate + WEAPONS[self.equipped['weapons2']]['weight'] * 20
                speed = speed + WEAPONS[self.equipped['weapons2']]['weight']/2 * 5

        if not self.in_vehicle:
            if self.swimming:
                self.animation_playing = self.body.swim_melee_anim

        now = pg.time.get_ticks()
        if now - self.last_shot > self.melee_rate:
            if self.melee_playing:
                self.body.animate(self.animation_playing, speed)
                if self.body.frame > len(self.animation_playing[0]) - 1:
                    self.melee_playing = False
                    self.dual_melee = False
                    self.last_shot = pg.time.get_ticks()

                    #Spawns breakable ore blocks when you hit the tiles.
                    if len(self.game.wall_tiles) > 0:
                        if self.weapon_hand == 'weapons':
                            melee_rect = self.body.weapon_melee_rect
                        else:
                            melee_rect = self.body.weapon2_melee_rect
                        x = int(melee_rect.centerx / self.game.map.tile_size)
                        y = int(melee_rect.centery / self.game.map.tile_size)
                        if x < 0: return
                        if y < 0: return
                        if x > self.game.map.tiles_wide: return
                        if y > self.game.map.tiles_high: return
                        tile = self.game.map.tmxdata.get_tile_gid(x, y, self.game.wall_tile_layer)
                        if tile in self.game.ore_tiles:
                            center = vec(x * self.game.map.tile_size + self.game.map.tile_size/2, y * self.game.map.tile_size + self.game.map.tile_size/2)
                            self.game.effects_sounds['rock_hit'].play()
                            breakable = Breakable(self.game, center, self.game.map.tile_size, self.game.map.tile_size, BLOCK_DICT[self.game.ore_tiles.index(tile)], self.game.previous_map)
                            # Checks to make sure you don't double spawn a breakable block.
                            self.game.breakable.remove(breakable)
                            hits = pg.sprite.spritecollide(breakable, self.game.breakable, False)
                            if hits:
                                breakable.kill()
                            else:
                                self.game.breakable.add(breakable)
                            self.game.map.tmxdata.layers[self.game.wall_tile_layer].data[y][x] = choice(self.game.empty_tiles)
                            self.game.map.redraw()



    def pre_jump(self):
        if not (self.melee_playing or self.in_vehicle or self.is_reloading):
            if self.stats['stamina'] > 10 or self.falling:
                if 'dragon' not in self.equipped['race']:
                    if not self.jumping :
                        self.add_stamina(-2)
                        self.jumping = True
                        self.body.frame = 0
                        self.jump()
                else:
                    if self.jumping:
                        if self.jump_count < 4:
                            self.add_stamina(-2)
                            self.jump_count += 1
                    else:
                        self.add_stamina(-2)
                        self.body.frame = 0
                        self.jumping = True
                        self.jump()

    def jump(self):
        delay = 500
        speed = 135
        if 'dragon' not in self.equipped['race']:
            if self.climbing:
                self.animation_playing = self.body.climb_jump_anim
                speed = 40
            elif self.falling:
                self.animation_playing = self.body.jump_anim
                speed = 20
                delay = 0
        else:
            delay = 60
        if self.swimming:
            if 'dragon' not in self.equipped['race']:
                self.animation_playing = self.body.swim_jump_anim
        else:
            self.animation_playing = self.body.jump_anim

        now = pg.time.get_ticks()
        if now - self.last_shot > delay:
            if self.jumping:
                self.body.animate(self.animation_playing, speed)
                if self.body.frame > len(self.animation_playing[0]) - 1:
                    if 'dragon' not in self.equipped['race']:
                        self.jumping = False
                        self.falling = False
                        if self.swimming or self.in_shallows:
                            self.game.effects_sounds['splash'].play()
                        else:
                            self.game.effects_sounds['jump'].play()
                        self.last_shot = pg.time.get_ticks()
                    else:
                        self.add_stamina(-2)
                        if self.stats['stamina'] == 0:
                            self.jumping = False
                            self.falling = False
                            self.jump_count = 0
                            if self.swimming or self.in_shallows:
                                self.game.effects_sounds['splash'].play()
                            else:
                                self.game.effects_sounds['jump'].play()
                            self.last_shot = pg.time.get_ticks()
                        elif self.jump_count < 1:
                            self.jump_count = 0
                            self.jumping = False
                            self.falling = False
                            if self.swimming or self.in_shallows:
                                self.game.effects_sounds['splash'].play()
                            else:
                                self.game.effects_sounds['jump'].play()
                            self.last_shot = pg.time.get_ticks()
                        else:
                            self.jump_count -= 1



    def gets_hit(self, damage, knockback = 0, rot = 0, dam_rate = DAMAGE_RATE):
        if self.in_vehicle:
            self.vehicle.gets_hit(damage, knockback, rot)
        elif self.possessing:
            self.possessing.gets_hit(damage, knockback, rot)
        else:
            now = pg.time.get_ticks()
            if now - self.last_hit > dam_rate:
                self.last_hit = now
                # Player takes damage based on their armor rating/
                temp_val = (damage + self.stats['armor']) # This part prevents division by 0 in the damage_reduction_factor calculation
                if temp_val == 0:
                    temp_val = 1
                damage_reduction_factor = damage/temp_val
                damage_done = damage * damage_reduction_factor
                if damage_done > 0:
                    if self.equipped['gender'] == 'male':
                        choice(self.game.male_player_hit_sounds).play()
                    else:
                        choice(self.game.female_player_hit_sounds).play()
                self.add_health(-damage_done)
                self.pos += vec(knockback, 0).rotate(-rot)
                if pg.sprite.spritecollide(self, self.game.barriers, False): #Prevents sprite from being knocked through a wall.
                    self.pos -= vec(knockback, 0).rotate(-rot)
                self.rect.center = self.hit_rect.center = self.pos
                self.stats['hits taken'] += 1

    def does_melee_damage(self, mob):
        if self.possessing: # Makes it so if you are in a mech suit or possessing an NPC your damage depends on their stats.
            now = pg.time.get_ticks()
            if now - self.last_damage > self.melee_rate:
                if self.equipped[self.weapon_hand] == None:
                    damage = self.possessing.damage
                    mob.vel = vec(0, 0)
                    choice(self.game.punch_sounds).play()
                    mob.gets_hit(damage, 2, self.rot)
                    self.game.hud_mobhp = mob.stats['health'] / mob.stats['max health']
                    self.game.last_mobhp_update = pg.time.get_ticks()
                    self.game.show_mobhp = True
                else:
                    weapon_damage = WEAPONS[self.equipped[self.weapon_hand]]['melee damage']
                    damage = self.possessing.damage + weapon_damage
                    mob.vel = vec(0, 0)
                    knockback = self.possessing.knockback / 2 + WEAPONS[self.equipped[self.weapon_hand]]['knockback']
                    self.play_weapon_hit_sound()
                    mob.gets_hit(damage, knockback, self.rot)
                    self.game.hud_mobhp = mob.stats['health'] / mob.stats['max health']
                    self.game.last_mobhp_update = pg.time.get_ticks()
                    self.game.show_mobhp = True
                self.stats['melee'] += 0.1
                self.last_damage = now
                mob.target = self.possessing
            if not self.game.guard_alerted:
                if mob.protected:
                    self.alert_guard()

        else:     # For when you are not in a mech suit or possessing
            damage_reduction = self.stats['stamina'] / self.stats['max stamina']
            now = pg.time.get_ticks()
            if now - self.last_damage > self.melee_rate:
                if self.equipped[self.weapon_hand] == None:
                    damage = damage_reduction * self.stats['strength']
                    mob.vel = vec(0, 0)
                    choice(self.game.punch_sounds).play()
                    mob.gets_hit(damage, 2, self.rot)
                    self.game.hud_mobhp = mob.stats['health'] / mob.stats['max health']
                    self.game.last_mobhp_update = pg.time.get_ticks()
                    self.game.show_mobhp = True
                else:
                    weapon_damage = WEAPONS[self.equipped[self.weapon_hand]]['melee damage']
                    damage = damage_reduction * (self.stats['strength'] + weapon_damage) + weapon_damage/4
                    mob.vel = vec(0, 0)
                    knockback = WEAPONS[self.equipped[self.weapon_hand]]['knockback']
                    self.play_weapon_hit_sound()
                    mob.gets_hit(damage, knockback, self.rot)
                    self.game.hud_mobhp = mob.stats['health'] / mob.stats['max health']
                    self.game.last_mobhp_update = pg.time.get_ticks()
                    self.game.show_mobhp = True
                #choice(mob.hit_sounds).play()
                self.stats['melee'] += 0.1
                self.last_damage = now
                mob.target = self
            if not self.game.guard_alerted:
                if mob.protected:
                    self.alert_guard()

    def alert_guard(self):
        for npc in self.game.npcs:
            if 'Guard' in npc.kind['name']:
                npc.approach_vector = vec(1, 0)
                npc.speed = npc.kind['walk speed'][1] * 1.5
                npc.detect_radius = npc.default_detect_radius = self.game.screen_width * 2
                npc.offensive = True
                npc.provoked = True
                npc.target = self.game.player
        self.game.guard_alerted = True

    def toggle_previous_weapons(self):
        if not self.swimming:
            self.equipped['weapons'] = self.last_weapon
            self.last_weapon = self.current_weapon
            self.current_weapon = self.equipped['weapons']
            self.equipped['weapons2'] = self.last_weapon2
            self.last_weapon2 = self.current_weapon2
            self.current_weapon2 = self.equipped['weapons2']
            self.human_body.update_animations()
            self.dragon_body.update_animations()

    def cast_spell(self):
        if self.equipped['magic']:
            now = pg.time.get_ticks()
            if now - self.last_cast > self.game.effects_sounds[MAGIC[self.equipped['magic']]['sound']].get_length() * 1000:
                if self.stats['magica'] >= MAGIC[self.equipped['magic']]['cost']:
                    if self.check_materials('magic', self.equipped['magic']):
                        self.game.effects_sounds[MAGIC[self.equipped['magic']]['sound']].play()
                        Spell_Animation(self.game, self.equipped['magic'], self.pos, self.rot, self.vel)
                        pos = vec(0, 0)
                        pos = self.pos + vec(60, 0).rotate(-self.rot)
                        if 'possession' in MAGIC[self.equipped['magic']]:
                            if self.possessing == None:
                                if 'wraith' in self.equipped['race']:
                                    if self.equipped['race'] == 'whitewraith': # Turns you into a black wraith for using dark magic.
                                        self.equipped['race'] = 'blackwraith'
                                        self.race = 'blackwraith'
                                        self.human_body.update_animations()
                                        self.dragon_body.update_animations()
                                    else:
                                        hits = pg.sprite.spritecollide(self, self.game.npcs, False, False)
                                        if hits:
                                            if hits[0].race not in ['whitewraith', 'blackwraith', 'demon', 'skeleton']:
                                                drop_all_items(self, False)
                                                hits[0].possess(self, True)
                                else:
                                    self.equipped['race'] = 'blackwraith'
                                    self.race = 'blackwraith'
                                    temp_inventory = self.inventory.copy()
                                    drop_all_items(self, True)
                                    corpse = Npc(self.game, self.pos.x, self.pos.y, map, 'villager')
                                    corpse.inventory = temp_inventory
                                    corpse.death()
                                    self.human_body.update_animations()
                                    self.dragon_body.update_animations()
                                    self.game.beg = perf_counter() # resets the counter so dt doesn't get messed up.
                            else:
                                self.add_health(self.possessing.stats['health'])
                                self.possessing.gets_hit(self.stats['stamina'])
                                self.possessing.depossess()

                        if 'summon' in MAGIC[self.equipped['magic']]:
                            if MAGIC[self.equipped['magic']]['summon'] in PEOPLE:
                                summoned = Npc(self.game, self.pos.x + 128, self.pos.y, self.game.map, MAGIC[self.equipped['magic']]['summon'])
                                summoned.make_companion()
                            elif MAGIC[self.equipped['magic']]['summon'] in ANIMALS:
                                Animal(self.game, pos.x, pos.y, self.game.map, MAGIC[self.equipped['magic']]['summon'])
                        if 'healing' in MAGIC[self.equipped['magic']]:
                            self.add_health(MAGIC[self.equipped['magic']]['healing'] + (self.stats['healing'] / 20) + (self.stats['casting'] / 100))
                        if 'fireballs' in MAGIC[self.equipped['magic']]:
                            balls = MAGIC[self.equipped['magic']]['fireballs']
                            damage = MAGIC[self.equipped['magic']]['damage'] + (self.stats['casting'] / 100)
                            for i in range(0, balls):
                                Fireball(self, self.game, self.pos, self.rot + (36 * i), damage, 30, 1300, 500, self.vel, 'fire', False, self.in_flying_vehicle)
                        self.add_magica(-MAGIC[self.equipped['magic']]['cost'])
                        self.stats['casting'] += MAGIC[self.equipped['magic']]['cost'] / 10

                        #dir = vec(1, 0).rotate(-self.rot)
                        self.last_cast = now

    def check_materials(self, item_type, chosen_item, subtract_materials = True):
        enough = True
        if 'materials' not in eval(item_type.upper())[chosen_item]:
            return enough
        else:
            self.count_resources()
            materials_list = eval(item_type.upper())[chosen_item]['materials']
            for material in materials_list:
                if material in self.items_numbered:  # Sees if you have any of the required material
                    if materials_list[material] > self.items_numbered[material]:  # Sees if you have enough of the required material
                        enough = False
                else:
                    enough = False
            if enough:
                if subtract_materials:
                    self.remove_materials(materials_list)
            return enough

    def count_resources(self):
        # This block creates a dictionary which includes each type of item in the player's item inventory and how many of each.
        item_counter = Counter(self.game.player.inventory['items'])
        self.items_numbered = {}
        for item in self.inventory['items']:
            if item not in self.items_numbered:
                self.items_numbered[item] = item_counter[item]

    def remove_materials(self, materials_list):
        for material in materials_list:
            items_removed = 0
            for number, x in enumerate(self.inventory['items']):
                if x == material:
                    if items_removed < materials_list[material]:
                        self.inventory['items'][number] = None
                        items_removed += 1
        self.calculate_weight()

    def use_item(self):
        remove = False
        if self.equipped['items']:
            if self.equipped['items'] == 'airship fuel':
                if self.in_vehicle:
                    if self.vehicle.cat == 'airship':
                        self.vehicle.fuel += 100
                        self.game.effects_sounds['pee'].play()
                        remove = True
            if 'spell' in ITEMS[self.equipped['items']]:
                if ITEMS[self.equipped['items']]['spell'] not in self.inventory['magic']:
                    self.inventory['magic'].append(ITEMS[self.equipped['items']]['spell'])
                    self.game.effects_sounds['page turn'].play()
                    self.game.effects_sounds[ITEMS[self.equipped['items']]['sound']].play()
            if 'ammo' in ITEMS[self.equipped['items']]:
                self.ammo[ITEMS[self.equipped['items']]['type']] += ITEMS[self.equipped['items']]['ammo']
                self.pre_reload()
                remove = True
            if 'food' in ITEMS[self.equipped['items']]:
                if self.hungers or 'mechanima' in self.race:  # Makes it so only races that can eat can eat.
                    if self.stats['hunger'] < 100: # You can only eat when you are hungry
                        if 'health' in ITEMS[self.equipped['items']]:
                            self.add_health(ITEMS[self.equipped['items']]['health'] + (self.stats['healing'] / 20))
                            remove = True
                        if 'stamina' in ITEMS[self.equipped['items']]:
                            self.add_stamina(ITEMS[self.equipped['items']]['stamina'] + (self.stats['stamina regen'] / 20))
                            remove = True
                        if 'magica' in ITEMS[self.equipped['items']]:
                            self.add_magica(ITEMS[self.equipped['items']]['magica'] + (self.stats['magica regen'] / 20))
                            remove = True
                        if 'hunger' in ITEMS[self.equipped['items']]:
                            self.add_hunger(ITEMS[self.equipped['items']]['hunger'])
                            remove = True
                        self.game.effects_sounds['eat'].play()
                    else:
                        return "You are too full to eat that."
            else:
                if 'health' in ITEMS[self.equipped['items']]:
                    self.add_health(ITEMS[self.equipped['items']]['health'] + (self.stats['healing'] / 20))
                    remove = True
                if 'stamina' in ITEMS[self.equipped['items']]:
                    self.add_stamina(ITEMS[self.equipped['items']]['stamina'] + (self.stats['stamina regen'] / 20))
                    remove = True
                if 'magica' in ITEMS[self.equipped['items']]:
                    self.add_magica(ITEMS[self.equipped['items']]['magica'] + (self.stats['magica regen'] / 20))
                    remove = True
                if 'hunger' in ITEMS[self.equipped['items']]:
                    self.add_hunger(ITEMS[self.equipped['items']]['hunger'])
                    remove = True
            if 'change race' in ITEMS[self.equipped['items']]:
                self.equipped['race'] = ITEMS[self.equipped['items']]['change race']
                self.human_body.update_animations()
                self.dragon_body.update_animations()
                remove = True
            if 'change sex' in ITEMS[self.equipped['items']]:
                self.equipped['gender'] = ITEMS[self.equipped['items']]['change sex']
                if self.equipped['gender'] == 'female':
                    random_dress_top = choice(DRESS_TOPS_LIST)
                    random_dress_skirt = choice(DRESS_BOTTOMS_LIST)
                    random_hair = choice(LONG_HAIR_LIST)
                    self.inventory['tops'].append(random_dress_top)
                    self.inventory['bottoms'].append(random_dress_skirt)
                    self.inventory['hair'].append(random_hair)
                    self.equipped['tops'] = random_dress_top
                    self.equipped['bottoms'] = random_dress_skirt
                    self.equipped['hair'] = random_hair
                else:
                    random_hair = choice(SHORT_HAIR_LIST)
                    self.inventory['tops'].append('tshirt M')
                    self.inventory['bottoms'].append('jeans M')
                    self.inventory['hair'].append(random_hair)
                    self.equipped['tops'] = 'tshirt M'
                    self.equipped['bottoms'] = 'jeans M'
                    self.equipped['hair'] = random_hair
                self.human_body.update_animations()
                self.dragon_body.update_animations()
                remove = True
            if 'flint and steel' in self.equipped['items']:
                if self.change_used_item('items', self.equipped['items']):
                    self.game.effects_sounds['fire blast'].play()
                    Stationary_Animated(self.game, self.pos + vec(64, 0).rotate(-self.rot), 'fire', 500)
                else: # Makes it so it doesn't try to use a None Type in the other if statements.
                    return
            if 'potion' in self.equipped['items']:
                self.inventory['items'].append('empty bottle') # lets you keep the bottle to use for creating new potions.
            if 'fuel' in self.equipped['items']:
                self.inventory['items'].append('empty barrel')
            if remove:
                self.inventory['items'].remove(self.equipped['items'])
            if self.equipped['items'] not in self.inventory['items']: # This lets you keep equipping items of the same kind. This way you can use multiple heath potions in a row for example.
                self.equipped['items'] = None
            self.game.player.calculate_weight()
            return False # Used to verify the item was used. False means it used the item.

    def change_used_item(self, item_type, item, return_new_name = False):
        # Renames used items to add hp to the end of their names.
        item_dic = eval(item_type.upper())
        if 'hp' in item_dic[item]:
            used_item = item_dic[item].copy()
            used_item['hp'] -= 1
            if used_item['hp'] <= 0: # Removes broken items from inventory.
                self.inventory[item_type].remove(item)
                if item_type == 'weapons':
                    if self.equipped[self.weapon_hand] == item:
                        self.equipped[self.weapon_hand] = None
                elif self.equipped[item_type] == item:
                    self.equipped[item_type] = None
                self.game.effects_sounds['metal hit'].play()
                if item_type == 'weapons':
                    self.current_weapon = self.equipped['weapons']
                    self.current_weapon2 = self.equipped['weapons2']
                    self.human_body.update_animations()  # Updates animations so you don't have broken weapons in your hand.
                    self.dragon_body.update_animations()
                if return_new_name:
                    return False, None
                return False # Used to tell that the item is broken.
            if 'HP' in item:
                temp_name, _ = item.split(' HP')
                new_item_name = temp_name + ' HP' + str(used_item['hp'])
            else:
                new_item_name = item + ' HP' + str(used_item['hp'])
            upgrade_dic = eval('UPGRADED_' + item_type.upper())
            upgrade_dic[new_item_name] = used_item
            item_dic[new_item_name] = used_item
            self.inventory[item_type].remove(item)  # removes non-used item
            self.inventory[item_type].append(new_item_name)  # adds used item to inventory
            if return_new_name:
                return True, new_item_name
            # Unequips old item and equips used one if you were equipping it.
            if item_type == 'weapons':
                if self.equipped[self.weapon_hand] == item:
                    self.equipped[self.weapon_hand] = new_item_name
            else:
                if self.equipped[item_type] == item:
                    self.equipped[item_type] = new_item_name
            return True
        else:
            return True

    def place_item(self):
        if self.equipped['items']:
            dropped_item = Dropped_Item(self.game, self.pos + vec(50, 0).rotate(-self.rot), 'items', self.equipped['items'], self.rot - 90)
            self.inventory['items'].remove(self.equipped['items'])
            self.equipped['items'] = None

    def is_moving(self):
        keys = pg.key.get_pressed()
        mouse_buttons_down = pg.mouse.get_pressed()
        return (keys[self.game.key_map['forward']] or mouse_buttons_down == (0, 1, 0) or mouse_buttons_down == (0, 1, 1) or mouse_buttons_down == (1, 1, 0))
    def is_attacking(selfself):
        mouse_buttons_down = pg.mouse.get_pressed()
        return (mouse_buttons_down == (1, 0, 0) or mouse_buttons_down == (0, 0, 1) or mouse_buttons_down == (1, 1, 0) or mouse_buttons_down == (0, 1, 1))

    def check_map_pos(self):
        if self.pos.x < 0:
            self.game.change_map('west')
        if self.pos.x > self.game.map.width:
            self.game.change_map('east')
        if self.pos.y < 0:
            self.game.change_map('north')
        if self.pos.y > self.game.map.height:
            self.game.change_map('south')

    def level_stats(self):
        level_kills = self.stats['kills'] - self.last_kills
        level_exercise = self.stats['exercise'] - self.last_exercise
        level_hits = self.stats['hits taken'] - self.last_hits_taken
        level_melee = self.stats['melee'] - self.last_melee
        level_stam = self.stats['stamina regen'] - self.last_stamina_regen
        level_healing = self.stats['healing'] - self.last_healing
        level_casting = self.stats['casting'] - self.last_casting
        level_magica = self.stats['magica regen'] - self.last_magica_regen

        self.calculate_fire_power()

        self.stats['agility'] += level_exercise / 37
        self.stats['strength'] += (level_exercise + level_hits + level_melee + level_kills)/100 + self.stats['weight']/(5*self.stats['max weight'])
        self.stats['max health'] += level_exercise/20 + level_healing
        self.stats['max stamina'] += level_exercise/20 + level_stam
        self.stats['max magica'] +=  level_casting/20 + level_magica

        self.last_kills = self.stats['kills']
        self.last_exercise = self.stats['exercise']
        self.last_hits_taken = self.stats['hits taken']
        self.last_melee = self.stats['melee']
        self.last_stamina_regen = self.stats['stamina regen']
        self.last_healing = self.stats['healing']
        self.last_casting = self.stats['casting']
        self.last_magica_regen = self.stats['magica regen']

    def add_health(self, amount):
        if amount > 20:
            self.stats['healing'] += 1
        self.stats['health'] += amount
        if self.stats['health'] > self.stats['max health']:
            self.stats['health'] = self.stats['max health']
        if self.stats['health'] < 0:
            self.game.playing = False
        if self.game.hud_health_stats == self.stats:
            self.game.hud_health = self.stats['health'] / self.stats['max health']

    def add_stamina(self, amount, percent = 0):
        if percent != 0:
            amount = amount * self.stats['stamina']
        if amount < 0:
            self.stats['exercise'] -= amount/10
        if amount > 20:
            self.stats['stamina regen'] += 1
        self.stats['stamina'] += amount
        if self.stats['stamina'] > self.stats['max stamina']:
            self.stats['stamina'] = self.stats['max stamina']
        elif (self.stats['stamina'] < 11) and (self.stats['hunger'] > 50):
            self.add_hunger(-1) # Makes you more hungry if you use your stamina.
        elif self.stats['stamina'] < 0:
            self.add_health(self.stats['stamina']) # Subtracts from your health if your stamina is too low.
            self.stats['stamina'] = 0
        self.game.hud_stamina = self.stats['stamina'] / self.stats['max stamina']

    def add_magica(self, amount):
        if amount > 20:
            self.stats['magica regen'] += 1
        self.stats['magica'] += amount
        if self.stats['magica'] > self.stats['max magica']:
            if self.magical_being:
                self.add_health(self.stats['magica regen'] / 80)  # You heal based on your skill if your magic is full if you are a magical being
            self.stats['magica'] = self.stats['max magica']
        elif self.stats['magica'] < 0:
            self.stats['magica'] = 0
        self.game.hud_magica = self.stats['magica'] / self.stats['max magica']

    def add_hunger(self, amount):
        self.stats['hunger'] += amount
        if self.stats['hunger'] > self.stats['max hunger']:
            self.stats['hunger'] = self.stats['max hunger']
        elif self.stats['hunger'] < 0:
            self.add_stamina(self.stats['hunger']) # Subtracts from your stamina if you're too hungry.
            self.stats['hunger'] = 0
        self.game.hud_hunger = self.stats['hunger'] / self.stats['max hunger']

    def calculate_weight(self):
        # Calculates the weight the player is carrying
        self.stats['weight'] = 0
        for item_type in self.inventory:
            if isinstance(self.inventory[item_type], list):
                for item in self.inventory[item_type]:
                    if item:
                        if 'weight' in eval(item_type.upper())[item]:
                            self.stats['weight'] += eval(item_type.upper())[item]['weight']
        self.stats['weight'] = round(self.stats['weight'], 1)

    def calculate_fire_power(self):
        self.fire_damage = self.start_fire_damage + self.stats['casting']
        if self.fire_damage > 30:
            self.fire_damage = 30 + self.stats['casting']/10
        elif self.fire_damage > 80:
            self.fire_damage = 80 + self.stats['casting']/100
        elif self.fire_damage > 120:
            self.fire_damage = 120 + self.stats['casting']/1000
        if self.fire_damage > 200:
            self.fire_damage = 200
        if not self.equipped_after_effect:
            if self.fire_damage > 75:
                self.after_effect = 'fire'
            else:
                self.after_effect = None

    def calculate_perks(self):
        # Calculates equipment based perks:
        fire_perks = 0 # Used to count how many armor items are dragon fire enchanted
        health_perks = 0
        stamina_perks = 0
        magica_perks = 0
        invisibility_perks = 0
        self.health_perk = 0
        self.stamina_perk = 0
        self.magica_perk = 0
        self.fireball_rate_perk = 0
        self.invisible = False
        for item_type in self.equipped:
            if item_type == 'race' and (self.equipped['race'] not in list(RACE.keys())):
                continue
            if item_type == 'weapons2':
                temp_item_type = 'weapons'
            else:
                temp_item_type = item_type
            item_dict = eval(temp_item_type.upper())
            if self.equipped[item_type]:
                if 'fire enhance' in item_dict[self.equipped[item_type]]:
                    self.after_effect = item_dict[self.equipped[item_type]]['fire enhance']['after effect']
                    self.fire_damage += item_dict[self.equipped[item_type]]['fire enhance']['damage']
                    self.fireball_rate_perk += item_dict[self.equipped[item_type]]['fire enhance']['rate reduction']
                    fire_perks += 1
                if 'reinforce magica' in item_dict[self.equipped[item_type]]:
                    self.magica_perk += item_dict[self.equipped[item_type]]['reinforce magica']
                    magica_perks += 1
                if 'reinforce stamina' in item_dict[self.equipped[item_type]]:
                    self.stamina_perk += item_dict[self.equipped[item_type]]['reinforce stamina']
                    stamina_perks += 1
                if 'reinforce health' in item_dict[self.equipped[item_type]]:
                    self.health_perk += item_dict[self.equipped[item_type]]['reinforce health']
                    health_perks += 1
                if 'property' in item_dict[self.equipped[item_type]]:
                    if item_dict[self.equipped[item_type]]['property'] == 'invisibility':
                        invisibility_perks += 1
        if invisibility_perks > 0:
            if self.body in self.game.group:
                self.game.group.remove(self.body)
                self.invisible = True
        else:
            if self.body not in self.game.group:
                self.game.group.add(self.body)
                self.invisible = False
        if fire_perks == 0:
            self.equipped_after_effect = False
            self.fireball_rate_perk = 0
        else:
            self.equipped_after_effect = True
        if magica_perks == 0: # Removes perks if there are none
            self.stats['magica'] -= self.old_magica_perk
            self.stats['max magica'] -= self.old_magica_perk
            if self.stats['magica'] < 0:
                self.stats['magica'] = 0
            self.old_magica_perk = 0
        else: # Adds new perks based on equipment changes
            self.stats['magica'] += self.magica_perk - self.old_magica_perk
            self.stats['max magica'] += self.magica_perk - self.old_magica_perk
            self.old_magica_perk = self.magica_perk

        if stamina_perks == 0: # Removes perks if there are none
            self.stats['stamina'] -= self.old_stamina_perk
            self.stats['max stamina'] -= self.old_stamina_perk
            if self.stats['stamina'] < 0:
                self.stats['stamina'] = 0
            self.old_stamina_perk = 0
        else: # Adds new perks based on equipment changes
            self.stats['stamina'] += self.stamina_perk - self.old_stamina_perk
            self.stats['max stamina'] += self.stamina_perk - self.old_stamina_perk
            self.old_stamina_perk = self.stamina_perk

        if health_perks == 0: # Removes perks if there are none
            health_percent = self.stats['health']/self.stats['max health']
            self.stats['max health'] -= self.old_health_perk
            self.stats['health'] = int(self.stats['max health'] * health_percent) # Gives you the same percentage of health after removing health perks
            if self.stats['health'] < 1:
                self.stats['health'] = 1
            self.old_health_perk = 0
        else: # Adds new perks based on equipment changes
            self.stats['health'] += self.health_perk - self.old_health_perk
            self.stats['max health'] += self.health_perk - self.old_health_perk
            self.old_health_perk = self.health_perk


        self.fireball_rate = self.original_fireball_rate - self.fireball_rate_perk
        if self.fireball_rate < 1:
            self.fireball_rate = 1

    def breathe_fire(self):
        now = pg.time.get_ticks()
        if now - self.last_fireball > self.fireball_rate:
            if self.stats['magica'] > 5:
                Fireball(self, self.game, self.pos, self.rot, self.fire_damage, 5, 1000, 300, self.vel, self.after_effect, False, self.in_flying_vehicle)
                self.last_fireball = now
                self.stats['magica'] -= 5
                if self.stats['magica'] < 0:
                    self.stats['magica'] = 0


class Npc(pg.sprite.Sprite):
    def __init__(self, game, x, y, map, kind, health = None, inventory = None, colors = None):
        self._layer = ITEMS_LAYER # The NPC's body is set to the PLAYER LAYER, but the NPC is set to the ITEMS_LAYER so its corpse appears under the player when it dies.
        self.game = game
        if kind == 'mech suit':
            self.groups = game.all_sprites, game.mobs, game.npcs, game.detectables, game.moving_targets, game.mechsuits
        else:
            self.groups = game.all_sprites, game.mobs, game.npcs, game.detectables, game.moving_targets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.map = map # This keeps track of which NPCs belong on which maps
        self.image = self.game.body_surface
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.brightness = 1
        self.mask_kind = 0
        self.light_mask_orig = pg.transform.scale(self.game.light_mask_images[0], (self.brightness, self.brightness))
        self.light_mask = self.light_mask_orig.copy()
        self.light_mask_rect = self.light_mask.get_rect()
        self.light_mask_rect.center = self.rect.center
        self.lamp_hand = 'weapons'
        self.talk_rect = XLARGE_HIT_RECT.copy()
        self.talk_rect.center = self.rect.center
        self.talk_counter = 0 # Used to keep track of how many times you talk to someone. So you can changed the dialogue based on it.
        self.elevation = 0
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.direction = vec(1, 0)
        self.target_dist = vec(0, 0)
        self.rect.center = self.pos
        self.rot = randrange(0, 360)
        self.rot_speed = MOB_ROT_SPEED
        self.frame = 0
        self.melee_rate = 1000
        self.melee_range = 50
        self.mag_size = 0
        self.bullets_shot = 0
        # Timing vars
        self.last_path_change = 0
        self.last_seek = 0
        self.last_damage = 0
        self.last_step = 0
        self.last_move = 0
        self.last_move_check = 0
        self.last_wall_hit = 0
        self.hit_wall = False
        self.last_hit = 0
        self.last_shot = 0
        self.last_reload = 0
        self.reloading = False
        self.animating_reload = False
        self.melee_playing = False
        self.last_melee = 0
        self.last_melee_sound = 0
        self.last_climb = 0
        # State vars
        self.talk_attempt = False
        self.running = False
        self.fleeing = False
        self.needs_move = False
        self.last_weapon = None
        self.last_weapon2 = None
        self.current_weapon = None
        self.current_weapon2 = None
        self.jumping = False
        self.falling = False
        self.climbing = False
        self.swimming = False
        self.invisible = False
        self.flying = False
        self.in_shallows = False
        self.in_grass = False
        self.in_vehicle = False
        self.in_player_vehicle = False
        self.in_flying_vehicle = False
        self.possessing = None
        self.arrow = None
        self.driver = None
        self.possessed = False
        self.has_dragon_body = False
        self.living = True
        self.weapon_hand = 'weapons'
        self.gun = False
        self.bow = False
        self.offensive = False  # Used to tell weather or not the npc will attack
        self.provoked = False  # Used to tell if the player attacked the npc

        self.wall_hit_or = ""
        self.last_pos = self.rect.center # Used for tracking whether or not the NPC is moving towards its target.
        #NPC specific data:
        self.species = kind
        try:  # This makes it so you can load a saved game even if there were new NPCs added.
            self.kind = self.game.people[kind]
        except:
            self.kind = PEOPLE[kind]
            self.game.people[kind] = self.kind
        self.race = self.kind['race']
        if not colors:
            self.colors = self.kind['colors'].copy()
        else:
            self.colors = colors
        if 'random' in self.colors['skin']:
            skin_list = eval(self.colors['skin'].replace('random', ''))
            self.colors['skin'] = choice(skin_list)
        if 'random' in self.colors['hair']:
            hair_list = eval(self.colors['hair'].replace('random', ''))
            self.colors['hair'] = choice(hair_list)
        self.name = self.kind['name']
        self.protected = self.kind['protected']
        if 'Guard' in self.kind['name']:
            self.guard = True
        else:
            self.guard = False
        self.dialogue = self.kind['dialogue']
        self.aggression = self.kind['aggression']
        self.touch_damage = self.kind['touch damage']
        if not health:
            self.stats = {'health': self.kind['health'], 'max health': self.kind['health']}
        else:
            self.stats = {'health': health, 'max health': self.kind['health']}
        self.speed = randrange(self.kind['walk speed'][0], self.kind['walk speed'][1])
        self.run_speed = self.kind['run speed']
        self.armed = self.kind['armed']
        self.dual_wield = self.kind['dual wield']
        #self.dual_melee = False
        if len(self.game.random_targets) > 0:
            self.target = self.goal_target = choice(list(self.game.random_targets))
        else:
            self.target = self.goal_target = self.game.player
        if kind != 'generic':
            self.temp_target = Target(self.game)
        self._aipath = None
        self.selected_path = None
        self.damage = self.kind['damage']
        self.knockback = self.kind['knockback']
        self.detect_radius = self.default_detect_radius = self.kind['detect radius']
        self.avoid_radius = self.kind['avoid radius']
        if 'walls' not in self.kind['collide'] and 'obstacles' not in self.kind['collide']:
            self.immaterial = True
        else:
            self.immaterial = False
        self.collide_list = []
        for item in self.kind['collide']:
            self.collide_list.append(eval("self.game." + item + "_on_screen"))

        # These are empty dictionaries used for adding random values to.
        self.equipped = {'gender': self.kind['gender'], 'race': self.kind['race'], 'weapons': None, 'weapons2': None, 'hair': None, 'hats': None, 'tops': None, 'bottoms': None, 'shoes': None, 'gloves': None, 'items': None, 'magic': None}
        # NPC character properties: Determines whether or not the NPC is randomized or imported from the info in npcs.py
        if self.kind['race'] == 'random':
            self.equipped['race'] = choice(list(RACE.keys()))
        elif 'random' in self.kind['race']:
            _, temp_list = self.kind['race'].split(' ')
            self.equipped['race'] = choice(eval(temp_list))
        else:
            self.equipped['race'] = self.kind['race']
        if self.kind['gender'] == 'random':
            randnumber = randrange(0, 100)
            if randnumber < 48:
                self.gender = 'male'
            if randnumber > 47:
                self.gender = 'female'
            if randnumber > 95:
                self.gender = 'other'
            self.equipped['gender'] = self.gender
        else:
            self.gender = self.kind['gender']
            self.equipped['gender'] = self.gender
        if not inventory:
            if self.kind['inventory'] == 'random':
                random_inventory(self)
            else:
                self.inventory = copy.deepcopy(self.kind['inventory'])
                random_inventory_item(self, self.kind['inventory']) # assigns individual randomized items to NPC
        else:
            self.inventory = inventory

        change_clothing(self)
        # Sets sounds the NPCs randomly make
        self.sounds = None
        if self.equipped['race'] == 'immortui':
            self.sounds = self.game.zombie_moan_sounds
        if 'wraith' in self.equipped['race']:
            self.sounds = self.game.wraith_sounds
        self.set_vectors()

        # Create Body object (keep this as the last attribute.
        self.current_weapon = self.equipped['weapons']
        self.current_weapon2 = self.equipped['weapons2']
        self.body = self.human_body = self.dragon_body = Character(self.game, self)
        if 'walk' in self.kind['animations']: # Overrides default animations for custom NPCs
            self.body.walk_anim = self.body.render_animation(self.kind['animations']['walk'])
        if 'run' in self.kind['animations']: # Overrides default animations for custom NPCs
            self.body.run_anim = self.body.render_animation(self.kind['animations']['run'])
        self.body.update_animations()
        if self.inventory['magic'][0]:
            self.has_magic = True
        else:
            self.has_magic = False
        if self.bow:
            self.reload()

        if self.race == 'mechanima':
            self.brightness = 400
            self.game.lights.add(self)
            self.light_mask = pg.transform.scale(self.game.light_mask_images[2], (self.brightness, self.brightness))
            self.light_mask_rect = self.light_mask.get_rect()
        elif self.race == 'mech_suit':
            self.brightness = 550
            self.game.lights.add(self)
            self.light_mask = pg.transform.scale(self.game.light_mask_images[2], (self.brightness, self.brightness))
            self.light_mask_rect = self.light_mask.get_rect()

        # Sets elevation to the highest elevation you hit.
        set_elevation(self)
        # kills Npcs that spawn in wall tiles
        if wall_check(self):
            self.body.kill()
            self.kill()

    @property
    def aipath(self):
        return self._aipath

    @aipath.setter
    def aipath(self, value):
        if value != self._aipath: # Runs if the path list changes
            self._aipath = value
            if value and self.aggression in ['fwp', 'awp'] and (not self.offensive):
                self.last_path_change = pg.time.get_ticks()
                self.target = self.goal_target # Resets the target back to the goal target whenever you cross new pathways.
                self.set_aipath_target()
        else:
            pass

    def set_aipath_target(self):
        if self.target != self.temp_target:
            RL_paths = []
            UD_paths = []
            for aipath in self.aipath: # Sorts hits paths by direction
                if aipath.kind == 'UD':
                    UD_paths.append(aipath)
                else:
                    RL_paths.append(aipath)

            path_dir = None
            npc_dir = None
            last_dist = 100000
            if len(RL_paths) > 0:
                if (abs(self.goal_target_dist.x) > abs(self.goal_target_dist.y)) or (len(UD_paths) == 0): # Taking an RL path is more beneficial
                    path_dir = 'RL'
                    if self.goal_target_dist.x < 0: # take a left path because the target is to the left.
                        npc_dir = 'left'
                        for aipath in RL_paths: # Finds the path that goes closest to the target.
                            dist = abs(aipath.rect.left - self.goal_target.pos.x)
                            if last_dist > dist:
                                self.selected_path = aipath
                                last_dist = dist

                    else: # take a right path.
                        npc_dir = 'right'
                        for aipath in RL_paths: # Finds the path that goes closest to the target.
                            dist = abs(aipath.rect.right - self.goal_target.pos.x)
                            if last_dist > dist:
                                self.selected_path = aipath
                                last_dist = dist
                else:
                    path_dir = 'UD'
                    if self.goal_target_dist.y < 0: # take an up path because the target is upward.
                        npc_dir = 'top'
                        for aipath in UD_paths: # Finds the path that goes closest to the target.
                            dist = abs(aipath.rect.top - self.goal_target.pos.y)
                            if last_dist > dist:
                                self.selected_path = aipath
                                last_dist = dist
                    else: # take a down path.
                        npc_dir = 'bottom'
                        for aipath in UD_paths: # Finds the path that goes closest to the target.
                            dist = abs(aipath.rect.bottom - self.goal_target.pos.y)
                            if last_dist > dist:
                                self.selected_path = aipath
                                last_dist = dist
            else:
                path_dir = 'UD'
                if self.goal_target_dist.y < 0:  # take an up path because the target is upward.
                    npc_dir = 'top'
                    for aipath in UD_paths:  # Finds the path that goes closest to the target.
                        dist = abs(aipath.rect.top - self.goal_target.pos.y)
                        if last_dist > dist:
                            self.selected_path = aipath
                            last_dist = dist
                else:  # take a down path.
                    for aipath in UD_paths:  # Finds the path that goes closest to the target.
                        npc_dir = 'bottom'
                        dist = abs(aipath.rect.bottom - self.goal_target.pos.y)
                        if last_dist > dist:
                            self.selected_path = aipath
                            last_dist = dist

            if path_dir == 'UD':
                x = self.selected_path.rect.centerx
                ystr = "self.selected_path.rect." + npc_dir
                y = eval(ystr)
                if npc_dir == 'top': # Makes it so you don't overshoot the goal target.
                    if y < self.goal_target.pos.y:
                        y = self.goal_target.pos.y
                else:
                    if y > self.goal_target.pos.y:
                        y = self.goal_target.pos.y
            else:
                y = self.selected_path.rect.centery
                xstr = "self.selected_path.rect." + npc_dir
                x = eval(xstr)
                if npc_dir == 'left': # Makes it so you don't overshoot the goal target.
                    if x < self.goal_target.pos.x:
                        x = self.goal_target.pos.x
                else:
                    if x > self.goal_target.pos.x:
                        x = self.goal_target.pos.x
            self.temp_target.set_position(x, y)
            self.target = self.temp_target

    def update_collide_list(self):
        self.collide_list = [self.game.walls_on_screen]

    def set_vectors(self):
        if self.aggression == 'fwd':
            self.approach_vector = vec(-1, 0)
        if self.aggression == 'awd':
            self.approach_vector = vec(1, 0)
            self.offensive = True
        if self.aggression == 'fwp':
            self.approach_vector = vec(1, 0)
        if self.aggression == 'awp':
            self.approach_vector = vec(1, 0)
        if self.aggression == 'sap':
            self.approach_vector = vec(0, 0)
            self.speed = 0

    def equip_lamp(self):
        if self.race not in ['mechanima', 'mech_suit']:
            if self.game.night:
                if self not in self.game.lights:
                    if randrange(0, 2) == 1:
                        lamp_check(self)
            elif self in self.game.lights:
                if randrange(0, 2) == 1:
                    lamp_check(self)

    def seek_random_target(self):
        if randrange(0, 5) == 1: # Makes it so NPCs randomly target nearby doors.
            self.seek_door()
        else:
            try:
                self.target = self.goal_target = choice(list(choice(self.game.target_list)))
            except:
                self.target = self.game.player

    def seek_door(self):
        last_dist = 3000
        for entry in self.game.entryways_on_screen:
            dist = self.pos - entry.pos
            dist = dist.length()
            if last_dist > dist:  # Finds closest door
                self.target = entry
                self.offensive = False
                self.provoked = False
                self.approach_vector = vec(1, 0)
                last_dist = dist

    def seek_mobs(self):
        last_dist = 100000
        non_targets = 0
        if self.guard:
            for mob in self.game.moving_targets_on_screen:
                if mob != self:
                    if not mob.invisible:
                        if mob.aggression == 'awd':
                            if mob.race != self.race:
                                dist = self.pos - mob.pos
                                dist = dist.length()
                                if 0 < dist < self.detect_radius:
                                    if last_dist > dist: # Finds closest mob
                                        self.target = mob
                                        self.detect_radius = self.default_detect_radius
                                        self.approach_vector = vec(1, 0)
                                        self.offensive = True
                                        last_dist = dist
                                else:
                                    non_targets += 1
                            else:
                                non_targets += 1
                        else:
                            non_targets += 1
                    else:
                        non_targets += 1

        elif self.aggression == 'awd':
            for mob in self.game.moving_targets_on_screen: # Only looks at mobs that are on screen
                if mob != self:
                    if not mob.invisible:
                        if mob.race != self.race:
                            self.offensive = True
                            dist = self.pos - mob.pos
                            dist = dist.length()
                            if 0 < dist < self.detect_radius:
                                if last_dist > dist:  # Finds closest NPC and sets to target
                                    self.target = mob
                                    self.detect_radius = self.default_detect_radius
                                    self.approach_vector = vec(1, 0)
                                    last_dist = dist
                            else:
                                non_targets += 1
                        else:
                            non_targets += 1
                    else:
                        non_targets += 1

        #if self.aggression in ['fwp', 'sap', 'awp']:  # Makes it so non aggressive mobs target the player when you are close.
        #    dist = self.pos - self.game.player.pos
        #    dist = dist.length()
        #    if dist < TALK_RADIUS:
        #        self.target = self.game.player

        # Seeks a random target if there are no target mobs in range.
        elif non_targets == len(self.game.moving_targets_on_screen) - 1:
            if not self.aipath:
                self.target = self.goal_target

    def is_moving(self):
        # This checks to see if the NPC has moved since the last check.
        dist = self.pos - self.last_pos
        if dist.length() < 10:
            self.last_pos = self.rect.center
            return False
        else:
            self.last_pos = self.rect.center
            return True

    def turn(self):
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.direction = vec(1, 0).rotate(-self.rot)

    def accelerate(self):
        if self.in_player_vehicle:
            pass
        else:
            self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
            self.direction = vec(1, 0).rotate(-self.rot)
            self.acc += self.vel * -1
            self.avoid_mobs()
            self.vel += self.acc
            self.pos += (self.vel + 0.5 * self.acc) * self.game.dt
            collide(self)
            self.rect.center = self.talk_rect.center = self.pos

    def avoid_mobs(self):
        for mob in self.game.mobs_on_screen:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < self.avoid_radius:
                    self.acc += dist

    def animate(self):
        # Animates Character's Walking
        if self.speed == 0:
            temp_animate_speed = 500
        else:
            if self.running:
                temp_animate_speed = 20000 / self.run_speed
            else:
                temp_animate_speed = 20000 / self.speed
        if self.swimming:
            self.body.animate(self.body.swim_anim, temp_animate_speed)
        elif self.in_shallows:
            self.body.animate(self.body.shallows_anim, temp_animate_speed)
        elif self.in_grass:
            self.body.animate(self.body.shallows_anim, temp_animate_speed)
        elif self.climbing:
            self.body.animate(self.body.climbing_anim, temp_animate_speed)
        elif self.jumping:
            self.jump()
        elif self.running:
            self.body.animate(self.body.run_anim, temp_animate_speed)
        else:
            self.body.animate(self.body.walk_anim, temp_animate_speed)

    def rotate_to(self, vec):
        vector = vec
        angle = fix_angle(vector.angle_to(self.direction))
        if self.in_vehicle:
            rot_speed = self.vehicle.rot_speed/3
            if self.vehicle.turret == None:
                self.set_rot_speed(rot_speed, angle)
        else:
            rot_speed = MOB_ROT_SPEED
            self.set_rot_speed(rot_speed, angle)

    def set_rot_speed(self, rot_speed, angle):
        if angle < 0:
            self.rot_speed = -rot_speed * 10 * abs(angle) / 180
        else:
            self.rot_speed = rot_speed * 10 * abs(angle) / 180

    def avoid_wall(self):
        hits = pg.sprite.spritecollide(self, self.game.inside_on_screen, False) # Checks to see if the NPC is in a building
        if hits:
            if not pg.sprite.spritecollide(self.goal_target, self.game.inside_on_screen, False): # checks to see if they are trying to go outside of the building.
                self.seek_door()
        else:
            goal_angle = self.goal_target_dist.angle_to(self.direction)
            if self.wall_hit_or == 'h':
                if abs(180 - goal_angle) > abs(0 - goal_angle):
                    angle = 0
                else:
                    angle = 180
            elif self.wall_hit_or == 'v':
                if abs(270 - goal_angle) > abs(90 - goal_angle):
                    angle = 90
                else:
                    angle = 270
            proj_vec = vec(WALL_DETECT_DIST, 0).rotate(angle)
            proj_vec += self.pos
            self.temp_target.set_position(proj_vec.x, proj_vec.y) # Temporarily moves the temp target
            self.target = self.temp_target
            hits = pg.sprite.spritecollide(self.temp_target, self.game.barriers_on_screen, False) # Switches the direction of the target if it hits a wall the other way.
            if hits:
                if hits[0] not in self.game.door_walls:
                    self.seek_random_target()
            #    proj_vec = vec(MOB_HIT_RECT.width * 3 / 2 - 10, 0).rotate((angle + 180)%360)
            #    proj_vec += self.pos
            #    self.temp_target.set_position(proj_vec.x, proj_vec.y)  # Temporarily moves the temp target

    def check_walls(self):
        proj_vec = vec(self.direction.x, self.direction.y)
        proj_vec.scale_to_length(WALL_DETECT_DIST) # makes a vector that projects out in front of NPC the max detect distance for a wall with no walls in between.
        proj_vec += self.pos
        if self.target == self.game.player:
            hit = in_wall(self.game, self.game.walls_on_screen, proj_vec)
        else:
            hit = in_wall(self.game, self.game.barriers_on_screen, proj_vec)
        if hit:
            self.wall_hit_or = hit.orient
        elif next_wall_check(self):
            self.wall_hit_or = choice(('v', 'h'))
            return False
        else:
            hit = in_wall(self.game, self.game.players, proj_vec) #makes Npc walk around player
            if hit:
                self.target = self.game.player
                return True
        return not hit

    def check_target(self, target = 'player'): # Sees if the player or another target group is in front of it.
        if target == 'player':
            target = self.game.players
        proj_vec = vec(self.direction.x, self.direction.y)
        proj_vec.scale_to_length(WALL_DETECT_DIST)
        proj_vec += self.pos
        return in_wall(self.game, target, proj_vec)

    def target_forward(self):
        proj_vec = vec(self.direction.x, self.direction.y)
        vec_length = MOB_HIT_RECT.width * 3/2 - 10
        proj_vec.scale_to_length(vec_length) # makes a vector that projects out in front of NPC the max detect distance for a wall with no walls in between.
        proj_vec += self.pos
        self.temp_target.set_position(proj_vec.x, proj_vec.y) # moves the temp target forward a bit.
        self.target = self.temp_target

    def update(self):
        # This parts synchs the body sprite with the NPC's soul.
        self.body.rot = self.rot
        self.body.image = pg.transform.rotate(self.body.body_surface, self.rot)
        self.body.rect = self.body.image.get_rect()
        self.body.rect.center = self.pos

        if self.living:
            if self.driver:
                self.pos = self.driver.pos
                self.rect.center = self.pos
                self.hit_rect.center = self.pos
                if self.stats['health'] <= 0:
                    self.depossess()
                    self.death()
            else:
                self.acc = vec(0, 0)
                if not self.needs_move and (self.target in self.game.moving_targets) and (not self.target.living):  # Makes it so NPC switches target after it kills one.
                    self.seek_mobs()

                if self in self.game.companions:
                    if self.target == self.game.player:
                        self.offensive = False

                if self.melee_playing:
                    self.melee()
                elif self.reloading:
                    self.reload()

                ora = pg.time.get_ticks() # Makes it so the NPCs don't stay in one place too long.
                #if not self.offensive:
                #    if not self.needs_move:
                #        if ora - self.last_move_check > randrange(4000, 6000):
                #            if not self.is_moving():
                #                self.seek_random_target()
                #                self.needs_move = True
                #            self.last_move_check = ora
                #    else:
                #        if ora - self.last_move_check > randrange(3000, 6000):
                #            self.needs_move = False
                #            self.last_move_check = ora

                if ora - self.last_hit > 3000: # Used to set the time NPCs flee for after being attacked.
                    if self.running:
                        if self.aggression == 'fwp':
                            self.approach_vector = vec(1, 0)
                        self.running = False
                        self.fleeing = False

                if not self.needs_move:
                    if ora - self.last_seek > 1000: # Checks for the closest target
                        self.seek_mobs()
                        self.last_seek = ora

                # Stops them from climbing after a certain time if they aren't on an object that requires you climb on it.
                if self.climbing:
                    if ora - self.last_climb > CLIMB_TIME:
                        if not pg.sprite.spritecollide(self, self.game.climbs, False):
                            self.climbing = False


                self.target_dist = self.target.pos - self.pos
                self.goal_target_dist = self.goal_target.pos - self.pos
                self.temp_target_dist = self.temp_target.pos - self.pos
                target_dist_lsquared = self.target_dist.length_squared()

                # This part makes the NPC avoid walls
                now = pg.time.get_ticks()
                if not self.immaterial:
                    hits = pg.sprite.spritecollide(self, self.game.walls_on_screen, False)
                    if hits and (hits[0] not in self.game.door_walls):
                        self.acc = vec(0, 0)
                        self.hit_wall = True
                        if now - self.last_wall_hit > 1000:
                            self.last_wall_hit = now
                            self.seek_random_target()
                    elif now - self.last_wall_hit > randrange(3000, 5000):
                        self.last_wall_hit = now
                        self.hit_wall = False

                # The AI that controlls NPC attacking.
                if self.target in self.game.moving_targets_on_screen:
                    if True not in [self.melee_playing, self.animating_reload]:
                        if self.offensive:
                            if (self.aggression not in ['fwd', 'fwp']):
                                if self.race != self.target.race or self.provoked: # Won't attack same race unless provoked.
                                    if target_dist_lsquared < self.melee_range**2:
                                        self.approach_vector = vec(1, 0)
                                        now = pg.time.get_ticks()
                                        if now - self.last_melee > randrange(1000, 3000):
                                            self.last_melee = now
                                            self.pre_melee()
                                    elif True not in [self.reloading, self.hit_wall, self.swimming]:
                                        if self.gun:
                                            if target_dist_lsquared < self.weapon_range ** 2:
                                                if self.bow:
                                                    if self.arrow:
                                                        self.shoot()
                                                        self.arrow.kill()
                                                        self.arrow = None
                                                    else:
                                                        self.reloading = True
                                                        self.animating_reload = True
                                                else:
                                                    self.shoot()
                                                if self.bullets_shot >= self.mag_size:
                                                    self.bullets_shot = 0
                                                    self.reloading = True
                                                    self.animating_reload = True
                                        else:
                                            if target_dist_lsquared < self.detect_radius ** 2:
                                                magic_chance = randrange(0, 100)
                                                if magic_chance == 1:
                                                    self.cast_spell()
                                if self.game.player.in_vehicle:
                                    if target_dist_lsquared < 3*self.melee_range**2:
                                        now = pg.time.get_ticks()
                                        if now - self.last_melee > randrange(1000, 3000):
                                            self.last_melee = now
                                            self.pre_melee()
                            elif not self.running: # Non agressive but provoked NPCs
                                if target_dist_lsquared < self.melee_range**2:
                                    self.approach_vector = vec(1, 0)
                                    now = pg.time.get_ticks()
                                    if self.last_melee != 0:
                                        if now - self.last_melee > 20000: # Makes it so the villagers stop attacking you if you've left them alone for 20 seconds.
                                            self.offensive = False
                                            self.last_melee = 0
                                    if self.offensive:
                                        if now - self.last_melee > 3000:
                                            self.last_melee = now
                                            self.pre_melee()

                target_angle = self.target_dist.angle_to(self.approach_vector)
                if (target_dist_lsquared < self.melee_range**2) and (self.target in self.game.moving_targets_on_screen) and self.offensive and (not self.fleeing): # NPC stops in combat range if offensive
                    if self.race != self.target.race:
                        self.animate()
                    elif self.talk_attempt and self.check_target():
                        self.game.dialogue_menu_npc = self
                        self.talk_attempt = False
                    self.rotate_to(vec(1, 0).rotate(-target_angle))
                    self.turn()
                elif (target_dist_lsquared < TALK_RADIUS**2) and (self.target in self.game.moving_targets_on_screen) and (not self.offensive) and (not self.fleeing): # NPC stops in talking range if not offensive.
                    self.rotate_to(vec(1, 0).rotate(-target_angle))
                    self.turn()
                    if self.talk_attempt and self.check_target():
                        self.game.dialogue_menu_npc = self
                        self.talk_attempt = False
                elif (target_dist_lsquared > 4) and self.check_walls() and True not in [self.melee_playing, self.animating_reload]:
                    self.move_forward(target_angle)
                elif not self.check_walls():
                    self.avoid_wall()
                    self.move_forward(target_angle)
                elif self.target not in self.game.entryways_on_screen:
                    self.target = self.goal_target
                else:  # Makes NPCs keep moving after they open doors.
                    self.move_forward(target_angle)
                    self.target_forward()
                if self.goal_target_dist.length_squared() < 30: # Seeks a new target once it has reached it's goal.
                    self.seek_random_target()

                # Used for lights NPCs are carrying.
                if self in self.game.lights:
                    if self.race in ['mechanima', 'mech_suit']:
                        self.light_mask_rect.center = self.rect.center
                    elif self.lamp_hand == 'weapons':
                        self.light_mask_rect.center = self.body.melee_rect.center
                    else:
                        self.light_mask_rect.center = self.body.melee2_rect.center
                    if self.mask_kind in DIRECTIONAL_LIGHTS:
                        new_image = self.game.flashlight_masks[int(self.rot / 3)]
                        old_center = self.light_mask_rect.center
                        self.light_mask = new_image
                        self.light_mask_rect = self.light_mask.get_rect()
                        self.light_mask_rect.center = old_center

    def move_forward(self, target_angle):
        self.animate()
        self.rotate_to(vec(1, 0).rotate(-target_angle))
        speed = self.speed
        if self.running:
            speed = self.run_speed
        self.acc = vec(speed, 0).rotate(-self.rot)
        self.accelerate()
        if self.sounds and random() < 0.002:  # This makes different sounds for each type of npc
            choice(self.sounds).play()

    def check_empty(self):
        count = 0
        for key in self.inventory:
            if key in ITEM_TYPE_LIST:
                if len(self.inventory[key]) == 0 or (self.inventory[key][0] == None and len(self.inventory[key]) == 1):
                    count += 1
                    if count == len(ITEM_TYPE_LIST):
                        self.kill()

    def make_companion(self):
        self.remove(self.game.mobs)
        self.game.player_group.add(self)
        self.game.companions.add(self)
        self.game.companion_bodies.add(self.body)
        self.body.update_animations()
        self.update_collide_list()
        self.target = self.game.player
        self.approach_vector = vec(1, 0)
        self.default_detect_radius = self.detect_radius = self.game.screen_height
        self.guard = True
        self.speed = self.walk_speed = 400
        self.run_speed = 500

    def unfollow(self):
        self.game.mobs.add(self)
        self.remove(self.game.player_group)
        self.remove(self.game.companions)
        self.body.remove(self.game.companion_bodies)
        self.default_detect_radius = self.detect_radius = 250
        self.guard = False
        self.speed = self.walk_speed = 80
        self.run_speed = 100

    def possess(self, driver, demon = False):
        if not self.driver:
            if not driver.possessing:
                self.game.group.change_layer(self.body, PLAYER_LAYER)
                if demon:
                    self.possessed = True
                self.frame = 0
                self.knockback = 0
                self.driver = driver
                if driver == self.game.player:
                    self.game.hud_health_stats = self.stats
                if self.driver.dragon:
                    self.driver.transform()
                self.driver.possessing = self
                self.driver.body = self.body
                self.driver.body.mother = self.driver
                self.driver.body.update()
                self.driver.human_body.remove(self.game.all_sprites)
                self.driver.human_body.remove(self.game.npc_bodies)
                self.game.group.remove(self.driver.human_body)
                self.body = self.driver.human_body
                self.body.mother = self
                self.remove(self.game.mobs)
                self.remove(self.game.npcs)
                self.remove(self.game.moving_targets)
                self.driver.temp_equipped = copy.deepcopy(self.driver.equipped)
                self.driver.equipped = self.equipped
                self.driver.equipped['magic'] = self.driver.temp_equipped['magic']
                self.driver.rot = self.rot
                if demon:
                    for item_type in ITEM_TYPE_LIST:
                        for item in self.inventory[item_type]:
                            self.driver.inventory[item_type].append(item)
                self.driver.body.update_animations()
                self.game.beg = perf_counter() # resets the counter so dt doesn't get messed up.

    def depossess(self):
        if self.driver:
            if self.driver == self.game.player:
                self.game.hud_health_stats = self.driver.stats
            self.driver.possessing = None
            self.knockback = self.kind['knockback']
            if self.driver.swimming:
                self.driver.equipped['weapons'] = None
                self.driver.current_weapon = self.driver.last_weapon
                self.driver.equipped['weapons2'] = None
                self.driver.current_weapon2 = self.driver.last_weapon2
            self.body = self.driver.body
            self.body.mother = self
            self.driver.body = self.driver.human_body
            self.driver.body.mother = self.driver
            self.driver.human_body.add(self.game.all_sprites)
            self.driver.human_body.add(self.game.npc_bodies)
            self.game.group.add(self.driver.human_body)
            if self.possessed:
                self.equipped = copy.deepcopy(self.driver.equipped)
                self.inventory = copy.deepcopy(self.driver.inventory)
            else:
                change_clothing(self, False, True) # Takes off all equipped items.
            self.driver.equipped = self.driver.temp_equipped
            self.driver.body.update_animations()
            self.add(self.game.mobs)
            self.add(self.game.npcs)
            self.add(self.game.moving_targets)
            if self.possessed:
                self.possessed = False
                drop_all_items(self.driver, True)
            self.driver.human_body.update_animations()
            if self.driver.has_dragon_body:
                self.driver.dragon_body.update_animations()
            self.pos = self.driver.pos
            self.rect.center = self.driver.pos
            self.driver.pos = self.driver.pos + vec(40, 0).rotate(-self.driver.rot)
            self.rot = self.driver.rot
            self.driver = None
            self.game.group.change_layer(self.body, MOB_LAYER)
            self.body.update_animations()
            self.frame = 0
            self.game.beg = perf_counter()  # resets dt

    def set_gun_vars(self):
        if self.equipped[self.weapon_hand]:
            if WEAPONS[self.equipped[self.weapon_hand]]['gun']:
                self.gun = True
                self.mag_size = WEAPONS[self.equipped[self.weapon_hand]]['magazine size']
                self.weapon_range = (WEAPONS[self.equipped[self.weapon_hand]]['bullet_speed'] * WEAPONS[self.equipped[self.weapon_hand]]['bullet_lifetime']) / 700
            else:
                self.gun = False
                self.mag_size = 0
                self.weapon_range = 0
            self.bow = False
            if 'bow' in self.equipped[self.weapon_hand]:
                self.bow = True

    def gets_hit(self, damage, knockback = 0, rot = 0, dam_rate = DAMAGE_RATE):
        now = pg.time.get_ticks()
        if now - self.last_hit > dam_rate:
            self.last_hit = now
            self.add_health(-damage)
            self.pos += vec(knockback, 0).rotate(-rot)
            if pg.sprite.spritecollide(self, self.game.barriers, False):  # Prevents sprite from being knocked through a wall.
                self.pos -= vec(knockback, 0).rotate(-rot)
            self.rect.center = self.hit_rect.center = self.pos
            if damage > 0.5:
                if self.equipped['gender'] == 'male':
                    choice(self.game.male_player_hit_sounds).play()
                else:
                    choice(self.game.female_player_hit_sounds).play()
                if self not in self.game.companions:
                    if self.aggression == 'fwp':
                        self.approach_vector = vec(-1, 0)
                        self.running = True
                        self.fleeing = True
                        self.run_speed = self.kind['run speed']
                        self.detect_radius = self.game.screen_width

                    if self.aggression =='awp':
                        self.approach_vector = vec(1, 0)
                        self.speed = self.kind['walk speed'][1] * 1.5
                        self.detect_radius = self.game.screen_width

                    if self.aggression == 'fup':
                        self.approach_vector = vec(1, 0)
                        self.speed = self.kind['walk speed'][1] * 1.2
                        self.detect_radius = self.detect_radius * 2

                    if self.aggression == 'awd':
                        self.approach_vector = vec(1, 0)
                        self.speed = self.kind['walk speed'][1] * 1.5
                        self.detect_radius = self.game.screen_width

                    if self.aggression =='sap':
                        self.approach_vector = vec(1, 0)
                        self.detect_radius = self.game.screen_width
                        self.speed = self.kind['walk speed'][1]

    def does_melee_damage(self, mob):
        now = pg.time.get_ticks()
        if now - self.last_damage > self.melee_rate:
            if self.equipped[self.weapon_hand] == None:
                mob.vel = vec(0, 0)
                choice(self.game.punch_sounds).play()
                mob.gets_hit(self.damage, self.knockback, self.rot)
            else:
                weapon_damage = WEAPONS[self.equipped[self.weapon_hand]]['melee damage']
                damage = self.damage + weapon_damage*(self.stats['health']/self.stats['max health'])
                mob.vel = vec(0, 0)
                self.knockback = WEAPONS[self.equipped[self.weapon_hand]]['knockback']
                self.play_weapon_hit_sound()
                mob.gets_hit(damage, self.knockback, self.rot)

            #choice(mob.hit_sounds).play()
            self.last_damage = now
            mob.target = self

    def add_health(self, amount):
        self.stats['health'] += amount
        if self.stats['health'] > self.stats['max health']:
            self.stats['health'] = self.stats['max health']
        if self.game.hud_health_stats == self.stats:
            self.game.hud_health = self.stats['health'] / self.stats['max health']
        if self.stats['health'] <= 0:
            self.living = False
            self.death()

    def use_item(self):
        if self.equipped['items']:
            if 'spell' in ITEMS[self.equipped['items']]:
                self.inventory['magic'].append(ITEMS[self.equipped['items']]['spell'])
                self.game.effects_sounds['page turn'].play()
                self.game.effects_sounds[ITEMS[self.equipped['items']]['sound']].play()
            if 'ammo' in ITEMS[self.equipped['items']]:
                self.ammo[ITEMS[self.equipped['items']]['type']] += ITEMS[self.equipped['items']]['ammo']
                self.pre_reload()
            if 'magica' in ITEMS[self.equipped['items']]:
                self.add_magica(ITEMS[self.equipped['items']]['magica'])
            if 'health' in ITEMS[self.equipped['items']]:
                self.add_health(ITEMS[self.equipped['items']]['health'])
            if 'stamina' in ITEMS[self.equipped['items']]:
                self.add_stamina(ITEMS[self.equipped['items']]['stamina'])
            if 'change race' in ITEMS[self.equipped['items']]:
                self.equipped['race'] = ITEMS[self.equipped['items']]['change race']
                self.body.update_animations()
            if 'change sex' in ITEMS[self.equipped['items']]:
                self.equipped['gender'] = ITEMS[self.equipped['items']]['change sex']
                if self.equipped['gender'] == 'female':
                    random_dress_top = choice(DRESS_TOPS_LIST)
                    random_dress_skirt = choice(DRESS_BOTTOMS_LIST)
                    random_hair = choice(LONG_HAIR_LIST)
                    self.inventory['tops'].append(random_dress_top)
                    self.inventory['bottoms'].append(random_dress_skirt)
                    self.inventory['hair'].append(random_hair)
                    self.equipped['tops'] = random_dress_top
                    self.equipped['bottoms'] = random_dress_skirt
                    self.equipped['hair'] = random_hair
                else:
                    random_hair = choice(SHORT_HAIR_LIST)
                    self.inventory['tops'].append('tshirt M')
                    self.inventory['bottoms'].append('jeans M')
                    self.inventory['hair'].append(random_hair)
                    self.equipped['tops'] = 'tshirt M'
                    self.equipped['bottoms'] = 'jeans M'
                    self.equipped['hair'] = random_hair
                self.human_body.update_animations()
                self.dragon_body.update_animations()
            if 'potion' in self.equipped['items']:
                self.inventory['items'].append('empty bottle')  # lets you keep the bottle to use for creating new potions.
            if 'fuel' in self.equipped['items']:
                self.inventory['items'].append('empty barrel')
            self.inventory['items'].remove(self.equipped['items'])
            if self.equipped['items'] not in self.inventory['items']:  # This lets you keep equipping items of the same kind. This way you can use multiple heath potions in a row for example.
                self.equipped['items'] = None

    def cast_spell(self):
        if self.inventory['magic'][0]:
            self.equipped['magic'] = choice(self.inventory['magic'])
            if 'healing' in MAGIC[self.equipped['magic']]:
                if self.stats['health'] < (self.stats['max health'] - 15):
                    self.add_health(MAGIC[self.equipped['magic']]['healing'])
                    self.game.effects_sounds[MAGIC[self.equipped['magic']]['sound']].play()
                    Spell_Animation(self.game, self.equipped['magic'], self.pos, self.rot, self.vel)

            else:
                pos = vec(0, 0)
                pos = self.pos + vec(60, 0).rotate(-self.rot)
                self.game.effects_sounds[MAGIC[self.equipped['magic']]['sound']].play()
                Spell_Animation(self.game, self.equipped['magic'], self.pos, self.rot, self.vel)
                if 'fireballs' in MAGIC[self.equipped['magic']]:
                    balls = MAGIC[self.equipped['magic']]['fireballs']
                    damage = MAGIC[self.equipped['magic']]['damage']
                    for i in range(0, balls):
                        Fireball(self, self.game, self.pos, self.rot + (36 * i), damage, 30, 1300, 500, self.vel, 'fire', True, self.in_flying_vehicle)
                if 'summon' in MAGIC[self.equipped['magic']]:
                    if MAGIC[self.equipped['magic']]['summon'] in PEOPLE:
                        summoned = Npc(self.game, self.pos.x + 128, self.pos.y, self.game.map, MAGIC[self.equipped['magic']]['summon'])
                        summoned.make_companion()
                    elif MAGIC[self.equipped['magic']]['summon'] in ANIMALS:
                        Animal(self.game, pos.x, pos.y, self.game.map, MAGIC[self.equipped['magic']]['summon'])

    def death(self):
        self.depossess()
        if self in self.game.companions:
            self.unfollow()
        choice(self.game.zombie_hit_sounds).play()
        self.living = False
        self.body.kill()
        self.remove(self.game.mobs)
        self.remove(self.game.npcs)
        self.remove(self.game.moving_targets)
        self.add(self.game.corpses)
        self.game.group.add(self)
        if self.equipped['race'] == 'demon':
            Npc(self.game, self.pos.x, self.pos.y, self.map, 'blackwraith')
        if self.equipped['race'] in RACE_CORPSE_DICT:
            self.image = pg.transform.rotate(self.game.corpse_images[RACE_CORPSE_DICT[self.equipped['race']]], self.rot)
        else:
            self.image = pg.transform.rotate(self.game.corpse_images[0], self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.game.player.stats['kills'] += 1
        if 'dead' in self.game.people[self.species]:
            self.game.people[self.species]['dead'] = True

    def pre_melee(self): # Used to get the timing correct between each melee strike, and for the sounds
        if not (self.jumping or self.melee_playing):
            if self.arrow:
                self.arrow.kill()
                self.arrow = None
            magic_chance = randrange(0, 40)
            if self.has_magic:
                if magic_chance == 1:
                    self.cast_spell()
            # Selects which hand they attack with based on which hands are armed.
            if self.equipped['weapons']:
                if self.equipped['weapons2']:
                    self.weapon_hand = choice(['weapons', 'weapons2'])
                    #self.dual_melee = choice([True, False])
                else:
                    self.weapon_hand = 'weapons'
            elif self.equipped['weapons2']:
                self.weapon_hand = 'weapons2'
            else:
                self.weapon_hand = choice(['weapons', 'weapons2'])
            now = pg.time.get_ticks()
            if self.equipped[self.weapon_hand]:
                rate =  WEAPONS[self.equipped[self.weapon_hand]]['rate']
                if now - self.last_melee_sound > rate:
                    self.last_melee_sound = now
                    if not WEAPONS[self.equipped[self.weapon_hand]]['gun']:
                        self.play_weapon_sound()
                    else:
                        self.play_weapon_sound('gun')
            else:
                if now - self.last_melee_sound > 100:
                    self.last_melee_sound = now
            self.melee_playing = True
            self.body.frame = 0
            self.melee()
    def melee(self): # Used for the melee animations
        # Default values if no weapons
        self.melee_rate = 200 #default timing between melee attacks if no agility. Reduces with higher agility
        speed = 60 #default speed of melee attacks
        if self.weapon_hand == 'weapons':
            self.animation_playing = self.body.melee_anim
        else:
            self.animation_playing = self.body.l_melee_anim
        if self.equipped[self.weapon_hand]:
            # Slows down attacks with heavier weapons
            if WEAPONS[self.equipped[self.weapon_hand]]['type'] == 'shield':
                self.melee_rate = self.melee_rate + WEAPONS[self.equipped[self.weapon_hand]]['weight'] * 2
                speed = WEAPONS[self.equipped[self.weapon_hand]]['weight'] * 4
            else:
                self.melee_rate = self.melee_rate + WEAPONS[self.equipped[self.weapon_hand]]['weight'] * 20
                speed = speed + WEAPONS[self.equipped[self.weapon_hand]]['weight'] * 5

        #if self.dual_melee:
        #    self.animation_playing = self.body.dual_melee_anim
        #    if self.equipped['weapons'] and self.equipped['weapons2']:
        #        self.melee_rate = self.melee_rate + (WEAPONS[self.equipped['weapons']]['weight'] + WEAPONS[self.equipped['weapons2']]['weight'])/2 * 30
        #        speed = speed + (WEAPONS[self.equipped['weapons']]['weight'] + WEAPONS[self.equipped['weapons2']]['weight'])/4 * 5
        #    elif self.equipped['weapons']:
        #        self.melee_rate = self.melee_rate + WEAPONS[self.equipped['weapons']]['weight'] * 20
        #        speed = speed + WEAPONS[self.equipped['weapons']]['weight']/2 * 5
        #    elif self.equipped['weapons2']:
        #        self.melee_rate = self.melee_rate + WEAPONS[self.equipped['weapons2']]['weight'] * 20
        #        speed = speed + WEAPONS[self.equipped['weapons2']]['weight']/2 * 5

        now = pg.time.get_ticks()
        if now - self.last_shot > self.melee_rate:
            if self.melee_playing:
                self.body.animate(self.animation_playing, speed)
                if self.body.frame > len(self.animation_playing[0]) - 1:
                    self.melee_playing = False
                    #self.dual_melee = False
                    self.last_shot = pg.time.get_ticks()
    def reload(self):
        speed = WEAPONS[self.equipped[self.weapon_hand]]['reload speed']
        self.animation_playing = self.body.reload_anim
        now = pg.time.get_ticks()
        if self.animating_reload:
            self.body.animate(self.animation_playing, speed)
            if self.body.frame > len(self.animation_playing[0]) - 1:
                self.animating_reload = False
                if self.bow:
                    if self.arrow == None:
                        Arrow(self.game, self, self.equipped[self.weapon_hand])
        if now - self.last_reload > 10000:  # Makes it so Npc isn't always shooting
            self.reloading = False
            self.animating_reload = False
            self.last_reload = now

    def shoot(self):
        self.melee_playing = False
        if self.weapon_hand == 'weapons2':
            self.animation_playing = self.body.l_shoot_anim
        else:
            self.animation_playing = self.body.shoot_anim
        if self.climbing:
            self.animation_playing = self.body.climbing_shoot_anim

        self.body.animate(self.animation_playing, 120)
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.equipped[self.weapon_hand]]['rate']:
            self.last_shot = now
            self.fire_bullets()

    def fire_bullets(self):
        if self.weapon_hand == 'weapons':
            angle = self.body.weapon_angle
        else:
            angle = self.body.weapon2_angle
        if not self.in_vehicle:
            self.vel = vec(-WEAPONS[self.equipped[self.weapon_hand]]['kickback'], 0).rotate(-self.rot)
        dir = vec(1, 0).rotate(-(self.rot + angle))
        if self.weapon_hand == 'weapons':
            pos = self.pos + (self.body.weapon_pos + WEAPONS[self.equipped['weapons']]['offset']).rotate(-(self.rot + angle))
        else:
            pos = self.pos + (self.body.weapon2_pos + vec(WEAPONS[self.equipped['weapons2']]['offset'].x, -WEAPONS[self.equipped['weapons2']]['offset'].y)).rotate(-(self.rot + angle))
        for i in range(WEAPONS[self.equipped[self.weapon_hand]]['bullet_count']):
            Bullet(self, self.game, pos, dir, self.rot, self.equipped[self.weapon_hand], True, self.in_flying_vehicle)
            self.bullets_shot += 1
            self.play_weapon_sound()
        if WEAPONS[self.equipped[self.weapon_hand]]['gun']:
            MuzzleFlash(self.game, pos)


    def play_weapon_sound(self, default = ''):
        if default == '':
            snd = choice(self.game.weapon_sounds[WEAPONS[self.equipped[self.weapon_hand]]['type']])
        else:
            snd = choice(self.game.weapon_sounds['mace'])
        if snd.get_num_channels() > 2:
            snd.stop()
        snd.play()

    def play_weapon_hit_sound(self):
        snd = choice(self.game.weapon_hit_sounds[WEAPONS[self.equipped[self.weapon_hand]]['type']])
        if snd.get_num_channels() > 2:
            snd.stop()
        snd.play()

    def draw_health(self):
        if self.stats['health'] > self.stats['max health'] * 0.6:
            col = GREEN
        elif self.stats['health'] > self.stats['max health'] * 0.3:
            col = YELLOW
        else:
            col = RED
        width = int(MOB_HEALTH_BAR_LENGTH * self.stats['health'] / self.stats['max health'])
        return width

    def pre_jump(self):
        if True not in [self.melee_playing, self.in_vehicle, self.jumping, self.swimming]:
            self.jumping = True
            self.body.frame = 0
            self.jump()

    def jump(self):
        delay = 500
        speed = 135
        if self.falling:
            speed = 20
            delay = 0
        self.animation_playing = self.body.jump_anim

        now = pg.time.get_ticks()
        if now - self.last_shot > delay:
            if self.jumping:
                self.body.animate(self.animation_playing, speed)
                if self.body.frame > len(self.animation_playing[0]) - 1:
                    self.jumping = False
                    self.falling = False
                    self.last_shot = pg.time.get_ticks()

class Animal(pg.sprite.Sprite):
    def __init__(self, game, x, y, map, species, health = None):
        self.game = game
        self.species = self.race = species
        self.kind = self.cat = ANIMALS[species]
        self.name = self.kind['name']
        self.protected = self.kind['protected']
        if 'flying' in self.kind.keys():
            self.flying = self.kind['flying']
        else:
            self.flying = False
        if self.flying:
            self._layer = SKY_LAYER
            self.in_flying_vehicle = True
        elif 'horse' in self.name:
            self._layer = BULLET_LAYER
            self.in_flying_vehicle = False
        else:
            self._layer = MOB_LAYER
            self.in_flying_vehicle = False
        if self.kind['grabable']:
            self.groups = game.all_sprites, game.mobs, game.animals, game.grabable_animals, game.detectables, game.moving_targets
        else:
            self.groups = game.all_sprites, game.mobs, game.animals, game.moving_targets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game.group.add(self)
        self.original_layer = self._layer
        self.map = map
        self.aggression = self.kind['aggression']
        self.touch_damage = self.kind['touch damage']
        self.damage = self.kind['damage']
        self.knockback = self.kind['knockback']
        self.detect_radius = self.default_detect_radius = self.kind['detect radius']
        self.avoid_radius = self.kind['avoid radius']
        if not health:
            self.stats = {'health': self.kind['health'], 'max health': self.kind['health']}
        else:
            self.stats = {'health': health, 'max health': self.kind['health']}
        self.mountable = self.kind['mountable']
        self.occupied = False
        self.run_speed = self.kind['run speed'] * (randrange(7, 10)/10)
        self.walk_speed = self.kind['walk speed'] * (randrange(7, 10)/10)
        self.run_animate_speed = self.kind['run animate speed']
        self.walk_animate_speed = self.kind['walk animate speed']
        self.item_type = self.kind['item type']
        if 'magic' in self.kind.keys():
            self.spells = self.kind['magic']
        else:
            self.spells = None
        self.item = self.kind['item']
        self.collide_list = []
        for item in self.kind['collide']:
            self.collide_list.append(eval("self.game." + item + "_on_screen"))
        self.walk_image_list = self.game.animal_animations[self.name]['walk']
        if 'run' in list(self.game.animal_animations[self.name].keys()):
            self.run_image_list = self.game.animal_animations[self.name]['run']
        else:
            self.run_image_list = self.walk_image_list
        self.old_run_image_list = None
        self.old_walk_image_list = None
        self.selected_image_list = self.walk_image_list
        self.image = self.walk_image_list[1].copy()
        self.rot = randrange(0, 360)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.elevation = 0
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.hideable = False
        if self.kind['hit rect'] == SMALL_HIT_RECT:
            if not self.flying:
                self.hideable = True # Used for animals that can hide in long grass
        self._in_grass = False
        self.hit_rect = self.kind['hit rect'].copy()
        self.width = self.hit_rect.width
        self.hit_rect.center = self.pos
        self.rect.center = self.pos
        self.target = game.player
        self.last_hit = 0
        self.last_damage = 0
        self.melee_rate = 800
        self.last_move = 0
        self.last_wall_hit = 0
        self.last_target_seek = 0
        self.hit_wall = False
        self.living = True
        self.immaterial = False
        self.eating_corpse = 0
        self.rotate_direction = randrange(-1, 1)
        self.rot_speed = self.orig_rot_speed = 6 * self.walk_speed / self.width
        self.frame = 0 #used to keep track of what frame the animation is on.
        self.running = False
        self.jumping = False
        if 'climbing' in self.kind.keys() and self.kind['climbing']:
            self.climbing = True
        else:
            self.climbing = False
        if 'aquatic' in self.kind.keys() and self.kind['aquatic']:
            self.aquatic = True
        else:
            self.aquatic = False
        self.swimming = False
        self.falling = False
        self.invisible = False
        self.in_shallows = False
        self.in_player_vehicle = False
        self.in_vehicle = False
        self.turret = None
        self.driver = None
        if 'a' in self.aggression:
            self.aggressive = self.offensive = True
        else:
            self.aggressive = self.offensive = False
        self.provoked = False

        #Changes animals behavior to be more friendly towards elves. I need to change this because it will make all animals friendly to everyone if you are an elf.
        if 'elf' in self.game.player.race:
            #if self.aggression == 'awd':
            #    self.aggression = 'awp'
            if self.aggression == 'fwd':
                self.aggression = 'fwp'
        if self.aggression == 'fwd':
            self.approach_vector = vec(-1, 0)
        if self.aggression == 'fup':
            self.approach_vector = vec(-1, 0)
        if self.aggression == 'awd':
            self.approach_vector = vec(1, 0)
        if self.aggression == 'fwp':
            self.approach_vector = vec(choice([1, 0]), choice([1, -1, 0]))
        if self.aggression == 'awp':
            self.approach_vector = vec(0, -1)

        set_elevation(self)
        if wall_check(self): # Kills animals that spawn in wall tiles.
            self.kill()

    @property
    def in_grass(self):
        return self._in_grass
    @in_grass.setter
    def in_grass(self, value): # This hides small animals when they go into long grass by changing their images to a tiny shadow.
        if value!=self._in_grass:
            if self.hideable:
                if value:
                    self.old_run_image_list = self.run_image_list
                    self.old_walk_image_list = self.walk_image_list
                    self.walk_image_list = self.run_image_list = [self.game.invisible_image, self.game.invisible_image]
                    self.frame = 0
                else:
                    self.run_image_list = self.old_run_image_list
                    self.walk_image_list = self.old_walk_image_list
            self._in_grass = value

    def avoid_mobs(self):
        for mob in self.game.mobs_on_screen:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < self.avoid_radius:
                    self.acc += dist.normalize()

        # Makes it so non aggressive animals don't cling to you.
        if not self.aggressive:
            dist = self.pos - self.game.player.pos
            if 0 < dist.length() < self.avoid_radius:
                self.acc += dist.normalize()

    def seek_random_target(self):
        self.target = choice(list(self.game.random_targets))
        self.detect_radius = self.game.map.height / 2
        temp_dist = self.target.pos - self.pos
        temp_dist = temp_dist.length()
        if temp_dist > self.detect_radius:
            self.target = choice(list(self.game.random_targets))
        if temp_dist < 200:
            self.target = choice(list(self.game.random_targets))

    def seek_mobs(self):
        last_dist = 100000
        player_dist = self.game.player.pos - self.pos
        player_dist = player_dist.length()

        # Used for setting random NPC targets if the player isn't visible.
        if self.game.player.invisible:
            if self.target == self.game.player:
                self.seek_random_target()

        elif self.game.player.in_vehicle:
            if self.game.player.vehicle.kind == 'airship':
                if not self.flying:
                    self.seek_random_target()
            else:
                if player_dist < self.detect_radius:
                    self.target = self.game.player.vehicle
                else:
                    if self.target == self.game.player.vehicle:
                        self.seek_random_target()
        else:
            if self.target not in self.game.npcs:
                if player_dist < self.detect_radius * 2:
                    self.target = self.game.player
                else:
                    if self.target == self.game.player:
                        self.seek_random_target()

        if self.aggression == 'awd':
            self.offensive = True
            for mob in self.game.moving_targets_on_screen: # Only looks at mobs that are on screen
                if mob != self:
                    if mob.aggression != 'awd' or mob in self.game.npcs_on_screen:
                        dist = self.pos - mob.pos
                        dist = dist.length()
                        if 0 < dist < self.detect_radius:
                            if last_dist > dist:  # Finds closest NPC
                                if player_dist > dist: # Only targets player if you are closer than the others NPCs
                                    self.target = mob
                                    self.approach_vector = vec(1, 0)
                                    last_dist = dist
                                else:
                                    if self.game.player.invisible:
                                        self.target = mob
                                    else:
                                        self.target = self.game.player

            if self.target == self.game.player or not self.target.living:
                for item in self.game.dropped_items_on_screen:# animals target dead animals
                    if 'dead' in item.name:
                        dist = self.pos - item.pos
                        dist = dist.length()
                        if 0 < dist < self.detect_radius:
                            if last_dist > dist:  # Finds closest item
                                if player_dist > dist: # Only targets player if you are closer than the others NPCs
                                    self.target = item
                                    self.approach_vector = vec(1, 0)
                                    last_dist = dist

            if not self.target.living: # Kills corps after so many hits.
                if self.target in self.game.animals_on_screen:
                    self.target.kill()
                    self.target = self.game.player
                else:
                    self.eating_corpse += 1
                    if self.eating_corpse > 4:
                        self.target.kill()
                        self.target = self.game.player
                        self.eating_coprse = 0
                        self.stats['health']= self.stats['max health'] # heals animal
            else:
                self.eating_coprse = 0

        if self.target not in self.game.random_targets:
            self.detect_radius = self.default_detect_radius

    def animate(self, images):
        self.frame += 1
        if self.frame > len(images) - 1:
            self.frame = 0

    def accelerate(self, speed):
        try:
            self.acc.scale_to_length(speed)
        except:
            self.acc = vec(0, 0)
        self.acc += self.vel * -0.75 # Velocity times friction
        self.vel += self.acc * self.game.dt
        #self.vel = vec(speed, 0).rotate(-self.rot)
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[self.game.key_map['sprint']]:
            self.driver.acceleration = self.run_speed / 40
            self.running = True
        else:
            self.driver.acceleration = self.walk_speed / 14
            self.running = False
        if keys[self.game.key_map['dismount']]:
            self.unmount()

    def mount(self, driver):
        if driver == self.game.player:
            self.game.hud_health_stats = self.stats
        self.rot_speed = 60 * self.walk_speed / self.width
        if driver.possessing:
            if driver.possessing.race == 'mech_suit':
                return
        self.game.group.change_layer(self, MOB_LAYER)
        self.frame = 0
        self.occupied = True
        self.knockback = 0
        self.driver = driver
        self.driver.in_vehicle = True
        self.driver.vehicle = self
        self.driver.human_body.update_animations()
        if self.driver.has_dragon_body:
            self.driver.dragon_body.update_animations()
        self.add(self.game.occupied_vehicles)
        self.add(self.game.all_vehicles)
        self.remove(self.game.mobs)
        if self.species == 'horse':
            if self.driver == self.game.player:
                if 'horse bridle' in self.game.player.inventory['items']:
                    self.make_companion()
        self.game.beg = perf_counter() # resets the counter so dt doesn't get messed up.

    def unmount(self):
        if self.driver == self.game.player:
            self.game.hud_health_stats = self.driver.stats
        self.rot_speed = self.orig_rot_speed
        self.game.group.change_layer(self, self.original_layer)
        self.occupied = False
        self.knockback = self.kind['knockback']
        self.driver.in_vehicle = False
        self.driver.friction = PLAYER_FRIC
        self.driver.acceleration = PLAYER_ACC
        if self.driver.swimming:
            self.driver.equipped['weapons'] = None
            self.driver.current_weapon = self.driver.last_weapon
            self.driver.equipped['weapons2'] = None
            self.driver.current_weapon2 = self.driver.last_weapon2
        self.driver.vehicle = None
        self.remove(self.game.occupied_vehicles)
        self.remove(self.game.all_vehicles)
        self.add(self.game.mobs)
        self.driver.human_body.update_animations()
        if self.driver.has_dragon_body:
            self.driver.dragon_body.update_animations()
        self.driver.pos = self.driver.pos + (80, 80)
        self.driver = None
        self.frame = 0
        self.game.beg = perf_counter()  # resets dt

    def make_companion(self):
        self.game.companions.add(self)
        self.update_collide_list()
        self.target = self.game.player
        self.approach_vector = vec(1, 0)
        self.aggression = 'awp'
        self.default_detect_radius = self.detect_radius = self.game.screen_height
        self.guard = True
        self.speed = self.walk_speed = 200
        self.run_speed = 480

    def unfollow(self):
        self.remove(self.game.companions)
        self.default_detect_radius = self.detect_radius = 250
        self.guard = False
        self.speed = self.walk_speed = 80
        self.run_speed = 100

    def update_collide_list(self):
        self.collide_list = [self.game.walls_on_screen]

    def cast_spell(self):
        spell = choice(self.spells)
        self.game.effects_sounds[MAGIC[spell]['sound']].play()
        if 'healing' in MAGIC[spell]:
            Spell_Animation(self.game, spell, self.pos, self.rot, self.vel)
            self.add_health(MAGIC[spell]['healing'])
        if 'fireballs' in MAGIC[spell]:
            balls = MAGIC[spell]['fireballs']
            damage = MAGIC[spell]['damage']
            for i in range(0, balls):
                Fireball(self, self.game, self.pos, self.rot + (36 * i), damage, 30, 1300, 500, self.vel, 'fire', True, self.in_flying_vehicle)

    def update(self):
        if self.living:
            if not self.occupied:
                now0 = pg.time.get_ticks()
                if now0 - self.last_target_seek > 4000:
                    self.seek_mobs()
                    self.last_target_seek = now0
                target_dist = self.target.pos - self.pos

                # This part makes the animal avoid walls
                if self.climbing:
                    hits = pg.sprite.spritecollide(self, self.game.walls_on_screen, False) + pg.sprite.spritecollide(self, self.game.shallows_on_screen, False)
                else:
                    hits = pg.sprite.spritecollide(self, self.game.barriers_on_screen, False) + pg.sprite.spritecollide(self, self.game.shallows_on_screen, False) # This part makes the animal avoid walls
                if hits:
                    self.hit_wall = True
                    now = pg.time.get_ticks()
                    if now - self.last_wall_hit > randrange(300, 1000):
                        self.animate(self.run_image_list)
                        self.last_wall_hit = now
                        if random() < 0.5:
                            self.rotate_direction = choice([-1, 0, 1])
                    self.rot += (3 * (self.walk_speed / self.width) * self.rotate_direction) % 360
                    self.avoid_mobs()
                    self.accelerate(self.walk_speed)

                if (target_dist.length_squared() < self.detect_radius**2) and (self.target not in self.game.random_targets):
                    #if random() < 0.002:
                    #    choice(self.game.zombie_moan_sounds).play()
                    if self.spells:
                        direction_vec = self.pos + vec(self.detect_radius, 0).rotate(-self.rot)
                        difx = abs(self.target.pos.x - direction_vec.x)
                        dify = abs(self.target.pos.y - direction_vec.y)
                        if difx < 300:
                            if dify < 300:
                                magic_chance = randrange(0, 10)
                                if magic_chance == 1:
                                    self.cast_spell()

                    now = pg.time.get_ticks()
                    if now - self.last_move > self.run_animate_speed: # What animal does when you are close it.
                        self.animate(self.run_image_list)
                        self.last_move = now
                    elif now - self.last_wall_hit > randrange(3000, 5000):
                        self.last_wall_hit = now
                        self.hit_wall = False
                    if not self.hit_wall:
                        self.rot = target_dist.angle_to(self.approach_vector)
                    self.rotate_image(self.run_image_list)
                    self.acc = vec(1, 0).rotate(-self.rot)
                    self.avoid_mobs()
                    self.accelerate(self.run_speed)
                    collide(self)

                else:
                    now = pg.time.get_ticks()
                    if now - self.last_move > self.walk_animate_speed:  # animates animal
                        self.animate(self.walk_image_list)
                        self.last_move = now
                        if random() < 0.25:
                            self.rotate_direction = choice([-1, 0, 1])
                        self.rot += (self.rot_speed * self.rotate_direction) % 360
                    if self.frame > len(self.walk_image_list) - 1:
                        self.frame = 0
                    self.rotate_image(self.walk_image_list)
                    self.acc = vec(1, 0).rotate(-self.rot)
                    self.avoid_mobs()
                    self.accelerate(self.walk_speed)
                    collide(self)

            else: # This is what the animal does if you are riding it
                # Increases animal friction when not accelerating
                if self.driver.is_moving():
                    # Makes the friction greater when the vehicle is sliding in a direction that is not straight forward.
                    angle_difference = abs(fix_angle(self.driver.vel.angle_to(self.driver.direction)))
                    if angle_difference > 350:
                        angle_difference = 0
                    if angle_difference < 0.1:
                        angle_difference = 0
                    self.driver.friction = -(angle_difference / 1000 + .015)
                    # Animates the animal
                    now = pg.time.get_ticks()
                    if self.running:
                        animate_speed = self.run_animate_speed
                        self.selected_image_list = self.run_image_list
                    else:
                        animate_speed = self.walk_animate_speed
                        self.selected_image_list = self.walk_image_list

                    if now - self.last_move > animate_speed:  # animates animal
                        self.animate(self.selected_image_list)
                        self.last_move = now
                    if self.frame > len(self.selected_image_list) - 1:
                        self.frame = 0
                else:
                    self.driver.friction = -.28
                self.rot = self.driver.rot
                self.pos = self.driver.pos
                self.rotate_image(self.selected_image_list)
                collide(self)
                self.get_keys()  # this needs to be last in this method to avoid executing the rest of the update section if you exit

    def check_empty(self):
        if len(self.inventory['items']) == 0 or (self.inventory['items'][0] == None and len(self.inventory['items']) == 1):
            self.kill()

    def rotate_image(self, image_list):
        self.image = pg.transform.rotate(image_list[self.frame], self.rot)
        old_center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.center = vec(old_center) #+ self.rect_offset.rotate(-self.rot)

    def add_health(self, amount):
        self.stats['health']+= amount
        if self.stats['health']> self.stats['max health']:
            self.stats['health']= self.stats['max health']
        if self.stats['health'] <= 0:
            self.living = False
            self.death()
        if self.game.hud_health_stats == self.stats:
            self.game.hud_health = self.stats['health'] / self.stats['max health']

    def gets_hit(self, damage, knockback = 0, rot = 0, dam_rate = DAMAGE_RATE):
        now = pg.time.get_ticks()
        if now - self.last_hit > dam_rate:
            self.last_hit = now
            self.add_health(-damage)
            self.pos += vec(knockback, 0).rotate(-rot)
            if pg.sprite.spritecollide(self, self.game.barriers, False):  # Prevents sprite from being knocked through a wall.
                self.pos -= vec(knockback, 0).rotate(-rot)
            self.rect.center = self.hit_rect.center = self.pos
            if self.game.hud_health_stats == self.stats:
                self.game.hud_health = self.stats['health'] / self.stats['max health']
            if damage > 0:
                if self.aggression == 'fwp':
                    self.approach_vector = vec(-1, 0)
                if self.aggression == 'awp':
                    self.approach_vector = vec(1, 0)
                if self.aggression == 'fup':
                    self.approach_vector = vec(1, 0)
                self.run_speed = self.kind['run speed'] * 1.5

    def does_melee_damage(self, mob):
        now = pg.time.get_ticks()
        if now - self.last_damage > self.melee_rate:
            mob.gets_hit(self.damage, self.knockback, self.rot)
            self.last_damage = now
            mob.target = self
            self.melee_rate = randrange(800, 2000)

    def death(self, silent = False):
        if self in self.game.companions:
            self.unfollow()
        if self.occupied:
            self.unmount()
        if not silent:
            choice(self.game.zombie_hit_sounds).play()
        self.game.player.stats['kills'] += 1
        if 'death action' in self.kind.keys():
            if self.kind['death action'] == 'explode':
                Explosion(self.game, self, 0.5, self.damage * 4)

        if self.kind['corpse']:
            self.living = False
            self.inventory = {'locked': False, 'combo': None, 'difficulty': 0,'weapons': [None], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None],
                  'items': self.kind['dropped items'].copy(), 'magic': [None], 'gold': 0}
            self.remove(self.game.mobs)
            self.remove(self.game.animals)
            self.remove(self.game.moving_targets)
            self.add(self.game.corpses)
            self.game.group.change_layer(self, ITEMS_LAYER) # Switches the corpse to items layer
            self.image = pg.transform.rotate(self.game.corpse_images[self.kind['corpse']], self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
        else:
            for i in self.kind['dropped items']:
                if i:
                    for item_type in ITEM_TYPE_LIST:
                        if i in eval(item_type.upper()).keys():
                            Dropped_Item(self.game, self.pos, item_type, i, self.rot)
            if self.kind['name'] == 'sea turtle':
                Breakable(self.game, self.pos, self.pos.x - 60, self.pos.y - 60, 120, 120, BREAKABLES['empty turtle shell'], 'empty turtle shell', self.map)
            self.kill()

    def pre_jump(self):
        pass
    def jump(self):
        pass

    def draw_health(self):
        pass


# Used for arrows shown in loaded bows (not ones being shot)
class Arrow(pg.sprite.Sprite):
    def __init__(self, game, mother, weapon):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.arrows
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.mother = mother
        self.game.group.add(self)
        self.weapon = weapon
        self.image_orig = self.game.bullet_images[WEAPONS[self.weapon]['bullet_size']]
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        if self.mother.weapon_hand == 'weapons':
            self.offset = self.mother.body.weapon_pos
        else:
            self.offset = self.mother.body.weapon2_pos
        self.rect.center = self.mother.pos + self.offset.rotate(-self.mother.rot)
        self.mother.arrow = self

    def update(self):
        self.image = pg.transform.rotate(self.image_orig, self.mother.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.mother.pos + self.offset.rotate(-self.mother.rot)


class Bullet(pg.sprite.Sprite):
    def __init__(self, mother, game, pos, dir, rot, weapon, enemy = False, sky = False):
        self.sky = sky
        if self.sky:
            self._layer = SKY_LAYER
        else:
            self._layer = BULLET_LAYER
        self.mother = mother
        self.enemy = enemy
        if self.enemy:
            self.groups = game.all_sprites, game.bullets, game.enemy_bullets
        else:
            self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.game.group.add(self)
        self.weapon = weapon
        self.target = None
        self.size = WEAPONS[self.weapon]['bullet_size']
        self.rot = rot
        self.image = pg.transform.rotate(game.bullet_images[WEAPONS[self.weapon]['bullet_size']], self.rot)
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.pos = vec(pos)
        self.knockback = WEAPONS[self.weapon]['knockback']
        self.rect.center = pos
        spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
        self.dir = dir.rotate(spread)
        self.vel = self.dir * WEAPONS[self.weapon]['bullet_speed'] * uniform(0.9, 1.1) + self.mother.vel
        self.lifetime = WEAPONS[self.weapon]['bullet_lifetime']

        self.spawn_time = pg.time.get_ticks()
        self.damage = WEAPONS[self.weapon]['damage']
        self.exp_damage = self.damage
        self.exp = False
        self.energy = False
        self.fire = False
        self.shock = False
        self.rob_health = False
        for bullet in EXPLOSIVE_BULLETS:
            if bullet in self.size:
                self.exp = True
                if '10' in bullet:
                    self.exp_damage = self.damage * 3
                else:
                    self.exp_damage = self.damage * 25
        for bullet in ENCHANTED_BULLETS:
            if bullet in self.size:
                self.energy = True
        for bullet in ROB_HEALTH_BULLETS:
            if bullet in self.size:
                self.rob_health = True
        for bullet in FIRE_BULLETS:
            if bullet in self.size:
                self.fire = True
        for bullet in SHOCK_BULLETS:
            if bullet in self.size:
                if '12' not in self.size:
                    self.shock = True


    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if pg.sprite.spritecollideany(self, self.game.walls_on_screen):
            self.death()
        # Kills bullets of current and previous weapons
        if pg.time.get_ticks() - self.spawn_time > self.lifetime:
            self.death()

    def death(self, target = None):
        if target == None:
            self.target = self
        else:
            self.target = target
        if self.exp:
            if self.fire:
                self.explode('fire')
            elif self.shock:
                self.explode('shock')
            elif self.rob_health:
                if self.target != self:
                    self.mother.add_health(int(self.damage / 2))
                self.explode()
            else:
                self.explode()
        else:
            if self.fire:
                Stationary_Animated(self.game, self.target.pos, 'fire', 1000, True)
            if self.shock:
                Stationary_Animated(self.game, self.target.pos, 'shock', 333)
            if self.rob_health:
                if self.target != self:
                    self.mother.add_health(int(self.damage / 2))
            self.kill()

    def explode(self, after_effect = None):
        pos = self.pos
        Explosion(self.game, self.target, 0.5, self.exp_damage, pos, after_effect, self.sky)
        self.kill()

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites, game.lights
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.game.group.add(self)
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()
        self.light_mask = pg.transform.scale(self.game.light_mask_images[0], (150, 150))
        self.light_mask_rect = self.light_mask.get_rect()
        self.light_mask_rect.center = self.rect.center


    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

class Dropped_Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type, item, rot = None, random_spread = False):
        self.brightness = 0
        if 'plate' in item:
            self._layer = WALL_LAYER
        else:
            self._layer = ITEMS_LAYER
        if 'fire pit' in item:
            self.groups = game.all_sprites, game.dropped_items, game.detectables, game.firepits
        elif item in LIGHTS_LIST:
            if 'flashlight' not in item:
                self.groups = game.all_sprites, game.dropped_items, game.detectables, game.lights
                self.light = True
                if item in WEAPONS:
                    self.brightness = WEAPONS[item]['brightness']
                    self.mask_type = WEAPONS[item]['light mask']
                else:
                    self.brightness = ITEMS[item]['brightness']
                    self.mask_type = ITEMS[item]['light mask']
            else:
                self.groups = game.all_sprites, game.dropped_items, game.detectables
        else:
            self.groups = game.all_sprites, game.dropped_items, game.detectables
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.game.group.add(self)
        self.map = None
        self.item_type = type
        self.item = self.name = item
        self.rot = rot
        self.dropped_fish = False
        self.lit = False
        self.floats = False
        self.random_spread = random_spread
        self.pos = pos
        self.living = False
        # Looks up the item image from the list of dictionaries in the settings based on the item type and item name.
        if self.item_type[-1:] == 's':
            image_path = "self.game." + self.item_type[:-1] + "_images[" + self.item_type.upper() + '["' + item + '"]["image"]]'
        else:
            image_path = "self.game." + self.item_type + "_images[" + self.item_type.upper() + '["' + item + '"]["image"]]'
        if self.rot == None:
            self.rot = randrange(0, 360)

        itemdict = eval(self.item_type.upper())
        temp_img = eval(image_path)
        if 'color' in itemdict[self.name]:
            temp_img = color_image(temp_img, itemdict[self.name]['color'])
        self.image = pg.transform.rotate(temp_img, self.rot)
        self.rect = self.hit_rect = self.image.get_rect()
        if self.random_spread:
            self.pos = self.pos + (randrange(-50, 50), randrange(-50, 50))
        self.rect.center = self.hit_rect.center = self.pos
        if self.brightness > 0:
            self.light_mask = pg.transform.scale(self.game.light_mask_images[self.mask_type], (self.brightness, self.brightness))
            self.light_mask = pg.transform.rotate(self.light_mask, self.rot)
            self.light_mask_rect = self.light_mask.get_rect()
            self.light_mask_rect.center = self.rect.center

        count = 0
        for i in FLOAT_LIST:
            if i in self.item:
                count += 1
        if count != 0:
            self.floats = True

        # Controls dropping live animals
        if self.item[:4] == 'live':
            temp_item = self.item.replace('live ', '')
            if 'enchanted' in temp_item:
                temp_item = temp_item[:-5]
                temp_item = temp_item.replace('fire spark enchanted ', '')
                temp_item = temp_item.replace('electric spark enchanted ', '')
            if 'fish' in temp_item:
                fish = Dropped_Item(self.game, self.pos, 'items', 'dead ' + temp_item)
                fish.dropped_fish = True
            else:
                Animal(self.game, self.pos.x, self.pos.y, self.map, temp_item)
            self.kill()

        # Dropping items in grass
        hits = pg.sprite.spritecollide(self, self.game.long_grass, False)
        if hits:
            self.image = self.game.invisible_image
            self.rect = self.hit_rect = self.image.get_rect()
            self.rect.center = self.pos

    def update(self):
        pass

class LightSource(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, kind = 1, rot = 0):
        self.groups = game.lights, game.all_static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.kind = kind
        self.rot = rot
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.light_mask = pg.transform.scale(self.game.light_mask_images[self.kind], (int(w * 7), int(h * 7)))
        if self.rot != 0:
            self.light_mask = pg.transform.rotate(self.light_mask, self.rot)
        self.light_mask_rect = self.light_mask.get_rect()
        self.light_mask_rect.center = self.rect.center


class Stationary_Animated(pg.sprite.Sprite): # Used for fires and other stationary animated sprites
    def __init__(self, game, obj_center, kind, lifetime = None, offset = False, sky = False):
        self.sky = sky
        if self.sky:
            self._layer = SKY_LAYER
        else:
            self._layer = BULLET_LAYER
        self.game = game
        self.center = obj_center
        self.kind = kind
        self.offset = offset
        if self.kind == 'fire':
            self.image_list = self.game.fire_images
            self.groups = game.all_sprites, game.fires, game.lights
            self.damage = 1
            self.animate_speed = 50
            self.light_radius = FIRE_LIGHT_RADIUS
            if not self.offset:
                self.center.y -= 40
                self.center.x -= 8
        elif self.kind == 'shock':
            self.light_radius = (150, 150)
            self.image_list = self.game.shock_images
            self.groups = game.all_sprites, game.fires, game.lights #game.shocks
            self.damage = 1
            self.animate_speed = 10
        else:
            self.light_radius = LIGHT_RADIUS
            self.groups = game.all_sprites
            self.damage = 0
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game.group.add(self)
        self.image = self.image_list[1].copy()
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
        self.light_mask = pg.transform.scale(self.game.light_mask_images[2], self.light_radius)
        self.light_mask_rect = self.light_mask.get_rect()
        self.light_mask_rect.center = self.rect.center
        self.frame = 0
        self.last_move = 0
        self.knockback = 0
        self.spawn_time = pg.time.get_ticks()
        self.lifetime = lifetime
        self.last_sound = 0
        try:
            self.pos = vec(self.center.x, self.center.y)
        except:
            self.pos = vec(0, 0)

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_move > self.animate_speed:
            self.animate(self.image_list)
            self.last_move = now
            self.image = self.image_list[self.frame]
            if not self.offset:
                self.rect.center = self.center
                self.light_mask_rect.center = self.rect.center
            else:
                self.rect.center = self.center + vec(-8, -40)
                self.light_mask_rect.center = self.rect.center


        if self.lifetime:
            if now - self.spawn_time > self.lifetime:
                self.kill()

    def animate(self, images):
        self.frame += 1
        if self.frame > len(images) - 1:
            self.frame = 0

class Entryway(pg.sprite.Sprite):
    def __init__(self, game, x, y, orientation = 'L', kind = 'wood', name = 'generic', locked = False):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.entryways
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.game.group.add(self)
        self.name = name
        self.kind = kind
        self.orientation = orientation
        self.locked = locked
        self.combo = randrange(10, 350)
        self.difficulty = randrange(0, 30)
        self.length = 88
        self.stats = {'health': DOOR_STYLES[self.kind]['hp'], 'max health': DOOR_STYLES[self.kind]['hp']}
        self.protected = False
        self.orig_rot = 0
        temp_img = self.game.door_images[DOOR_STYLES[self.kind]['image']]
        if self.orientation in 'L':
            self.image_orig = temp_img
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.rect.x = x - 19
            self.rect.y = y
            self.wall = Obstacle(self.game, self.rect.x, self.rect.y, 20, self.length)
            self.wall.add(self.game.door_walls)
        elif self.orientation == 'R':
            self.image_orig = pg.transform.rotate(temp_img, 180)
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.rect.x = x - 10
            self.rect.y = y - self.length
            self.wall = Obstacle(self.game, self.rect.x, self.rect.y + self.length, 20, self.length)
            self.wall.add(self.game.door_walls)
            self.orig_rot = 180
        elif self.orientation == 'D':
            self.image_orig = pg.transform.rotate(temp_img, 90)
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y - 10
            self.wall = Obstacle(self.game, self.rect.x, self.rect.y, self.length, 20)
            self.wall.add(self.game.door_walls)
            self.orig_rot = 90
        elif self.orientation == 'U':
            self.image_orig = pg.transform.rotate(temp_img, -90)
            self.image = self.image_orig.copy()
            self.rect = self.image.get_rect()
            self.rect.x = x - self.length
            self.rect.y = y - 19
            self.wall = Obstacle(self.game, self.rect.x + self.length, self.rect.y, self.length, 20)
            self.wall.add(self.game.door_walls)
            self.orig_rot = -90
        self.last_move = 0
        self.rot = 0
        self.animate_speed = 10
        self.rotate_amount = 5
        self.open = False
        self.close = False
        self.opened = False
        self.hit_rect = self.wall.rect
        self.hit_rect.center = self.wall.rect.center
        self.sound_played = False
        self.inventory = {'locked': self.locked, 'combo': self.combo,'difficulty': self.difficulty}
        self.last_hit = 0
        self.living = True
        self.frame = 0
        self.pos = vec(self.hit_rect.centerx, self.hit_rect.centery)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        if self.open:
            now = pg.time.get_ticks()
            if now - self.last_move > self.animate_speed:
                self.animate_open()
                self.rotate_image()
                self.last_move = now

        if self.close:
            now = pg.time.get_ticks()
            if now - self.last_move > self.animate_speed:
                self.animate_close()
                self.rotate_image()
                self.last_move = now

        if not self.living:
            now = pg.time.get_ticks()
            if now - self.last_move > self.animate_speed:
                self.animate_death()
                self.last_move = now


    def rotate_image(self):
        new_image = pg.transform.rotate(self.image_orig, self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def animate_open(self):
        if not self.sound_played:
            self.game.effects_sounds['door open'].play()
            self.sound_played = True
        self.rot += self.rotate_amount
        if self.rot > 90:
            self.rot = 90
            self.open = False
            self.opened = True
            self.wall.kill()
            if self.orientation == 'L':
                self.wall = Obstacle(self.game, self.rect.x, self.rect.y, self.length, 20)
            elif self.orientation == 'D':
                self.wall = Obstacle(self.game, self.rect.x, self.rect.y + self.length, 20, self.length)
            elif self.orientation == 'R':
                self.wall = Obstacle(self.game, self.rect.x + self.length, self.rect.y, self.length, 20)
            elif self.orientation == 'U':
                self.wall = Obstacle(self.game, self.rect.x, self.rect.y, 20, self.length)
            self.hit_rect = self.wall.rect
            self.hit_rect.center = self.wall.rect.center
            self.sound_played = False

    def animate_close(self):
        self.rot -= self.rotate_amount
        if self.rot < 0:
            self.rot = 0
            self.close = False
            self.opened = False
            self.wall.kill()
            if self.orientation == 'L':
                self.wall = Obstacle(self.game, self.rect.x, self.rect.y, 20, self.length)
                self.wall.add(self.game.door_walls)
            elif self.orientation == 'D':
                self.wall = Obstacle(self.game, self.rect.x, self.rect.y, self.length, 20)
                self.wall.add(self.game.door_walls)
            elif self.orientation == 'R':
                self.wall = Obstacle(self.game, self.rect.x, self.rect.y + self.length, 20, self.length)
                self.wall.add(self.game.door_walls)
            elif self.orientation == 'U':
                self.wall = Obstacle(self.game, self.rect.x + self.length, self.rect.y, self.length, 20)
                self.wall.add(self.game.door_walls)
            self.hit_rect = self.wall.rect
            self.hit_rect.center = self.wall.rect.center
            self.game.effects_sounds['door close'].play()

    def animate_death(self):
        if len(self.game.door_break_images) > self.frame:
            temp_image = self.game.door_break_images[self.frame]
            self.frame += 1
            new_image = pg.transform.rotate(temp_image, self.rot + self.orig_rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
        else:
            self.wall.kill()
            self.kill()

    def gets_hit(self, damage, knockback = 0, rot = 0, dam_rate = DAMAGE_RATE):
        now = pg.time.get_ticks()
        if now - self.last_hit > dam_rate:
            self.last_hit = now
            self.stats['health'] -= damage
        if self.stats['health'] <= 0:
            if self.living:
                self.game.channel5.stop()
                self.game.channel5.play(self.game.effects_sounds['rocks'])
                self.animate_speed = 50
            self.living = False

class ElectricDoor(pg.sprite.Sprite): # Used for fires and other stationary animated sprites
    def __init__(self, game, x, y, w, h, locked = False):
        self._layer = BULLET_LAYER
        self.game = game
        self.image_list = self.game.electric_door_images
        self.groups = game.all_sprites, game.entryways, game.lights, game.electric_doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.animate_speed = 50
        self.game.group.add(self)
        if h > w:
            self.orientation = 'v'
            self.image = pg.transform.rotate(self.image_list[0], 90)
        else:
            self.orientation = 'h'
            self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.center = (x + w/2, y + h/2)
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center = self.center
        self.w = w
        self.h = h
        self.light_mask = pg.transform.scale(self.game.light_mask_images[4], (int(self.w + 90), int(self.h + 90)))
        self.light_mask_rect = self.light_mask.get_rect()
        self.light_mask_rect.center = self.rect.center
        self.frame = 0
        self.last_move = 0
        self.locked = locked
        self.combo = randrange(10, 350)
        self.difficulty = randrange(0, 30)
        self.length = 88
        self.stats = {'health': 100, 'max health': 100}
        self.protected = False
        self.open = False
        self.close = False
        self.opened = False
        self.inventory = {'locked': self.locked, 'combo': self.combo,'difficulty': self.difficulty}
        self.last_hit = 0
        self.living = True
        self.pos = vec(self.rect.centerx, self.rect.centery)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.damage = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_move > self.animate_speed:
            self.animate()
            self.last_move = now
            if self.orientation == 'v':
                self.image = pg.transform.rotate(self.image_list[self.frame], 90)
                self.rect = self.image.get_rect()
            else:
                self.image = self.image_list[self.frame]
            self.rect.center = self.center
            self.light_mask_rect.center = self.rect.center

        if self.open:
            now = pg.time.get_ticks()
            if now - self.last_move > self.animate_speed:
                self.animate_open()
                self.last_move = now

        if self.close:
            now = pg.time.get_ticks()
            if now - self.last_move > self.animate_speed:
                self.animate_close()
                self.last_move = now

    def animate(self):
        self.frame += 1
        if self.frame > len(self.image_list) - 1:
            self.frame = 0

    def animate_open(self):
        self.open = False
        self.opened = True

    def animate_close(self):
        self.close = False
        self.opened = False
        #self.game.effects_sounds['door close'].play()

    def gets_hit(self, damage, knockback = 0, rot = 0, dam_rate = DAMAGE_RATE, player = None):
        if not player:
            return
        elif 'plasma' in player.equipped[player.weapon_hand]:  #makes it so plasma weapons can kill electric doors.
            now = pg.time.get_ticks()
            if now - self.last_hit > dam_rate:
                self.last_hit = now
                self.stats['health'] -= damage
                self.game.channel5.stop()
                self.game.channel5.play(self.game.weapon_hit_sounds['plasma'][0])
            if self.stats['health'] <= 0:
                self.kill()


class Explosion(pg.sprite.Sprite):
    def __init__(self, game, target = None, knockback = 0, damage = 0, center = None, after_effect = None, sky = False):
        self.sky = sky
        if self.sky:
            self._layer = SKY_LAYER
        else:
            self._layer = BULLET_LAYER
        self.game = game
        self.groups = game.all_sprites, game.explosions, game.lights
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game.group.add(self)
        self.target = target
        self.center = center
        self.after_effect = after_effect
        self.damage = damage
        # Scales explosion's size based on damage
        self.scale = int(5 * damage)
        if self.scale > 600:
            self.scale = 600
        self.image_list = []
        if damage == 0:
            self.scale = 400
            self.image_list = self.game.explosion_images
        else:
            for image in self.game.explosion_images:
                new_img = pg.transform.scale(image, (self.scale, self.scale))
                self.image_list.append(new_img)
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.hit_rect = pg.Rect(0, 0, int(self.scale/2), int(self.scale/2))
        self.light_mask = pg.transform.scale(self.game.light_mask_images[2], (self.scale + 100, self.scale + 100))
        self.light_mask_rect = self.light_mask.get_rect()
        self.light_mask_rect.center = self.rect.center
        if self.target == None:
            self.rect.center = self.center
            if self.center == None:
                self.center = (0, 0)
        else:
            self.rect.center = self.target.pos
        self.hit_rect.center = self.rect.center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 40
        self.knockback = knockback

    def update(self):
        now = pg.time.get_ticks()
        if now -self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == 1:
                self.game.channel7.play(self.game.effects_sounds['fire blast'])
            if self.frame == len(self.image_list):
                if self.target == None:
                    if self.after_effect == 'fire':
                        Stationary_Animated(self.game, self.rect.center, 'fire', 1000, True, self.sky)
                    elif self.after_effect == 'shock':
                        Stationary_Animated(self.game, self.rect.center, 'shock', 333, False, self.sky)
                else:
                    if self.after_effect == 'fire':
                        Stationary_Animated(self.game, self.target.pos, 'fire', 1000, True, self.sky)
                    elif self.after_effect == 'shock':
                        Stationary_Animated(self.game, self.target.pos, 'shock', 333, False, self.sky)
                self.kill()
            else:
                center = self.rect.center
                self.image = self.image_list[self.frame]
                self.rect = self.image.get_rect()
                if self.target == None:
                    self.rect.center = self.center
                    self.hit_rect.center = self.rect.center
                    self.light_mask_rect.center = self.rect.center
                else:
                    self.rect.center = self.target.pos
                    self.hit_rect.center = self.rect.center
                    self.light_mask_rect.center = self.rect.center

class Fireball(pg.sprite.Sprite):
    def __init__(self, mother, game, pos, rot, damage, knockback = 2, lifetime = 1000, speed = 200, source_vel = 0, after_effect = None, enemy = False, sky = False):
        self.sky = sky
        if self.sky:
            self._layer = SKY_LAYER
        else:
            self._layer = MOB_LAYER
        self.mother = mother
        self.game = game
        self.enemy = enemy
        if self.enemy:
            self.groups = game.all_sprites, game.fireballs, game.enemy_fireballs, game.lights
        else:
            self.groups = game.all_sprites, game.fireballs, game.lights
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game.group.add(self)
        self.rot = rot
        self.image = pg.transform.rotate(self.game.fireball_images[0], self.rot + 90)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hit_rect = FIREBALL_HIT_RECT.copy()
        self.offset = vec(44, 0).rotate(-self.rot)
        self.hit_rect.center = vec(pos) + self.offset # A separate hitbox is used bexause the fireball is offset from the center of the image
        self.light_mask = pg.transform.scale(self.game.light_mask_images[1], FIREBALL_LIGHT_RADIUS)
        self.light_mask_rect = self.light_mask.get_rect()
        self.light_mask_rect.center = self.hit_rect.center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.spawn_time = pg.time.get_ticks()
        self.frame_rate = 40
        self.damage = damage
        self.after_effect = after_effect
        self.knockback = knockback
        self.pos = vec(pos)
        self.vel = vec(1, 0).rotate(-self.rot) * speed + source_vel
        self.lifetime = lifetime

    def animate(self):
        self.frame += 1
        if self.frame == 1:
            self.game.effects_sounds['fire blast'].play()
        if self.frame == len(self.game.fireball_images):
            self.frame = 0
        self.image = pg.transform.rotate(self.game.fireball_images[self.frame], self.rot + 90)

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        now = pg.time.get_ticks()
        if now -self.last_update > self.frame_rate:
            self.last_update = now
            self.animate()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.center = self.pos + self.offset
        self.light_mask_rect.center = self.hit_rect.center

        if pg.sprite.spritecollideany(self, self.game.walls_on_screen, fire_collide):
            self.explode()
        # Kills bullets of current and previous weapons
        if pg.time.get_ticks() - self.spawn_time > self.lifetime:
            self.explode()

    def explode(self, target = None):
        if target == None:
            pos = self.pos + self.offset
        else:
            pos = target.pos
        Explosion(self.game, target, 0.5, self.damage, pos, self.after_effect, self.sky)
        self.kill()

class FirePot(pg.sprite.Sprite):
    def __init__(self, game, center, number, elev = 2):
        self.groups = game.elevations, game.all_sprites, game.firepots
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.game.group.add(self)
        self.image = self.game.body_surface.copy()
        self.rect = pg.Rect(0, 0, 64, 64)
        self.hit_rect = self.rect
        self.rect.center = center
        self.center = center
        self.number = number
        self.hit = False
        self.lit = False
        self.lit_time = 0
        self.life_time = 8000
        self.elevation = elev
        self.orient = choice(['h', 'v'])

    def update(self):
        now = pg.time.get_ticks()
        if self.hit:
            self.hit = False
            if not self.lit:
                Stationary_Animated(self.game, self.center, 'fire', self.life_time)
                self.lit = True
                self.lit_time = now
                self.center = vec(self.rect.center)
                self.game.portal_combo += self.number
        if now - self.lit_time > self.life_time:
            self.lit = False
            self.game.portal_combo = self.game.portal_combo.replace(self.number, '')


class Spell_Animation(pg.sprite.Sprite):
    def __init__(self, game, kind, pos, rot, source_vel = None, damage = 0, knockback = 0, lifetime = 1000, speed = 0, after_effect = None, loop = False):
        self._layer = EFFECTS_LAYER
        self.game = game
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game.group.add(self)
        self.rot = rot
        self.kind = kind
        self.loop = loop
        if source_vel == None:
            source_vel = vec(0, 0)
        self.image_list = self.game.magic_animation_images[MAGIC[self.kind]['image']]
        self.image = self.image_list[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.hit_rect = self.rect
        self.hit_rect.center = self.rect.center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.spawn_time = pg.time.get_ticks()
        self.frame_rate = 40
        self.damage = damage
        self.after_effect = after_effect
        self.knockback = knockback
        self.pos = vec(pos)
        self.vel = vec(1, 0).rotate(-self.rot) * speed + source_vel
        self.lifetime = lifetime

    def animate(self):
        self.frame += 1
        if self.frame == len(self.image_list):
            self.frame = 0
            if not self.loop:
                self.explode()
        self.image = self.image_list[self.frame]

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        now = pg.time.get_ticks()
        if now -self.last_update > self.frame_rate:
            self.last_update = now
            self.animate()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.hit_rect.center = self.pos

        # Kills bullets of current and previous weapons
        if pg.time.get_ticks() - self.spawn_time > self.lifetime:
            self.explode()

    def explode(self):
        pos = self.pos
        #Explosion(self.game, None, 0.5, self.damage, pos, self.after_effect)
        self.kill()



class Portal(pg.sprite.Sprite):
    def __init__(self, game, obj_center, coordinate, location):
        self._layer = EFFECTS_LAYER
        self.coordinate = coordinate
        self.location = location
        self.game = game
        self.center = obj_center
        self.groups = game.all_sprites, game.portals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game.group.add(self)
        self.image_list = self.game.portal_images
        self.image = self.image_list[1].copy()
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        self.frame = 0
        self.animate_speed = 50
        self.last_move = 0
        self.spawn_time = pg.time.get_ticks()
        self.lifetime = 80000
        self.rot = 0

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_move > self.animate_speed:  # What animal does when you are close it.
            self.animate(self.image_list)
            self.last_move = now
            new_image = pg.transform.rotate(self.game.portal_images[self.frame], self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

        if self.lifetime:
            if now - self.spawn_time > self.lifetime:
                self.kill()

    def animate(self, images):
        self.frame += 1
        self.rot = (self.rot + 150 * self.game.dt) % 360
        if self.frame > len(images) - 1:
            self.frame = 0

class Breakable(pg.sprite.Sprite): # Used for fires and other stationary animated sprites
    def __init__(self, game, obj_center, w, h, name, map, fixed_rot = None, size = None):
        under = False
        if 'palm tree' in name:
            self._layer = EFFECTS_LAYER
        elif 'tree' in name:
            self._layer = ROOF_LAYER
        elif 'block' in name or name == 'dirt':
            for i in UNDERWORLD:
                if i in map:
                    under = True
            if under:
                self._layer = 0
            else:
                self._layer = WALL_LAYER
        else:
            self._layer = WALL_LAYER
        self.game = game
        self.w = w
        self.h = h
        self.map = map
        self.center = obj_center
        x = int(self.center.x - (w/2))
        y = int(self.center.y - (h/2))
        self.size = size
        self.name = name
        self.kind =  BREAKABLES[self.name]
        if 'tree' in self.name:
            if self.size == None:
                self.size = choice(['sm', 'md', 'lg'])
            self.image_list = self.game.tree_images[self.size + self.name]
        elif 'block' in self.name:
            if len(self.game.breakable_images[self.name]) > 1:
                self.image_list = self.game.breakable_images[self.name]
            else:
                self.image_list = []
                self.image_list.append(self.game.breakable_images[self.name][0])
                for i in range(0, 10):
                    # superimposes the crack images over the ore images.
                    if i < 5:
                        temp_image = self.game.breakable_images[self.name][0].copy()
                        temp_image.blit(self.game.breakable_images['crack'][i], (0, 0))
                        self.image_list.append(temp_image)
                    else:
                        self.image_list.append(self.game.breakable_images['crack'][i])
                self.game.breakable_images[self.name] = self.image_list
        else:
            self.image_list = self.game.breakable_images[self.name]
        self.scale_factor = 1

        self.groups = game.all_sprites, game.breakable
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game.group.add(self)
        # Image vars
        if 'block' in self.name:
            self.rot = 0
        elif self.name == 'dirt':
            self.rot = 0
        elif fixed_rot == None:
            self.rot = randrange(0, 360)
        else:
            self.rot = fixed_rot
        self.image = pg.transform.rotate(self.image_list[0].copy(), self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.center
        self.trunk = Obstacle(self.game, x, y, w, h)
        if self.name in VEIN_LIST: # Makes it so all rocks spawn at a jumpable height.
            hits = pg.sprite.spritecollide(self.trunk, self.game.elevations, False)
            if hits:
                self.trunk.kill()
                self.trunk = Elevation(self.game, x, y, w, h, hits[0].elevation + 2)
            else:
                self.trunk.kill()
                self.trunk = Elevation(self.game, x, y, w, h, 2)
        self.hit_rect = self.trunk.rect
        self.hit_rect.center = self.trunk.rect.center
        # Animation vars
        self.animate_speed = self.kind['animate speed']
        self.frame = 0
        self.last_hit = 0
        self.last_move = 0
        self.dead = False
        self.hit = False
        self.hits = 0
        self.right_hits = 0
        self.hit_weapon = None

        self.hit_sound = self.game.effects_sounds[self.kind['hit sound']]
        self.right_hit_sound = self.game.effects_sounds[self.kind['right weapon hit sound']]
        self.break_sound = self.game.effects_sounds[self.kind['break sound']]
        self.protected = self.kind['protected']
        self.damage = self.kind['damage']
        self.knockback = self.kind['knockback']
        self.hp = self.kind['health']
        self.items = self.kind['items']
        self.rare_items = self.kind['rare items']
        self.weapon_required = self.kind['weapon required']
        self.break_type = self.kind['break type']
        self.wobble = self.kind['wobble']
        self.min_drop = 0
        if 'min drop' in self.kind:
            self.min_drop = self.kind['min drop']
        self.random_drop_number = self.kind['random drop number']
        self.rect.center = self.trunk.rect.center

    def update(self):
        if self.hit and not self.dead:
            now = pg.time.get_ticks()
            if now - self.last_move > 80:
                self.hit = False
                if self.wobble: # Used for objects that rustle like bushes
                    self.animate_hit()
                    self.last_move = now
                    new_image = pg.transform.rotate(self.image_list[0], self.rot - randrange(-20, 20))
                    old_center = self.rect.center
                    self.image = new_image
                    self.rect = self.image.get_rect()
                    self.rect.center = self.trunk.rect.center = self.hit_rect.center = old_center
            if self.break_type == 'gradual':
                if self.hit_weapon in self.weapon_required:
                    self.frame = self.right_hits
                    if self.frame > len(self.image_list) - 2:
                        self.frame = 0
                    self.last_move = now
                    self.image = pg.transform.rotate(self.image_list[self.frame], self.rot)
                    self.rect.center = self.trunk.rect.center = self.hit_rect.center = self.center

        elif self.dead:
            now = pg.time.get_ticks()
            if now - self.last_move > self.animate_speed:
                self.animate_death(self.image_list)
                self.last_move = now
                self.image = pg.transform.rotate(self.image_list[self.frame], self.rot)
                self.rect.center = self.trunk.rect.center = self.hit_rect.center = self.center
        else:
            pass

    def animate_death(self, images):
        self.frame += 1
        if self.frame > len(images) - 2:
            self.remove_bush()

    def animate_hit(self):
        self.frame += 1
        if self.frame > 1:
            self.frame = 0
            self.image = pg.transform.rotate(self.image_list[0], self.rot)
            self.rect.center = self.trunk.rect.center = self.hit_rect.center = self.center

    def gets_hit(self, weapon_type, knockback = 0, rot = 0, dam_rate = DAMAGE_RATE):
        now = pg.time.get_ticks()
        if now - self.last_hit > dam_rate * 10:
            if not self.hit:
                if self.hp > 0:
                    if weapon_type in self.weapon_required:
                        self.right_hit_sound.play()
                    else:
                        self.hit_sound.play()
                else:
                    self.break_sound.play()
            self.hit = True
            self.hit_weapon = weapon_type
            self.last_hit = now
            self.hits += 1
            if weapon_type in self.weapon_required:
                self.hp -= 1
                self.right_hits += 1
            elif weapon_type == 'explosion':
                self.hp -= 1
                self.right_hits += 1
            elif weapon_type == 'tank':
                if ('block' not in self.name) and ('vein' not in self.name):
                    self.hp -= 1
                    self.right_hits += 1
            if self.hp < 1:
                self.dead = True

    def remove_bush(self):
        random_value = randrange(0, 100)  # random number in range [0.0,1.0)
        if 'tree' not in self.name:
            for thing in self.items:
                if self.random_drop_number:
                    drop_number = randrange(self.min_drop, self.items[thing])
                else:
                    drop_number = self.items[thing]
                for i in range(0, drop_number):
                    if thing in ANIMALS:
                        Animal(self.game, self.center.x, self.center.y, self.map, thing)
                    else:
                        for kind in ITEM_TYPE_LIST:
                            if thing in eval(kind.upper()):
                                rand_rot = randrange(0, 360)
                                Dropped_Item(self.game, self.center, kind, thing, rand_rot, True)
        else: # Wood drops for trees are based on size.
            for thing in self.items:
                drop_number = ceil(self.items[thing] * TREE_SIZES[self.size]/TREE_SIZES['lg'])
                for i in range(0, drop_number):
                    if thing in ANIMALS:
                        Animal(self.game, self.center.x, self.center.y, self.map, thing)
                    else:
                        for kind in ITEM_TYPE_LIST:
                            if thing in eval(kind.upper()):
                                rand_rot = randrange(0, 360)
                                Dropped_Item(self.game, self.center, kind, thing, rand_rot, True)

        if None not in self.rare_items:
            if random_value < 5: # Chance of getting a rare item
                random_item = choice(self.rare_items)
                if random_item in ANIMALS:
                    Animal(self.game, self.center.x, self.center.y, self.map, random_item)
                else:
                    Dropped_Item(self.game, self.center, 'items', random_item)
        self.trunk.kill()
        self.kill()


# The rest of these sprites are static sprites that are never updated: water, walls, etc.

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.obstacles, game.walls, game.all_static_sprites, game.barriers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        if self.rect.width > self.rect.height:
            self.orient = 'h'
        else:
            self.orient = 'v'

class Charger(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, amount = 4, rate = 2000):
        self.groups = game.chargers, game.all_static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.pos = vec(self.rect.center)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.energy = 1000
        self.last_charge = 0
        self.rate = rate
        self.amount = amount

    def charge(self, hit):
        player_dist = self.game.player.pos - self.pos
        player_dist = player_dist.length()
        now = pg.time.get_ticks()
        if now - self.last_charge > self.rate:
            self.last_charge = now
            if hit.possessing:
                if hit.possessing.race == 'mech_suit':
                    hit.possessing.add_health(self.amount)
            else:
                hit.add_health(self.amount)
                try:
                    hit.add_magica(self.amount)
                    hit.add_stamina(self.amount)
                except:
                    pass
            if player_dist < 700: # This part makes it so if something is on the charging pad the charging volume decreases as you walk away from it.
                volume = 150 / player_dist
                self.game.effects_sounds['charge'].set_volume(volume)
                self.game.effects_sounds['charge'].play()

class Inside(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.inside, game.all_static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class NoSpawn(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.nospawn, game.all_static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Elevation(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, elev, climb = False, kind = None):
        if climb:
            self.groups = game.elevations, game.all_static_sprites, game.climbs, game.barriers
        elif kind:
            self.groups = game.elevations, game.all_static_sprites, game.climbables_and_jumpables, game.barriers
        else:
            self.groups = game.elevations, game.all_static_sprites, game.barriers
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.elevation = elev
        self.climb = climb
        if kind == 'jumpable':
            set_elevation(self)
            self.elevation += 2
        if kind == 'climbable':
            set_elevation(self)
            self.elevation += 3
        if self.rect.width > self.rect.height:
            self.orient = 'h'
        else:
            self.orient = 'v'

class Water(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.water, game.obstacles, game.all_static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Shallows(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.shallows, game.obstacles, game.all_static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class LongGrass(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.long_grass, game.all_static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Lava(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.lava, game.obstacles, game.all_static_sprites, game.lights
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.damage = 10
        mask_width = int(w * 9/5) + 256
        mask_height = int(h * 9/5) + 256
        self.light_mask = pg.transform.scale(self.game.light_mask_images[4], (mask_width, mask_height))
        self.light_mask_rect = self.light_mask.get_rect()
        self.light_mask_rect.center = self.rect.center

class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, name):
        self.groups = game.doors, game.all_static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.map = self.name[:-5]
        locx = int(self.name[-4:-2])
        locy = int(self.name[-2:])
        self.loc = vec(locx, locy)
        self.map = self.map[4:] + '.tmx'

class Chest(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, name, elev = 2):
        self.groups = game.containers, game.chest_containers, game.elevations, game.all_static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name.replace('chest', '')
        self.kind = 'chest'
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect.x = x
        self.rect.y = y
        self.temp_inventory = self.game.chests[self.name] # Creates a temporary reference to the chest contents dictionary.
        self.inventory = copy.deepcopy(self.game.chests[self.name]) # Creates an independent copy of the chest contents to later use and replace 'random' entries with actual items.
        random_inventory_item(self, self.temp_inventory)
        CHESTS[self.name] = self.inventory
        self.locked = self.inventory['locked']
        self.elevation = 0
        set_elevation(self)
        self.elevation += elev
        if self.rect.width > self.rect.height:
            self.orient = 'h'
        else:
            self.orient = 'v'

class Work_Station(pg.sprite.Sprite): # Used for work benches, tanning racks, grinders, forges, enchanting tables, etc.
    def __init__(self, game, x, y, w, h, kind):
        self.groups = game.work_stations, game.all_static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.kind = kind
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.pos = vec(self.rect.centerx, self.rect.centery)

class Bed(pg.sprite.Sprite): # Used to rest in
    def __init__(self, game, x, y, w, h, name, elev = 2):
        self.groups = game.beds, game.all_static_sprites, game.elevations
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        if ' cost' in self.name:
            self.cost = int(self.name[-3:])
            self.name = 'bed'
        else:
            self.cost = 0
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.elevation = 0
        set_elevation(self)
        self.elevation += elev
        if self.rect.width > self.rect.height:
            self.orient = 'h'
        else:
            self.orient = 'v'

class Toilet(pg.sprite.Sprite): # Used to rest in
    def __init__(self, game, x, y, w, h, elev = 2):
        self.groups = game.toilets, game.all_static_sprites, game.elevations, game.climbs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.elevation = 0
        set_elevation(self)
        self.elevation += elev
        if self.rect.width > self.rect.height:
            self.orient = 'h'
        else:
            self.orient = 'v'

class Detector(pg.sprite.Sprite): # Used to rest in
    def __init__(self, game, x, y, w, h, name):
        self.groups = game.detectors, game.all_static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.name = name
        self.quest = 'None'
        self.item = None
        self.action = 'None'
        self.detected = False
        self.kill_item = False
        _, self.item, self.action, self.quest, self.kill_item = self.name.split('_')
        self.kill_item = eval(self.kill_item)
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def trigger(self, detectable):
        if not self.detected:
            if self.action != 'None':
                self.do_action(detectable)
            if self.quest != 'None':
                self.game.quests[self.quest]['completed'] = True
            self.detected = True

    def do_action(self, detectable):
        if self.action == 'changeKimmy':
            detectable.kind['dialogue'] = 'KIMMY_DLG2'
            detectable.kind['aggression'] = 'awp'
        if self.action == 'changeFelius':
            detectable.remove(self.game.companions)
            try:
                detectable.body.remove(self.game.companion_bodies)
            except:
                pass
            detectable.default_detect_radius = detectable.detect_radius = 250
            detectable.guard = False
            detectable.speed = detectable.walk_speed = 80
            detectable.run_speed = 100
            self.game.people['catrina']['dialogue'] = 'CATRINA_DLG2'

# This class generates random points for NPCs and animals to walk towards
class Target(pg.sprite.Sprite): # Used for fires and other stationary animated sprites
    def __init__(self, game, x = 0, y = 0):
        self._layer = WALL_LAYER
        self.game = game
        self.groups = game.all_static_sprites, game.random_targets
        self.rect_size = 60
        pg.sprite.Sprite.__init__(self, self.groups)
        if x == 0:
            x = randrange(200, self.game.map.width - 200)
            y = randrange(200, self.game.map.height - 200)
        self.rect = self.hit_rect = pg.Rect(x, y, self.rect_size, self.rect_size)
        self.pos = vec(self.rect.centerx, self.rect.centery)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.living = True

    def new_position(self, npc_loc):
        x = randrange(self.game.screen_width, self.game.map.width - self.game.screen_width)
        y = randrange(self.game.screen_width, self.game.map.height - self.game.screen_width)
        self.rect = self.hit_rect = pg.Rect(x, y, self.rect_size, self.rect_size)
        self.pos = vec(self.rect.centerx, self.rect.centery)

    def set_position(self, x, y):
        self.rect = self.hit_rect = pg.Rect(x - self.rect_size/2, y - self.rect_size/2, self.rect_size, self.rect_size)
        self.pos = vec(self.rect.centerx, self.rect.centery)

class AIPath(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, kind):
        self.groups = game.aipaths, game.all_static_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.kind = kind
        self.pos = vec(self.rect.centerx, self.rect.centery)