from race_info import *
from color_palettes import *

HATS = {}
for color in CLOTHING_COLORS:
    HATS[color + ' baseball hat'] = {'armor': 1, 'image': 1, 'weight': 0.1, 'upgrade': {'leather': 1}, 'value': 10, 'color': CLOTHING_COLORS[color]}
for material in MATERIALS:
    HATS[material + ' crown'] = {'armor': 10 * MATERIALS[material]['hardness'], 'image': 0, 'weight': 0.3 * MATERIALS[material]['weight'], 'materials': {material + ' ingot': 2}, 'upgrade': {material + ' ingot': 1, 'green crystal': 1}, 'value': 100 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}
    HATS[material + ' guard helmet'] = {'armor': 15 * MATERIALS[material]['hardness'], 'image': 4, 'weight': 1 * MATERIALS[material]['weight'], 'materials': {material + ' ingot': 2, 'leather': 1}, 'upgrade': {material + ' ingot': 2}, 'value': 50 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}
    HATS[material + ' helmet'] = {'armor': 25 * MATERIALS[material]['hardness'], 'image': 6, 'weight': 2 * MATERIALS[material]['weight'], 'materials': {material + ' ingot': 3}, 'upgrade': {material + ' ingot': 2}, 'value': 250 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}
    HATS[material + ' paladin crown'] = {'armor': 30 * MATERIALS[material]['hardness'], 'image': 12, 'weight': 1.5 * MATERIALS[material]['weight'], 'value': 700 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}
    HATS[material + ' knight helmet'] = {'armor': 28 * MATERIALS[material]['hardness'], 'image': 7, 'weight': 3 * MATERIALS[material]['weight'], 'materials': {material + ' ingot': 3, 'leather': 1},  'upgrade': {material + ' ingot': 2}, 'value': 270 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}
HATS['white wizard cloak'] = {'armor': 3, 'image': 19, 'weight': 0.7, 'reinforce magica': 200, 'value': 1000}
HATS['blue cloak'] = {'armor': 3, 'image': 19, 'weight': 0.7, 'reinforce magica': 30, 'value': 200, 'color': CLOTHING_COLORS['blue']}
HATS['black cloak'] = {'armor': 3, 'image': 19, 'weight': 0.7, 'reinforce magica': 100, 'value': 800, 'color': CLOTHING_COLORS['black']}
HATS['cloak of invisibility'] = {'armor': 3, 'image': 19, 'weight': 0.7, 'reinforce magica': 50, 'property': 'invisibility', 'value': 10000, 'color': CLOTHING_COLORS['gold']}
HATS['red cloak'] = {'armor': 3, 'image': 19, 'weight': 0.7, 'reinforce magica': 70, 'value': 500, 'color': CLOTHING_COLORS['red']}
# unique images
HATS['The Golden Toupee'] = {'armor': 35, 'image': 14, 'weight': 3, 'value': 1200}
HATS['tactical helmet'] = {'armor': 20, 'image': 2, 'weight': 1.5, 'upgrade': {'steel ingot': 1}, 'value': 100}
HATS['military helmet'] = {'armor': 18, 'image': 3, 'weight': 0.9, 'value': 75}
HATS['royal guard helmet'] = {'armor': 18, 'image': 5, 'weight': 1.3, 'upgrade': {'steel ingot': 2}, 'value': 150}
HATS['skull helmet'] = {'armor': 15, 'image': 8, 'weight': 2, 'value': 150}
HATS['demon helmet'] = {'armor': 35, 'image': 9, 'weight': 4, 'value': 666}
HATS['dragon mask'] = {'armor': 30, 'image': 10, 'weight': 3, 'fire enhance': {'after effect': 'fire', 'damage': 20, 'life time': 1000, 'speed': 50, 'rate reduction': 300}, 'reinforce magica': 200, 'reinforce health': 200, 'reinforce stamina': 200, 'value': 1050}
HATS['elf hat'] = {'armor': 3, 'image': 11, 'weight': 0.2, 'reinforce magica': 20, 'value': 20}
HATS['ant helmet'] = {'armor': 30, 'image': 13, 'weight': 0.5, 'value': 550}
HATS['dark wizard cloak'] = {'armor': 3, 'image': 18, 'weight': 0.7, 'reinforce magica': 300, 'value': 3000}
HATS['turtle plate helmet'] = {'armor': 34, 'image': 17, 'weight': 3.5, 'materials': {'turtle shell plate': 4, 'leather': 1}, 'upgrade': {'steel ingot': 1, 'leather strips': 1}, 'value': 170}
HATS['dark wizard hood'] = {'armor': 3, 'image': 16, 'weight': 0.7, 'reinforce magica': 200, 'value': 3000}
HATS['aetherial helmet'] = {'armor': 25, 'reinforce magica': 25, 'reinforce stamina': 25, 'image': 15, 'gender': 'other', 'weight': 0, 'value': 1100, 'materials': {'demon dust': 2, 'ectoplasm': 2, 'sage': 1, 'blue crystal': 1}, 'upgrade': {'demon dust': 1, 'ectoplasm': 1}}

