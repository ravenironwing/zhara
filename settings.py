import pygame as pg
import os
from os import path
from weapons import *
from armor import *
from magic import *
from interactables import *
from items import *
from chests import *
from race_info import *
from color_palettes import *

vec = pg.math.Vector2
vec3 = pg.math.Vector3

# define game folders
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'img')
books_folder = path.join(game_folder, 'books')
saves_folder = path.join(game_folder, 'saves')
fonts_folder = path.join(game_folder, 'fonts')
snd_folder = path.join(game_folder, 'snd')
female_player_sound_folder = path.join(snd_folder, 'female_player')
male_player_sound_folder = path.join(snd_folder, 'male_player')
music_folder = path.join(game_folder, 'music')
map_folder = path.join(game_folder, 'maps')
# image folder and subfolders
male_mech_suit_parts_folder = female_mech_suit_parts_folder = path.join(img_folder, 'mech_suit')
male_golem_parts_folder = female_golem_parts_folder = path.join(img_folder, 'golem_parts')
male_icegolem_parts_folder = female_icegolem_parts_folder = path.join(img_folder, 'icegolem_parts')
male_blackwraith_parts_folder = female_blackwraith_parts_folder = path.join(img_folder, 'blackwraith_parts')
male_whitewraith_parts_folder = female_whitewraith_parts_folder = path.join(img_folder, 'whitewraith_parts')
male_blackwraithdragon_parts_folder = female_blackwraithdragon_parts_folder = path.join(img_folder, 'blackwraithdragon_parts')
male_whitewraithdragon_parts_folder = female_whitewraithdragon_parts_folder = path.join(img_folder, 'whitewraithdragon_parts')
male_skeleton_parts_folder = female_skeleton_parts_folder = path.join(img_folder, 'skeleton_parts')
male_skeletondragon_parts_folder = female_skeletondragon_parts_folder = path.join(img_folder, 'skeletondragon_parts')
female_shaktele_parts_folder = female_osidine_parts_folder = path.join(img_folder, 'female_osidine_parts')
male_shaktele_parts_folder = male_osidine_parts_folder = path.join(img_folder, 'male_osidine_parts')
female_shakteledragon_parts_folder = female_osidinedragon_parts_folder = path.join(img_folder, 'female_osidinedragon_parts')
male_shakteledragon_parts_folder = male_osidinedragon_parts_folder = path.join(img_folder, 'male_osidinedragon_parts')
female_elfdragon_parts_folder = path.join(img_folder, 'female_elfdragon_parts')
male_elfdragon_parts_folder = path.join(img_folder, 'male_elfdragon_parts')
female_miewdradragon_parts_folder = path.join(img_folder, 'female_miewdradragon_parts')
male_miewdradragon_parts_folder = path.join(img_folder, 'male_miewdradragon_parts')
female_lacertoliandragon_parts_folder = path.join(img_folder, 'female_lacertoliandragon_parts')
male_lacertoliandragon_parts_folder = path.join(img_folder, 'male_lacertoliandragon_parts')
male_mechanimadragon_parts_folder = path.join(img_folder, 'male_mechanimadragon_parts')
female_mechanimadragon_parts_folder = path.join(img_folder, 'female_mechanimadragon_parts')
male_immortuidragon_parts_folder = path.join(img_folder, 'male_immortuidragon_parts')
female_immortuidragon_parts_folder = path.join(img_folder, 'female_immortuidragon_parts')
female_miewdra_parts_folder = path.join(img_folder, 'female_miewdra_parts')
male_miewdra_parts_folder = path.join(img_folder, 'male_miewdra_parts')
female_immortui_parts_folder = path.join(img_folder, 'female_immortui_parts')
male_immortui_parts_folder = path.join(img_folder, 'male_immortui_parts')
male_elf_parts_folder = path.join(img_folder, 'male_elf_parts')
female_elf_parts_folder = path.join(img_folder, 'female_elf_parts')
male_lacertolian_parts_folder = path.join(img_folder, 'male_lacertolian_parts')
female_lacertolian_parts_folder = path.join(img_folder, 'female_lacertolian_parts')
male_mechanima_parts_folder = path.join(img_folder, 'male_mechanima_parts')
female_mechanima_parts_folder = path.join(img_folder, 'female_mechanima_parts')
male_vadashay_parts_folder = path.join(img_folder, 'male_vadashay_parts')
female_vadashay_parts_folder = path.join(img_folder, 'female_vadashay_parts')
male_demon_parts_folder = path.join(img_folder, 'male_demon_parts')
female_demon_parts_folder = path.join(img_folder, 'female_demon_parts')
male_goblin_parts_folder = path.join(img_folder, 'male_goblin_parts')
female_goblin_parts_folder = path.join(img_folder, 'female_goblin_parts')
animals_folder = path.join(img_folder, 'animals')
items_folder = path.join(img_folder, 'items')
doors_folder = path.join(img_folder, 'doors')
door_break_folder = path.join(img_folder, 'door_break_animation')
bullets_folder = path.join(img_folder, 'bullets')
fire_folder = path.join(img_folder, 'fire_animation')
breakable_folder = path.join(img_folder, 'breakable')
shock_folder = path.join(img_folder, 'shock_animation')
fireball_folder = path.join(img_folder, 'fireball')
explosion_folder = path.join(img_folder, 'explosion')
weapons_folder = path.join(img_folder, 'weapons')
hats_folder = path.join(img_folder, 'hats')
hair_folder = path.join(img_folder, 'hair')
tops_folder = path.join(img_folder, 'tops')
bottoms_folder = path.join(img_folder, 'bottoms')
shoes_folder = path.join(img_folder, 'shoes')
gloves_folder = path.join(img_folder, 'gloves')
magic_folder = path.join(img_folder, 'magic')
gender_folder = path.join(img_folder, 'gender')
race_folder = path.join(img_folder, 'race')
enchantments_folder = path.join(img_folder, 'enchantments')
corpse_folder = path.join(img_folder, 'corpses')
loading_screen_folder = path.join(img_folder, 'loading_screens')
vehicles_folder = path.join(img_folder, 'vehicles')
color_swatches_folder = path.join(img_folder, 'color_swatches')
light_masks_folder = path.join(img_folder, 'light_masks')

