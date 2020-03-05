import pygame as pg
from sprites import Dropped_Item, toggle_equip, remove_nones, change_clothing, color_image
from random import uniform, choice, randint, random, randrange
from settings import *
from npcs import *
from quests import *
#from tilemap import collide_hit_rect
from os import path
import sys
from random import choice, shuffle
from collections import Counter
from glob import glob
from textwrap import wrap
import copy
from dialogue import *
import re
from npc_design import Npc_Info_Designer
from math import ceil
from sprites import Npc, Animal
from time import perf_counter

vec = pg.math.Vector2

#default_font = pg.font.match_font('arial') #python looks for closest match to arial on whatever computer
default_font = MENU_FONT

#def empty_dictionary(d):
#    for x in d:
#        if x not in ['race', 'gender']
#            d[x] = [None]

# This makes sure the player or any other sprite is not equipping items they don't have. Also makes sure players aren't equipping armor in mechsuits
def check_equip(sprite):
    for item_type in ITEM_TYPE_LIST:
        if sprite.equipped[item_type] not in sprite.inventory[item_type]:
            sprite.equipped[item_type] = None
        if item_type == 'weapons':
            if sprite.equipped['weapons2'] not in sprite.inventory[item_type]:
                sprite.equipped['weapons2'] = None
    if sprite.equipped['race'] in NO_CLOTHES_RACES:
        for item_type in ['hair', 'tops', 'bottoms', 'shoes', 'hats', 'gloves']:
            sprite.equipped[item_type] = None

class Draw_Text():
    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.game.screen.blit(text_surface, text_rect)

class Text(pg.sprite.Sprite):
    def __init__(self, mother, text, font_name, size, color, x, y, align="topleft", type = None):
        self.mother = mother
        self.type = type
        self.size = size
        self.groups = self.mother.menu_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        font = pg.font.Font(font_name, size)
        self.image = font.render(text, True, color)
        self.rect = self.image.get_rect(**{align: (x, y)})
        self.text = text

class Picture(pg.sprite.Sprite):
    def __init__(self, game, mother, item_image, x, y):
        self.game = game
        self.mother = mother
        self.groups = self.mother.menu_sprites, self.mother.item_pictures
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.transform.scale2x(item_image)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Menu():  # used as the parent class for other menus.
    def __init__(self, game, character = 'player'):
        self.game = game
        self.running = True
        self.menu_sprites = pg.sprite.Group()
        self.menu_heading_sprites = pg.sprite.Group()
        self.item_sprites = pg.sprite.Group()
        self.item_pictures = pg.sprite.Group()
        self.item_tags_sprites = pg.sprite.Group()  # Used to show things like if the item is equipped
        self.item_selected = False
        self.selected_item = None
        self.printable_stat_list = []
        # These items are changed for inherrited menus.
        self.exit_keys = [pg.K_e]  # The keys used to enter/exit the menu.
        self.action_keys = [pg.K_b, pg.K_x, pg.K_y]
        self.spacing = 20  # Spacing between headings
        self.heading_list = ['Heading1', 'Heading2']  # This is the list of headings
        self.warning_message = False

    def generate_headings(self):
        previous_rect_right = 0
        for i, heading in enumerate(self.heading_list):
            heading_sprite = Text(self, heading, default_font, 30, WHITE, previous_rect_right + self.spacing, 10, "topleft")
            if i == 0:
                self.selected_heading = heading_sprite
                self.item_type = heading.lower()
            previous_rect_right = heading_sprite.rect.right
            self.menu_heading_sprites.add(heading_sprite)

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key in self.exit_keys:
                    if self.game.in_load_menu:
                        if not self.no_save_selected:
                            self.clear_menu()
                            self.running = False
                    else:
                        self.clear_menu()
                        self.running = False
                if event.key == pg.K_ESCAPE:
                    self.game.quit()
                if event.key == self.action_keys[0]: # use/buy
                    if self.selected_item:
                        self.use_item()
                if event.key == self.action_keys[1]:  # drop/sell item
                    if self.selected_item:
                        self.drop_item()
                        self.clear_item_info()
                if event.key == self.action_keys[2]:  # place item
                    if self.selected_item:
                        self.place_item()
                        self.clear_item_info()
            if event.type == pg.MOUSEBUTTONDOWN:  # Clears off pictures and stats from previously clicked item when new item is clicked.
                self.warning_message = False
                self.mouse_click = pg.mouse.get_pressed()
                pos = pg.mouse.get_pos()
                if [s for s in self.menu_sprites if s.rect.collidepoint(pos)]:
                    self.game.effects_sounds['click'].play()
                self.printable_stat_list = []
                self.item_selected = False
                for picture in self.item_pictures:
                    picture.kill()
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                # get a list of all heading sprites that are under the mouse cursor
                self.clicked_sprites = [s for s in self.menu_sprites if s.rect.collidepoint(pos)]
                for heading in self.menu_heading_sprites:
                    if heading in self.clicked_sprites:
                        self.item_type = heading.text.lower()
                        self.selected_heading = heading
                        self.item_selected = False
                        self.selected_item = None
                        self.list_items()
                # Equips items
                for item in self.clicked_sprites:
                    if item in self.item_sprites:
                        self.selected_item = item
                        self.item_selected = True
                        self.display_item_info(item)
                        if self.mouse_click == (0, 0, 1):
                            self.right_equip(item)
                        # Equipping weapon in left hand
                        if self.mouse_click == (1, 0, 0):
                            self.left_equip(item)
                        self.list_items()

    def clear_menu(self):
        for item in self.item_sprites:
            item.kill()
        for item in self.item_tags_sprites:
            item.kill()

    def clear_item_info(self):
        for item in self.item_pictures:
            item.kill()
        self.selected_item = None
        self.clicked_sprites = []
        self.printable_stat_list = []

    def clear_pictures(self):
        for item in self.item_pictures:
            item.kill()

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.game.screen.blit(text_surface, text_rect)

    def draw(self):
        self.game.screen.fill(BLACK)
        list_rect = pg.Rect(10, 50, self.game.screen_width / 2 - 10, self.game.screen_height - 100)
        list_rect_fill = pg.Rect(20, 60, self.game.screen_width / 2 - 30, self.game.screen_height - 120)
        description_rect = pg.Rect(self.game.screen_width / 2 + 10, 50, self.game.screen_width / 2 - 20, self.game.screen_height - 100)
        description_rect_fill = pg.Rect(self.game.screen_width / 2 + 20, 60, self.game.screen_width / 2 - 40, self.game.screen_height - 120)
        pg.draw.rect(self.game.screen, WHITE, list_rect, 2)
        pg.draw.rect(self.game.screen, WHITE, description_rect, 2)
        pg.draw.rect(self.game.screen, BLACK, list_rect_fill)
        pg.draw.rect(self.game.screen, BLACK, description_rect_fill)
        if not self.selected_item == None:
            if self.item_selected:
                selected_rect = pg.Rect(self.selected_item.rect.x - 4, self.selected_item.rect.y, self.selected_item.rect.width + 8, self.selected_item.size + 2)
                pg.draw.rect(self.game.screen, YELLOW, selected_rect, 2)
        selected_heading_rect = pg.Rect(self.selected_heading.rect.x - 4, self.selected_heading.rect.y, self.selected_heading.rect.width + 8, self.selected_heading.size + 2)
        pg.draw.rect(self.game.screen, YELLOW, selected_heading_rect, 2)
        self.menu_sprites.draw(self.game.screen)
        if self.item_selected:
            for i, item_stat in enumerate(self.printable_stat_list):
                self.draw_text(item_stat, default_font, 20, WHITE, self.game.screen_width / 2 + 50, self.game.screen_height / 3 + 30 * i, "topleft")
        self.draw_text(str(self.game.player.inventory['gold']) + " gold in inventory.", default_font, 25, WHITE, 20, self.game.screen_height - 120, "topleft")
        self.draw_text("Armor Rating: " + str(self.game.player.stats['armor']) + "   Carry Weight: " + str(self.game.player.stats['weight']) + "  Max Carry Weight: " + str(self.game.player.stats['max weight']), default_font, 25, WHITE, 20, self.game.screen_height - 80, "topleft")
        self.draw_text("Right Click: Equip/Unequip   Left Click: Equip second weapon/View Item    B: use Items    X: drop selected item    E: Exit Menu   ESCAPE: quit game", default_font, 20, WHITE, 10, self.game.screen_height - 40, "topleft")
        if self.warning_message != "":
            self.draw_text(self.warning_message, default_font, 30, YELLOW, self.game.screen_width/2, self.game.screen_height/2, "topleft")
        pg.display.flip()

    def update(self):
        self.clear_item_info()
        self.generate_headings()
        self.list_items()
        self.running = True
        while self.running:
            self.game.clock.tick(30)
            self.events()
            self.draw()
        self.update_external_variables()

    def update_external_variables(self):
        self.game.in_menu = False
        self.game.beg = perf_counter() # resets the counter so dt doesn't get messed up.

    def use_item(self):
        pass

    def drop_item(self):
        pass

    def place_item(self):
        pass

    def right_equip(self, item):
        pass

    def left_equip(self, item):
        pass

    def list_items(self):
        pass

    def display_item_info(self, item):
        pass


class Character_Design_Menu(Menu):
    def __init__(self, game, character = 'player'):
        super().__init__(game)
        if character == 'player':
            self.character = self.game.player
        else:
            self.character = character
        self.exit_keys = [pg.K_e]  # The keys used to enter/exit the menu.
        self.heading_list = ['Gender', 'Race', 'Hair']  # This is the list of headings
        self.palette = None

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key in self.exit_keys:
                    self.clear_menu()
                    self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if [s for s in self.menu_sprites if s.rect.collidepoint(pos)]:
                    self.game.effects_sounds['click'].play()
                self.mouse_click = pg.mouse.get_pressed()
                self.printable_stat_list = []
                self.printable_stat_vals = []
                self.item_selected = False
                for picture in self.item_pictures:
                    picture.kill()
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                # get a list of all sprites that are under the mouse cursor
                self.clicked_sprites = [s for s in self.menu_sprites if s.rect.collidepoint(pos)]
                if self.palette in self.clicked_sprites:
                    if self.item_type == 'hair':
                        self.character.colors['hair'] = self.game.screen.get_at((pos[0], pos[1]))
                    if self.item_type == 'race':
                        self.character.colors['skin'] = self.game.screen.get_at((pos[0], pos[1]))
                for heading in self.menu_heading_sprites:
                    if heading in self.clicked_sprites:
                        self.item_type = heading.text.lower()
                        self.list_items()
                        self.selected_heading = heading
                        self.clear_pictures()
                for item in self.clicked_sprites:
                    if item in self.item_sprites:
                        self.selected_item = item
                        self.item_selected = True
                        self.display_item_info(item)
                        self.character.equipped[self.item_type] = item.text
                        self.list_items()
                # This if and else block sets up default inventory based on gender
                if self.character == self.game.player:
                    if self.character.equipped['gender'] == 'other':
                        self.character.inventory = copy.deepcopy(DEFAULT_INVENTORIES['female' + ' ' + self.character.equipped['race']])
                    else:
                        self.character.inventory = copy.deepcopy(DEFAULT_INVENTORIES[self.character.equipped['gender'] + ' ' + self.character.equipped['race']])
                    for kind in ITEM_TYPE_LIST:
                        if kind != 'hair':
                            self.character.equipped[kind] = self.character.inventory[kind][0]
                else:
                    if self.character.equipped['race'] in list(RACE.keys()):
                        temp_inventory = None
                        if self.character.equipped['gender'] == 'other':
                            temp_inventory = copy.deepcopy(DEFAULT_INVENTORIES['female' + ' ' + self.character.equipped['race']])
                        else:
                            temp_inventory = copy.deepcopy(DEFAULT_INVENTORIES[self.character.equipped['gender'] + ' ' + self.character.equipped['race']])
                        for kind in ITEM_TYPE_LIST:
                            if kind != 'hair':
                                self.character.equipped[kind] = temp_inventory[kind][0]
                # Makes sure you are not wearing hair that does not fit your race.
                if self.character.equipped['hair'] not in RACE_HAIR[self.character.equipped['race']]:
                    self.character.equipped['hair'] = None
                self.character.body.update_animations()  # Updates animations for newly equipped or removed weapons etc.
                character_image = self.character.body.body_surface
                character_preview = Picture(self.game, self, character_image, int(self.game.screen_width * (3 / 4)), self.game.screen_height - 200)


    def list_items(self):
        self.clear_menu()
        i = 0
        for item in self.character.inventory[self.item_type]:
            if (self.item_type == 'race') and ('dragon' in item):
                pass
            elif (self.item_type == 'hair') and (item in RACE_HAIR[self.character.equipped['race']]):
                item_name = Text(self, item, default_font, 20, WHITE, 50, 30 * i + 75, "topleft")
                self.item_sprites.add(item_name)
                i += 1
            elif self.item_type != 'hair':
                item_name = Text(self, item, default_font, 20, WHITE, 50, 30 * i + 75, "topleft")
                self.item_sprites.add(item_name)
                i += 1
            else:
                pass

    def display_item_info(self, item):
        if self.item_type != 'hair':
            image_path = "self.game." + self.item_type + "_images[" + self.item_type.upper() + "['" + item.text + "']['image']]"
            item_image = eval(image_path)
            picture = Picture(self.game, self, item_image, int(self.game.screen_width * (3/4)), 150)
        if self.item_type == 'race':
            # This part wraps the descriptions of the character races. So they are displayed in paragraph form.
            description = wrap(RACE[item.text]['description'], 80)
            for line in description:
                self.printable_stat_list.append(line)
                self.printable_stat_vals.append("")
            self.printable_stat_list.append(" ")
            self.printable_stat_vals.append(" ")
            stat_list = ['health', 'stamina', 'magica', 'max weight', 'strength', 'agility','healing', 'stamina regen', 'magica regen']

            for x in stat_list:
                stat = str(RACE[item.text]['start_stats'][x])
                self.printable_stat_list.append(x)
                self.printable_stat_vals.append(stat)
            self.printable_stat_list.append("armor ")
            self.printable_stat_vals.append(str(RACE[item.text]['armor']))


    def draw(self):
        self.game.screen.fill(BLACK)
        list_rect = pg.Rect(10, 50, self.game.screen_width / 2 - 10, self.game.screen_height - 100)
        list_rect_fill = pg.Rect(20, 60, self.game.screen_width / 2 - 30, self.game.screen_height - 120)
        description_rect = pg.Rect(self.game.screen_width / 2 + 10, 50, self.game.screen_width / 2 - 20, self.game.screen_height - 100)
        description_rect_fill = pg.Rect(self.game.screen_width / 2 + 20, 60, self.game.screen_width / 2 - 40, self.game.screen_height - 120)
        pg.draw.rect(self.game.screen, WHITE, list_rect, 2)
        pg.draw.rect(self.game.screen, WHITE, description_rect, 2)
        pg.draw.rect(self.game.screen, BLACK, list_rect_fill)
        pg.draw.rect(self.game.screen, BLACK, description_rect_fill)
        if self.item_type == 'hair':
            self.draw_text("Pick Your Hair Color:", default_font, 24, WHITE, int(self.game.screen_width * (3 / 4)) - 70, 90, "topleft")
            if self.palette:
                self.palette.kill()
            try:
                self.palette = Picture(self.game, self, self.game.color_swatch_images[HAIR_PALETE_IMAGES[self.character.equipped['race']]], int(self.game.screen_width * (3/ 4)), 300)
            except:
                self.palette = Picture(self.game, self, self.game.color_swatch_images[0], int(self.game.screen_width * (3 / 4)), 300)

        elif self.item_type == 'race':
            self.draw_text("Pick Your Skin Tone:", default_font, 24, WHITE, int(self.game.screen_width * (1 / 4) + 30), 90, "topleft")
            if self.palette:
                self.palette.kill()
            try:
                self.palette = Picture(self.game, self, self.game.color_swatch_images[PALETE_IMAGES[self.character.equipped['race']]], int(self.game.screen_width * (1 / 4) + 100), 300)
            except:
                self.palette = Picture(self.game, self, self.game.color_swatch_images[0], int(self.game.screen_width * (1 / 4) + 100), 300)

        if not self.selected_item == None:
            if self.item_selected:
                selected_rect = pg.Rect(self.selected_item.rect.x - 4, self.selected_item.rect.y, self.selected_item.rect.width + 8, self.selected_item.size + 2)
                pg.draw.rect(self.game.screen, YELLOW, selected_rect, 2)
        selected_heading_rect = pg.Rect(self.selected_heading.rect.x - 4, self.selected_heading.rect.y, self.selected_heading.rect.width + 8, self.selected_heading.size + 2)
        pg.draw.rect(self.game.screen, YELLOW, selected_heading_rect, 2)
        self.menu_sprites.draw(self.game.screen)
        if self.item_selected:
            for i, item_stat in enumerate(self.printable_stat_list):
                self.draw_text(item_stat, default_font, 20, WHITE, self.game.screen_width / 2 + 50, self.game.screen_height / 3 + 30 * i, "topleft")
                self.draw_text(self.printable_stat_vals[i], default_font, 20, WHITE, self.game.screen_width / 2 + 225, self.game.screen_height / 3 + 30 * i, "topleft")
        self.draw_text("Preview:", default_font, 20, WHITE, int(self.game.screen_width * (3 / 4)), self.game.screen_height - 350, "topleft")
        self.draw_text("Click to Choose Item. Press E when finished.", default_font, 20, WHITE, 10, self.game.screen_height - 40, "topleft")
        pg.display.flip()

    def update_external_variables(self):
        # This code calculates the player's armor rating
        self.character.inventory['hair'] = [self.character.equipped['hair']] # Removes all other hairstyles from inventory.
        for item in self.character.equipped:
            if self.character.equipped[item]:
                if '2' in item:
                    temp_item = item.replace('2', '')
                else:
                    temp_item = item
                if 'armor' in eval(temp_item.upper())[self.character.equipped[item]]:
                    self.character.stats['armor'] += eval(item.upper())[self.character.equipped[item]]['armor']
        self.character.calculate_weight()
        self.character.last_weapon = self.character.equipped['weapons']  # This string is used to keep track of what the player's last weapon was for equipping and unequipping toggling weapons and keeping track of bullets from old weapons
        self.character.current_weapon = self.character.equipped['weapons']  # weapon you had for autoequipping when your weapon is sheathed.
        self.character.last_weapon2 = self.character.equipped['weapons2']  # This string is used to keep track of what the player's last weapon was for equipping and unequipping toggling weapons and keeping track of bullets from old weapons
        self.character.current_weapon2 = self.character.equipped['weapons2']
        self.character.race = self.character.equipped['race']
        self.game.in_character_menu = False
        self.game.in_menu = False
        check_equip(self.character)
        self.character.human_body.update_animations()  # Updates animations for newly equipped or removed weapons etc.
        self.character.dragon_body.update_animations()
        if self.character.possessing:
            self.character.body.update_animations()
        self.character.pre_reload()
        self.character.stats = RACE[self.character.race]['start_stats'] # Gives player different stats based on selected race.
        if self.character.stats['max hunger'] == 1:
            self.character.hungers = False
        if 'wraith' in self.character.equipped['race'] :
            self.character.immaterial = True
        if self.character.immaterial or 'skeleton' in self.character.equipped['race']:
            self.character.magical_being = True
        if 'mechanima' in self.character.race:
            self.character.brightness = 400
            self.game.lights.add(self.character)
            self.character.light_mask_orig = pg.transform.scale(self.game.light_mask_images[2], (self.character.brightness, self.character.brightness))
            self.character.light_mask = self.character.light_mask_orig.copy()
            self.character.light_mask_rect = self.character.light_mask.get_rect()
        if self.character.equipped['race'] in ['skeleton', 'immortui', 'blackwraith', 'skeleton dragon', 'immortui dragon', 'blackwraith dragon']:
            self.character.aggression = 'awd'
        else:
            self.character.aggression = 'awp'
        self.game.beg = perf_counter()  # resets the counter so dt doesn't get messed up.