HAIR = {}
HAIR['long pony'] = {'races': ['osidine', 'shaktele', 'elf'], 'image': 1}
HAIR['long straight'] = {'races': ['osidine', 'shaktele', 'immortui'],'image': 8}
HAIR['long curly'] = {'races': ['osidine', 'shaktele'], 'image': 2}
HAIR['medium messy'] = {'races': ['osidine', 'shaktele', 'immortui'], 'image': 3}
HAIR['long side pony'] = {'races': ['osidine', 'shaktele', 'elf'], 'image': 6}
HAIR['short messy'] = {'races': ['osidine', 'shaktele', 'immortui'], 'image': 4}
HAIR['short'] = {'races': ['osidine', 'shaktele', 'elf', 'immortui'], 'image': 5}
HAIR['short combed'] = {'races': ['osidine', 'shaktele', 'elf', 'immortui'], 'image': 29}
HAIR['dreadlocks'] = {'races': ['osidine', 'shaktele', 'immortui'], 'image': 12}
HAIR['elf braids'] = {'races': ['elf'], 'image': 9}
HAIR['lizard horns'] = {'races': ['lacertolian'], 'image': 10}
HAIR['lizard spikes'] = {'races': ['lacertolian', 'demon'], 'image': 11}
HAIR['cat tufts'] = {'races': ['miewdra'], 'image': 13}
HAIR['frizzy cat'] = {'races': ['miewdra'], 'image': 14}
HAIR['fluffy cat'] = {'races': ['miewdra'], 'image': 15}
HAIR['long straight cat'] = {'races': ['miewdra'], 'image': 16}
HAIR['bald'] = {'races': ['osidine', 'shaktele', 'elf', 'lacertolian', 'miewdra', 'immortui', 'blackwraith', 'whitewraith', 'skeleton', 'demon', 'vadashay'], 'image': 0}
HAIR['ram horns'] = {'races': ['skeleton', 'demon'], 'image': 18}
HAIR['demon horns'] = {'races': ['skeleton', 'demon'], 'image': 19}
HAIR['short horns'] = {'races': ['skeleton', 'demon'], 'image': 20}
HAIR['long wraith'] = {'races': ['blackwraith', 'whitewraith'], 'image': 21}
HAIR['back strip lights'] = {'races': ['mechanima'], 'image': 22}
HAIR['two strip lights'] = {'races': ['mechanima'], 'image': 23}
HAIR['bug lights'] = {'races': ['mechanima'], 'image': 24}
HAIR['basic lights'] = {'races': ['mechanima'], 'image': 25}
HAIR['full LED skin'] = {'races': ['mechanima'], 'image': 26}
HAIR['light strips'] = {'races': ['mechanima'], 'image': 27}
HAIR['LED stripes'] = {'races': ['mechanima'], 'image': 28}
HAIR['beard'] = {'races': ['osidine', 'shaktele', 'elf', 'immortui'], 'image': 17}

# Makes a dictionary containing the hairstyles appropriate for each race.
#temp_race_list = ['demon', 'osidine', 'shaktele', 'elf', 'lacertolian', 'miewdra', 'immortui', 'mechanima', 'blackwraith', 'whitewraith', 'skeleton']
RACE_HAIR = {}
for race in RACE_TYPE_LIST:
    RACE_HAIR[race] = []
for item in HAIR:
    for race in RACE_TYPE_LIST:
        if race in HAIR[item]['races']:
            RACE_HAIR[race].append(item)