# Font settings:
HEADING_FONT = path.join(fonts_folder, 'UncialAntiqua-Regular.ttf')
SCRIPT_FONT = path.join(fonts_folder, 'EagleLake-Regular.ttf')
HUD_FONT = path.join(fonts_folder, 'Aegean.ttf')
MENU_FONT = path.join(fonts_folder, 'LinBiolinum_Rah.ttf')
WRITING_FONT = path.join(fonts_folder, 'DancingScript-Regular.ttf')
KAWTHI_FONT = path.join(fonts_folder, 'Kawthi.ttf')

ITEM_TYPE_LIST = ['weapons', 'tops', 'bottoms', 'hats', 'hair', 'shoes', 'gloves', 'items', 'magic']
EQUIP_DRAW_LIST = ['shoes', 'shoes', 'bottoms', 'gloves', 'gloves', None, None, 'tops']
EQUIP_IMG_LIST = ['shoe', 'shoe', 'bottom', 'glove', 'glove', None, None, 'top']

#print(len([name for name in os.listdir(body_parts_folder) if os.path.isfile(os.path.join(body_parts_folder, name))]))

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)
TRANSPARENT = (255, 0, 255)
SHADOW = (0, 0, 0, 150)
DEFAULT_HAIR_COLOR = (138,54,15)
DEFAULT_SKIN_COLOR = (255, 255, 255)
UNDERWORLD = ['cave', 'tunnel', 'hole', 'mine', 'tower'] # Used for map naming conventions that are under or over the overworld maps.

# game settings
pg.mixer.pre_init(44100, -16, 4, 2048)
pg.init()
pg.mixer.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
infoObject = pg.display.Info() #creates an info object to detect native screen resolution.
# Sets maximum screen resolution to 1920 by 1080
MODES = pg.display.list_modes()
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h
#if WIDTH > 1600: # Allowing for 1080 slows down performance by about 10+ fps and really doesn't improve the experience much.
#WIDTH = 1600
#HEIGHT = 900
#WIDTH = 1024
#HEIGHT = 768
if WIDTH > 1920: # Allowing for 1080p slows down performance by about 10+ fps and really doesn't improve the experience much.
    WIDTH = 1920
    HEIGHT = 1080
#MAPWIDTH = 8192 # Number of tiles wide times pixel width of tile or 65 * 128
#MAPHEIGHT = 8192 # Number of tiles high times pixel height of tile or 65 * 128
FPS = 60
TITLE = "Legends of Zhara"
BGCOLOR = BROWN
TITLE_IMAGE = 'skyrealm.png'
LOGO_IMAGE = 'a two headed snick.png'
MPY_WORDS = 'mpy_words.png'
ICON_IMG = 'zhara_icon.png'
OVERWORLD_MAP_IMAGE = 'worldmap.png'
#MAP_TILE_WIDTH = 64 # 64 tiles by 64 tiles per map
#GRIDWIDTH = WIDTH / MAP_TILE_WIDTH
#GRIDHEIGHT = HEIGHT / MAP_TILE_WIDTH
#TILESIZE = 128 # 128 pixels by 128 pixels per tile
START_WORLD = 'worldmap.tmx'

UPGRADE_FACTOR = 1.2 # This number determines how much item value increases when upgrading armor and weapons. The higher the number the lower the value.

# Day/Night
DAY_LENGTH = 15 * 60 * 1000
NIGHT_LENGTH = 9 * 60 * 1000
DAY_PERIOD = DAY_LENGTH + NIGHT_LENGTH
NIGHTFALL_SPEED = 100 # The higher the slower. In ms.
GAME_HOUR = DAY_PERIOD/24

# Player settings
PLAYER_HEALTH = 100
PLAYER_STAMINA = 100
PLAYER_STRENGTH = 1
PLAYER_ACC = 28
PLAYER_RUN = 38
MAX_RUN = 80
CLIMB_TIME = 1000
PLAYER_CLIMB = 14
PLAYER_FRIC = -.12
PLAYER_ROT_SPEED = 200
PLAYER_TUR = 'turret.png'
PLAYER_TANK = 'tank.png'
TALK_RADIUS = 85
TANK_IN_WATER = 'tank_underwater.png'
SUNKEN_TANK = 'sunken_tank.png'
PLAYER_IMG = 'player1.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 45, 45)
WING1_OFFSET = (-15, 21)
WING2_OFFSET = (-15, -21)

#Misc Sprite Settings
TREE_SIZES = {'sm': 400, 'md': 580, 'lg': 750}
DOOR_STYLES = {}
DOOR_STYLES['wood'] = {'image': 0, 'hp': 500}
DOOR_STYLES['heavy'] = {'image': 1, 'hp': 1000}
DOOR_STYLES['steel'] = {'image': 2, 'hp': 3000}
DOOR_STYLES['bronze'] = {'image': 3, 'hp': 2000}