class Npc_Design_Menu(Character_Design_Menu):
    def __init__(self, game, character = 'player'):
        super().__init__(game, character)

    def display_item_info(self, item):
        if self.item_type != 'race':
            image_path = "self.game." + self.item_type + "_images[" + self.item_type.upper() + "['" + item.text + "']['image']]"
            itemdict = eval(self.item_type.upper())
            item_image = eval(image_path)
            if 'color' in itemdict[item.text]:
                item_image = color_image(item_image, itemdict[item.text]['color'])
            Picture(self.game, self, item_image, int(self.game.screen_width * (3 / 4)), 150)

    def update_external_variables(self):
        inv_menu = Inventory_Menu(self.game, self.character)
        inv_menu.update()
        self.save()
        self.game.in_npc_menu = False
        self.game.in_menu = False
        self.game.generic_npc.kill()

    def save(self):
        inv_list = ['weapons', 'weapons2', 'tops', 'bottoms', 'hats', 'hair', 'shoes', 'gloves', 'items', 'magic']
        temp_inv = {}
        for kind in inv_list:
            temp_list = []
            temp_list.append(self.character.equipped[kind])
            temp_inv[kind] = temp_list
        self.character.kind['inventory'] = temp_inv
        self.character.kind['inventory']['gold'] = 0
        self.character.kind['gender'] = self.character.equipped['gender']
        self.character.kind['race'] = self.character.equipped['race']
        tkinter_menu = Npc_Info_Designer(self, self.character)
        if self.character.kind['name'] != 'generic': # This makes it so it doesn't write unfinished NPCs
            if self.character.kind['name'] != "":
                file = open("npcs.py", "a")
                file.write("\n")
                file.write("PEOPLE[\'" + self.character.species + "\'] = " + str(self.character.kind))
                file.close()
        if not self.running:
            self.game.quit()
        else:
            self.update()

class Inventory_Menu(Menu): # Inventory Menu, also used as the parent class for other menus.
    def __init__(self, game, character = 'player'):
        super().__init__(game, character)
        if character == 'player':
            self.character = self.game.player
        else:
            self.character = character
        # These items are changed for inherrited menus.
        self.exit_keys = [pg.K_i, pg.K_e] # The keys used to enter/exit the menu.
        self.spacing = 20 # Spacing between headings
        self.heading_list = ['Weapons', 'Hats', 'Hair', 'Tops', 'Bottoms', 'Shoes', 'Gloves', 'Items', 'Magic'] # This is the list of headings

    def generate_headings(self):
        previous_rect_right = 0
        for i, heading in enumerate(self.heading_list):
            heading_sprite = Text(self, heading, default_font, 30, WHITE, previous_rect_right + self.spacing, 10, "topleft")
            if i == 0:
                self.selected_heading = heading_sprite
                self.item_type = heading.lower()
            previous_rect_right = heading_sprite.rect.right
            self.menu_heading_sprites.add(heading_sprite)

    def use_item(self):
        if self.item_type == 'items':
            for x in ['book', 'tome', 'letter']:
                if x in self.selected_item.text:
                    self.read_book()
            self.character.equipped['items'] = self.selected_item.text
            if self.character == self.game.player:
                self.warning_message = self.character.use_item()
            self.selected_item = None
            self.list_items()

    def read_book(self):
        self.letter = False
        if 'letter' in self.selected_item.text:
            self.book_image = self.game.open_letter_image
            self.letter = True
        else:
            self.book_image = self.game.open_book_image
        self.page = 0
        self.wrap_factor = int(ceil((self.game.screen_width / 2) / 19))
        self.number_of_lines = int(ceil((self.game.screen_height / 54)))
        self.book_font = eval(ITEMS[self.selected_item.text]['font'])
        if self.book_font == 'KAWTHI_FONT':
            self.heading_font = KAWTHI_FONT
        else:
            self.heading_font = HEADING_FONT
        self.book_heading = ITEMS[self.selected_item.text]['heading']
        self.book_author = ITEMS[self.selected_item.text]['author']
        spellwords = ITEMS[self.selected_item.text]['spell words']
        self.book_spellwords = wrap(spellwords, self.wrap_factor)
        if 'book:' in self.selected_item.text:
            book_file_name = self.selected_item.text.replace('book: ', '')
        else:
            book_file_name = self.selected_item.text
        with open(path.join(books_folder, book_file_name + '.txt'), 'r') as file:
            self.book_text = file.read()
        book_lines = self.book_text.split('\n')
        wrapped_lines = []
        for line in book_lines:
            wrapped_line = wrap(line, self.wrap_factor, replace_whitespace=False, drop_whitespace=False)
            wrapped_lines.extend(wrapped_line)

        self.book_data = [wrapped_lines[z:z + self.number_of_lines] for z in range(0, len(wrapped_lines), self.number_of_lines)]
        self.display_page()
        waiting = True
        while waiting:
            self.game.clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if pg.mouse.get_pressed() == (0, 0, 1):
                        self.page += 1
                        self.display_page()
                    elif pg.mouse.get_pressed() == (1, 0, 0):
                        if self.page == 0:
                            pass
                        elif not self.page <= 0:
                            self.page -= 2
                            self.game.effects_sounds['page turn'].play()
                        else:
                            self.game.effects_sounds['page turn'].play()
                        if self.page < 0:
                            self.page = 0
                        self.display_page()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_e:
                        waiting = False
                    elif event.key in [pg.K_SPACE, pg.K_RIGHT]:
                        self.page += 1
                        self.display_page()
                    elif event.key in [pg.K_BACKSPACE, pg.K_LEFT]:
                        if self.page == 0:
                            pass
                        elif not self.page <= 0:
                            self.page -= 2
                            self.game.effects_sounds['page turn'].play()
                        else:
                            self.game.effects_sounds['page turn'].play()
                        if self.page < 0:
                            self.page = 0
                        self.display_page()

    def display_page(self):
        self.game.screen.fill(BLACK)
        self.game.screen.blit(self.book_image, (0, 0))
        self.draw_text("Press SPACE to turn page or RIGHT and LEFT Arrow Keys, E to exit.", default_font, 20, WHITE, self.game.screen_width / 2, self.game.screen_height - 15, "center")
        font_size = 25
        byword = 'by'
        if self.book_font == WRITING_FONT:
            font_size = 35
            self.heading_font = WRITING_FONT
        if self.letter:
            byword = 'from'
        if self.page == 0:
            self.draw_text(self.book_heading, self.heading_font, 40, BLACK, self.game.screen_width * (3/4), self.game.screen_height * (1/5), "center")
            self.draw_text(byword, self.book_font, 28, BLACK, self.game.screen_width * (3/4), self.game.screen_height * (2/5), "center")
            self.draw_text(self.book_author, self.book_font, 28, BLACK, self.game.screen_width * (3/4), self.game.screen_height * (3/5), "center")
        else:
            if self.page > len(self.book_data):
                self.page -= 1
                return
            self.game.effects_sounds['page turn'].play()
            #lines = len(self.book_data[self.page])
            left_margin = 125
            top_margin = 45
            right_margin = self.game.screen_width/2 + 50
            j = 0
            for i, line in enumerate(self.book_data[self.page - 1]):
                self.draw_text(line, self.book_font, font_size, BLACK, left_margin, top_margin + (45 * i), "topleft")
                j += 1
            if self.page == len(self.book_data):
                for line in self.book_spellwords:
                    self.draw_text(line, KAWTHI_FONT, font_size, BLACK, left_margin, top_margin + (45 * j), "topleft")
                    j += 1
            self.page += 1
            if self.page > len(self.book_data):
                pg.display.flip()
                self.page -= 1
                return
            j = 0
            for i, line in enumerate(self.book_data[self.page - 1]):
                self.draw_text(line, self.book_font, font_size, BLACK, right_margin, top_margin + (45 * i), "topleft")
                j += 1
            if self.page == len(self.book_data):
                for line in self.book_spellwords:
                    self.draw_text(line, KAWTHI_FONT, font_size, BLACK, right_margin, top_margin + (45 * j), "topleft")
                    j += 1
        pg.display.flip()


    def drop_item(self):
        if self.item_type != 'magic':
            # Unequips item if you drop one you are equipping and don't have another one.
            number_of_each = 0
            for i, item in enumerate(self.character.inventory[self.item_type]):
                if item == self.selected_item.text:
                    number_of_each += 1
            if number_of_each == 1:
                if self.character.equipped[self.item_type] == self.selected_item.text:
                    self.character.equipped[self.item_type] = None
                elif self.character.equipped['weapons2'] == self.selected_item.text: # Unequips dropped secondary weapon.
                    self.character.equipped['weapons2'] = None
            # Removes dropped item from inventory
            for i, item in enumerate(self.character.inventory[self.item_type]):
                if item == self.selected_item.text:
                    dropped_item = Dropped_Item(self.game, self.character.pos + vec(randrange(-50, 50), randrange(-100, 100)), self.item_type, item)
                    self.character.inventory[self.item_type][i] = None
                    self.selected_item.text = 'None'  # Makes it so it doesn't drop more than one of the same item.
            remove_nones(self.character.inventory[self.item_type])
            self.list_items()

    def place_item(self):
        if self.item_type != 'magic':
            # Unequips item if you drop one you are equipping and don't have another one.
            number_of_each = 0
            for i, item in enumerate(self.character.inventory[self.item_type]):
                if item == self.selected_item.text:
                    number_of_each += 1
            if number_of_each == 1:
                if self.character.equipped[self.item_type] == self.selected_item.text:
                    self.character.equipped[self.item_type] = None
                elif self.character.equipped['weapons2'] == self.selected_item.text: # Unequips dropped secondary weapon.
                    self.character.equipped['weapons2'] = None
            # Removes dropped item from inventory
            for i, item in enumerate(self.character.inventory[self.item_type]):
                if item == self.selected_item.text:
                    dropped_item = Dropped_Item(self.game, self.character.pos + vec(50, 0).rotate(-self.character.rot), self.item_type, item, self.character.rot - 90)
                    self.character.inventory[self.item_type][i] = None
                    self.selected_item.text = 'None'  # Makes it so it doesn't drop more than one of the same item.
            remove_nones(self.character.inventory[self.item_type])
            self.list_items()

    def right_equip(self, item):
        if self.character.equipped[self.item_type] == item.text:  # Unequipping
            if self.item_type == 'weapons':
                self.character.last_weapon = item.text
            self.character.equipped[self.item_type] = None
        else:
            if self.item_type == 'weapons':  # Equipping
                if self.character.equipped['weapons2'] == item.text:
                    if self.character.inventory['weapons'].count(item.text) > 1:
                        self.character.last_weapon = self.character.equipped['weapons']  # Used to keep track of bullets fired from unequipped weapons
                        self.character.equipped[self.item_type] = item.text
                else:
                    self.character.last_weapon = self.character.equipped['weapons']  # Used to keep track of bullets fired from unequipped weapons
                    self.character.equipped[self.item_type] = item.text
            else:
                self.character.equipped[self.item_type] = item.text
        self.check_dual()

    def left_equip(self, item):
        if self.item_type == 'weapons':
            if self.character.equipped['weapons'] == item.text:
                if self.character.inventory['weapons'].count(item.text) > 1:
                    if self.character.equipped['weapons2'] == item.text:
                        self.character.last_weapon2 = item.text  # Used to keep track of bullets fired from unequipped weapons
                        self.character.equipped['weapons2'] = None
                    else:
                        self.character.last_weapon2 = self.character.equipped['weapons2']  # Used to keep track of bullets fired from unequipped weapons
                        self.character.equipped['weapons2'] = item.text
            else:
                if self.character.equipped['weapons2'] == item.text:
                    self.character.last_weapon2 = item.text  # Used to keep track of bullets fired from unequipped weapons
                    self.character.equipped['weapons2'] = None
                else:
                    self.character.last_weapon2 = self.character.equipped['weapons2']  # Used to keep track of bullets fired from unequipped weapons
                    self.character.equipped['weapons2'] = item.text
        self.check_dual()

    def check_dual(self):
        # This section prevents dual equipping with two handed weapons.
        dual_list = ['bow', 'rifle', 'shotgun', 'launcher']
        for kind in dual_list:
            if kind in str(self.character.equipped['weapons']):
                self.character.equipped['weapons2'] = None
            if kind in str(self.character.equipped['weapons2']):
                self.character.equipped['weapons'] = None

    def list_items(self):
        remove_nones(self.character.inventory[self.item_type]) # Makes sure to remove empty slots in inventory.
        self.clear_menu()
        self.counter = Counter(self.character.inventory[self.item_type])
        displayed_list = [] # Keeps track of which items have been displayed

        row = 0
        x_row = 50
        max_width = 0
        for item in self.character.inventory[self.item_type]:
            if item not in displayed_list:
                if 30 * row + 75 > (self.game.screen_height - 195):
                    row = 0
                    x_row += max_width + 10
                item_name = Text(self, item, default_font, 20, WHITE, x_row, 30 * row + 75, "topleft")
                self.item_sprites.add(item_name)
                if self.character.equipped[self.item_type] and self.character.equipped[self.item_type] == item:
                    if self.item_type == 'weapons':
                        equipped_text = Text(self, "(R)", default_font, 20, WHITE, item_name.rect.right + 25, 30 * row + 75, "topleft")
                        self.item_tags_sprites.add(equipped_text)
                    else:
                        equipped_text = Text(self, "(E)", default_font, 20, WHITE, item_name.rect.right + 25, 30 * row + 75, "topleft")
                        self.item_tags_sprites.add(equipped_text)
                if self.character.equipped['weapons2'] and self.character.equipped['weapons2'] == item:
                    left_equipped_text = Text(self, "(L)", default_font, 20, WHITE, item_name.rect.left - 32, 30 * row + 75, "topleft")
                    self.item_tags_sprites.add(left_equipped_text)
                if self.counter[item] > 1:
                    item_count = Text(self, str(self.counter[item]), default_font, 20, WHITE, item_name.rect.right + 10, 30 * row + 75, "topleft")
                    self.item_tags_sprites.add(item_count)
                if item_name.rect.right > max_width:
                    max_width = item_name.rect.right
                displayed_list.append(item)
                row += 1

        # Calculates the player's armor rating
        if self.character == self.game.player:
            self.character.stats['armor'] = 0
            for item in self.character.equipped:
                if self.character.equipped[item]:
                    if '2' in item:
                        temp_item = item.replace('2', '')
                    else:
                        temp_item = item
                    try:
                        if 'armor' in eval(temp_item.upper())[self.character.equipped[item]]:
                            self.character.stats['armor'] += eval(temp_item.upper())[self.character.equipped[item]]['armor']
                    except:
                        pass

            self.character.calculate_weight()

    def display_item_info(self, item):
        item_dictionary = globals()[self.item_type.upper()] #converts the item_type string into the correct dictionary to get the item stats from
        if self.item_type[-1:] == 's':
            image_path = "self.game." + self.item_type[:-1] + "_images[" + self.item_type.upper() + "['" + item.text + "']['image']]"
        else:
            image_path = "self.game." + self.item_type + "_images[" + self.item_type.upper() + "['" + item.text + "']['image']]"
        itemdict = eval(self.item_type.upper())
        item_image = eval(image_path)
        if 'color' in itemdict[item.text]:
            item_image = color_image(item_image, itemdict[item.text]['color'])
        Picture(self.game, self, item_image, int(self.game.screen_width * (3/4)), 150)

        for key in item_dictionary:
            if key == item.text:
                i = 0
                for stat in item_dictionary[key]:
                    if stat in ['image', 'offset', 'walk', 'grip']:
                        continue
                    else:
                        item_stats = ""
                        item_stats += (stat + " " + str(item_dictionary[key][stat]))
                        self.printable_stat_list.append(item_stats)
                        i += 1

    def update_external_variables(self):
        add_light = False
        light_reach = 1
        if self.character.equipped['weapons2'] in LIGHTS_LIST:
            self.character.lamp_hand = 'weapons2'
            self.character.brightness = WEAPONS[self.character.equipped['weapons2']]['brightness']
            self.character.mask_kind = WEAPONS[self.character.equipped['weapons2']]['light mask']
            if 'light reach' in WEAPONS[self.character.equipped['weapons2']]:
                light_reach = WEAPONS[self.character.equipped['weapons2']]['light reach']
            add_light = True
        elif self.character.equipped['weapons'] in LIGHTS_LIST:
            self.character.lamp_hand = 'weapons'
            self.character.brightness = WEAPONS[self.character.equipped['weapons']]['brightness']
            self.character.mask_kind = WEAPONS[self.character.equipped['weapons']]['light mask']
            if 'light reach' in WEAPONS[self.character.equipped['weapons']]:
                light_reach = WEAPONS[self.character.equipped['weapons']]['light reach']
            add_light = True
        if add_light:
            self.game.lights.add(self.character)
            self.character.light_mask_orig = pg.transform.scale(self.game.light_mask_images[self.character.mask_kind], (int(self.character.brightness * light_reach), self.character.brightness))
            self.character.light_mask = self.character.light_mask_orig.copy()
            self.character.light_mask_rect = self.character.light_mask.get_rect()
            if self.character.lamp_hand == 'weapons2':
                self.character.light_mask_rect.center = self.character.body.melee2_rect.center
            else:
                self.character.light_mask_rect.center = self.character.body.melee_rect.center
        else:
            if self.character.race != "mechanima":
                if self.character in self.game.lights:
                    self.game.lights.remove(self.character)
        if 'plasma' in self.character.equipped[self.character.lamp_hand] or 'elven' in self.character.equipped[self.character.lamp_hand]:
            self.character.light_on = True
        if 'Zhara Talisman' in self.game.player.inventory['items']: # Only lets you transform into a dragon if you have the Zhara Talisman
            self.game.player.transformable = True
        else:
            self.game.player.transformable = False
        if self.character.in_vehicle:
            if not self.character.vehicle.mountable:
                self.character.vehicle.reequip()
        self.game.player.bow = False
        if self.game.player.equipped['weapons']:
            if 'bow' in self.game.player.equipped['weapons']:
                self.game.player.bow = True
        if self.game.player.equipped['weapons2']:
            if 'bow' in self.game.player.equipped['weapons2']:
                self.game.player.bow = True
        self.game.in_inventory_menu = False
        self.game.in_menu = False
        self.character.current_weapon = self.character.equipped['weapons']
        self.character.current_weapon2 = self.character.equipped['weapons2']
        if self.character.swimming:
            if self.character.in_vehicle:
                if not self.character.vehicle.mountable:
                    self.character.vehicle.reequip()
            else:
                toggle_equip(self.character, True)
        check_equip(self.character)
        self.character.human_body.update_animations()  # Updates animations for newly equipped or removed weapons etc.
        self.character.dragon_body.update_animations()
        if self.character.possessing:
            self.character.body.update_animations()
        if self.character == self.game.player:
            self.character.calculate_fire_power()
            self.character.calculate_perks()
            # Reloads
            self.character.pre_reload()
        if self.character.equipped['race'] in ['skeleton', 'immortui', 'blackwraith', 'skeleton dragon', 'immortui dragon', 'blackwraith dragon']:
            self.character.aggression = 'awd'
        else:
            self.character.aggression = 'awp'
        self.game.beg = perf_counter() # resets the counter so dt doesn't get messed up.


    def draw(self):
        self.game.screen.fill(BLACK)
        list_rect = pg.Rect(10, 50, self.game.screen_width / 2 - 10, self.game.screen_height - 100)
        list_rect_fill = pg.Rect(20, 60, self.game.screen_width / 2 - 30, self.game.screen_height - 120)
        description_rect = pg.Rect(self.game.screen_width / 2 + 10, 50, self.game.screen_width / 2 - 20, self.game.screen_height - 100)
        description_rect_fill = pg.Rect(self.game.screen_width / 2 + 20, 60, self.game.screen_width / 2 - 40, self.game.screen_height - 120)
        pg.draw.rect(self.game.screen, WHITE, list_rect, 2)
        pg.draw.rect(self.game.screen, WHITE, description_rect, 2)
        pg.draw.rect(self.game.screen, BLACK, list_rect_fill)
        pg.draw.rect(self.game.screen, BLACK, description_rect_fill)
        # Used for NPC designing menu
        if self.character != self.game.player:
            self.clear_pictures()
            self.character.body.update_animations()  # Updates animations for newly equipped or removed weapons etc.
            character_image = self.character.body.body_surface
            character_preview = Picture(self.game, self, character_image, int(self.game.screen_width * (3 / 4)), self.game.screen_height - 200)
        if not self.selected_item == None:
            if self.item_selected:
                selected_rect = pg.Rect(self.selected_item.rect.x - 4, self.selected_item.rect.y, self.selected_item.rect.width + 8, self.selected_item.size + 2)
                pg.draw.rect(self.game.screen, YELLOW, selected_rect, 2)
        selected_heading_rect = pg.Rect(self.selected_heading.rect.x - 4, self.selected_heading.rect.y, self.selected_heading.rect.width + 8, self.selected_heading.size + 2)
        pg.draw.rect(self.game.screen, YELLOW, selected_heading_rect, 2)
        self.menu_sprites.draw(self.game.screen)
        if self.item_selected:
            for i, item_stat in enumerate(self.printable_stat_list):
                self.draw_text(item_stat, default_font, 20, WHITE, self.game.screen_width / 2 + 50, self.game.screen_height / 3 + 30 * i, "topleft")
        self.draw_text(str(self.character.inventory['gold']) + " gold in inventory.", default_font, 25, WHITE, 20, self.game.screen_height - 120, "topleft")
        if self.character == self.game.player:
            self.draw_text("Armor Rating: " + str(self.character.stats['armor']) + "   Carry Weight: " + str(self.character.stats['weight']) + "  Max Carry Weight: " + str(self.character.stats['max weight']), default_font, 25, WHITE, 20, self.game.screen_height - 80, "topleft")
        self.draw_text("Right Click: Equip/Unequip   Left Click: Equip second weapon/View Item   B: use Items   X: drop selected item  Y: place item  E: Exit Menu   ESC: quit game", default_font, 20, WHITE, 10, self.game.screen_height - 40, "topleft")
        if self.warning_message:
            self.draw_text(self.warning_message, default_font, 60, YELLOW, self.game.screen_width/2, self.game.screen_height/2, "center")
        pg.display.flip()