# Separates long and short hair styles into lists
SHORT_HAIR_LIST = []
MEDIUM_HAIR_LIST = []
LONG_HAIR_LIST = []
for item in HAIR:
    if ('osidine' in HAIR[item]['races']) or ('shaktele' in HAIR[item]['races']):
        if 'short' in item:
            SHORT_HAIR_LIST.append(item)
        if 'medium' in item:
            MEDIUM_HAIR_LIST.append(item)
        if 'long' in item:
            LONG_HAIR_LIST.append(item)

SHOES = {}
for material in MATERIALS:
    SHOES[material + ' boots'] = {'armor': 15 * MATERIALS[material]['hardness'], 'weight': 5 * MATERIALS[material]['weight'], 'image': 0, 'materials': {material + ' ingot': 2, 'leather': 2},  'upgrade': {material + ' ingot': 1, 'leather': 1}, 'value': 120 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}
    SHOES[material + ' mechanima boots'] = {'armor': 35 * MATERIALS[material]['hardness'], 'weight': 5.2 * MATERIALS[material]['weight'], 'image': 6, 'materials': {material + ' ingot': 2, 'machine screws': 2},  'upgrade': {material + ' ingot': 1, 'machine screws': 1}, 'value': 120 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}
SHOES['black combat'] = {'armor': 2, 'weight': 0.8, 'image': 1, 'materials': {'steel ingot': 1, 'leather': 2}, 'upgrade': {'leather': 1}, 'value': 45}
SHOES['green combat'] = {'armor': 2, 'weight': 0.8, 'image': 2, 'materials': {'steel ingot': 1, 'leather': 2}, 'upgrade': {'leather': 1}, 'value': 45}
SHOES['brown boots'] = {'armor': 1, 'weight': 0.3, 'image': 3, 'materials': {'leather': 2}, 'upgrade': {'leather': 1}, 'value': 5}
SHOES['demon boots'] = {'armor': 46, 'weight': 2.1, 'image': 5, 'value': 150}
SHOES['aetherial boots'] = {'armor': 16, 'reinforce magica': 16, 'reinforce stamina': 16, 'image': 4, 'gender': 'other', 'weight': 0, 'value': 960, 'materials': {'demon dust': 1, 'ectoplasm': 2, 'sage': 1, 'blue crystal': 1}, 'upgrade': {'demon dust': 1, 'ectoplasm': 1}}

GLOVES = {}
# This first part generates clothing items that have different colors for the same kind of item
for color in CLOTHING_COLORS:
    GLOVES[color + ' dress gloves'] = {'armor': 1, 'weight': 0.1, 'image': 3, 'color': CLOTHING_COLORS[color]}
for material in MATERIALS:
    GLOVES[material + ' gauntlets'] = {'armor': 12 * MATERIALS[material]['hardness'], 'weight': 4 * MATERIALS[material]['weight'], 'image': 0, 'materials': {material + ' ingot': 2, 'leather': 1}, 'upgrade': {material + ' ingot': 1, 'leather': 1}, 'value': 110 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}
    GLOVES[material + ' mechanima gauntlets'] = {'armor': 34 * MATERIALS[material]['hardness'], 'weight': 4.2 * MATERIALS[material]['weight'], 'image': 5, 'materials': {material + ' ingot': 3, 'machine screws': 2}, 'upgrade': {material + ' ingot': 2, 'machine screws': 1}, 'value': 110 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}
GLOVES['demon gauntlets'] = {'armor': 45, 'weight': 2, 'value': 666, 'image': 1}
GLOVES['leather gauntlets'] = {'armor': 5, 'weight': 0.4, 'image': 2, 'materials': {'leather': 2}, 'value': 55}
GLOVES['aetherial gauntlets'] = {'armor': 15, 'reinforce magica': 15, 'reinforce stamina': 15, 'image': 4, 'gender': 'other', 'weight': 0, 'value': 900, 'materials': {'demon dust': 1, 'ectoplasm': 2, 'sage': 1, 'blue crystal': 1}, 'upgrade': {'demon dust': 1, 'ectoplasm': 1}}