# Used for mapping portal firepot combos with map locations
# 1234-Goblin Island, 4132: Demon's Lair, 3421-Dewcastle Graveyard, 2143-Norwald the Miewdra Village, 1342-Mechanima Village, 1243-Lacertolia, 2413-Zombieland, 4321-Elf Town, 3124-South Pole
PORTAL_CODES = {'1234': [107, 34, 32, 26], '4132': [53, 75, 31, 5], '3421': [27, 40, 5, 33], '2143': [89, 49, 32, 32], '1342': [126, 22, 32, 32], '1243': [146, 43, 32, 32], '2413': [65, 20, 32, 32],  '4321': [38, 27, 32, 42], '3124': [85, 96, 32, 32]}

AIPATHS = ['UD', 'RL']

# Sets up randomizable map files by type:
MOUNTAIN_MAPS = []
FOREST_MAPS = []
GRASSLAND_MAPS = []
TUNDRA_MAPS = []
DESERT_MAPS = []
for file in os.listdir(map_folder):
    name = file.replace('.tmx', '')
    if file.startswith("MOUNTAIN"):
        MOUNTAIN_MAPS.append(name)
    elif file.startswith("FOREST"):
        FOREST_MAPS.append(name)
    elif file.startswith("GRASSLAND"):
        GRASSLAND_MAPS.append(name)
    elif file.startswith("TUNDRA"):
        TUNDRA_MAPS.append(name)
    elif file.startswith("DESERT"):
        DESERT_MAPS.append(name)
RANDOM_MAP_TILES = {'53': 'MOUNTAIN_MAPS', '27': 'FOREST_MAPS', '11': 'GRASSLAND_MAPS'}

# Player body image settings
gender_list = ['male', 'female']
HUMANOID_IMAGES = {}
for kind in RACE_TYPE_LIST:
    for gender in gender_list:
        temp_images = []
        number_of_files = len([name for name in os.listdir(eval(gender + '_' + kind + '_parts_folder')) if os.path.isfile(os.path.join(eval(gender + '_' + kind + '_parts_folder'), name))])
        for i in range(1, number_of_files + 1):
            filename = 'player_layer{}.png'.format(i)
            temp_images.append(filename)
        HUMANOID_IMAGES[gender + '_' + kind + '_images'] = temp_images


PORTAL_SHEET = path.join(img_folder, 'portal.png')

BULLET_IMAGES = []
number_of_files = len([name for name in os.listdir(bullets_folder) if os.path.isfile(os.path.join(bullets_folder, name))])
for i in range(0, number_of_files):
    filename = 'bullet{}.png'.format(i)
    BULLET_IMAGES.append(filename)

FIRE_IMAGES = []
number_of_files = len([name for name in os.listdir(fire_folder) if os.path.isfile(os.path.join(fire_folder, name))])
for i in range(1, number_of_files + 1):
    filename = 'fire_1b_40_{}.png'.format(i)
    FIRE_IMAGES.append(filename)

BREAKABLE_IMAGES = {}
for breakable in BREAKABLES:
    temp_list = []
    number_of_files = len([name for name in os.listdir(breakable_folder) if breakable in name if os.path.isfile(os.path.join(breakable_folder, name))])
    for i in range(0, number_of_files):
        filename = breakable + '{}.png'.format(i)
        temp_list.append(filename)
    BREAKABLE_IMAGES[breakable] = temp_list

SHOCK_IMAGES = []
number_of_files = len([name for name in os.listdir(shock_folder) if os.path.isfile(os.path.join(shock_folder, name))])
for i in range(1, number_of_files + 1):
    filename = 'shock{}.png'.format(i)
    SHOCK_IMAGES.append(filename)

FIREBALL_IMAGES = []
number_of_files = len([name for name in os.listdir(fireball_folder) if os.path.isfile(os.path.join(fireball_folder, name))])
for i in range(1, number_of_files + 1):
    filename = 'f{}.png'.format(i)
    FIREBALL_IMAGES.append(filename)

EXPLOSION_IMAGES = []
number_of_files = len([name for name in os.listdir(explosion_folder) if os.path.isfile(os.path.join(explosion_folder, name))])
for i in range(1, number_of_files + 1):
    filename = 'E000{}.png'.format(i)
    EXPLOSION_IMAGES.append(filename)

DOOR_IMAGES = []
number_of_files = len([name for name in os.listdir(doors_folder) if os.path.isfile(os.path.join(doors_folder, name))])
for i in range(0, number_of_files):
    filename = 'door{}.png'.format(i)
    DOOR_IMAGES.append(filename)

DOOR_BREAK_IMAGES = []
number_of_files = len([name for name in os.listdir(door_break_folder) if os.path.isfile(os.path.join(door_break_folder, name))])
for i in range(0, number_of_files):
    filename = 'door{}.png'.format(i)
    DOOR_BREAK_IMAGES.append(filename)

ITEM_IMAGES = []
number_of_files = len([name for name in os.listdir(items_folder) if os.path.isfile(os.path.join(items_folder, name))])
for i in range(0, number_of_files):
    filename = 'item{}.png'.format(i)
    ITEM_IMAGES.append(filename)

WEAPON_IMAGES = []
number_of_files = len([name for name in os.listdir(weapons_folder) if os.path.isfile(os.path.join(weapons_folder, name))])
for i in range(0, number_of_files):
    filename = 'weapon{}.png'.format(i)
    WEAPON_IMAGES.append(filename)