class Loot_Menu(Inventory_Menu):
    def __init__(self, game, container):
        super().__init__(game)
        # These items are changed for inherrited menus.
        self.loot_sprites = pg.sprite.Group()
        self.action_keys = [pg.K_a, pg.K_s]
        self.exit_keys = [pg.K_e]  # The keys used to enter/exit the menu.
        self.heading_list = ['Loot', 'Weapons', 'Hats', 'Hair', 'Tops', 'Bottoms', 'Shoes', 'Gloves', 'Items']  # This is the list of headings
        self.item_type = None
        self.container = container
        self.game.player.inventory['gold'] += self.container.inventory['gold']

    def generate_headings(self):
        previous_rect_right = 0
        for i, heading in enumerate(self.heading_list):
            heading_sprite = Text(self, heading, default_font, 30, WHITE, previous_rect_right + self.spacing, 10, "topleft")
            if i == 0:
                self.selected_heading = heading_sprite
                self.item_type = heading.lower()
            previous_rect_right = heading_sprite.rect.right
            self.menu_heading_sprites.add(heading_sprite)

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key in self.exit_keys:
                    self.clear_menu()
                    self.game.e_down = False
                    self.running = False
                if event.key == pg.K_ESCAPE:
                    self.game.quit()
                if event.key == self.action_keys[0]: # A key Takes all loot
                    for item_type in range(0, 8):
                        for item in self.container.inventory[ITEM_TYPE_LIST[item_type]]:
                            if item:
                                if self.game.player.equipped['gender'] == 'male':  # Makes it so looted clothes fit you based on gender.
                                    item = item.replace(' F', ' M')
                                else:
                                    item = item.replace(' M', ' F')
                                self.game.player.inventory[ITEM_TYPE_LIST[item_type]].append(item)
                                self.game.player.stats['looting'] += 1
                    self.game.player.calculate_weight()
                    # Removes items from inventory if you don't have room for them
                    if self.game.player.stats['weight'] > self.game.player.stats['max weight']:
                        for item_type in range(0, 8):
                            for i, item in enumerate(self.container.inventory[ITEM_TYPE_LIST[item_type]]):
                                if item:
                                    self.game.player.inventory[ITEM_TYPE_LIST[item_type]].remove(item)
                                    self.game.player.stats['looting'] -= 1
                        self.game.player.calculate_weight()

                    else:
                        for item in list(ITEM_TYPE_LIST):
                            self.container.inventory[item] = [None]
                        self.list_loot()

                if event.key == self.action_keys[1]: # S key Stores items in containers
                    if self.selected_heading.text != 'Loot':
                        if not self.selected_item == None:
                            # Unequips item if you store one you are equipping and don't have another one.
                            number_of_each = 0
                            for i, item in enumerate(self.game.player.inventory[self.item_type]):
                                if item == self.selected_item.text:
                                    number_of_each += 1
                            if number_of_each == 1:
                                if self.game.player.equipped[self.item_type] == self.selected_item.text:
                                    self.game.player.equipped[self.item_type] = None
                            # Stores item in container and removes from inventory
                            for i, item in enumerate(self.game.player.inventory[self.item_type]):
                                if item == self.selected_item.text:
                                    self.container.inventory[self.item_type].append(item)
                                    self.game.player.inventory[self.item_type][i] = None
                                    self.selected_item.text = 'None'

                            remove_nones(self.game.player.inventory[self.item_type])
                            self.list_items()
                    self.clear_item_info()

            if event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_click = pg.mouse.get_pressed()
                pos = pg.mouse.get_pos()
                if [s for s in self.menu_sprites if s.rect.collidepoint(pos)]:
                    self.game.effects_sounds['click'].play()
                self.printable_stat_list = []
                self.item_selected = False
                for picture in self.item_pictures:
                    picture.kill()
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                # get a list of all sprites that are under the mouse cursor
                self.clicked_sprites = [s for s in self.menu_sprites if s.rect.collidepoint(pos)]
                for heading in self.menu_heading_sprites:
                    if heading in self.clicked_sprites:
                        if heading.text != 'Loot':
                            self.item_type = heading.text.lower()
                            self.list_items()
                        else:
                            self.list_loot()
                        self.selected_heading = heading
                for item in self.clicked_sprites:
                    if item in self.item_sprites:
                        self.selected_item = item
                        self.item_selected = True
                        self.display_item_info(item)
                        if self.mouse_click == (0, 0, 1):
                            self.right_equip(item)
                        if self.mouse_click == (1, 0, 0):
                            self.left_equip(item)
                        self.list_items()
                    elif item in self.loot_sprites:
                        self.selected_item = item
                        self.item_selected = True
                        self.item_type = item.type
                        self.display_item_info(item)
                        if self.mouse_click == (0, 0, 1):
                            counter = Counter(self.container.inventory[self.item_type])
                            for x in range(0, counter[item.text]):
                                if self.game.player.equipped['gender'] == 'male':  # Makes it so looted clothes fit you based on gender.
                                    item.text = item.text.replace(' F', ' M')
                                else:
                                    item.text = item.text.replace(' M', ' F')
                                self.game.player.stats['looting'] += 1
                                self.game.player.inventory[self.item_type].append(item.text)
                                self.game.player.calculate_weight()
                                # Puts item back if you don't have room form it
                                if self.game.player.stats['weight'] > self.game.player.stats['max weight']:
                                    self.game.player.stats['looting'] -= 1
                                    self.game.player.inventory[self.item_type].remove(item.text)
                                else:
                                    for i, thing in enumerate(self.container.inventory[self.item_type]):
                                        if thing == self.selected_item.text:
                                            self.container.inventory[self.item_type][i] = None
                                    try:
                                        self.container.inventory[self.item_type].remove(None)
                                    except:
                                        pass
                        self.list_loot()

    def list_loot(self):
        if self.item_type != 'loot':
            remove_nones(self.game.player.inventory[self.item_type])  # Makes sure to remove empty slots in inventory.
        self.clear_menu()
        self.game.player.calculate_weight()
        displayed_list = [] # Keeps track of which items have been displayed
        row = 0
        for item_type in range(0, 8):
            loot_counter = Counter(self.container.inventory[ITEM_TYPE_LIST[item_type]])
            for item in self.container.inventory[ITEM_TYPE_LIST[item_type]]:
                    if item not in displayed_list:
                        if item:
                            item_name = Text(self, item, default_font, 20, WHITE, 50, 30 * row + 75, "topleft", ITEM_TYPE_LIST[item_type])
                            if loot_counter[item] > 1:
                                item_count = Text(self, str(loot_counter[item]), default_font, 20, WHITE, item_name.rect.right + 10, 30 * row + 75, "topleft")
                                self.item_tags_sprites.add(item_count)
                            row += 1
                            displayed_list.append(item)
                            self.loot_sprites.add(item_name)

    def clear_menu(self):
        super().clear_menu()
        for item in self.loot_sprites:
            item.kill()

    def update(self):
        self.clear_item_info()
        self.generate_headings()
        self.list_loot()
        self.running = True
        while self.running:
            self.game.clock.tick(30)
            self.events()
            self.draw()
        self.update_external_variables()

    def update_external_variables(self):
        if self.game.player.in_vehicle:
            if not self.game.player.vehicle.mountable:
                self.game.player.vehicle.reequip()
        self.game.in_loot_menu = False
        self.game.in_menu = False
        check_equip(self.game.player)
        self.game.player.human_body.update_animations()  # Updates animations for newly equipped or removed weapons etc.
        self.game.player.dragon_body.update_animations()
        self.game.player.current_weapon = self.game.player.equipped['weapons']
        self.game.player.current_weapon2 = self.game.player.equipped['weapons2']
        self.game.player.calculate_fire_power()
        self.game.player.calculate_perks()
        self.container.inventory['gold'] = 0
        if self.container in self.game.corpses:
            self.container.check_empty()
        self.game.beg = perf_counter() # resets the counter so dt doesn't get messed up.
        del self

    def draw(self):
        self.game.screen.fill(BLACK)
        list_rect = pg.Rect(10, 50, self.game.screen_width / 2 - 10, self.game.screen_height - 100)
        list_rect_fill = pg.Rect(20, 60, self.game.screen_width / 2 - 30, self.game.screen_height - 120)
        description_rect = pg.Rect(self.game.screen_width / 2 + 10, 50, self.game.screen_width / 2 - 20, self.game.screen_height - 100)
        description_rect_fill = pg.Rect(self.game.screen_width / 2 + 20, 60, self.game.screen_width / 2 - 40, self.game.screen_height - 120)
        pg.draw.rect(self.game.screen, WHITE, list_rect, 2)
        pg.draw.rect(self.game.screen, WHITE, description_rect, 2)
        pg.draw.rect(self.game.screen, BLACK, list_rect_fill)
        pg.draw.rect(self.game.screen, BLACK, description_rect_fill)
        if not self.selected_item == None:
            if self.item_selected:
                selected_rect = pg.Rect(self.selected_item.rect.x - 4, self.selected_item.rect.y, self.selected_item.rect.width + 8, self.selected_item.size + 2)
                pg.draw.rect(self.game.screen, YELLOW, selected_rect, 2)
        selected_heading_rect = pg.Rect(self.selected_heading.rect.x - 4, self.selected_heading.rect.y, self.selected_heading.rect.width + 8, self.selected_heading.size + 2)
        pg.draw.rect(self.game.screen, YELLOW, selected_heading_rect, 2)
        self.menu_sprites.draw(self.game.screen)
        if self.item_selected:
            for i, item_stat in enumerate(self.printable_stat_list):
                self.draw_text(item_stat, default_font, 20, WHITE, self.game.screen_width / 2 + 50, self.game.screen_height / 3 + 30 * i, "topleft")
        self.draw_text(str(self.container.inventory['gold']) + " gold added.", default_font, 25, WHITE, 20, self.game.screen_height - 160, "topleft")
        self.draw_text(str(self.game.player.inventory['gold']) + " gold in inventory.", default_font, 25, WHITE, 20, self.game.screen_height - 120, "topleft")
        self.draw_text("Armor Rating: " + str(self.game.player.stats['armor']) + "   Carry Weight: " + str(self.game.player.stats['weight']) + "  Max Carry Weight: " + str(self.game.player.stats['max weight']), default_font, 25, WHITE, 20, self.game.screen_height - 80, "topleft")
        self.draw_text("Right Click to Loot/Equip    A Take all   S: Store selected item   E: Exit menu    ESCAPE: Quit game", default_font, 20, WHITE, 10, self.game.screen_height - 40, "topleft")
        pg.display.flip()