TOPS = {}
# This first part generates clothing items that have different colors for the same kind of item
for color in CLOTHING_COLORS:
    TOPS[color + ' tshirt M'] = {'armor': 1, 'image': 5, 'gender': 'male', 'weight': 0.4, 'value': 5, 'color': CLOTHING_COLORS[color]}
    TOPS[color + ' tshirt F'] = {'armor': 1, 'image': 14, 'gender': 'female', 'weight': 0.4, 'value': 5, 'color': CLOTHING_COLORS[color]}
    TOPS[color + ' decayed shirt F'] = {'armor': 1, 'image': 3, 'gender': 'female', 'weight': 0.4, 'value': 1, 'color': CLOTHING_COLORS[color]}
    TOPS[color + ' decayed shirt M'] = {'armor': 1, 'image': 4, 'gender': 'male', 'weight': 0.4, 'value': 1, 'color': CLOTHING_COLORS[color]}
    TOPS[color + ' dress top'] = {'armor': 1, 'image': 9, 'gender': 'female', 'weight': 0.2, 'value': 78, 'color': CLOTHING_COLORS[color]}
    TOPS[color + ' racerback tank top'] = {'armor': 2,'image': 1,'gender': 'female', 'weight': 0.3, 'value': 5, 'color': CLOTHING_COLORS[color]}
    TOPS[color + ' elf dress top'] = {'armor': 2, 'image': 10, 'gender': 'female', 'weight': 0.1, 'value': 55, 'color': CLOTHING_COLORS[color]}
# These are different colors but have different attributes for each color.
TOPS['blue mage robe top M'] = {'armor': 10, 'image': 12, 'gender': 'male', 'weight': 0.6, 'reinforce magica': 70, 'value': 70, 'color': CLOTHING_COLORS['blue']}
TOPS['blue mage robe top F'] = {'armor': 10, 'image': 11, 'gender': 'female', 'weight': 0.6, 'reinforce magica': 70, 'value': 70, 'color': CLOTHING_COLORS['blue']}
TOPS['red mage robe top M'] = {'armor': 8, 'image': 12, 'gender': 'male', 'weight': 0.6, 'reinforce magica': 50, 'value': 50, 'color': CLOTHING_COLORS['red']}
TOPS['red mage robe top F'] = {'armor': 8, 'image': 11, 'gender': 'female', 'weight': 0.6, 'reinforce magica': 50, 'value': 50, 'color': CLOTHING_COLORS['red']}
TOPS['black mage robe top M'] = {'armor': 38, 'image': 12, 'gender': 'male', 'weight': 0.6, 'reinforce magica': 150, 'value': 1000, 'color': CLOTHING_COLORS['black']}
TOPS['black mage robe top F'] = {'armor': 38, 'image': 11, 'gender': 'female', 'weight': 0.6, 'reinforce magica': 150, 'value': 1000, 'color': CLOTHING_COLORS['black']}
# These are generated based on the types of materials.
for material in MATERIALS:
    TOPS[material + ' guard armor'] = {'armor': 30 * MATERIALS[material]['hardness'], 'image': 15, 'gender': 'other', 'weight': 10 * MATERIALS[material]['weight'], 'materials': {material + ' ingot': 4, 'leather': 2}, 'upgrade': {material + ' ingot': 2, 'leather strips': 1}, 'value': 220 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}
    TOPS[material + ' plate armor'] = {'armor': 44 * MATERIALS[material]['hardness'], 'image': 0, 'gender': 'other', 'weight': 15 * MATERIALS[material]['weight'], 'materials': {material + ' ingot': 6, 'leather': 3}, 'upgrade': {material + ' ingot': 3, 'leather strips': 1}, 'value': 300 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}
    TOPS[material + ' knight armor'] = {'armor': 50 * MATERIALS[material]['hardness'], 'image': 16, 'gender': 'other', 'weight': 15 * MATERIALS[material]['weight'], 'materials': {material + ' ingot': 7, 'leather': 3}, 'upgrade': {material + ' ingot': 4, 'leather strips': 1}, 'value': 400 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}
    TOPS[material + ' mechanima armor'] = {'armor': 55 * MATERIALS[material]['hardness'], 'image': 22, 'gender': 'other', 'weight': 15 * MATERIALS[material]['weight'], 'materials': {material + ' ingot': 8, 'machine screws': 3}, 'upgrade': {material + ' ingot': 4, 'machine screws': 1}, 'value': 400 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}