HAT_IMAGES = []
number_of_files = len([name for name in os.listdir(hats_folder) if os.path.isfile(os.path.join(hats_folder, name))]) #This line counts the number of files in the folder so I can just drop new files into the folder without modifying the code.
for i in range(0, number_of_files):
    filename = 'hat{}.png'.format(i)
    HAT_IMAGES.append(filename)

HAIR_IMAGES = []
number_of_files = len([name for name in os.listdir(hair_folder) if os.path.isfile(os.path.join(hair_folder, name))])
for i in range(0, number_of_files):
    filename = 'hair{}.png'.format(i)
    HAIR_IMAGES.append(filename)

TOP_IMAGES = []
number_of_files = len([name for name in os.listdir(tops_folder) if os.path.isfile(os.path.join(tops_folder, name))])
for i in range(0, number_of_files):
    filename = 'top{}.png'.format(i)
    TOP_IMAGES.append(filename)

BOTTOM_IMAGES = []
number_of_files = len([name for name in os.listdir(bottoms_folder) if os.path.isfile(os.path.join(bottoms_folder, name))])
for i in range(0, number_of_files):
    filename = 'bottom{}.png'.format(i)
    BOTTOM_IMAGES.append(filename)

SHOE_IMAGES = []
number_of_files = len([name for name in os.listdir(shoes_folder) if os.path.isfile(os.path.join(shoes_folder, name))])
for i in range(0, number_of_files):
    filename = 'shoe{}.png'.format(i)
    SHOE_IMAGES.append(filename)

GLOVE_IMAGES = []
number_of_files = len([name for name in os.listdir(gloves_folder) if os.path.isfile(os.path.join(gloves_folder, name))])
for i in range(0, number_of_files):
    filename = 'glove{}.png'.format(i)
    GLOVE_IMAGES.append(filename)

MAGIC_IMAGES = []
number_of_files = len([name for name in os.listdir(magic_folder) if os.path.isfile(os.path.join(magic_folder, name))])
for i in range(0, number_of_files):
    filename = 'magic{}.png'.format(i)
    MAGIC_IMAGES.append(filename)

ENCHANTMENT_IMAGES = []
number_of_files = len([name for name in os.listdir(enchantments_folder) if os.path.isfile(os.path.join(enchantments_folder, name))])
for i in range(0, number_of_files):
    filename = 'enchantment{}.png'.format(i)
    ENCHANTMENT_IMAGES.append(filename)

GENDER_IMAGES = []
number_of_files = len([name for name in os.listdir(gender_folder) if os.path.isfile(os.path.join(gender_folder, name))])
for i in range(0, number_of_files):
    filename = 'gender{}.png'.format(i)
    GENDER_IMAGES.append(filename)

RACE_IMAGES = []
number_of_files = len([name for name in os.listdir(race_folder) if os.path.isfile(os.path.join(race_folder, name))])
for i in range(0, number_of_files):
    filename = 'race{}.png'.format(i)
    RACE_IMAGES.append(filename)

CORPSE_IMAGES = []
number_of_files = len([name for name in os.listdir(corpse_folder) if os.path.isfile(os.path.join(corpse_folder, name))])
for i in range(0, number_of_files):
    filename = 'corpse{}.png'.format(i)
    CORPSE_IMAGES.append(filename)

LOADING_SCREEN_IMAGES = []
number_of_files = len([name for name in os.listdir(loading_screen_folder) if os.path.isfile(os.path.join(loading_screen_folder, name))])
for i in range(0, number_of_files):
    filename = 'screen{}.png'.format(i)
    LOADING_SCREEN_IMAGES.append(filename)

VEHICLES_IMAGES = []
number_of_files = len([name for name in os.listdir(vehicles_folder) if os.path.isfile(os.path.join(vehicles_folder, name))])
for i in range(0, number_of_files):
    filename = 'vehicle{}.png'.format(i)
    VEHICLES_IMAGES.append(filename)

COLOR_SWATCH_IMAGES = []
number_of_files = len([name for name in os.listdir(color_swatches_folder) if os.path.isfile(os.path.join(color_swatches_folder, name))])
for i in range(0, number_of_files):
    filename = 'swatch{}.png'.format(i)
    COLOR_SWATCH_IMAGES.append(filename)

LIGHT_MASK_IMAGES = []
number_of_files = len([name for name in os.listdir(light_masks_folder) if os.path.isfile(os.path.join(light_masks_folder, name))])
for i in range(0, number_of_files):
    filename = 'light{}.png'.format(i)
    LIGHT_MASK_IMAGES.append(filename)

# Bullet Images
BULLET_IMG = path.join(img_folder, 'bullet.png')
BLUELASER_IMG = path.join(img_folder, 'laserBlue.png')

# Hit Rects
EXPLOSION_HIT_RECT = pg.Rect(0, 0, 128, 128)
FIREBALL_HIT_RECT = pg.Rect(0, 0, 20, 20)
SMALL_HIT_RECT = pg.Rect(0, 0, 40, 40)
MEDIUM_HIT_RECT = pg.Rect(0, 0, 80, 80)
LARGE_HIT_RECT = pg.Rect(0, 0, 128, 128)
XLARGE_HIT_RECT = pg.Rect(0, 0, 200, 200)