class Lock_Menu():
    def __init__(self, game, lock):
        spacing = 20
        self.game = game
        self.lock = lock
        if self.lock.kind == 'chest':
            self.key_name = self.lock.name + ' chest key'
        else:
            self.key_name = self.lock.name + ' key'
        self.menu_sprites = pg.sprite.Group()
        self.keyway_sprite = pg.sprite.Group()
        self.running = True
        self.key_unlocked = False
        self.lock_radius = self.game.lock_image.get_width() / 2
        if not self.lock.inventory['locked']: # Guards against bugs that might trigger the lock menu for unlocked chests
            self.running = False
        if self.key_name in self.game.player.inventory['items']:
            self.key_unlocked = True
            self.lock.inventory['locked'] = False
            self.lock.locked = False
            self.game.effects_sounds['unlock'].play()
            self.game.player.stats['lock picking'] += 2
            self.keyway = Lock_Keyway(self.game, self, True)
            self.keyway.turn = True
            self.label_menu = Text(self, "It looks like you have the right key.", default_font, 30, WHITE, 30, 10, "topleft")
        elif self.game.player.inventory['items'] != [None] and [s for s in self.game.player.inventory['items'] if 'lock pick' in s]: # sees if you have a lock pick of any type in your inventory.
            self.keyway = Lock_Keyway(self.game, self)
            self.pick = Lock_Pick(self.game, self)
            self.label_menu = Text(self, "Pick Lock: Use W/S to move lock pick and SPACE to try to open the lock.", default_font, 30, WHITE, 30, 10, "topleft")
        else:
            self.label_menu = Text(self, 'You need a key or lock pick to open this lock!', default_font, 30, WHITE, 30, 100, "topleft")
        self.menu_sprites.add(self.label_menu)
        self.broken = False
        pg.mixer.music.stop() # Music is annoying while picking locks.

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game.quit()
                if event.key in [pg.K_e]:
                    self.game.e_down = False
                    self.running = False

    def update(self):
        self.running = True
        while self.running:
            self.game.clock.tick(30)
            try:
                if self.pick.alive():
                    self.pick.update()
            except:
                pass
            try:
                if self.keyway.alive():
                    self.keyway.update()
            except:
                pass
            self.events()
            self.draw()
        self.game.in_lock_menu = self.game.in_menu = False
        pg.mixer.music.play(loops=-1)
        self.game.beg = perf_counter() # resets the counter so dt doesn't get messed up.
        del self

    def draw(self):
        self.game.screen.fill(BLACK)
        self.game.screen.blit(self.game.lock_image, (self.game.screen_width/2 - self.lock_radius, self.game.screen_height/2 - self.lock_radius))
        self.keyway_sprite.draw(self.game.screen)
        self.menu_sprites.draw(self.game.screen)
        if self.key_unlocked:
            self.draw_text("You unlocked the lock with the key.", default_font, 60, WHITE, 120, int(self.game.screen_height * 3/4), "topleft")
        elif not self.lock.inventory['locked']:
            self.draw_text("You successfully picked the lock!", default_font, 60, WHITE, 120, int(self.game.screen_height * 3/4), "topleft")
        if self.broken:
            self.draw_text("You broke your lock pick!", default_font, 60, WHITE, 120, int(self.game.screen_height * 3/4), "topleft")
        self.draw_text("Right Click to Select Menu    E: Exit menu    ESCAPE: Quit game", default_font, 20, WHITE, 10, self.game.screen_height - 40, "topleft")
        pg.display.flip()

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.game.screen.blit(text_surface, text_rect)

class Lock_Pick(pg.sprite.Sprite):
    def __init__(self, game, mother):
        self.mother = mother
        self.groups = self.mother.menu_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.surface_width = 30
        self.surface_height = 600
        self.surface = pg.Surface((self.surface_width, self.surface_height)).convert()
        self.surface.fill(TRANSPARENT)
        self.surface.set_colorkey(TRANSPARENT)  # makes transparent
        self.image_orig = self.game.lock_pick_image
        #self.surface.blit(self.image_orig, (5, -100))
        self.image = self.surface
        self.rect = self.image.get_rect()
        self.rect.center = (self.game.screen_width/2, self.game.screen_height/2 + self.surface_height/2 + 3)
        self.old_center = self.rect.center
        self.pos = vec(0, self.rect.center[1])
        self.rot = 0
        self.rot_speed = 0
        self.combo = self.mother.lock.inventory['combo']
        self.difficulty = self.mother.lock.inventory['difficulty']
        self.move = False
        self.last_move = 0
        self.hp = 25
        self.toggle = 5
        self.y_offset = 0
        for item in self.game.player.inventory['items']: # Uses the first lockpick in the list.
            if 'lock pick' in item:
                self.selected_pick = item
                break

    def get_keys(self):
        self.rot_speed = 0
        self.move = False
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.rot_speed = -PLAYER_ROT_SPEED
            self.move = True
        if keys[pg.K_s]:
            self.rot_speed = PLAYER_ROT_SPEED
            self.move = True
        if keys[pg.K_SPACE]:
            self.toggle = -self.toggle
            self.pick()
        if self.move:
            now = pg.time.get_ticks()
            if now - self.last_move > self.game.effects_sounds['lock click'].get_length() * 1000:
                self.last_move = now
                if abs(self.rot - self.combo) <= self.difficulty:
                    self.game.effects_sounds['lock click'].play()
                else:
                    choice(self.game.lock_picking_sounds).play()

    def pick(self):
        self.pos.x += self.toggle
        self.y_offset += self.toggle
        if self.selected_pick == None:
            self.hp = -1
            self.mother.keyway.rot += self.toggle
            self.mother.broken = True
            choice(self.game.lock_picking_sounds).play()
            self.mother.keyway.kill()
            self.kill()
        working, self.selected_pick = self.game.player.change_used_item('items', self.selected_pick, True) # Makes it so the lock pick wears out.
        if working:
            if abs(self.rot - self.combo) <= self.difficulty:
                self.mother.keyway.turn = True
            else:
                self.hp -= 1
                self.mother.keyway.rot += self.toggle
                choice(self.game.lock_picking_sounds).play()
                if self.hp < 0:
                    self.game.player.inventory['items'].remove(self.selected_pick)
                    self.mother.broken = True
                    choice(self.game.lock_picking_sounds).play()
                    self.mother.keyway.kill()
                    self.kill()
        else:
            self.hp = -1
            self.mother.keyway.rot += self.toggle
            self.mother.broken = True
            choice(self.game.lock_picking_sounds).play()
            self.mother.keyway.kill()
            self.kill()


    def update(self):
        if self.mother.keyway.open:
            self.mother.lock.inventory['locked'] = False
            self.mother.lock.locked = False
            self.game.effects_sounds['unlock'].play()
            self.game.player.stats['lock picking'] += 20 / self.difficulty
            self.kill()
        self.get_keys()
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        y_disp = abs(self.rot - 180) + 160
        self.pos.y = self.old_center[1] + y_disp + self.y_offset
        self.surface.fill(BLACK)
        self.surface.set_colorkey(BLACK)  # makes transparent
        self.surface.blit(self.image_orig, (5, 70 -y_disp))
        self.image = self.surface
        self.rect = self.image.get_rect()
        pos =  (self.old_center) + vec(self.pos.x, 0)
        self.rect.center = pos


class Lock_Keyway(pg.sprite.Sprite):
    def __init__(self, game, mother, key = False):
        self.mother = mother
        self.groups = self.mother.keyway_sprite
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.keyway_radius = self.game.lock_keyway_image.get_width() / 2
        if key:
            self.image_orig = self.game.keyed_keyway_image
        else:
            self.image_orig = self.game.lock_keyway_image
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (self.game.screen_width/2 - 2, self.game.screen_height/2 + 17)
        self.rot = 0
        self.last_frame = 0
        self.turn = False
        self.open = False

    def animate(self):
        if self.rot > -90:
            self.rot -= 5
            if self.rot < -91:
                self.rot = -91
        else:
            self.open = True

    def update(self):
        now = pg.time.get_ticks()
        if self.turn:
            if now - self.last_frame > 1:
                self.last_fram = now
                self.animate()
        self.image = pg.transform.rotate(self.game.lock_pick_image, self.rot)
        new_image = pg.transform.rotate(self.image_orig, self.rot)
        old_center = self.rect.center
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center


class Load_Menu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.exit_keys = [pg.K_l, pg.K_e] # The keys used to enter/exit the menu.
        self.spacing = 40 # Spacing between headings
        self.heading_list = ['Saves'] # This is the list of headings
        self.previous_item = None
        self.no_save_selected = True

    def use_item(self):
        if self.selected_item:
            pass

    def drop_item(self):
        if not self.game.in_character_menu:
            if self.selected_item:
                pass

    def right_equip(self, item):
        keys = pg.key.get_pressed()
        if keys[pg.K_r]:
            self.game.update_old_save(path.join(saves_folder, item.text))
            print('save updated: quests/chests/npcs reset')
        else:
            self.game.load_save(path.join(saves_folder, item.text))
        self.running = False
        self.no_save_selected = False

    def left_equip(self, item):
        if self.previous_item:
            if item.text == self.previous_item.text:
                self.game.load_save(path.join(saves_folder, item.text))
                self.running = False
        self.previous_item = item

    def list_items(self):
        self.clear_menu()
        for i, filepath in enumerate(sorted(glob(path.join(saves_folder, "*.sav")), reverse = True)):
            save_name = Text(self, path.basename(filepath), default_font, 20, WHITE, 50, 30 * i + 75, "topleft")
            if self.selected_item == None:
                if i == 0:
                    self.selected_item = save_name
            self.item_sprites.add(save_name)

    def display_item_info(self, item):
        pass

    def update_external_variables(self):
        self.game.in_load_menu = False
        self.game.in_menu = False
        self.game.beg = perf_counter() # resets the counter so dt doesn't get messed up.

    def draw(self):
        self.game.screen.fill(BLACK)
        list_rect = pg.Rect(10, 50, self.game.screen_width / 2 - 10, self.game.screen_height - 100)
        list_rect_fill = pg.Rect(20, 60, self.game.screen_width / 2 - 30, self.game.screen_height - 120)
        description_rect = pg.Rect(self.game.screen_width / 2 + 10, 50, self.game.screen_width / 2 - 20, self.game.screen_height - 100)
        description_rect_fill = pg.Rect(self.game.screen_width / 2 + 20, 60, self.game.screen_width / 2 - 40, self.game.screen_height - 120)
        pg.draw.rect(self.game.screen, WHITE, list_rect, 2)
        pg.draw.rect(self.game.screen, WHITE, description_rect, 2)
        pg.draw.rect(self.game.screen, BLACK, list_rect_fill)
        pg.draw.rect(self.game.screen, BLACK, description_rect_fill)
        if not self.selected_item == None:
            if self.item_selected:
                selected_rect = pg.Rect(self.selected_item.rect.x - 4, self.selected_item.rect.y, self.selected_item.rect.width + 8, self.selected_item.size + 2)
                pg.draw.rect(self.game.screen, YELLOW, selected_rect, 2)
        selected_heading_rect = pg.Rect(self.selected_heading.rect.x - 4, self.selected_heading.rect.y, self.selected_heading.rect.width + 8, self.selected_heading.size + 2)
        pg.draw.rect(self.game.screen, YELLOW, selected_heading_rect, 2)
        self.menu_sprites.draw(self.game.screen)
        if self.item_selected:
            for i, item_stat in enumerate(self.printable_stat_list):
                self.draw_text(item_stat, default_font, 20, WHITE, self.game.screen_width / 2 + 50, self.game.screen_height / 3 + 30 * i, "topleft")
        self.draw_text("Left Click: Select Save    Right or Double Click: Load Save    ESCAPE: quit game", default_font, 20, WHITE, 10, self.game.screen_height - 40, "topleft")
        pg.display.flip()