# These have unique images
TOPS['aetherial armor'] = {'armor': 45, 'reinforce magica': 50, 'reinforce stamina': 50, 'image': 6, 'gender': 'other', 'weight': 0, 'value': 2100, 'materials': {'demon dust': 2, 'ectoplasm': 3, 'sage': 1, 'blue crystal': 2}, 'upgrade': {'blue crystal': 1, 'ectoplasm': 1}}
TOPS['gold plated royal armor'] = {'armor': 42, 'image': 2, 'gender': 'other', 'weight': 10, 'materials': {'bronze ingot': 1, 'gold ingot':2, 'steel ingot': 3, 'leather': 3}, 'upgrade': {'steel ingot': 1, 'gold ingot': 1, 'leather strips': 1}, 'value': 250}
TOPS['wedding dress top'] = {'armor': 1, 'image': 9, 'gender': 'female', 'weight': 0.3, 'value': 200}
TOPS['demon armor F'] = {'armor': 60, 'image': 17, 'gender': 'female', 'weight': 17, 'value': 2250}
TOPS['demon armor M'] = {'armor': 60, 'image': 18, 'gender': 'male', 'weight': 17, 'value': 2250}
TOPS['leather armor F'] = {'armor': 10, 'image': 19, 'gender': 'female', 'weight': 4, 'materials': {'leather': 4}, 'upgrade': {'leather': 2, 'leather strips': 1}, 'upgrade': {'steel ingot': 1, 'leather': 1}, 'value': 100}
TOPS['leather armor M'] = {'armor': 10, 'image': 20, 'gender': 'male', 'weight': 4, 'materials': {'leather': 4}, 'upgrade': {'leather': 2, 'leather strips': 1}, 'upgrade': {'steel ingot': 1, 'leather': 1}, 'value': 100}
TOPS['shaktele guard armor'] = {'armor': 25, 'image': 21, 'gender': 'other', 'weight': 7, 'materials': {'steel ingot': 2, 'leather': 3}, 'upgrade': {'steel ingot': 1, 'leather strips': 1, 'leather': 1}, 'value': 260}
TOPS['turtle plate armor'] = {'armor': 38, 'image': 13, 'gender': 'other', 'weight': 7, 'materials': {'turtle shell plate': 8, 'leather': 2}, 'upgrade': {'steel ingot': 2, 'leather strips': 1}, 'value': 360}
TOPS['melerous armor'] = {'armor': 38, 'image': 7, 'gender': 'male', 'weight': 0.6, 'reinforce magica': 150, 'value': 1000}

BOTTOMS = {}
# This first part generates clothing items that have different colors for the same kind of item
for color in CLOTHING_COLORS:
    BOTTOMS[color + ' yoga pants'] = {'armor': 1, 'image': 1, 'gender': 'female', 'weight': 0.5, 'value': 10, 'color': CLOTHING_COLORS[color]}
    BOTTOMS[color + ' fancy dress skirt'] = {'armor': 1, 'image': 4, 'gender': 'female', 'weight': 2, 'value': 100, 'color': CLOTHING_COLORS[color]}
    BOTTOMS[color + ' dress skirt'] = {'armor': 1, 'image': 6, 'gender': 'female', 'weight': 1, 'value': 110, 'color': CLOTHING_COLORS[color]}
    BOTTOMS[color + ' mini dress skirt'] = {'armor': 1, 'image': 7, 'gender': 'female', 'weight': 0.4, 'value': 80, 'color': CLOTHING_COLORS[color]}
# different colors have different properties
BOTTOMS['blue mage robe bottom'] = {'armor': 6, 'image': 0, 'gender': 'other', 'weight': 0.5, 'reinforce magica': 30, 'value': 40, 'color': CLOTHING_COLORS['blue']}
BOTTOMS['red mage robe bottom'] = {'armor': 4, 'image': 0, 'gender': 'other', 'weight': 0.5, 'reinforce magica': 30, 'value': 30, 'color': CLOTHING_COLORS['red']}
BOTTOMS['black mage robe bottom'] = {'armor': 24, 'image': 0, 'gender': 'other', 'weight': 0.5, 'reinforce magica': 100, 'value': 1000, 'color': CLOTHING_COLORS['black']}
for material in MATERIALS:
    BOTTOMS[material + ' chainmail leggings M'] = {'armor': 20 * MATERIALS[material]['hardness'], 'image': 9, 'gender': 'male', 'weight': 8 * MATERIALS[material]['weight'], 'materials': {material + ' ingot': 4}, 'upgrade': {material + ' ingot': 2}, 'value': 150 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}
    BOTTOMS[material + ' chainmail leggings F'] = {'armor': 20 * MATERIALS[material]['hardness'], 'image': 8, 'gender': 'female', 'weight': 8 * MATERIALS[material]['weight'], 'materials': {material + ' ingot': 4}, 'upgrade': {material + ' ingot': 2}, 'value': 150 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}
    BOTTOMS[material + ' mechanima plated leggings'] = {'armor': 42 * MATERIALS[material]['hardness'], 'image': 13, 'gender': 'other', 'weight': 10 * MATERIALS[material]['weight'], 'materials': {material + ' ingot': 5, 'machine screws': 3}, 'upgrade': {material + ' ingot': 2, 'machine screws': 1}, 'value': 150 * MATERIALS[material]['value'], 'color': MATERIALS[material]['color']}