# Mob settings
MOB_SPEEDS = [150, 100, 75, 125]
MOB_ROT_SPEED = 200
MOB_HIT_RECT = pg.Rect(0, 0, 60, 60)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
MOB_HEALTH_BAR_LENGTH = 80
MOB_HEALTH_SHOW_TIME = 1000
AVOID_RADIUS = 50
DETECT_RADIUS = 400

DAMAGE_RATE = 100

# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
FLASH_DURATION = 50
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (400, 400)
EXPLODE_LIGHT_RADIUS = (500, 500)
FIRE_LIGHT_RADIUS = (800, 800)
FIREBALL_LIGHT_RADIUS = (300, 300)
LIGHT_MASK = "light_350_med.png"
SQUARE_LIGHT_MASK = 'light_square.png'
MAX_DARKNESS = 180
DIRECTIONAL_LIGHTS = [3, 5]
# This is a list of items and weapons that are light sources:
LIGHTS_LIST = []
for x in ITEMS:
    if 'brightness' in ITEMS[x]:
        LIGHTS_LIST.append(x)
for x in WEAPONS:
    if 'brightness' in WEAPONS[x]:
        LIGHTS_LIST.append(x)

NON_GUN_LIGHTS = []
for x in WEAPONS:
    if not WEAPONS[x]['gun']:
        if 'brightness' in WEAPONS[x]:
            NON_GUN_LIGHTS.append(x)

# Layers
WALL_LAYER = 7
ITEMS_LAYER = 8
MOB_LAYER = 9
PLAYER_LAYER = 10
VEHICLE_LAYER = 11
BULLET_LAYER = 12
ROOF_LAYER = 13
EFFECTS_LAYER = 14
SKY_LAYER = 15

# Music
TITLE_MUSIC = 'WendaleAbbey.ogg'
BG_MUSIC = 'Cloudforest_Awakening.ogg'
OCEAN_MUSIC = 'Eternal Renewal.ogg'
BEACH_MUSIC = 'Emerald Paradise.ogg'
ICEBEACH_MUSIC = 'Emerald Paradise.ogg'
ANT_TUNNEL_MUSIC = 'The Road Ahead.ogg'
CAVE_MUSIC = 'The Road Ahead.ogg'
FOREST_MUSIC = 'Light from the Shadows.ogg'
GRASSLAND_MUSIC = 'The Forgotten Age.ogg'
TOWN_MUSIC = 'Last Haven.ogg'
ZOMBIELAND_MUSIC = 'DarkWinds.ogg'
TUNDRA_MUSIC = 'Tales and Tidings.ogg'
MOUNTAIN_MUSIC = 'Cloudforest_Awakening.ogg'
DESERT_MUSIC = 'Eternal Renewal.ogg'

# Sounds
LOCK_PICKING_SOUNDS = ['pick_lock1.ogg', 'pick_lock2.ogg', 'pick_lock3.ogg', 'pick_lock4.ogg']
MALE_PLAYER_HIT_SOUNDS = ['pain/8.ogg', 'pain/9.ogg', 'pain/10.ogg', 'pain/11.ogg', 'pain/12.ogg', 'pain/13.ogg']
FEMALE_PLAYER_HIT_SOUNDS = ['pain/f8.ogg', 'pain/f9.ogg', 'pain/f10.ogg', 'pain/f11.ogg', 'pain/f12.ogg', 'pain/f13.ogg']
FEMALE_PLAYER_VOICE = {'out of ammo': ['exasperation.ogg', 'out_ammo1.ogg', 'out_ammo2.ogg', 'out_ammo3.ogg', 'no_bullets.ogg', 'need_bullets.ogg', 'need_bullets2.ogg'], 'empty clip': ['empty1.ogg', 'empty2.ogg','empty3.ogg','empty4.ogg','need_bullets3.ogg', 'man.ogg', 'need_reload.ogg']}
MALE_PLAYER_VOICE = {'out of ammo': ['out_ammo1.ogg', 'out_ammo2.ogg', 'out_ammo3.ogg', ], 'empty clip': ['empty1.ogg']}
ZOMBIE_MOAN_SOUNDS = ['brains2.ogg', 'brains3.ogg', 'zombie-roar-1.ogg', 'zombie-roar-2.ogg',
                      'zombie-roar-3.ogg', 'zombie-roar-5.ogg', 'zombie-roar-6.ogg', 'zombie-roar-7.ogg']
ZOMBIE_HIT_SOUNDS = ['splat-15.ogg']
WRAITH_SOUNDS = ['wraith1.ogg', 'wraith2.ogg', 'wraith3.ogg', 'wraith4.ogg']
EFFECTS_SOUNDS = {'eat': 'eat.ogg', 'door close': 'door_close.ogg', 'door open': 'door_open.ogg', 'charge': 'charge.ogg', 'bow reload': 'bow reload.ogg', 'level_start': 'Day_1_v2_mod.ogg', 'click': 'click.ogg', 'fanfare': 'fanfare.ogg', 'rustle': 'rustle.ogg', 'pickaxe': 'pickaxe.ogg', 'rocks': 'rocks.ogg', 'rock_hit': 'rock_hit.ogg', 'fart': 'fart.ogg', 'pee': 'pee.ogg', 'toilet': 'toilet.ogg',
                  'health_up': 'health_pack.ogg', 'casting healing': 'casting_healing.ogg', 'page turn': 'page_turn.ogg',
                  'gun_pickup': 'gun_pickup.ogg', 'jump': 'jump.ogg', 'tank': 'tank.ogg', 'tank engine': 'tank_engine.ogg','splash': 'splash.ogg', 'grass': 'grass.ogg', 'swim': 'swim.ogg', 'shallows': 'shallows.ogg', 'climb': 'climb.ogg', 'unlock': 'unlock.ogg', 'lock click': 'lock_click.ogg', 'fire blast': 'fire_blast.ogg', 'knock':
                  'knock.ogg', 'metal hit': 'metal_hit.ogg', 'anvil': 'anvil.ogg', 'scrape': 'scrape.ogg', 'grindstone': 'grindstone.ogg', 'hammering': 'hammering.ogg', 'snore': 'snore.ogg', 'cashregister': 'cashregister.ogg', 'alchemy': 'alchemy.ogg', 'enchant': 'enchant.ogg', 'fire crackle': 'fire_crackling.ogg'}