class Stats_Menu(Draw_Text):
    def __init__(self, game):
        spacing = 20
        self.game = game
        self.menu_sprites = pg.sprite.Group()
        self.menu_heading_sprites = pg.sprite.Group()
        self.item_sprites = pg.sprite.Group()
        self.weapons_menu = Text(self, "Stats:", default_font, 30, WHITE, 30, 10, "topleft")
        self.menu_heading_sprites.add(self.weapons_menu)
        self.running = True

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game.quit()
                if event.key in [pg.K_e, pg.K_k]:
                    self.running = False

    def update(self):
        self.running = True
        while self.running:
            self.game.clock.tick(30)
            self.events()
            self.draw()
        self.game.in_stats_menu = self.game.in_menu = False
        self.game.beg = perf_counter() # resets the counter so dt doesn't get messed up.

    def draw(self):
        self.game.screen.fill(BLACK)
        list_rect = pg.Rect(10, 50, self.game.screen_width / 2 - 10, self.game.screen_height - 100)
        list_rect_fill = pg.Rect(20, 60, self.game.screen_width / 2 - 30, self.game.screen_height - 120)
        description_rect = pg.Rect(self.game.screen_width / 2 + 10, 50, self.game.screen_width / 2 - 20, self.game.screen_height - 100)
        description_rect_fill = pg.Rect(self.game.screen_width / 2 + 20, 60, self.game.screen_width / 2 - 40, self.game.screen_height - 120)
        pg.draw.rect(self.game.screen, WHITE, list_rect, 2)
        pg.draw.rect(self.game.screen, WHITE, description_rect, 2)
        pg.draw.rect(self.game.screen, BLACK, list_rect_fill)
        pg.draw.rect(self.game.screen, BLACK, description_rect_fill)
        self.menu_sprites.draw(self.game.screen)

        # Prints out player's stats
        for i, item in enumerate(self.game.player.stats):
            self.draw_text(item + ": " + str(round(self.game.player.stats[item], 2)), default_font, 30, WHITE, 20, 60 + (30 * i), "topleft")
        self.draw_text("Right Click to Select Menu  E or K to exit menu       ESCAPE: quit game", default_font, 20, WHITE, 10, self.game.screen_height - 40, "topleft")
        pg.display.flip()