# Unique images per item
BOTTOMS['jeans M'] = {'armor': 1, 'image': 3, 'gender': 'male', 'weight': 0.6, 'value': 12}
BOTTOMS['jeans F'] = {'armor': 1, 'image': 2, 'gender': 'female', 'weight': 0.6, 'value': 12}
BOTTOMS['wedding dress skirt'] = {'armor': 1, 'image': 4, 'gender': 'female', 'weight': 3, 'value': 500}
BOTTOMS['leaf skirt'] = {'armor': 2, 'image': 5, 'gender': 'female', 'weight': 0.4, 'value': 55}
BOTTOMS['leather leggings M'] = {'armor': 10, 'image': 11, 'gender': 'male', 'weight': 1, 'materials': {'leather': 4}, 'upgrade': {'leather': 2, 'leather strips': 1}, 'value': 90}
BOTTOMS['leather leggings F'] = {'armor': 10, 'image': 10, 'gender': 'female', 'weight': 1, 'materials': {'leather': 4}, 'upgrade': {'leather': 2, 'leather strips': 1}, 'value': 90}
BOTTOMS['aetherial chainmail'] = {'armor': 22, 'reinforce magica': 15, 'reinforce stamina': 15, 'image': 12, 'gender': 'other', 'weight': 0, 'value': 1200, 'materials': {'demon dust': 2, 'ectoplasm': 3, 'sage': 1, 'blue crystal': 2}, 'upgrade': {'demon dust': 1, 'ectoplasm': 1}}

MALE_TOPS = []
for top in TOPS:
    if TOPS[top]['gender'] in ['male', 'other']:
        MALE_TOPS.append(top)
MALE_BOTTOMS = []
for bottom in BOTTOMS:
    if BOTTOMS[bottom]['gender'] in ['male', 'other']:
        MALE_BOTTOMS.append(bottom)

FEMALE_TOPS = []
for top in TOPS:
    if TOPS[top]['gender'] in ['female', 'other']:
        FEMALE_TOPS.append(top)
FEMALE_BOTTOMS = []
for bottom in BOTTOMS:
    if BOTTOMS[bottom]['gender'] in ['female', 'other']:
        FEMALE_BOTTOMS.append(bottom)


# Puts all dresses in a list
DRESS_TOPS_LIST = []
for item in TOPS:
    if 'dress' in item:
        DRESS_TOPS_LIST.append(item)
DRESS_BOTTOMS_LIST = []
for item in BOTTOMS:
    if 'dress' in item:
        DRESS_BOTTOMS_LIST.append(item)

CASUAL_TOPS_LIST = DRESS_TOPS_LIST.copy()
for item in TOPS:
    if 'tshirt' in item:
        CASUAL_TOPS_LIST.append(item)
    if 'tank top' in item:
        CASUAL_TOPS_LIST.append(item)
CASUAL_BOTTOMS_LIST = ['grey yoga pants', 'blue yoga pants', 'jeans M', 'jeans F', 'blue dress skirt', 'red mini dress skirt', 'green mini dress skirt', 'leather leggings M', 'leather leggings F']

IMMORTUI_TOPS = []
for item in TOPS:
    if 'decayed' in item:
        IMMORTUI_TOPS.append(item)

UPGRADED_HATS = {}
UPGRADED_TOPS = {}
UPGRADED_GLOVES = {}
UPGRADED_BOTTOMS = {}
UPGRADED_SHOES = {}