PUNCH_SOUNDS = []
for i in range(0, 10):
    PUNCH_SOUNDS.append('punch'+ str(i+1) + '.ogg')

# Body mods/characteristics are stored in the players inventory like items. This just makes it way easier to customize them and give them attributes
GENDER = {}
GENDER['female'] = {'armor': 1,
                              'image': 1}
GENDER['male'] = {'armor': 1,
                              'image': 0}
GENDER['other'] = {'armor': 1,
                              'image': 2}
RACE = {}
RACE['osidine'] = {'armor': 1, 'image': 0, 'start map': (27, 39), 'start pos': (23, 41),
                   'start_stats': {'health': 100, 'max health': 100, 'stamina': 100, 'max stamina': 100, 'magica': 100, 'max magica': 100, 'hunger': 100, 'max hunger': 100, 'weight': 0, 'max weight': 100, 'strength': 2, 'agility': 1.5, 'armor': 0, 'kills': 0, 'marksmanship hits': 0, 'marksmanship shots fired': 0, 'marksmanship accuracy': 0, 'melee': 0, 'hits taken': 0, 'exercise': 0, 'healing': 0, 'stamina regen': 0, 'magica regen': 0, 'looting': 0, 'casting': 0, 'lock picking': 0, 'smithing': 0},
                   'description': 'The Osidines are descendants of the ancients who fought along side the dragons of Zhara for the liberation of Arroshay during the great war. They specialize in the construction of armor and melee weapons.'}
RACE['shaktele'] = {'armor': 1, 'image': 9, 'start map': (64, 17), 'start pos': (32, 52),
                    'start_stats': {'health': 100, 'max health': 100, 'stamina': 100, 'max stamina': 100, 'magica': 100, 'max magica': 100, 'hunger': 100, 'max hunger': 100, 'weight': 0, 'max weight': 100, 'strength': 2.2, 'agility': 1, 'armor': 0, 'kills': 0, 'marksmanship hits': 0, 'marksmanship shots fired': 0, 'marksmanship accuracy': 0, 'melee': 0, 'hits taken': 0, 'exercise': 0, 'healing': 0, 'stamina regen': 0, 'magica regen': 0, 'looting': 0, 'casting': 0, 'lock picking': 0, 'smithing': 0},
                    'description': 'The Shaktele are a technologically advanced race that live in a modernized post-apocalyptic land created by biological warfare gone wrong. They specialize in the usage and construction of firearms and advanced weaponry.'}
RACE['elf'] = {'armor': 1, 'image': 2, 'start map': (36, 31), 'start pos': (29, 34),
               'start_stats': {'health': 90, 'max health': 90, 'stamina': 120, 'max stamina': 120, 'magica': 120, 'max magica': 120, 'hunger': 120, 'max hunger': 120, 'weight': 0, 'max weight': 75, 'strength': 1, 'agility': 2, 'armor': 0, 'kills': 0, 'marksmanship hits': 0, 'marksmanship shots fired': 0, 'marksmanship accuracy': 0, 'melee': 0, 'hits taken': 0, 'exercise': 0, 'healing': 0, 'stamina regen': 0.2, 'magica regen': 0.2, 'looting': 0, 'casting': 0, 'lock picking': 0, 'smithing': 0},
                'description': 'The elves of Arroshay live in harmony with the forces of nature. Animals are less fearful of elves and usually only attack them if provoked.'}
RACE['immortui'] = {'armor': 1, 'image': 1, 'start map': (27, 40), 'start pos': (30, 34),
                    'start_stats': {'health': 200, 'max health': 200, 'stamina': 60, 'max stamina': 60, 'magica': 100, 'max magica': 100, 'hunger': 110, 'max hunger': 110, 'weight': 0, 'max weight': 90, 'strength': 1, 'agility': 0.5, 'armor': 0, 'kills': 0, 'marksmanship hits': 0, 'marksmanship shots fired': 0, 'marksmanship accuracy': 0, 'melee': 0, 'hits taken': 0, 'exercise': 0, 'healing': 0, 'stamina regen': 0, 'magica regen': 0, 'looting': 0, 'casting': 0, 'lock picking': 0, 'smithing': 0},
                    'description': 'The Immortui are the undead either raised from the grave by dark magic or created in biological warfare gone wrong. They are slow but hard to kill and have the advantage of not attracting the attention of other Immortui.'}