class Work_Station_Menu(Menu): # Used for upgrading weapons
    def __init__(self, game, kind):
        super().__init__(game)
        # These items are changed for inherrited menus.
        self.exit_keys = [pg.K_i, pg.K_e]  # The keys used to enter/exit the menu.
        self.action_keys = [pg.K_f]
        self.spacing = 20  # Spacing between headings
        self.kind = kind
        if self.kind == 'forge':
            self.heading_list = ['Weapons', 'Hats', 'Tops', 'Bottoms', 'Shoes', 'Gloves', 'Items']  # This is the list of headings
        elif self.kind == 'smelter':
            self.heading_list = ['Items']  # This is the list of headings
        elif self.kind == 'tanning rack':
            self.heading_list = ['Items']  # This is the list of headings
        elif self.kind == 'workbench':
            self.heading_list = ['Hats', 'Tops', 'Bottoms', 'Shoes', 'Gloves']  # This is the list of headings
        elif self.kind == 'grinder':
            self.heading_list = ['Weapons']  # This is the list of headings
        elif self.kind == 'cooking fire':
            self.heading_list = ['Items']
        elif self.kind == 'alchemy lab':
            self.heading_list = ['Items']
        elif self.kind == 'enchanter':
            self.heading_list = ['Enchantments', 'Weapons', 'Hats', 'Tops', 'Bottoms', 'Shoes', 'Gloves']  # This is the list of headings
        elif self.kind == 'crafting':
            self.heading_list = ['Weapons', 'Hats', 'Tops', 'Bottoms', 'Shoes', 'Gloves', 'Items']
        self.clicked_sprites = []
        self.items_numbered = {}
        self.item_counter = Counter(self.game.player.inventory['items'])
        self.not_enough_text = False
        self.materials_list = {}
        self.item_type = self.heading_list[0].lower()
        self.selected_item = None
        self.selected_enchantment = None
        self.list_items()

    def generate_headings(self):
        previous_rect_right = 0
        for i, heading in enumerate(self.heading_list):
            heading_sprite = Text(self, heading, default_font, 30, WHITE, previous_rect_right + self.spacing, 10, "topleft")
            if i == 0:
                self.selected_heading = heading_sprite
                self.item_type = heading.lower()
            previous_rect_right = heading_sprite.rect.right
            self.menu_heading_sprites.add(heading_sprite)

    def forge_item(self):
        if self.item_type != 'enchantments':
            task_accomplished = False
            if self.kind == 'tanning rack':
                sound = 'scrape'
                for i, item in enumerate(self.game.player.inventory['items']):
                    if not task_accomplished:
                        if item:
                            if 'skin' in item:
                                self.game.player.inventory[self.item_type].append(self.selected_item.text)  # adds forged item to inventory
                                self.game.player.inventory['items'][i] = None
                                self.game.player.stats['smithing'] += 1
                                task_accomplished = True
                        else:
                            break
                if not task_accomplished:
                    self.not_enough_text = True

            elif self.kind == 'grinder':
                sound = 'grindstone'
                enough = self.check_materials(self.selected_item.text, True)
                if enough:
                    # Subtracts used materials from inventory
                    self.remove_materials()
                    # Upgrades item and adds it to the WEAPONS dictionary
                    upgraded_item = WEAPONS[self.selected_item.text].copy()
                    upgraded_item['melee damage'] += 1 + self.game.player.stats['smithing'] / 10
                    upgraded_item['damage'] += 1 + self.game.player.stats['smithing'] / 10
                    if 'value' in upgraded_item.keys():
                        upgraded_item['value'] += 1 + int(self.game.player.stats['smithing'] / UPGRADE_FACTOR)
                    new_item_name = self.rename_item()
                    UPGRADED_WEAPONS[new_item_name] = upgraded_item
                    WEAPONS[new_item_name] = upgraded_item
                    self.game.player.inventory[self.item_type].remove(self.selected_item.text) # removes non-upgraded item
                    self.game.player.inventory[self.item_type].append(new_item_name) # adds upgraded item to inventory
                    # Unequips old item and equips upgraded one if you were equipping it.
                    if self.game.player.equipped['weapons'] == self.selected_item.text:
                        self.game.player.equipped['weapons'] = new_item_name
                    if self.game.player.equipped['weapons2'] == self.selected_item.text:
                        self.game.player.equipped['weapons2'] = new_item_name
                    self.selected_item = None
                    self.game.player.stats['smithing'] += 1
                    task_accomplished = True
                else:
                    self.not_enough_text = True

            elif self.kind == 'forge':
                sound = 'anvil'
                enough = self.check_materials(self.selected_item.text)

                if enough:
                    # Subtracts used materials from inventory
                    self.remove_materials()
                    self.game.player.inventory[self.item_type].append(self.selected_item.text) # adds forged item to inventory
                    self.game.player.stats['smithing'] += 1
                    task_accomplished = True
                else:
                    self.not_enough_text = True

            elif self.kind == 'smelter':
                sound = 'fire blast'
                enough = self.check_materials(self.selected_item.text)

                if enough:
                    # Subtracts used materials from inventory
                    self.remove_materials()
                    self.game.player.inventory[self.item_type].append(self.selected_item.text) # adds forged item to inventory
                    self.game.player.stats['smithing'] += 1
                    task_accomplished = True
                else:
                    self.not_enough_text = True

            elif self.kind == 'workbench':
                sound = 'hammering'
                enough = self.check_materials(self.selected_item.text, True)
                if enough:
                    # Subtracts used materials from inventory
                    self.remove_materials()
                    # Upgrades item and adds it to the armor dictionary
                    upgraded_item = eval(self.item_type.upper())[self.selected_item.text].copy()
                    upgraded_item['armor'] += 1 + self.game.player.stats['smithing'] / 10
                    if 'value' in upgraded_item.keys():
                        upgraded_item['value'] += 1 + int(self.game.player.stats['smithing'] / UPGRADE_FACTOR)
                    new_item_name = self.rename_item()
                    if self.item_type == 'hats':
                        UPGRADED_HATS[new_item_name] = upgraded_item
                        HATS[new_item_name] = upgraded_item
                    elif self.item_type == 'tops':
                        UPGRADED_TOPS[new_item_name] = upgraded_item
                        TOPS[new_item_name] = upgraded_item
                    elif self.item_type == 'gloves':
                        UPGRADED_GLOVES[new_item_name] = upgraded_item
                        GLOVES[new_item_name] = upgraded_item
                    elif self.item_type == 'bottoms':
                        UPGRADED_BOTTOMS[new_item_name] = upgraded_item
                        BOTTOMS[new_item_name] = upgraded_item
                    elif self.item_type == 'shoes':
                        UPGRADED_SHOES[new_item_name] = upgraded_item
                        SHOES[new_item_name] = upgraded_item
                    self.game.player.inventory[self.item_type].remove(self.selected_item.text)  # removes non-upgraded item
                    self.game.player.inventory[self.item_type].append(new_item_name)  # adds upgraded item to inventory
                    # Unequips old item and equips upgraded one if you were equipping it.
                    if self.game.player.equipped[self.item_type] == self.selected_item.text:
                        self.game.player.equipped[self.item_type] = new_item_name
                    self.game.player.stats['smithing'] += 1
                    task_accomplished = True
                else:
                    self.not_enough_text = True

            elif self.kind == 'enchanter':
                casting_factor = int(self.game.player.stats['casting'] / 10) # This is how much your casting experience influences enchantment's potency
                sound = 'enchant'
                enough = self.check_materials(self.selected_enchantment)
                if enough:
                    # Subtracts used materials from inventory
                    self.remove_materials()
                    # Upgrades item and adds it to the armor dictionary
                    upgraded_item = eval(self.item_type.upper())[self.selected_item.text].copy()
                    if self.selected_enchantment == 'fire spark':
                        if upgraded_item['gun']:
                            upgraded_item['damage'] += self.game.player.stats['casting'] / 10
                            if 'value' in upgraded_item.keys():
                                upgraded_item['value'] += 1 + int(self.game.player.stats['casting'] / UPGRADE_FACTOR)
                            bullet = upgraded_item['bullet_size'][-1:]
                            size = upgraded_item['bullet_size'][:2]
                            if bullet == '1':
                                upgraded_item['bullet_size'] = size + '6'
                            elif bullet == '2':
                                upgraded_item['bullet_size'] = size + '9'
                            elif bullet == '3':
                                upgraded_item['bullet_count'] += 1
                            elif bullet == '4':
                                upgraded_item['bullet_size'] = size + '5'
                            else:
                                upgraded_item['bullet_size'] = 'md3'
                        else:
                            upgraded_item['bullet_speed'] = 200 + casting_factor
                            if upgraded_item['bullet_speed'] > 700:
                                upgraded_item['bullet_speed'] = 700
                            upgraded_item['bullet_lifetime'] = 400 + casting_factor * 5
                            if upgraded_item['bullet_lifetime'] > 2000:
                                upgraded_item['bullet_lifetime'] = 2000
                            upgraded_item['magazine size'] = 10 + casting_factor
                            upgraded_item['kickback'] = 0
                            upgraded_item['spread'] = 4
                            upgraded_item['damage'] = 1 + casting_factor
                            upgraded_item['bullet_size'] = 'lg3'
                            upgraded_item['bullet_count'] = 1
                            upgraded_item['offset'] = vec(38, 0)

                    elif self.selected_enchantment == 'electric spark':
                        if upgraded_item['gun']:
                            upgraded_item['damage'] += casting_factor
                            bullet = upgraded_item['bullet_size'][-1:]
                            size = upgraded_item['bullet_size'][:2]
                            if bullet == '1':
                                upgraded_item['bullet_size'] = size + '7'
                            elif bullet == '2':
                                upgraded_item['bullet_count'] += 1
                            elif bullet == '3':
                                upgraded_item['bullet_size'] = size + '9'
                            elif bullet == '4':
                                upgraded_item['bullet_size'] = size + '8'
                            else:
                                upgraded_item['bullet_size'] = 'lg2'

                        else:
                            upgraded_item['bullet_speed'] = 450 + casting_factor
                            if upgraded_item['bullet_speed'] > 700:
                                upgraded_item['bullet_speed'] = 700
                            upgraded_item['bullet_lifetime'] = 300 + casting_factor*5
                            if upgraded_item['bullet_lifetime'] > 2000:
                                upgraded_item['bullet_lifetime'] = 2000
                            upgraded_item['magazine size'] = 20 + casting_factor
                            upgraded_item['kickback'] = 0
                            upgraded_item['spread'] = 30
                            upgraded_item['damage'] = 1 + casting_factor
                            upgraded_item['bullet_size'] = 'lg2'
                            upgraded_item['bullet_count'] = 2 + int(casting_factor/10)
                            upgraded_item['offset'] = vec(38, 0)

                    elif self.selected_enchantment == 'explosive':
                        if upgraded_item['gun']:
                            upgraded_item['damage'] += casting_factor
                            bullet = upgraded_item['bullet_size'][-1:]
                            size = upgraded_item['bullet_size'][:2]
                            if bullet == '1':
                                upgraded_item['bullet_size'] = size + '10'
                            elif bullet == '2':
                                upgraded_item['bullet_size'] = size + 8
                            elif bullet == '3':
                                upgraded_item['bullet_size'] = size + '5'
                            elif bullet == '4':
                                upgraded_item['bullet_size'] = size + '10'
                                upgraded_item['bullet_count'] += 1
                            else:
                                upgraded_item['bullet_size'] = size + '10'
                        else:
                            upgraded_item['bullet_speed'] = 600 + casting_factor
                            if upgraded_item['bullet_speed'] > 700:
                                upgraded_item['bullet_speed'] = 700
                            upgraded_item['bullet_lifetime'] = 200 + casting_factor
                            if upgraded_item['bullet_lifetime'] > 2000:
                                upgraded_item['bullet_lifetime'] = 2000
                            upgraded_item['magazine size'] = 20 + casting_factor
                            upgraded_item['kickback'] = 0
                            upgraded_item['spread'] = 15
                            upgraded_item['damage'] = 1 + casting_factor
                            upgraded_item['bullet_size'] = 'md10'
                            upgraded_item['bullet_count'] = 1 + int(casting_factor / 10)
                            upgraded_item['offset'] = vec(38, 0)

                    elif self.selected_enchantment == 'dragon breath':
                        if 'fire enhance' not in upgraded_item.keys():
                            added_damage = 10 + casting_factor
                            if added_damage > 100:
                                added_damage = 100
                            reduced_rate = 100 + casting_factor
                            upgraded_item['fire enhance'] = {'after effect': 'fire', 'damage': added_damage, 'life time': 1000, 'speed': 50, 'rate reduction': reduced_rate}
                        else:
                            upgraded_item['fire enhance']['damage'] += added_damage

                    elif 'reinforced' in self.selected_enchantment:
                        reinforce_kind = self.selected_enchantment.replace('d', '')
                        if reinforce_kind not in upgraded_item.keys():
                            upgraded_item[reinforce_kind] = 10 + casting_factor
                        else:
                            upgraded_item[reinforce_kind] += 20

                    new_item_name = self.rename_item()
                    if self.item_type == 'weapons':
                        UPGRADED_WEAPONS[new_item_name] = upgraded_item
                        WEAPONS[new_item_name] = upgraded_item
                    if self.item_type == 'hats':
                        UPGRADED_HATS[new_item_name] = upgraded_item
                        HATS[new_item_name] = upgraded_item
                    elif self.item_type == 'tops':
                        UPGRADED_TOPS[new_item_name] = upgraded_item
                        TOPS[new_item_name] = upgraded_item
                    elif self.item_type == 'gloves':
                        UPGRADED_GLOVES[new_item_name] = upgraded_item
                        GLOVES[new_item_name] = upgraded_item
                    elif self.item_type == 'bottoms':
                        UPGRADED_BOTTOMS[new_item_name] = upgraded_item
                        BOTTOMS[new_item_name] = upgraded_item
                    elif self.item_type == 'shoes':
                        UPGRADED_SHOES[new_item_name] = upgraded_item
                        SHOES[new_item_name] = upgraded_item
                    self.game.player.inventory[self.item_type].remove(self.selected_item.text)  # removes non-upgraded item
                    self.game.player.inventory[self.item_type].append(new_item_name)  # adds upgraded item to inventory
                    # Unequips old item and equips upgraded one if you were equipping it.
                    if self.item_type == 'weapons':
                        if self.game.player.equipped['weapons'] == self.selected_item.text:
                            self.game.player.equipped['weapons'] = new_item_name
                        if self.game.player.equipped['weapons2'] == self.selected_item.text:
                            self.game.player.equipped['weapons2'] = new_item_name
                    elif self.game.player.equipped[self.item_type] == self.selected_item.text:
                        self.game.player.equipped[self.item_type] = new_item_name
                    self.game.player.stats['casting'] += 1
                    task_accomplished = True
                else:
                    self.not_enough_text = True

            elif self.kind == 'cooking fire':
                sound = 'fire blast'
                enough = self.check_materials(self.selected_item.text)

                if enough:
                    # Subtracts used materials from inventory
                    self.remove_materials()
                    self.game.player.inventory[self.item_type].append(self.selected_item.text) # adds forged item to inventory
                    task_accomplished = True
                else:
                    self.not_enough_text = True

            elif self.kind == 'alchemy lab':
                sound = 'alchemy'
                enough = self.check_materials(self.selected_item.text)

                if enough:
                    # Subtracts used materials from inventory
                    self.remove_materials()
                    self.game.player.inventory[self.item_type].append(self.selected_item.text) # adds forged item to inventory
                    task_accomplished = True
                else:
                    self.not_enough_text = True

            elif self.kind == 'crafting':
                sound = 'anvil'
                enough = self.check_materials(self.selected_item.text)

                if enough:
                    # Subtracts used materials from inventory
                    self.remove_materials()
                    self.game.player.inventory[self.item_type].append(self.selected_item.text) # adds forged item to inventory
                    task_accomplished = True
                else:
                    self.not_enough_text = True

            else:
                sound = 'anvil'
            if task_accomplished:
                remove_nones(self.game.player.inventory['items'])
                self.count_resources()
                self.game.effects_sounds[sound].play()
                self.game.player.calculate_weight()
                self.list_items()
        self.selected_enchantment = None
        self.selected_item = None

    def rename_item(self):
        new_item_name = self.selected_item.text
        if self.kind == 'enchanter':
            new_item_name = self.selected_enchantment + ' enchanted ' + self.selected_item.text + ' ELV' + str(self.game.player.stats['casting'])
        else:
            times_upgraded = 0
            if 'LV' in self.selected_item.text:
                times_upgraded = int(self.selected_item.text[-1:])
                new_item_name = self.selected_item.text.replace(' SLV', '')
                new_item_name = new_item_name.replace(' UP', '')
                new_item_name = re.sub(r'\d+', '', new_item_name)  # Removes numbers from the string
            times_upgraded += 1
            new_item_name = new_item_name + ' SLV' + str(self.game.player.stats['smithing']) + ' UP' + str(times_upgraded)
        return new_item_name

    def remove_materials(self):
        for material in self.materials_list:
            items_removed = 0
            for number, x in enumerate(self.game.player.inventory['items']):
                if x == material:
                    if items_removed < self.materials_list[material]:
                        self.game.player.inventory['items'][number] = None
                        items_removed += 1

    def check_materials(self, chosen_item, upgrade = False):
        if not upgrade:
            makeorupgrade = 'materials'
        else:
            makeorupgrade = 'upgrade'
        enough = True
        if 'aetherial' in chosen_item: # Only lets wraiths craft aetherial armor
            if 'wraith' not in self.game.player.equipped['race']:
                return False
        if 'elven' in chosen_item: # Only lets elves craft elven things
            if 'elf' not in self.game.player.equipped['race']:
                return False
        if 'mech' in chosen_item: # Only lets elves craft elven things
            if 'mechanima' not in self.game.player.equipped['race']:
                return False
        if 'dragon' in chosen_item: # Only lets dragons craft dragon things
            if 'dragon' not in self.game.player.equipped['race']:
                return False
        if self.kind == 'enchanter':
            self.materials_list = ENCHANTMENTS[chosen_item][makeorupgrade]
        else:
            self.materials_list = eval(self.item_type.upper())[chosen_item][makeorupgrade]
        for material in self.materials_list:
            if material in self.items_numbered:  # Sees if you have any of the required material
                if self.materials_list[material] > self.items_numbered[material]:  # Sees if you have enough of the required material
                    enough = False
            else:
                enough = False
        return enough


    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key in self.exit_keys:
                    self.clear_menu()
                    self.running = False
                if event.key == pg.K_ESCAPE:
                    self.game.quit()
                if event.key == self.action_keys[0]: # use/buy
                    if self.kind != 'enchanter':
                        if self.selected_item:
                            self.forge_item()
                    else:
                        if self.selected_item and self.selected_enchantment:
                            self.forge_item()

            if event.type == pg.MOUSEBUTTONDOWN:  # Clears off pictures and stats from previously clicked item when new item is clicked.
                self.not_enough_text = False # Clears of the warning text with next click
                self.mouse_click = pg.mouse.get_pressed()
                self.printable_stat_list = []
                self.item_selected = False
                for picture in self.item_pictures:
                    picture.kill()
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                # get a list of all sprites that are under the mouse cursor
                self.clicked_sprites = [s for s in self.menu_sprites if s.rect.collidepoint(pos)]
                for heading in self.menu_heading_sprites:
                    if heading in self.clicked_sprites:
                        self.item_type = heading.text.lower()
                        self.list_items()
                        self.selected_heading = heading

            for item in self.clicked_sprites:
                if item in self.item_sprites:
                    if self.item_type != 'enchantments':
                        self.selected_item = item
                    else:
                        self.selected_enchantment = item.text
                        self.selected_item = item
                    self.item_selected = True
                    self.display_item_info(item)
                    self.list_items()

    def list_items(self):
        self.clear_menu()
        if self.kind == 'forge':
            row = 0
            item_dict = eval(self.item_type.upper())
            for item in item_dict:
                if item:
                    if 'LV' not in item:    # no upgraded items show in forge
                        if ' M' in item:
                            if self.game.player.equipped['gender'] not in ['male']:
                                continue
                        elif ' F' in item:
                            if self.game.player.equipped['gender'] not in ['female', 'other']:
                                continue
                        if 'materials' in item_dict[item]:
                            if self.check_materials(item):
                                if self.item_type == 'items':
                                    if 'forgeable' in item_dict[item]:
                                        item_name = Text(self, item, default_font, 20, WHITE, 50, 30 * row + 75, "topleft")
                                        self.item_sprites.add(item_name)
                                        row += 1
                                else:
                                    item_name = Text(self, item, default_font, 20, WHITE, 50, 30 * row + 75, "topleft")
                                    self.item_sprites.add(item_name)
                                    row += 1

        elif self.kind == 'cooking fire':
            row = 0
            item_dict = eval(self.item_type.upper())
            for item in item_dict:
                if 'food' in item_dict[item]:
                    if item:
                        if 'materials' in item_dict[item]:
                            if self.check_materials(item):
                                item_name = Text(self, item, default_font, 20, WHITE, 50, 30 * row + 75, "topleft")
                                self.item_sprites.add(item_name)
                                row += 1

        elif self.kind == 'alchemy lab':
            row = 0
            item_dict = eval(self.item_type.upper())
            for item in item_dict:
                if 'alchemy' in ITEMS[item].keys():
                    if item:
                        if 'materials' in item_dict[item]:
                            if self.check_materials(item):
                                item_name = Text(self, item, default_font, 20, WHITE, 50, 30 * row + 75, "topleft")
                                self.item_sprites.add(item_name)
                                row += 1

        elif self.kind == 'crafting':
            row = 0
            item_dict = eval(self.item_type.upper())
            for item in item_dict:
                if item:
                    if 'LV' not in item:    # no upgraded items show in crafting
                        if 'materials' in item_dict[item]:
                            if self.check_materials(item):
                                if 'craftable' in item_dict[item]:
                                    item_name = Text(self, item, default_font, 20, WHITE, 50, 30 * row + 75, "topleft")
                                    self.item_sprites.add(item_name)
                                    row += 1

        elif self.kind == 'smelter':
            row = 0
            item_dict = eval(self.item_type.upper())
            for item in item_dict:
                if 'ingot' in item:
                    if item:
                        if 'materials' in item_dict[item]:
                            if self.check_materials(item):
                                item_name = Text(self, item, default_font, 20, WHITE, 50, 30 * row + 75, "topleft")
                                self.item_sprites.add(item_name)
                                row += 1

        elif self.kind == 'tanning rack':
            tan_list = ['leather', 'leather strips']
            row = 0
            for item in tan_list:
                item_name = Text(self, item, default_font, 20, WHITE, 50, 30 * row + 75, "topleft")
                self.item_sprites.add(item_name)
                row += 1

        elif self.kind == 'enchanter':
            row = 0
            for item in eval(self.item_type.upper()):
                if item:
                    if self.item_type == 'enchantments':  # Only lists enchantments you have materials to perform.
                        if 'materials' in ENCHANTMENTS[item]:
                            if self.check_materials(item):
                                item_name = Text(self, item, default_font, 20, WHITE, 50, 30 * row + 75, "topleft")
                                self.item_sprites.add(item_name)
                                row += 1
                    # Only shows items that you can enchant with selected enchantment
                    else:
                        self.clear_menu()
                        self.counter = Counter(self.game.player.inventory[self.item_type])
                        displayed_list = []  # Keeps track of which items have been displayed

                        row = 0
                        for item in self.game.player.inventory[self.item_type]:
                            if item not in displayed_list:
                                if item and self.selected_enchantment:
                                    if self.item_type in ENCHANTMENTS[self.selected_enchantment]['equip kind']:
                                        if 'enchanted' not in item:  # Only shows items that are not enchanted already
                                            item_name = Text(self, item, default_font, 20, WHITE, 50, 30 * row + 75, "topleft")
                                            self.item_sprites.add(item_name)
                                            if self.game.player.equipped[self.item_type] and self.game.player.equipped[self.item_type] == item:
                                                equipped_text = Text(self, "(Equipped)", default_font, 20, WHITE, item_name.rect.right + 25, 30 * row + 75, "topleft")
                                                self.item_tags_sprites.add(equipped_text)
                                            elif self.game.player.equipped['weapons2'] and self.game.player.equipped['weapons2'] == item:
                                                equipped_text = Text(self, "(Equipped Left)", default_font, 20, WHITE, item_name.rect.right + 25, 30 * row + 75, "topleft")
                                                self.item_tags_sprites.add(equipped_text)
                                            if self.counter[item] > 1:
                                                item_count = Text(self, str(self.counter[item]), default_font, 20, WHITE, item_name.rect.right + 10, 30 * row + 75, "topleft")
                                                self.item_tags_sprites.add(item_count)
                                            displayed_list.append(item)
                                            row += 1

        else:
            self.counter = Counter(self.game.player.inventory[self.item_type])
            displayed_list = []  # Keeps track of which items have been displayed

            row = 0
            for item in self.game.player.inventory[self.item_type]:
                if item not in displayed_list:
                    if item:
                        if item[-1:] != '4':
                            if 'upgrade' in eval(self.item_type.upper())[item]:
                                if self.check_materials(item, True):
                                    item_name = Text(self, item, default_font, 20, WHITE, 50, 30 * row + 75, "topleft")
                                    self.item_sprites.add(item_name)
                                    if self.game.player.equipped[self.item_type] and self.game.player.equipped[self.item_type] == item:
                                        equipped_text = Text(self, "(Equipped)", default_font, 20, WHITE, item_name.rect.right + 25, 30 * row + 75, "topleft")
                                        self.item_tags_sprites.add(equipped_text)
                                    elif self.game.player.equipped['weapons2'] and self.game.player.equipped['weapons2'] == item:
                                        equipped_text = Text(self, "(Equipped Left)", default_font, 20, WHITE, item_name.rect.right + 25, 30 * row + 75, "topleft")
                                        self.item_tags_sprites.add(equipped_text)
                                    if self.counter[item] > 1:
                                        item_count = Text(self, str(self.counter[item]), default_font, 20, WHITE, item_name.rect.right + 10, 30 * row + 75, "topleft")
                                        self.item_tags_sprites.add(item_count)
                                    displayed_list.append(item)
                                    row += 1

        # Calculates the player's armor rating
        self.game.player.stats['armor'] = 0
        for item in self.game.player.equipped:
            if self.game.player.equipped[item]:
                if '2' in item:
                    temp_item = item.replace('2', '')
                else:
                    temp_item = item
                if 'armor' in eval(temp_item.upper())[self.game.player.equipped[item]]:
                    self.game.player.stats['armor'] += eval(temp_item.upper())[self.game.player.equipped[item]]['armor']

        self.count_resources()

        self.game.player.calculate_weight()

    def count_resources(self):
        # This block creates a dictionary which includes each type of item in the player's item inventory and how many of each. Used to determine if the player has enough resources to forge.
        self.item_counter = Counter(self.game.player.inventory['items'])
        self.items_numbered = {}
        for item in self.game.player.inventory['items']:
            if item not in self.items_numbered:
                self.items_numbered[item] = self.item_counter[item]

    def display_item_info(self, item):
        item_dictionary = globals()[self.item_type.upper()]  # converts the item_type string into the correct dictionary to get the item stats from
        if self.item_type[-1:] == 's':
            image_path = "self.game." + self.item_type[:-1] + "_images[" + self.item_type.upper() + "['" + item.text + "']['image']]"
        else:
            image_path = "self.game." + self.item_type + "_images[" + self.item_type.upper() + "['" + item.text + "']['image']]"
        itemdict = eval(self.item_type.upper())
        item_image = eval(image_path)
        if 'color' in itemdict[item.text]:
            item_image = color_image(item_image, itemdict[item.text]['color'])
        Picture(self.game, self, item_image, int(self.game.screen_width * (3 / 4)), 150)

        for key in item_dictionary:
            if key == item.text:
                i = 0
                for stat in item_dictionary[key]:
                    if stat in ['image', 'offset', 'walk', 'grip']:
                        continue
                    else:
                        item_stats = ""
                        item_stats += (stat + " " + str(item_dictionary[key][stat]))
                        self.printable_stat_list.append(item_stats)
                        i += 1

    def update_external_variables(self):
        self.game.in_station_menu = False
        self.game.in_menu = False
        self.game.player.current_weapon = self.game.player.equipped['weapons']
        self.game.player.current_weapon2 = self.game.player.equipped['weapons2']
        if self.game.player.swimming:
            toggle_equip(self.game.player, True)
        check_equip(self.game.player)
        self.game.player.human_body.update_animations()  # Updates animations for newly equipped or removed weapons etc.
        self.game.player.dragon_body.update_animations()
        if self.game.player.possessing:
            self.game.player.body.update_animations()
        self.game.player.calculate_fire_power()
        self.game.player.calculate_perks()
        # Reloads
        self.game.player.pre_reload()
        self.game.beg = perf_counter() # resets the counter so dt doesn't get messed up.

    def draw(self):
        self.game.screen.fill(BLACK)
        list_rect = pg.Rect(10, 50, self.game.screen_width / 2 - 10, self.game.screen_height - 100)
        list_rect_fill = pg.Rect(20, 60, self.game.screen_width / 2 - 30, self.game.screen_height - 120)
        description_rect = pg.Rect(self.game.screen_width / 2 + 10, 50, self.game.screen_width / 2 - 20, self.game.screen_height - 100)
        description_rect_fill = pg.Rect(self.game.screen_width / 2 + 20, 60, self.game.screen_width / 2 - 40, self.game.screen_height - 120)
        pg.draw.rect(self.game.screen, WHITE, list_rect, 2)
        pg.draw.rect(self.game.screen, WHITE, description_rect, 2)
        pg.draw.rect(self.game.screen, BLACK, list_rect_fill)
        pg.draw.rect(self.game.screen, BLACK, description_rect_fill)
        if not self.selected_item == None:
            if self.item_selected:
                selected_rect = pg.Rect(self.selected_item.rect.x - 4, self.selected_item.rect.y, self.selected_item.rect.width + 8, self.selected_item.size + 2)
                pg.draw.rect(self.game.screen, YELLOW, selected_rect, 2)

        selected_heading_rect = pg.Rect(self.selected_heading.rect.x - 4, self.selected_heading.rect.y, self.selected_heading.rect.width + 8, self.selected_heading.size + 2)
        pg.draw.rect(self.game.screen, YELLOW, selected_heading_rect, 2)
        self.menu_sprites.draw(self.game.screen)
        if self.item_selected:
            for i, item_stat in enumerate(self.printable_stat_list):
                self.draw_text(item_stat, default_font, 20, WHITE, self.game.screen_width / 2 + 50, self.game.screen_height / 3 + 30 * i, "topleft")

        previous_line_location = 0
        for x in FORGEITEMS:
            if x in self.items_numbered:
                self.draw_text(x + " " + str(self.items_numbered[x]), default_font, 14, WHITE, 30 + previous_line_location, self.game.screen_height - 120, "topleft")
                previous_line_location += (len(x) * 10)

        if self.kind == 'enchanter' and self.selected_enchantment:
            self.draw_text(self.selected_enchantment.capitalize() + ' enchantment selected.', default_font, 30, WHITE, 50, self.game.screen_height - 170, "topleft")
        self.draw_text("Armor Rating: " + str(self.game.player.stats['armor']) + "   Carry Weight: " + str(self.game.player.stats['weight']) + "  Max Carry Weight: " + str(self.game.player.stats['max weight']), default_font, 25, WHITE, 20, self.game.screen_height - 80, "topleft")
        self.draw_text("Left Click: Select Item    F: create item    E: Exit Menu   ESCAPE: quit game", default_font, 20, WHITE, 10, self.game.screen_height - 40, "topleft")
        if self.not_enough_text:
            self.draw_text("Insufficient resources!", default_font, 40, YELLOW, self.game.screen_width/4, self.game.screen_height/2, "topleft")
        pg.display.flip()