RACE['lacertolian'] = {'armor': 20, 'image': 3, 'start map': (145, 44), 'start pos': (32, 26),
                       'start_stats': {'health': 120, 'max health': 120, 'stamina': 110, 'max stamina': 110, 'magica': 90, 'max magica': 90, 'hunger': 200, 'max hunger': 200, 'weight': 0, 'max weight': 125, 'strength': 2.5, 'agility': 2, 'armor': 0, 'kills': 0, 'marksmanship hits': 0, 'marksmanship shots fired': 0, 'marksmanship accuracy': 0, 'melee': 0, 'hits taken': 0, 'exercise': 0, 'healing': 0.5, 'stamina regen': 2, 'magica regen': 0, 'looting': 0, 'casting': 0, 'lock picking': 0, 'smithing': 0},
                        'description': 'The Lacertolians are a peaceful people who are expert mariners. They can go for long periods without eating, have naturally armored skin and are immune to venom.'}
RACE['miewdra'] = {'armor': 4, 'image': 4, 'start map': (89, 48), 'start pos': (15, 43),
                   'start_stats': {'health': 95, 'max health': 95, 'stamina': 150, 'max stamina': 150, 'magica': 105, 'max magica': 105, 'hunger': 100, 'max hunger': 100, 'weight': 0, 'max weight': 90, 'strength': 1, 'agility': 2.5, 'armor': 0, 'kills': 0, 'marksmanship hits': 0, 'marksmanship shots fired': 0, 'marksmanship accuracy': 0, 'melee': 0, 'hits taken': 0, 'exercise': 0, 'healing': 0, 'stamina regen': 1, 'magica regen': 0, 'looting': 0, 'casting': 0, 'lock picking': 0, 'smithing': 0},
                    'description': 'The Miewdra live near Arroshay\'s north pole. They are resistant to cold, have high stamina, and can run quickly.'}
RACE['mechanima'] = {'armor': 35, 'image': 5, 'start map': (126, 21), 'start pos': (45, 44),
                     'start_stats': {'health': 110, 'max health': 110, 'stamina': 100, 'max stamina': 100, 'magica': 70, 'max magica': 70, 'hunger': 1, 'max hunger': 1, 'weight': 0, 'max weight': 200, 'strength': 3.5, 'agility': 1.2, 'armor': 0, 'kills': 0, 'marksmanship hits': 0, 'marksmanship shots fired': 0, 'marksmanship accuracy': 0, 'melee': 0, 'hits taken': 0, 'exercise': 0, 'healing': 0, 'stamina regen': 0.2, 'magica regen': 0, 'looting': 0, 'casting': 0, 'lock picking': 0, 'smithing': 0},
                    'description': 'The Mechanima are the remnants of an advanced race who were driven into extinction who were able to preserve their souls in robot bodies. They are strong, naturally armored, immune to poison, and recharged by energy attacks. They do not need to eat, but can.'}
RACE['blackwraith'] = {'armor': 0, 'image': 8, 'start map': (53, 75), 'start pos': (17, 10),
                       'start_stats': {'health': 300, 'max health': 300, 'stamina': 150, 'max stamina': 150, 'magica': 150, 'max magica': 150, 'hunger': 1, 'max hunger': 1, 'weight': 0, 'max weight': 50, 'strength': 0.2, 'agility': 1, 'armor': 0, 'kills': 0, 'marksmanship hits': 0, 'marksmanship shots fired': 0, 'marksmanship accuracy': 0, 'melee': 0, 'hits taken': 0, 'exercise': 0, 'healing': 2, 'stamina regen': 0, 'magica regen': 2, 'looting': 0, 'casting': 0, 'lock picking': 0, 'smithing': 0},
                        'description': 'Black wraiths are disembodied practitioners of dark magic. They are immune to unenchanted melee weapons, bullets, cannot eat, and can walk through walls when not carrying any weight.'}
RACE['whitewraith'] = {'armor': 0, 'image': 7, 'start map': (59, 64), 'start pos': (40, 38),
                       'start_stats': {'health': 200, 'max health': 200, 'stamina': 160, 'max stamina': 160, 'magica': 220, 'max magica': 220, 'hunger': 1, 'max hunger': 1, 'weight': 0, 'max weight': 50, 'strength': 0.1, 'agility': 1, 'armor': 0, 'kills': 0, 'marksmanship hits': 0, 'marksmanship shots fired': 0, 'marksmanship accuracy': 0, 'melee': 0, 'hits taken': 0, 'exercise': 0, 'healing': 2, 'stamina regen': 0, 'magica regen': 2.5, 'looting': 0, 'casting': 0, 'lock picking': 0, 'smithing': 0},
                        'description': 'White wraiths are disembodied practitioners of white magic. They are immune to unenchanted melee weapons, bullets, cannot eat, and can walk through walls when not carrying any weight.'}
RACE['skeleton'] = {'armor': 12, 'image': 6, 'start map': (27, 40), 'start pos': (32, 30),
                    'start_stats': {'health': 50, 'max health': 50, 'stamina': 50, 'max stamina': 50, 'magica': 300, 'max magica': 300, 'hunger': 1, 'max hunger': 1, 'weight': 0, 'max weight': 60, 'strength': 2, 'agility': 1, 'armor': 0, 'kills': 0, 'marksmanship hits': 0, 'marksmanship shots fired': 0, 'marksmanship accuracy': 0, 'melee': 0, 'hits taken': 0, 'exercise': 0, 'healing': 4, 'stamina regen': 4, 'magica regen': 4, 'looting': 0, 'casting': 0, 'lock picking': 0, 'smithing': 0},
                    'description': 'Skeletons are undead beings who are reanimated by magic. They cannot eat, and are immune to poison and magic attacks'}