class Dialogue_Menu():
    def __init__(self, game, hit):
        self.game = game
        self.menu_sprites = pg.sprite.Group()
        # These next two numbers keep the text in the display window. They may need some tweeking for different resolutions.
        self.wrap_factor = int(ceil((self.game.screen_width * 2/5)/ 13))
        self.number_of_lines = int(ceil((self.game.screen_height * 1/7) / 35))
        self.item_selected = False
        self.selected_item = None
        self.exit_keys = [pg.K_e, pg.K_i]  # The keys used to enter/exit the menu.
        self.game.in_dialogue_menu = True
        self.game.in_menu = True
        self.hit = hit
        self.text_data = []
        self.response_text = []
        self.text_screen = 0
        self.YN = False
        self.inventory_check = False
        self.needed_item = None
        self.needed_item_count = 1
        self.player_has_item = False
        self.gifted = False
        self.name = self.hit.kind['name']
        self.do_action = False # Used so the NPC does the after quest action at the right time.
        self.previous_quest = None
        if self.game.player.race in self.hit.kind.keys(): # Checks for race specific dialogue and quests
            self.quest = self.hit.kind[self.game.player.race]['quest']
            self.hit.kind['dialogue'] = self.hit.kind[self.game.player.race]['dialogue']
            self.assign_quest_info()

        elif 'quest' in self.hit.kind.keys():
            self.quest = self.hit.kind['quest']
            self.assign_quest_info()
        else:
            self.quest = None
            self.format_text()
        self.store = self.hit.kind['store']

        self.lines = 0

    def assign_quest_info(self):
        if self.quest:
            # This is used for quests that involve giving the NPC an item.
            if self.game.quests[self.quest]['inventory check']:
                self.inventory_check = True
                if '&' in self.game.quests[self.quest]['needed item']:
                    self.needed_item, needed_item_count = self.game.quests[self.quest]['needed item'].split('&')
                    try:
                        self.needed_item_count = int(needed_item_count)
                    except:
                        pass
                else:
                    self.needed_item = self.game.quests[self.quest]['needed item']
            if self.game.quests[self.quest]['completed']:
                if (self.game.quests[self.quest]['next quest']) and (self.hit.talk_counter == 1):
                    self.hit.kind['dialogue'] = self.game.quests[self.quest]['next dialogue']
                    self.quest = self.hit.kind['quest'] = self.game.quests[self.quest]['next quest']
                    self.hit.talk_counter = 0
                    self.format_text()
                elif not self.game.quests[self.quest]['rewarded']:
                    self.game.quests[self.quest]['rewarded'] = True
                    self.game.effects_sounds['fanfare'].play()
                    self.format_response(self.game.quests[self.quest]['reward text'])
                    self.add_reward(self.game.quests[self.quest]['reward'])
                else:
                    self.format_response(self.game.quests[self.quest]['completed text'])
                    self.hit.talk_counter += 1
            elif self.game.quests[self.quest]['accepted']:
                if self.inventory_check:
                    if self.check_inventory():
                        self.format_response(self.game.quests[self.quest]['has item text'])
                    else:
                        self.format_response(self.game.quests[self.quest]['waiting text'])
                else:
                    self.format_response(self.game.quests[self.quest]['waiting text'])
            else:
                self.format_text()
        else:
            self.format_text()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key in self.exit_keys:
                    self.clear_menu()
                    self.running = False
                if event.key == pg.K_SPACE:
                    self.YN = False
                    self.text_screen += 1
                if event.key == pg.K_y:
                    if self.YN:
                        self.accept_quest()
                if event.key == pg.K_n:
                    if self.YN:
                        self.deny_quest()
                if event.key == pg.K_b:
                    if self.store:
                        self.game.in_dialogue_menu = False
                        self.running = False
                        self.game.store_menu = Store_Menu(self.game, self.store)
            if event.type == pg.MOUSEBUTTONDOWN:  # Clears off pictures and stats from previously clicked item when new item is clicked.
                self.mouse_click = pg.mouse.get_pressed()
                self.item_selected = False
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                # get a list of all sprites that are under the mouse cursor
                self.clicked_sprites = [s for s in self.menu_sprites if s.rect.collidepoint(pos)]
                for choice in self.menu_sprites:
                    if choice in self.clicked_sprites:
                        if self.YN:
                            self.game.effects_sounds['click'].play()
                            if choice.text == 'Yes':
                                self.accept_quest()
                            if choice.text == 'No':
                                self.deny_quest()

    def add_reward(self, reward):
        for item in reward:
            for kind in ITEM_TYPE_LIST:
                if item in eval(kind.upper()):
                    self.game.player.inventory[kind].append(item)
            if 'gold:' in item:
                gold = int(item.replace('gold:', ''))
                self.game.player.inventory['gold'] += gold

    def accept_quest(self):
        if self.quest:
            if self.game.quests[self.quest]['accepted'] == True: #This block of code is used for a second quesiton in the 'accept text' section. For NPCs who don't want to go through the bother of asking you to give them the item later
                if not self.player_has_item:
                    self.check_inventory()
                if not self.player_has_item:
                    self.response_text = self.game.quests[self.quest]['lie text']
                    self.format_response()
                    self.clear_menu()
                    self.YN = False

            if self.player_has_item:
                self.take_item()
                self.game.quests[self.quest]['rewarded'] = True
                self.game.effects_sounds['fanfare'].play()
                self.response_text = self.game.quests[self.quest]['reward text']
                self.response_text.append(self.game.quests[self.quest]['completed text'][0])
                self.format_response()
                self.add_reward(self.game.quests[self.quest]['reward'])
                self.clear_menu()
                self.YN = False
                self.inventory_check = False
                self.needed_item = None
                self.player_has_item = False
                self.hit.kind['dialogue'] = self.game.quests[self.quest]['next dialogue']
                self.quest = self.hit.kind['quest'] = self.game.quests[self.quest]['next quest']
                if self.quest:
                    if 'autoaccept' in self.game.quests[self.quest]:
                        if self.game.quests[self.quest]['autoaccept']:
                            self.game.quests[self.quest]['accepted'] = True
            elif self.game.quests[self.quest]['accepted'] != True:
                self.game.quests[self.quest]['accepted'] = True
                self.response_text = self.game.quests[self.quest]['accept text']
                self.format_response()
                self.clear_menu()
                self.YN = False
                if self.quest:
                    if 'autocomplete' in self.game.quests[self.quest]:
                        if self.game.quests[self.quest]['autocomplete']:
                            self.game.quests[self.quest]['completed'] = True
                            self.do_action = True
                            self.previous_quest = self.quest

    def deny_quest(self):
        if self.quest:
            if self.player_has_item:
                self.response_text = self.game.quests[self.quest]['refuse to give text']
                self.format_response()
                self.clear_menu()
                self.YN = False
            else:
                self.game.quests[self.quest]['accepted'] = False
                self.response_text = self.game.quests[self.quest]['deny text']
                self.format_response()
                self.clear_menu()
                self.YN = False

    def take_item(self):
        self.player_has_item = False
        self.inventory_check = False
        count = 0
        if 'gold:' not in self.needed_item:
            for item_type in ITEM_TYPE_LIST:
                for i, item in enumerate(self.game.player.inventory[item_type]):
                    if item:
                        if self.needed_item in item:
                            count += 1
                            if count <= self.needed_item_count:
                                self.hit.inventory[item_type].append(item) # Adds item to NPCs inventory
                                self.hit.kind['inventory'][item_type].append(item) # Adds the item to NPCs dictionary file so it loads when you leave the map and come back.
                                self.game.player.inventory[item_type][i] = None  # Removes item from player's inventory
                            if count >= self.needed_item_count:
                                change_clothing(self.hit, True)
                                self.hit.body.update_animations()
                                remove_nones(self.game.player.inventory[item_type])

        else:
            gold = int(self.needed_item.replace('gold:', ''))
            if gold < self.game.player.inventory['gold']:
                self.game.player.inventory['gold'] -= gold
                self.hit.inventory['gold'] += gold
        self.game.quests[self.quest]['completed'] = True
        if 'action' in self.game.quests[self.quest]:
            self.do_action = True
            self.previous_quest = self.quest


    def check_inventory(self):
        if 'gold:' not in self.needed_item:
            for item_type in ITEM_TYPE_LIST:
                counter = Counter(self.game.player.inventory[item_type])
                for item in self.game.player.inventory[item_type]:
                    if item:
                        if self.needed_item in item:
                            if counter[item] >= self.needed_item_count:
                                self.player_has_item = True
                                return True
        else:
            gold = int(self.needed_item.replace('gold:', ''))
            if gold < self.game.player.inventory['gold']:
                self.player_has_item = True
                return True

    def action(self):
        if 'summon' in self.game.quests[self.previous_quest]['action']:
            _, creature = self.game.quests[self.previous_quest]['action'].split(':')
            if creature in PEOPLE:
                self.game.effects_sounds['enchant'].play()
                summoned = Npc(self.game, self.hit.pos.x + 128, self.hit.pos.y, self.game.map, creature)
                summoned.make_companion()
            elif creature in ANIMALS:
                self.game.effects_sounds['enchant'].play()
                Animal(self.game, pos.x, pos.y, self.game.map, creature)
        if self.game.quests[self.previous_quest]['action'] == 'companion':
            self.hit.make_companion()

        if self.game.quests[self.previous_quest]['action'] == 'unfollow':
            self.hit.remove(self.game.companions)
            try:
                self.hit.body.remove(self.game.companion_bodies)
            except:
                pass
            self.hit.default_detect_radius = self.hit.detect_radius = 250
            self.hit.guard = False
            self.hit.speed = self.hit.walk_speed = 80
            self.hit.run_speed = 100


    def clear_menu(self):
        for item in self.menu_sprites:
            item.kill()

    def format_response(self, text = None): # Used for formatting quest responses.
        if text:
            self.response_text = text
        self.text_data = []
        self.text_screen = 0
        for x in self.response_text:
            if 'SAMERACE' in x:
                if self.game.player.race == self.hit.kind['race']:
                    x = x.replace('SAMERACE', '')
                    self.divide_lines(x)
            elif 'DIFFRACE' in x:
                if self.game.player.race != self.hit.kind['race']:
                    x = x.replace('DIFFRACE', '')
                    self.divide_lines(x)
            else:
                self.divide_lines(x)

    def format_text(self): # Used for formatting dialogue.
        # This part wraps text, so it is displayed in paragraph form.
        if 'random' not in self.hit.kind['dialogue']:
            for x in eval(self.hit.kind['dialogue']):
                if 'SAMERACE' in x:
                    if self.game.player.race == self.hit.kind['race']:
                        x = x.replace('SAMERACE', '')
                        self.divide_lines(x)
                elif 'DIFFRACE' in x:
                    if self.game.player.race != self.hit.kind['race']:
                        x = x.replace('DIFFRACE', '')
                        self.divide_lines(x)
                else:
                    self.divide_lines(x)

        else: # This part is used for characters with a randomized dialogue.
            dialogue = self.hit.kind['dialogue'].replace('random ', '')
            randomized_list = copy.copy(eval(dialogue))
            shuffle(randomized_list)
            for x in randomized_list:
                if 'SAMERACE' in x:
                    if self.game.player.race == self.hit.kind['race']:
                        x = x.replace('SAMERACE', '')
                        self.divide_lines(x)
                elif 'DIFFRACE' in x:
                    if self.game.player.race != self.hit.kind['race']:
                        x = x.replace('DIFFRACE', '')
                        self.divide_lines(x)
                else:
                    self.divide_lines(x)

    def divide_lines(self, x): # This is used to split long dialogue into separate screens.
        description = wrap(x, self.wrap_factor)
        chunks = [description[z:z + self.number_of_lines] for z in range(0, len(description), self.number_of_lines)]
        for y in chunks:
            self.text_data.append(y)

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.game.screen.blit(text_surface, text_rect)

    def list_choices(self):
        if self.YN:
            yes_text = Text(self, 'Yes', default_font, 40, YELLOW, self.game.screen_width/5 + 15, self.game.screen_height * 4/7 + 60 + (45 * self.lines), "topleft")
            self.menu_sprites.add(yes_text)
            no_text = Text(self, 'No', default_font, 40, YELLOW, self.game.screen_width/5 + 15,  self.game.screen_height * 4/7 + 60 + (45 * (self.lines + 1)), "topleft")
            self.menu_sprites.add(no_text)

    def draw(self):
        list_rect = pg.Rect(self.game.screen_width/5, int(self.game.screen_height * 4/7), self.game.screen_width * 3/5, self.game.screen_height * 3/7 - 50)
        list_rect_fill = pg.Rect(self.game.screen_width/5 + 2, self.game.screen_height * 4/7 + 2, self.game.screen_width * 3/5 - 2, self.game.screen_height)
        pg.draw.rect(self.game.screen, BLACK, list_rect_fill)
        pg.draw.rect(self.game.screen, WHITE, list_rect, 2)
        if self.text_screen > len(self.text_data) - 1:
            self.text_screen = 0
            self.running = False
            return
        self.lines = len(self.text_data[self.text_screen])
        for i, text_screens in enumerate(self.text_data[self.text_screen]):
            if 'YN' in text_screens:
                text_screens = text_screens.replace('YN', '')
                self.YN = True
            if 'GIFTS' in text_screens:
                text_screens = text_screens.replace('GIFTS', '')
                if not self.gifted:
                    self.game.effects_sounds['gun_pickup'].play()
                    self.add_reward(self.game.quests[self.quest]['gifts'])
                    self.gifted = True
            self.draw_text(text_screens, default_font, 40, WHITE, self.game.screen_width/5 + 15, self.game.screen_height * 4/7 + 60 + (45 * i), "topleft")
        if self.YN:
            self.list_choices()

        self.draw_text(self.name + ':', default_font, 40, BLUE, self.game.screen_width / 5 + 15, self.game.screen_height * 4 / 7 + 15, "topleft")
        self.draw_text("E: Exit Dialogue Menu   SPACE: Advance Dialogue", HUD_FONT, 30, WHITE, self.game.screen_width/5 + 50, self.game.screen_height - 40, "topleft")
        if self.store:
            self.draw_text("B: Buy/Sell", HUD_FONT, 30, WHITE, self.game.screen_width / 5 + 700, self.game.screen_height - 40, "topleft")
        self.menu_sprites.draw(self.game.screen)
        pg.display.flip()

    def update(self):
        self.running = True
        while self.running:
            self.game.clock.tick(30)
            self.events()
            self.draw()
        self.update_external_variables()

    def update_external_variables(self):
        if self.do_action:  # Only does the after quest action after you finish talking to them.
            self.action()
        self.game.in_dialogue_menu = False
        self.game.dialogue_menu_npc = None
        self.game.in_menu = False
        self.game.last_dialogue = pg.time.get_ticks() # Gets the time you exited the menu. This is used so that the menu doesn't keep popping up.
        self.game.beg = perf_counter()  # Resets the counter so the dt doesn't get messed up.
        del self