RACE['osidinedragon'] = {'armor': 20, 'image': 0}
RACE['shakteledragon'] = {'armor': 20, 'image': 9}
RACE['elfdragon'] = {'armor': 20, 'image': 2}
RACE['immortuidragon'] = {'armor': 30, 'image': 1}
RACE['lacertoliandragon'] = {'armor': 40, 'image': 3}
RACE['miewdradragon'] = {'armor': 22, 'image': 4}
RACE['mechanimadragon'] = {'armor': 40, 'image': 5}
#RACE['blackwraithdragon'] = {'armor': 40, 'image': 8}
RACE['whitewraithdragon'] = {'armor': 40, 'image': 7}
RACE['skeletondragon'] = {'armor': 40, 'image': 6}

DEFAULT_INVENTORIES = {}
DEFAULT_INVENTORIES['male osidine'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': [None], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': ['orange decayed shirt M'], 'bottoms': ['jeans M'], 'gloves': [None], 'shoes': [None], 'gold': 0, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['female osidine'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': [None], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': ['violet decayed shirt F'], 'bottoms': ['grey yoga pants'], 'gloves': [None], 'shoes': [None], 'gold': 0, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['male shaktele'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': ['pistol'], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': ['grey tshirt M'], 'bottoms': ['jeans M'], 'gloves': [None], 'shoes': ['black combat'], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['female shaktele'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': ['pistol'], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': ['black racerback tank top'], 'bottoms': ['blue yoga pants'], 'gloves': [None], 'shoes': ['green combat'], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['male elf'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': [None], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': ['green tshirt M'], 'bottoms': ['leather leggings M'], 'gloves': [None], 'shoes': ['black combat'], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['female elf'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': [None], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': ['red elf dress top'], 'bottoms': ['leaf skirt'], 'gloves': [None], 'shoes': ['green combat'], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['male lacertolian'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': ['bronze mace'], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': [None], 'bottoms': ['leather leggings M'], 'gloves': [None], 'shoes': [None], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['female lacertolian'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': ['bronze mace'], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': ['red dress top'], 'bottoms': ['leather leggings F'], 'gloves': [None], 'shoes': [None], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['male immortui'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': ['bone club'], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': ['green decayed shirt M'], 'bottoms': ['jeans M'], 'gloves': [None], 'shoes': [None], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['female immortui'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': ['bone club'], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': ['blue decayed shirt F'], 'bottoms': ['jeans F'], 'gloves': [None], 'shoes': [None], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['male miewdra'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': ['miewdra blade'], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': [None], 'bottoms': ['leather leggings M'], 'gloves': [None], 'shoes': [None], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['female miewdra'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': ['miewdra blade'], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': ['blue dress top'], 'bottoms': ['red mini dress skirt'], 'gloves': [None], 'shoes': [None], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['male mechanima'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': ['mechanima blaster'], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': [None], 'bottoms': [None], 'gloves': [None], 'shoes': [None], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['female mechanima'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': ['mechanima blaster'], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': [None], 'bottoms': [None], 'gloves': [None], 'shoes': [None], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['male whitewraith'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': [None], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': [None], 'bottoms': [None], 'gloves': [None], 'shoes': [None], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['female whitewraith'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': [None], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': [None], 'bottoms': [None], 'gloves': [None], 'shoes': [None], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['male skeleton'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': [None], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': [None], 'bottoms': [None], 'gloves': [None], 'shoes': [None], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['female skeleton'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': [None], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': [None], 'bottoms': [None], 'gloves': [None], 'shoes': [None], 'gold': 25, 'items': ['Guide book to Arroshay'], 'magic': [None]}
DEFAULT_INVENTORIES['male blackwraith'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': [None], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': [None], 'bottoms': [None], 'gloves': [None], 'shoes': [None], 'gold': 25, 'items': [None], 'magic': ['demonic possession']}
DEFAULT_INVENTORIES['female blackwraith'] = {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': [None], 'hats': [None], 'hair': list(HAIR.keys()), 'tops': [None], 'bottoms': [None], 'gloves': [None], 'shoes': [None], 'gold': 25, 'items': [None], 'magic': ['demonic possession']}


ENCHANTMENTS = {}
ENCHANTMENTS['explosive'] = {'materials':{'gun powder':1, 'black crystal':1}, 'equip kind': ['weapons'], 'image': 3}
ENCHANTMENTS['fire spark'] = {'materials':{'flint stone':1, 'steel ingot':1, 'red crystal':1}, 'equip kind': ['weapons'], 'image': 0}
ENCHANTMENTS['electric spark'] = {'materials':{'dead rabbit':1, 'blue crystal':1, 'white crystal':1}, 'equip kind': ['weapons'], 'image': 1}
ENCHANTMENTS['dragon breath'] = {'materials':{'gun powder':1, 'red crystal':1, 'dragon spit':1}, 'equip kind': ['hats'], 'image': 7}
ENCHANTMENTS['reinforced health'] = {'materials':{'potion of major healing':1, 'red crystal':1}, 'equip kind': ['hats', 'tops', 'bottoms', 'gloves', 'shoes'], 'image': 4}
ENCHANTMENTS['reinforced stamina'] = {'materials':{'potion of major stamina':1, 'blue crystal':1}, 'equip kind': ['hats', 'tops', 'bottoms', 'gloves', 'shoes'], 'image': 5}
ENCHANTMENTS['reinforced magica'] = {'materials':{'potion of major magica':1, 'white crystal':1}, 'equip kind': ['hats', 'tops', 'bottoms', 'gloves', 'shoes'], 'image': 6}

#ENCHANTMENTS['dragon fire '] = {'materials':{'red crystal':10}, 'equip kind': ['weapons'], 'image': 2}