class Store_Menu(Inventory_Menu): # Inventory Menu, also used as the parent class for other menus.
    def __init__(self, game, store):
        super().__init__(game)
        # These items are changed for inherrited menus.
        self.game.in_store_menu = True
        self.game.in_menu = True
        self.store = store
        self.exit_keys = [pg.K_e] # The keys used to enter/exit the menu.
        self.spacing = 20 # Spacing between headings
        self.heading_list = ['Weapons', 'Hats', 'Hair', 'Tops', 'Bottoms', 'Shoes', 'Gloves', 'Items'] # This is the list of headings
        self.store_inventory = self.store['inventory'].copy()
        self.markup = self.store['markup']
        self.pvalue = self.store['pvalue'] # percent of item value store buys at
        self.display_inventory = 'store'
        self.item_type = 'weapons'
        self.cost = 0
        self.worth = 0

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key in self.exit_keys:
                    self.clear_menu()
                    self.running = False
                if event.key == pg.K_ESCAPE:
                    self.game.quit()
                if event.key == pg.K_TAB:
                    if self.display_inventory == 'store':
                        self.display_inventory = 'player'
                        self.list_items()
                    else:
                        self.display_inventory = 'store'
                        self.list_store_items()
                    self.cost = 0
                    self.worth = 0
                if event.key == pg.K_b: # buy
                    if self.selected_item:
                        if self.display_inventory == 'store':
                            self.buy_item()
                if event.key == pg.K_s:  # drop/sell item
                    if self.selected_item:
                        if self.display_inventory == 'player':
                            self.sell_item()
            if event.type == pg.MOUSEBUTTONDOWN:  # Clears off pictures and stats from previously clicked item when new item is clicked.
                self.mouse_click = pg.mouse.get_pressed()
                pos = pg.mouse.get_pos()
                if [s for s in self.menu_sprites if s.rect.collidepoint(pos)]:
                    self.game.effects_sounds['click'].play()
                self.printable_stat_list = []
                self.item_selected = False
                for picture in self.item_pictures:
                    picture.kill()
            if event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                # get a list of all sprites that are under the mouse cursor
                self.clicked_sprites = [s for s in self.menu_sprites if s.rect.collidepoint(pos)]
                for heading in self.menu_heading_sprites:
                    if heading in self.clicked_sprites:
                        self.item_type = heading.text.lower()
                        if self.display_inventory == 'store':
                            self.list_store_items()
                        else:
                            self.list_items()
                        self.selected_heading = heading
                # Equips items
                for item in self.clicked_sprites:
                    if item in self.item_sprites:
                        self.selected_item = item
                        self.item_selected = True
                        self.calculate_cost()
                        self.calculate_worth()
                        self.display_item_info(item)
                        if self.mouse_click == (0, 0, 1):
                            pass
                        # Equipping weapon in left hand
                        if self.mouse_click == (1, 0, 0):
                            pass
                        if self.display_inventory == 'store':
                            self.list_store_items()
                        else:
                            self.list_items()

    def calculate_cost(self):
        if 'value' in eval(self.item_type.upper())[self.selected_item.text]:
            self.cost = int(eval(self.item_type.upper())[self.selected_item.text]['value'] * self.markup)
        else:
            self.cost = 0

    def calculate_worth(self):
        if 'value' in eval(self.item_type.upper())[self.selected_item.text]:
            self.worth = int(eval(self.item_type.upper())[self.selected_item.text]['value'] * self.pvalue)
        else:
            self.worth = 0

    def buy_item(self):
        if self.cost != 0:
            if self.game.player.inventory['gold'] > self.cost:
                self.game.player.inventory[self.item_type].append(self.selected_item.text)
                self.game.player.inventory['gold'] -= self.cost
                self.game.effects_sounds['cashregister'].play()

    def sell_item(self):
        if self.worth != 0:
            # Unequips item if you drop one you are equipping and don't have another one.
            number_of_each = 0
            for i, item in enumerate(self.game.player.inventory[self.item_type]):
                if item == self.selected_item.text:
                    number_of_each += 1
            if number_of_each == 1:
                if self.game.player.equipped[self.item_type] == self.selected_item.text:
                    self.game.player.equipped[self.item_type] = None
                elif self.game.player.equipped['weapons2'] == self.selected_item.text: # Unequips dropped secondary weapon.
                    self.game.player.equipped['weapons2'] = None
            # Removes dropped item from inventory
            for i, item in enumerate(self.game.player.inventory[self.item_type]):
                if item == self.selected_item.text:
                    self.game.player.inventory[self.item_type][i] = None
                    if self.selected_item.text not in self.store_inventory[self.item_type]:
                        self.store_inventory[self.item_type].append(self.selected_item.text)  #Adds item to store inventory
                    self.selected_item.text = 'None'  # Makes it so it doesn't drop more than one of the same item.
            remove_nones(self.game.player.inventory[self.item_type])
            self.game.player.inventory['gold'] += self.worth # Gives you gold for item
            self.game.effects_sounds['cashregister'].play()
            self.selected_item = None
            self.cost = 0
            self.worth = 0
            self.list_items()

    def list_store_items(self):
        self.clear_menu()
        displayed_list = [] # Keeps track of which items have been displayed

        row = 0
        for item in self.store_inventory[self.item_type]:
            if ' M' in item:
                if self.game.player.equipped['gender'] not in ['male']:
                    continue
            elif ' F' in item:
                if self.game.player.equipped['gender'] not in ['female', 'other']:
                    continue
            if item not in displayed_list:
                item_name = Text(self, item, default_font, 20, WHITE, 50, 30 * row + 75, "topleft")
                self.item_sprites.add(item_name)
                displayed_list.append(item)
                row += 1
        self.game.player.calculate_weight()

    def display_item_info(self, item):
        item_dictionary = globals()[self.item_type.upper()] #converts the item_type string into the correct dictionary to get the item stats from
        if self.item_type[-1:] == 's':
            image_path = "self.game." + self.item_type[:-1] + "_images[" + self.item_type.upper() + "['" + item.text + "']['image']]"
        else:
            image_path = "self.game." + self.item_type + "_images[" + self.item_type.upper() + "['" + item.text + "']['image']]"
        itemdict = eval(self.item_type.upper())
        item_image = eval(image_path)
        if 'color' in itemdict[item.text]:
            item_image = color_image(item_image, itemdict[item.text]['color'])
        Picture(self.game, self, item_image, int(self.game.screen_width * (3 / 4)), 150)

        for key in item_dictionary:
            if key == item.text:
                i = 0
                for stat in item_dictionary[key]:
                    if stat in ['image', 'offset', 'walk', 'grip']:
                        continue
                    else:
                        item_stats = ""
                        item_stats += (stat + " " + str(item_dictionary[key][stat]))
                        self.printable_stat_list.append(item_stats)
                        i += 1

    def update(self):
        self.generate_headings()
        self.list_store_items()
        self.running = True
        while self.running:
            self.game.clock.tick(30)
            self.events()
            self.draw()
        self.update_external_variables()

    def update_external_variables(self):
        self.game.in_store_menu = False
        self.game.in_menu = False
        self.game.player.current_weapon = self.game.player.equipped['weapons']
        self.game.player.current_weapon2 = self.game.player.equipped['weapons2']
        if self.game.player.swimming:
            toggle_equip(self.game.player, True)
        check_equip(self.game.player)
        self.game.player.human_body.update_animations()  # Updates animations for newly equipped or removed weapons etc.
        self.game.player.dragon_body.update_animations()
        if self.game.player.possessing:
            self.game.player.body.update_animations()
        self.game.player.calculate_fire_power()
        self.game.player.calculate_perks()
        # Reloads
        self.game.player.pre_reload()
        self.game.beg = perf_counter() # resets the counter so dt doesn't get messed up.

    def draw(self):
        self.game.screen.fill(BLACK)
        list_rect = pg.Rect(10, 50, self.game.screen_width / 2 - 10, self.game.screen_height - 100)
        list_rect_fill = pg.Rect(20, 60, self.game.screen_width / 2 - 30, self.game.screen_height - 120)
        description_rect = pg.Rect(self.game.screen_width / 2 + 10, 50, self.game.screen_width / 2 - 20, self.game.screen_height - 100)
        description_rect_fill = pg.Rect(self.game.screen_width / 2 + 20, 60, self.game.screen_width / 2 - 40, self.game.screen_height - 120)
        pg.draw.rect(self.game.screen, WHITE, list_rect, 2)
        pg.draw.rect(self.game.screen, WHITE, description_rect, 2)
        pg.draw.rect(self.game.screen, BLACK, list_rect_fill)
        pg.draw.rect(self.game.screen, BLACK, description_rect_fill)
        if not self.selected_item == None:
            if self.item_selected:
                selected_rect = pg.Rect(self.selected_item.rect.x - 4, self.selected_item.rect.y, self.selected_item.rect.width + 8, self.selected_item.size + 2)
                pg.draw.rect(self.game.screen, YELLOW, selected_rect, 2)
        selected_heading_rect = pg.Rect(self.selected_heading.rect.x - 4, self.selected_heading.rect.y, self.selected_heading.rect.width + 8, self.selected_heading.size + 2)
        pg.draw.rect(self.game.screen, YELLOW, selected_heading_rect, 2)
        self.menu_sprites.draw(self.game.screen)
        if self.item_selected:
            for i, item_stat in enumerate(self.printable_stat_list):
                self.draw_text(item_stat, default_font, 20, WHITE, self.game.screen_width / 2 + 50, self.game.screen_height / 3 + 30 * i, "topleft")
        if self.display_inventory == 'store':
            disp_text = 'Buy From Store'
            cost_text = 'This item costs ' + str(self.cost) + ' gold.'
        else:
            disp_text = 'Sell to Store'
            cost_text = 'This item is worth ' + str(self.worth) + ' gold.'
        self.draw_text(disp_text, default_font, 35, YELLOW, self.game.screen_width - 300, 10, "topright")
        self.draw_text(cost_text, default_font, 35, YELLOW, self.game.screen_width - 300, 50, "topright")
        self.draw_text(str(self.game.player.inventory['gold']) + " gold in inventory.", default_font, 25, WHITE, 20, self.game.screen_height - 120, "topleft")
        self.draw_text("Carry Weight: " + str(self.game.player.stats['weight']) + "  Max Carry Weight: " + str(self.game.player.stats['max weight']), default_font, 25, WHITE, 20, self.game.screen_height - 80, "topleft")
        self.draw_text("Click: Select Item    B: Buy Item    S: Sell item    TAB: Toggle Store & Player inventory   E: Exit Menu   ESCAPE: quit game", default_font, 20, WHITE, 10, self.game.screen_height - 40, "topleft")
        pg.display.flip()

class Quest_Menu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.exit_keys = [pg.K_j, pg.K_e] # The keys used to enter/exit the menu.
        self.spacing = 40 # Spacing between headings
        self.heading_list = ['Active Quests', 'Completed Quests'] # This is the list of headings
        self.previous_item = None
        self.selected_heading = 'Active Quests'

    def use_item(self):
        if self.selected_item:
            pass

    def drop_item(self):
        pass

    def right_equip(self, item):
        pass

    def left_equip(self, item):
        pass

    def list_items(self):
        self.clear_menu()
        i = 0
        if self.selected_heading.text == 'Active Quests':
            for quest in self.game.quests.keys():
                if self.game.quests[quest]['accepted']:
                    if not self.game.quests[quest]['completed']:
                        quest_name = Text(self, quest, default_font, 20, WHITE, 50, 30 * i + 75, "topleft")
                        self.item_sprites.add(quest_name)
                        i += 1
        elif self.selected_heading.text == 'Completed Quests':
            for quest in self.game.quests.keys():
                if self.game.quests[quest]['accepted']:
                    if self.game.quests[quest]['completed']:
                        quest_name = Text(self, quest, default_font, 20, WHITE, 50, 30 * i + 75, "topleft")
                        self.item_sprites.add(quest_name)
                        i += 1

    def display_item_info(self, item):
        # This part wraps the descriptions of the character races. So they are displayed in paragraph form.
        description = wrap(self.game.quests[item.text]['description'], 80)
        for line in description:
            self.printable_stat_list.append(line)
        self.printable_stat_list.append(" ")

    def update_external_variables(self):
        self.game.in_quest_menu = False
        self.game.in_menu = False
        self.game.beg = perf_counter() # resets the counter so dt doesn't get messed up.
        del self

    def draw(self):
        self.game.screen.fill(BLACK)
        list_rect = pg.Rect(10, 50, self.game.screen_width / 2 - 10, self.game.screen_height - 100)
        list_rect_fill = pg.Rect(20, 60, self.game.screen_width / 2 - 30, self.game.screen_height - 120)
        description_rect = pg.Rect(self.game.screen_width / 2 + 10, 50, self.game.screen_width / 2 - 20, self.game.screen_height - 100)
        description_rect_fill = pg.Rect(self.game.screen_width / 2 + 20, 60, self.game.screen_width / 2 - 40, self.game.screen_height - 120)
        pg.draw.rect(self.game.screen, WHITE, list_rect, 2)
        pg.draw.rect(self.game.screen, WHITE, description_rect, 2)
        pg.draw.rect(self.game.screen, BLACK, list_rect_fill)
        pg.draw.rect(self.game.screen, BLACK, description_rect_fill)
        if not self.selected_item == None:
            if self.item_selected:
                selected_rect = pg.Rect(self.selected_item.rect.x - 4, self.selected_item.rect.y, self.selected_item.rect.width + 8, self.selected_item.size + 2)
                pg.draw.rect(self.game.screen, YELLOW, selected_rect, 2)
        selected_heading_rect = pg.Rect(self.selected_heading.rect.x - 4, self.selected_heading.rect.y, self.selected_heading.rect.width + 8, self.selected_heading.size + 2)
        pg.draw.rect(self.game.screen, YELLOW, selected_heading_rect, 2)
        self.menu_sprites.draw(self.game.screen)
        if self.item_selected:
            for i, item_stat in enumerate(self.printable_stat_list):
                self.draw_text(item_stat, default_font, 20, WHITE, self.game.screen_width / 2 + 50, self.game.screen_height / 3 + 30 * i, "topleft")
        self.draw_text("Left Click: Select Quest    Right Click: Select Quest    E: Exit Menu   ESCAPE: quit game", default_font, 20, WHITE, 10, self.game.screen_height - 40, "topleft")
        pg.display.flip()

class Fly_Menu(Draw_Text):
    def __init__(self, game):
        self.game = game
        self.cell_width = self.game.screen_width / len(self.game.map_data_list[0])
        self.cell_height = self.game.screen_height / len(self.game.map_data_list)
        self.offsetx = int(self.game.world_location.x * self.cell_width)
        self.offsety = int(self.game.world_location.y * self.cell_height)
        self.currentmap_rect = pg.Rect(0, 0, self.cell_width, self.cell_height)
        self.currentmap_rect.topleft = (self.offsetx, self.offsety)
        self.update()

    def update(self):
        self.running = True
        while self.running:
            self.game.clock.tick(30)
            self.events()
            self.draw()
        self.update_external_variables()

    def update_external_variables(self):
        self.game.in_fly_menu = False
        self.game.in_menu = False
        self.game.beg = perf_counter() # resets the counter so dt doesn't get messed up.
        map = str(self.game.map_data_list[int(self.game.world_location.y)][int(self.game.world_location.x)]) + '.tmx'
        # Puts player in map center
        self.game.player.pos = vec(self.game.map.width/2, self.game.map.height/2)
        self.game.player.rect.center = self.game.player.pos
        self.game.load_map(map)
        del self

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.game.quit()
                if event.key in [pg.K_e, pg.K_u]:
                    self.running = False

        keys = pg.key.get_pressed()
        # WASD keys for moving ship to new maps
        if self.game.player.vehicle.fuel > 0:
            if keys[pg.K_w]:
                self.game.world_location.y -= 1
                if self.game.world_location.y < 0:
                    self.game.world_location.y = self.game.world_height
                self.set_position()
            if keys[pg.K_s]:
                self.game.world_location.y += 1
                if self.game.world_location.y > self.game.world_height:
                    self.game.world_location.y = 0
                self.set_position()
            if keys[pg.K_a]:
                self.game.world_location.x -= 1
                if self.game.world_location.x < 0:
                    self.game.world_location.x = self.game.world_width
                self.set_position()
            if keys[pg.K_d]:
                self.game.world_location.x += 1
                if self.game.world_location.x > self.game.world_width:
                    self.game.world_location.x = 0
                self.set_position()

    def set_position(self):
        self.game.player.vehicle.fuel -= 1
        if self.game.player.vehicle.fuel < 0:
            self.game.player.vehicle.fuel = 0
        self.offsetx = int(self.game.world_location.x * self.cell_width)
        self.offsety = int(self.game.world_location.y * self.cell_height)
        self.currentmap_rect.topleft = (self.offsetx, self.offsety)

    def draw(self):
        self.game.screen.blit(self.game.over_minimap_image, (0, 0))
        pg.draw.rect(self.game.screen, YELLOW, self.currentmap_rect, 4)
        self.draw_text("Use WASD to move ship", default_font, 20, WHITE, 10, self.game.screen_height - 40, "topleft")
        self.draw_text("Fuel: " + str(self.game.player.vehicle.fuel), default_font, 40, WHITE, 10, 40, "topleft")
        pg.display.flip()
