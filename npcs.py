from settings import *
from random import choice, randrange
from armor import *
from character_positions import *

# Stores
BLACKSMITH_STORE = {'markup': 1.5, 'pvalue': 0.8, 'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['steel broadsword', 'iron dagger'], 'hats': ['steel helmet'], 'hair': [None], 'tops': ['leather armor M', 'leather armor F'], 'bottoms': ['leather leggings M', 'leather leggings F'], 'shoes': ['steel boots'], 'gloves': ['steel gauntlets'], 'gold': 0, 'items': ['steel ingot', 'iron ingot', 'gold ingot', 'silver ingot', 'charcoal', 'wood block', 'leather', 'leather strips'], 'magic': [None]}}
LACERTOLIAN_BLACKSMITH_STORE = {'markup': 1, 'pvalue': 0.8, 'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['bronze mace', 'iron dagger'], 'hats': ['steel helmet'], 'hair': [None], 'tops': ['leather armor M', 'leather armor F'], 'bottoms': ['leather leggings M', 'leather leggings F'], 'shoes': ['steel boots'], 'gloves': ['steel gauntlets'], 'gold': 0, 'items': ['bronze ingot', 'iron ingot', 'copper ingot', 'brass ingot', 'charcoal', 'wood block', 'leather', 'leather strips'], 'magic': [None]}}
ELF_BLACKSMITH_STORE = {'markup': 1.5, 'pvalue': 0.8, 'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['steel dagger', 'iron dagger'], 'hats': ['steel helmet', 'elf hat'], 'hair': [None], 'tops': ['leather armor M', 'leather armor F'], 'bottoms': ['leather leggings M', 'leather leggings F'], 'shoes': ['steel boots'], 'gloves': ['steel gauntlets'], 'gold': 0, 'items': ['steel ingot', 'iron ingot', 'gold ingot', 'silver ingot', 'charcoal', 'wood block', 'leather', 'leather strips'], 'magic': [None]}}
SHAKTELE_BLACKSMITH_STORE = {'markup': 1.5, 'pvalue': 0.8, 'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['pistol', 'grenade launcher', 'mini gun', 'auto grenade launcher', 'shotgun', 'assault rifle'], 'hats': ['tactical helmet', 'military helmet'], 'hair': [None], 'tops': ['shaktele guard armor', 'leather armor M', 'leather armor F'], 'bottoms': ['leather leggings M', 'leather leggings F'], 'shoes': ['steel boots', 'black combat'], 'gloves': ['steel gauntlets', 'leather gauntlets'], 'gold': 0, 'items': ['steel ingot', 'iron ingot', 'aluminum', 'brass ingot', 'lead ingot', 'charcoal', 'gun powder', 'wood block', 'leather', 'leather strips'], 'magic': [None]}}
MIEWDRA_BLACKSMITH_STORE = {'markup': 1.5, 'pvalue': 0.8, 'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['miewdra blade', 'steel dagger'], 'hats': ['steel helmet'], 'hair': [None], 'tops': ['leather armor M', 'leather armor F'], 'bottoms': ['leather leggings M', 'leather leggings F'], 'shoes': ['steel boots'], 'gloves': ['steel gauntlets'], 'gold': 0, 'items': ['steel ingot', 'iron ingot', 'copper ingot', 'brass ingot', 'gold ingot', 'silver ingot', 'charcoal', 'wood block', 'leather', 'leather strips'], 'magic': [None]}}
MECHANIMA_BLACKSMITH_STORE = {'markup': 1.5, 'pvalue': 0.8, 'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['steel broadsword', 'steel dagger', 'mechanima blaster'], 'hats': ['tactical helmet'], 'hair': [None], 'tops': ['steel guard armor', 'steel plate armor', 'leather armor M', 'leather armor F'], 'bottoms': ['steel chainmail leggings M', 'steel chainmail leggings F', 'leather leggings M', 'leather leggings F'], 'shoes': ['steel boots'], 'gloves': ['steel gauntlets'], 'gold': 0, 'items': ['steel ingot', 'iron ingot', 'aluminum ingot', 'machine screws', 'springs', 'copper ingot', 'brass ingot', 'bronze ingot', 'large laser ammo module', 'medium laser ammo module', 'gold ingot', 'silver ingot', 'charcoal', 'wood block', 'leather', 'leather strips'], 'magic': [None]}}
TAMOLIN_STORE = {'markup': 1.2, 'pvalue': 0.7, 'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': ['red cloak', 'blue cloak', 'black cloak'], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 0, 'items': ['potion of moderate healing', 'potion of major healing', 'potion of moderate stamina', 'potion of moderate magica', 'empty bottle', 'yarrow', 'sulphur', 'potassium nitrate crystals', 'charcoal', 'red crystal', 'yellow crystal', 'green crystal', 'elementary healing tome', 'fire spray tome', 'fireball tome', 'book of basic enchantments'], 'magic': [None]}}
DANGERMAN_STORE = {'markup': 0.2, 'pvalue': 0.1, 'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 0, 'items': ['lock pick'], 'magic': [None]}}
FELIUS_STORE = {'markup': 2, 'pvalue': 0.5, 'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 0, 'items': ['wolf skin', 'deer skin', 'leather'], 'magic': [None]}}
KEVIN_STORE = {'markup': 2.5, 'pvalue': 0.9, 'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 0, 'items': ['distilled alcohol', 'squid ink', 'candle', 'potion of major healing', 'gun powder', 'charcoal', 'surphur', 'potassium nitrate crystals'], 'magic': [None]}}
ANNA_STORE = {'markup': 1.2, 'pvalue': 0.1, 'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 0, 'items': ['carrot', 'horse bridle'], 'magic': [None]}}
LIZ_STORE = {'markup': 1.2, 'pvalue': 0.7, 'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': ['red cloak'], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 0, 'items': ['potion of moderate healing', 'potion of major healing', 'potion of moderate stamina', 'potion of moderate magica', 'empty bottle', 'yarrow', 'charcoal', 'red crystal', 'blue crystal', 'green crystal', 'elementary healing tome', 'fireball tome', 'clay', 'cut wood', 'squid ink', 'squid eye', 'spider venom'], 'magic': [None]}}
MAX_STORE = {'markup': 1.1, 'pvalue': 0, 'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 0, 'items': ['potion of moderate healing', 'potion of major healing', 'potion of moderate stamina', 'potion of moderate magica', 'distilled alcohol', 'ale', 'bottled water', 'ale of the gods'], 'magic': [None]}}
CINDY_STORE = {'markup': 1.2, 'pvalue': 0, 'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 0, 'items': ['potion of moderate healing', 'potion of major healing', 'potion of moderate stamina', 'potion of moderate magica', 'distilled alcohol', 'ale', 'bottled water', 'ale of the gods', 'roasted chicken', 'roasted bluefish', 'french bread', 'baked potato', 'chicken soup'], 'magic': [None]}}


NPC_TYPE_LIST = ['people', 'animals']
# NPCs Settings
PEOPLE = {}
# Agression variable is used to determine the behavior of NPC when detected and attacked. awd = attack when detected, awp = attack when provoked, fwp = flee when provoked, fwd = flee when detected, fup = flee until provoked, sap = stationary then aggressive when provoked
PEOPLE['generic'] = {'name': 'generic', 'protected': True, 'health': 100, 'touch damage': False, 'damage': 0, 'knockback': 2, 'walk speed': (90, 100), 'run speed': 300, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['walls', 'lava'],
    'gender': 'male', 'race': 'osidine',
    'colors':  {'hair': DEFAULT_HAIR_COLOR, 'skin': DEFAULT_SKIN_COLOR}, 'dialogue': None, 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': list(WEAPONS.keys()), 'hats': list(HATS.keys()), 'hair': list(HAIR.keys()), 'tops': list(TOPS.keys()), 'bottoms': list(BOTTOMS.keys()), 'shoes': list(SHOES.keys()), 'gloves': list(GLOVES.keys()), 'gold': 100, 'items': list(ITEMS.keys()), 'magic': list(MAGIC.keys())},
    'animations': {None}}
PEOPLE['melerous'] = {'name': 'Melerous', 'dead': False, 'protected': False, 'health': 100, 'touch damage': True, 'damage': 10, 'knockback': 0, 'walk speed': (75, 150), 'run speed': 200, 'detect radius': 500, 'avoid radius': 10, 'aggression': 'awd', 'armed': False, 'dual wield': False,
    'collide': [],
    'gender': 'male', 'race': 'blackwraith',
    'colors':  {'hair': DEFAULT_HAIR_COLOR, 'skin': BLACK}, 'dialogue': None, 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['karang'], 'hats': ['dark wizard hood'], 'hair': [None], 'tops': ['melerous armor'], 'bottoms': ['steel chainmail leggings M'], 'shoes': ['demon boots'], 'gloves': ['demon gauntlets'], 'gold': 0, 'items': ['random BLACKWRAITH_'], 'magic': ['fireball']},
    'animations': {None}}
PEOPLE['vadashay'] = {'name': 'Vadashay', 'protected': False, 'health': 100, 'touch damage': True, 'damage': 10, 'knockback': 20, 'walk speed': (75, 150), 'run speed': 200, 'detect radius': 600, 'avoid radius': 100, 'aggression': 'awd', 'armed': False, 'dual wield': False,
    'collide': ['walls'],
    'gender': 'random', 'race': 'vadashay',
    'colors':  {'hair': DEFAULT_HAIR_COLOR, 'skin': DEFAULT_SKIN_COLOR}, 'dialogue': None, 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 100, 'items': ['dead bluefish'], 'magic': [None]},
    'animations': {None}}
PEOPLE['demon'] = {'name': 'demon', 'protected': False, 'health': 666, 'touch damage': True, 'damage': 10, 'knockback': 20, 'walk speed': (100, 150), 'run speed': 260, 'detect radius': 650, 'avoid radius': 100, 'aggression': 'awd', 'armed': True, 'dual wield': False,
    'collide': ['walls'],
    'gender': 'random', 'race': 'demon',
    'colors':  {'hair': DEFAULT_HAIR_COLOR, 'skin': DEFAULT_SKIN_COLOR}, 'dialogue': None, 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['random DEMON_'], 'hats': ['random DEMON_'], 'hair': ['random DEMON_'], 'tops': ['random DEMON_'], 'bottoms': ['random DEMON_'], 'shoes': [None], 'gloves': ['random DEMON_'], 'gold': 666, 'items': ['random DEMON_'], 'magic': [None]},
    'animations': {None}}

DEMON_HATS = [None, 'demon helmet']
DEMON_HAIR = RACE_HAIR['demon']
DEMON_GLOVES = [None, 'demon gauntlets']
DEMON_TOPS = [None, 'demon armor M', 'demon armor F']
DEMON_BOTTOMS = [None, 'leather leggings M', 'steel chainmail leggings M']
DEMON_WEAPONS = [None, 'ancient viking sword', 'bone club', 'steel mace', 'grenade launcher', 'auto grenade launcher', 'shotgun']
DEMON_ITEMS = [None, 'charcoal', 'charcoal', 'sulphur', 'sulphur', 'sulphur', 'sulphur', 'jar', 'empty bottle', 'potion of major magica', 'sheep horn', 'gun powder']
PEOPLE['clay golem guard'] = {'name': 'clay golem Guard', 'protected': False, 'health': 400, 'touch damage': False, 'damage': 50, 'knockback': 50, 'walk speed': (70, 100), 'run speed': 200, 'detect radius': 700, 'avoid radius': 100, 'aggression': 'awp', 'armed': False, 'dual wield': False,
    'collide': ['walls'],
    'gender': 'random', 'race': 'golem',
    'colors':  {'hair': DEFAULT_HAIR_COLOR, 'skin': DEFAULT_SKIN_COLOR}, 'dialogue': None, 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 300, 'items': ['clay', 'clay', 'clay', 'clay'], 'magic': [None]},
    'animations': {None}}
PEOPLE['ice golem'] = {'name': 'ice golem', 'protected': False, 'health': 400, 'touch damage': False, 'damage': 50, 'knockback': 50, 'walk speed': (70, 100), 'run speed': 200, 'detect radius': 700, 'avoid radius': 100, 'aggression': 'awd', 'armed': False, 'dual wield': False,
    'collide': ['walls'],
    'gender': 'random', 'race': 'icegolem',
    'colors':  {'hair': DEFAULT_HAIR_COLOR, 'skin': DEFAULT_SKIN_COLOR}, 'dialogue': None, 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 300, 'items': ['living water', 'living water', 'living water', 'living water'], 'magic': [None]},
    'animations': {None}}
PEOPLE['goblin'] = {'name': 'goblin', 'protected': False, 'health': 200, 'touch damage': False, 'damage': 10, 'knockback': 5, 'walk speed': (100, 200), 'run speed': 300, 'detect radius': 700, 'avoid radius': 100, 'aggression': 'awd', 'armed': True, 'dual wield': False,
    'collide': ['walls'],
    'gender': 'random', 'race': 'goblin',
    'colors':  {'hair': DEFAULT_HAIR_COLOR, 'skin': DEFAULT_SKIN_COLOR}, 'dialogue': None, 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['random SKELETON_'], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 100, 'items': ['random SKELETON_'], 'magic': [None]},
    'animations': {None}}
PEOPLE['goblin king'] = {'name': 'Tronold Grump', 'dead': False, 'protected': False, 'health': 10000, 'touch damage': False, 'damage': 100, 'knockback': 20, 'walk speed': (50, 75), 'run speed': 90, 'detect radius': 400, 'avoid radius': 80, 'aggression': 'sap', 'armed': True, 'dual wield': False,
    'collide': ['walls', 'water'],
    'gender': 'male', 'race': 'goblin',
    'colors':  {'hair': DEFAULT_HAIR_COLOR, 'skin': DEFAULT_SKIN_COLOR}, 'dialogue': 'GOBLIN_KING_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['live goldfish'], 'hats': ['The Golden Toupee'], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 1000000000, 'items': [None], 'magic': [None]},
    'animations': {None}}
PEOPLE['goblin guard'] = {'name': 'Goblin Guard', 'protected': True, 'health': 350, 'touch damage': False, 'damage': 15, 'knockback': 10, 'walk speed': (90, 100), 'run speed': 160, 'detect radius': 200, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['walls', 'water'],
    'gender': 'random', 'race': 'goblin',
    'colors':  {'hair': DEFAULT_HAIR_COLOR, 'skin': DEFAULT_SKIN_COLOR}, 'dialogue': 'random GUARD_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['bone club'], 'hats': ['skull helmet'], 'hair': [None], 'tops': ['iron plate armor'], 'bottoms': ['leather leggings M'], 'shoes': [None], 'gloves': [None], 'gold': 250, 'items': ['random'], 'magic': [None]},
    'animations': {None}}
PEOPLE['goblin slave'] = {'name': 'slave', 'protected': True, 'health': 100, 'touch damage': False, 'damage': 0, 'knockback': 2, 'walk speed': (90, 100), 'run speed': 300, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'fwp', 'armed': False, 'dual wield': False,
    'collide': ['walls', 'lava'],
    'gender': 'random', 'race': 'random HUMAN_RACES',
    'colors':  {'hair': 'random COLOR_PALETTE', 'skin': 'random HUMAN_SKIN_TONES'}, 'dialogue': 'random GOBLIN_SLAVE_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': [None], 'hair': ['random'], 'tops': ['random VILLAGER_'], 'bottoms': ['random VILLAGER_'], 'shoes': ['random'], 'gloves': [None], 'gold': 100, 'items': ['random'], 'magic': [None]},
    'animations': {None}}
HUMAN_RACES = ['shaktele', 'osidine']
PEOPLE['immortui'] = {'name': 'Immortui', 'protected': False, 'health': 100, 'touch damage': True, 'damage': 10, 'knockback': 20, 'walk speed': (75, 150), 'run speed': 200, 'detect radius': 600, 'avoid radius': 80, 'aggression': 'awd', 'armed': False, 'dual wield': False,
    'collide': ['obstacles'],
    'gender': 'random', 'race': 'immortui',
    'colors':  {'hair': 'random COLOR_PALETTE', 'skin': 'random IMMORTUI_SKIN_TONES'}, 'dialogue': 'random IMMORTUI_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': [None], 'hair': ['random IMMORTUI_'], 'tops': ['random IMMORTUI_'], 'bottoms': ['random IMMORTUI_'], 'shoes': ['random'], 'gloves': [None], 'gold': 100, 'items': ['random IMMORTUI_'], 'magic': [None]},
    'animations': {'walk': ZOMBIE_WALK}}
IMMORTUI_HAIR = ['medium messy', 'short messy']
IMMORTUI_BOTTOMS = CASUAL_BOTTOMS_LIST
IMMORTUI_ITEMS = ['zombie extract', 'zombie extract', 'zombie extract', 'zombie extract', 'zombie extract', 'charcoal', 'charcoal', 'sulphur', 'cheese wedge', 'potato', 'garlic', 'empty bottle', 'jar', 'potion of minor magica', 'potion of minor healing', 'potion of minor stamina']
PEOPLE['blackwraith'] = {'name': 'black wraith', 'protected': False, 'health': 100, 'touch damage': True, 'damage': 10, 'knockback': 0, 'walk speed': (75, 150), 'run speed': 200, 'detect radius': 500, 'avoid radius': 10, 'aggression': 'awd', 'armed': False, 'dual wield': False,
    'collide': [],
    'gender': 'random', 'race': 'blackwraith',
    'colors':  {'hair': 'random  BLACKWRAITH_SKIN_TONES', 'skin': 'random  BLACKWRAITH_SKIN_TONES'}, 'dialogue': None, 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 0, 'items': ['random BLACKWRAITH_'], 'magic': ['fireball']},
    'animations': {'walk': ZOMBIE_WALK}}
BLACKWRAITH_ITEMS = ['demon dust', 'ectoplasm']
PEOPLE['whitewraith'] = {'name': 'white wraith', 'protected': False, 'health': 100, 'touch damage': True, 'damage': 10, 'knockback': 0, 'walk speed': (75, 150), 'run speed': 200, 'detect radius': 500, 'avoid radius': 300, 'aggression': 'awd', 'armed': False, 'dual wield': False,
    'collide': [],
    'gender': 'random', 'race': 'whitewraith',
    'colors':  {'hair': 'random  WHITEWRAITH_SKIN_TONES', 'skin': 'random  WHITEWRAITH_SKIN_TONES'}, 'dialogue': None, 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 0, 'items': ['random BLACKWRAITH_'], 'magic': [None]},
    'animations': {'walk': ZOMBIE_WALK}}
PEOPLE['skeleton'] = {'name': 'skeleton', 'protected': False, 'health': 300, 'touch damage': False, 'damage': 10, 'knockback': 5, 'walk speed': (100, 200), 'run speed': 300, 'detect radius': 700, 'avoid radius': 150, 'aggression': 'awd', 'armed': True, 'dual wield': False,
    'collide': ['walls', 'water'],
    'gender': 'random', 'race': 'skeleton',
    'colors':  {'hair': 'random  SKELETON_SKIN_TONES', 'skin': 'random  SKELETON_SKIN_TONES'}, 'dialogue': None, 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['random SKELETON_'], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 100, 'items': ['random SKELETON_'], 'magic': [None]},
    'animations': {None}}
SKELETON_WEAPONS = ['ancient viking sword', 'bone club', 'ancient viking battleaxe']
SKELETON_ITEMS = ['charcoal', 'charcoal', 'sulphur', 'sulphur', 'sulphur', 'sulphur', 'jar', 'empty bottle', 'yarrow', 'sheep horn', 'gun powder']

PEOPLE['lafonda'] = {'name': 'Lafonda the Blacksmith', 'dead': False, 'protected': True, 'health': 500, 'touch damage': False, 'damage': 30, 'knockback': 10, 'walk speed': (90, 100), 'run speed': 160, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['obstacles'],
    'gender': 'female', 'race': 'osidine',
    'colors':  {'hair': COLOR_PALETTE[10], 'skin': OSIDINE_SKIN_TONES[3]}, 'dialogue': 'BLACKSMITH_DLG', 'store': BLACKSMITH_STORE,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['smithing hammer', 'lantern'], 'hats': [None], 'hair': ['long pony'], 'tops': ['black racerback tank top'], 'bottoms': ['leather leggings F'], 'shoes': ['brown boots'], 'gloves': ['leather gauntlets'], 'gold': randrange(100, 1000), 'items': ['dewcastle blacksmith chest key'], 'magic': [None]},
    'animations': {None}}
PEOPLE['tamolin'] = {'name': 'Tamolin the Mage', 'dead': False, 'quest': 'Ant eggs for Tamolin', 'protected': True, 'health': 550, 'touch damage': False, 'damage': 25, 'knockback': 10, 'walk speed': (90, 100), 'run speed': 160, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['obstacles'],
    'gender': 'male', 'race': 'shaktele',
    'colors':  {'hair': COLOR_PALETTE[20], 'skin': SHAKTELE_SKIN_TONES[8]}, 'dialogue': 'TAMOLIN_DLG', 'store': TAMOLIN_STORE,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['lantern', 'bronze mace'], 'hats': ['red cloak'], 'hair': ['short'], 'tops': ['blue mage robe top M'], 'bottoms': ['blue mage robe bottom'], 'shoes': ['brown boots'], 'gloves': [None], 'gold': randrange(100, 1000), 'items': ['random'], 'magic': [None]},
    'animations': {None}}
PEOPLE['kimmy'] = {'name': 'Kimmy', 'dead': False, 'protected': True,'health': 1000, 'touch damage': False, 'damage': 15, 'knockback': 1, 'walk speed': (300, 400), 'run speed': 400, 'detect radius': 200, 'avoid radius': 100, 'aggression': 'fwp', 'armed': True, 'dual wield': False,
    'collide': ['walls'],
    'gender': 'female', 'race': 'elf',
    'colors':  {'hair': COLOR_PALETTE[3], 'skin': OSIDINE_SKIN_TONES[2]}, 'dialogue': 'KIMMY_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['lantern'], 'hats': [None], 'hair': ['long straight'], 'tops': ['fuchsia tshirt F'], 'bottoms': ['red mini dress skirt'], 'shoes': [None], 'gloves': [None], 'gold': randrange(100, 200), 'items': ['random'], 'magic': [None]},
    'animations': {'walk': RUNNING}}
PEOPLE['loella'] = {'name': 'Loella', 'dead': False, 'quest': 'A fish for Loella', 'protected': True,'health': 1000, 'touch damage': False, 'damage': 0, 'knockback': 1, 'walk speed': (200, 300), 'run speed': 400, 'detect radius': 200, 'avoid radius': 100, 'aggression': 'fwp', 'armed': True, 'dual wield': False,
    'collide': ['walls', 'water'],
    'gender': 'female', 'race': 'elf',
    'colors':  {'hair': COLOR_PALETTE[15], 'skin': OSIDINE_SKIN_TONES[4]}, 'dialogue': 'LOELLA_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': [None], 'hair': ['long straight'], 'tops': ['pink tshirt F'], 'bottoms': ['green mini dress skirt'], 'shoes': [None], 'gloves': [None], 'gold': randrange(100, 200), 'items': ['random'], 'magic': [None]},
    'animations': {None}}
PEOPLE['steve'] = {'name': 'Steve the Guard', 'dead': False, 'quest': 'A mace for Steve', 'protected': True, 'health': 100, 'touch damage': False, 'damage': 15, 'knockback': 10, 'walk speed': (90, 100), 'run speed': 160, 'detect radius': 200, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['walls', 'water'],
    'gender': 'male', 'race': 'osidine',
    'colors':  {'hair': COLOR_PALETTE[25], 'skin': OSIDINE_SKIN_TONES[8]}, 'dialogue': 'STEVE_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['lantern'], 'hats': [None], 'hair': ['short messy'], 'tops': ['steel guard armor'], 'bottoms': ['random GUARD_'], 'shoes': ['steel boots'], 'gloves': ['steel gauntlets'], 'gold': 12, 'items': ['baked potato', 'cheese wedge'], 'magic': [None]},
    'animations': {None}}
PEOPLE['anna'] = {'name': 'Anna the Stable Guard', 'dead': False, 'quest': None, 'protected': True, 'health': 100, 'touch damage': False, 'damage': 15, 'knockback': 10, 'walk speed': (90, 100), 'run speed': 160, 'detect radius': 400, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['walls', 'water'],
    'gender': 'female', 'race': 'osidine',
    'colors':  {'hair': COLOR_PALETTE[21], 'skin': OSIDINE_SKIN_TONES[10]}, 'dialogue': 'ANNA_DLG', 'store': ANNA_STORE,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['steel dagger', 'lantern'], 'hats': [None], 'hair': ['long pony'], 'tops': ['leather armor F'], 'bottoms': ['leather leggings F'], 'shoes': ['steel boots'], 'gloves': ['leather gauntlets'], 'gold': 12, 'items': ['cheese wedge', 'carrot'], 'magic': [None]},
    'animations': {None}}
PEOPLE['guard'] = {'name': 'Guard', 'protected': True, 'health': 600, 'touch damage': False, 'damage': 15, 'knockback': 10, 'walk speed': (90, 100), 'run speed': 160, 'detect radius': 200, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['walls', 'water'],
    'gender': 'random', 'race': 'osidine',
    'colors':  {'hair': 'random COLOR_PALETTE', 'skin': 'random OSIDINE_SKIN_TONES'}, 'dialogue': 'random GUARD_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['random GUARD_', 'lantern'], 'hats': ['random GUARD_'], 'hair': ['random'], 'tops': ['steel guard armor'], 'bottoms': ['random GUARD_'], 'shoes': ['steel boots'], 'gloves': ['random GUARD_'], 'gold': 250, 'items': ['random'], 'magic': [None]},
    'animations': {None}}
GUARD_WEAPONS = ['steel broadsword', 'steel mace']
GUARD_HATS = ['steel guard helmet', 'steel helmet']
GUARD_GLOVES = ['steel gauntlets', 'leather gauntlets']
GUARD_BOTTOMS = ['steel chainmail leggings F', 'leather leggings F', 'steel chainmail leggings M', 'leather leggings M']
PEOPLE['villager'] = {'name': 'Villager', 'protected': True, 'health': 100, 'touch damage': False, 'damage': 5, 'knockback': 2, 'walk speed': (90, 100), 'run speed': 300, 'detect radius': 200, 'avoid radius': 100, 'aggression': 'fwp', 'armed': False, 'dual wield': False,
    'collide': ['walls', 'lava'],
    'gender': 'random', 'race': 'osidine',
    'colors':  {'hair': 'random COLOR_PALETTE', 'skin': 'random OSIDINE_SKIN_TONES'}, 'dialogue': 'random VILLAGER_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['lantern'], 'hats': [None], 'hair': ['random'], 'tops': ['random VILLAGER_'], 'bottoms': ['random VILLAGER_'], 'shoes': ['random'], 'gloves': [None], 'gold': 100, 'items': ['random'], 'magic': [None]},
    'animations': {None}}
VILLAGER_TOPS = CASUAL_TOPS_LIST
VILLAGER_BOTTOMS = CASUAL_BOTTOMS_LIST

PEOPLE['shaktelevillager'] = {'name': 'Villager', 'protected': True, 'health': 100, 'touch damage': False, 'damage': 0, 'knockback': 2, 'walk speed': (90, 100), 'run speed': 300, 'detect radius': 200, 'avoid radius': 100, 'aggression': 'fwp', 'armed': False, 'dual wield': False,
    'collide': ['walls', 'lava'],
    'gender': 'random', 'race': 'shaktele',
    'colors':  {'hair': 'random COLOR_PALETTE', 'skin': 'random SHAKTELE_SKIN_TONES'}, 'dialogue': 'random VILLAGER_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['flashlight'], 'hats': [None], 'hair': ['random SHAKTELEVILLAGER_'], 'tops': ['random VILLAGER_'], 'bottoms': ['random VILLAGER_'], 'shoes': ['random'], 'gloves': [None], 'gold': 100, 'items': ['random'], 'magic': [None]},
    'animations': {None}}
SHAKTELEVILLAGER_HAIR = RACE_HAIR['shaktele']
PEOPLE['shaktele blacksmith'] = {'name': 'Hank the Blacksmith', 'protected': True, 'health': 100, 'touch damage': False, 'damage': 30, 'knockback': 10, 'walk speed': (90, 100), 'run speed': 160, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['obstacles'],
    'gender': 'male', 'race': 'shaktele',
    'colors':  {'hair': COLOR_PALETTE[18], 'skin': SHAKTELE_SKIN_TONES[3]}, 'dialogue': 'BLACKSMITH_DLG', 'store': SHAKTELE_BLACKSMITH_STORE,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['smithing hammer', 'lantern'], 'hats': [None], 'hair': ['dreadlocks'], 'tops': ['black tshirt M'], 'bottoms': ['leather leggings F'], 'shoes': ['brown boots'], 'gloves': ['leather gauntlets'], 'gold': randrange(100, 1000), 'items': ['random'], 'magic': [None]},
    'animations': {None}}

PEOPLE['shakteleguard'] = {'name': 'Guard', 'protected': True, 'health': 600, 'touch damage': False, 'damage': 15, 'knockback': 10, 'walk speed': (130, 140), 'run speed': 260, 'detect radius': 1000, 'avoid radius': 130, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['walls', 'water'],
    'gender': 'random', 'race': 'shaktele',
    'colors':  {'hair': 'random COLOR_PALETTE', 'skin': 'random SHAKTELE_SKIN_TONES'}, 'dialogue': 'random GUARD_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['assault rifle with light'], 'hats': ['tactical helmet'], 'hair': ['random'], 'tops': ['shaktele guard armor'], 'bottoms': ['random GUARD_'], 'shoes': ['black combat'], 'gloves': ['leather gauntlets'], 'gold': 250, 'items': ['random'], 'magic': [None]},
    'animations': {None}}

PEOPLE['kevin'] = {'name': 'Kevin', 'dead': False, 'protected': True, 'health': 100, 'touch damage': False, 'damage': 15, 'knockback': 10, 'walk speed': (100, 120), 'run speed': 260, 'detect radius': 450, 'avoid radius': 130, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['walls', 'water'],
    'gender': 'male', 'race': 'shaktele',
    'colors':  {'hair': COLOR_PALETTE[15], 'skin': SHAKTELE_SKIN_TONES[8]}, 'dialogue': 'KEVIN_DLG', 'store': KEVIN_STORE,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['steel dagger', 'lantern'], 'hats': [None], 'hair': ['dreadlocks'], 'tops': ['shaktele guard armor'], 'bottoms': ['leather leggings M'], 'shoes': ['black combat'], 'gloves': [None], 'gold': 200, 'items': ['random'], 'magic': [None]},
    'animations': {None}}

PEOPLE['miewdravillager'] = {'name': 'Miewdra Villager', 'protected': True, 'health': 100, 'touch damage': False, 'damage': 0, 'knockback': 2, 'walk speed': (90, 100), 'run speed': 300, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'fwp', 'armed': False, 'dual wield': False,
    'collide': ['walls', 'lava'],
    'gender': 'random', 'race': 'miewdra',
    'colors':  {'hair': 'random COLOR_PALETTE', 'skin': 'random COLOR_PALETTE'}, 'dialogue': 'random MIEWDRA_VILLAGER_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['lantern'], 'hats': [None], 'hair': ['random MIEWDRAVILLAGER_'], 'tops': ['random MIEWDRAVILLAGER_'], 'bottoms': ['random MIEWDRAVILLAGER_'], 'shoes': ['random'], 'gloves': [None], 'gold': 100, 'items': ['random'], 'magic': [None]},
    'animations': {None}}
MIEWDRAVILLAGER_TOPS = CASUAL_TOPS_LIST
MIEWDRAVILLAGER_BOTTOMS = CASUAL_BOTTOMS_LIST
MIEWDRAVILLAGER_HAIR = RACE_HAIR['miewdra']
PEOPLE['miewdra blacksmith'] = {'name': 'Purrcy the Blacksmith', 'dead': False, 'protected': True, 'health': 100, 'touch damage': False, 'damage': 30, 'knockback': 10, 'walk speed': (90, 100), 'run speed': 160, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['obstacles'],
    'gender': 'male', 'race': 'miewdra',
    'colors':  {'hair': MIEWDRA_SKIN_TONES[12], 'skin': MIEWDRA_SKIN_TONES[12]}, 'dialogue': 'BLACKSMITH_DLG', 'store': MIEWDRA_BLACKSMITH_STORE,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['smithing hammer', 'lantern'], 'hats': ['elf hat'], 'hair': ['cat tufts'], 'tops': ['leather armor M'], 'bottoms': ['leather leggings M'], 'shoes': ['brown boots'], 'gloves': ['leather gauntlets'], 'gold': randrange(100, 1000), 'items': ['random'], 'magic': [None]},
    'animations': {None}}
PEOPLE['felius'] = {'name': 'Felius', 'dead': False, 'quest': 'Fuel for Felius', 'protected': True, 'health': 1000, 'touch damage': False, 'damage': 50, 'knockback': 10, 'walk speed': (90, 100), 'run speed': 160, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['obstacles'],
    'gender': 'male', 'race': 'miewdra',
    'colors':  {'hair': MIEWDRA_SKIN_TONES[20], 'skin': MIEWDRA_SKIN_TONES[20]}, 'dialogue': 'FELIUS_DLG', 'store': FELIUS_STORE,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['miewdra blade', 'lantern'], 'hats': [None], 'hair': ['cat tufts'], 'tops': ['demon armor M'], 'bottoms': ['steel chainmail leggings M'], 'shoes': ['demon boots'], 'gloves': ['demon gauntlets'], 'gold': randrange(100, 1000), 'items': ['fireball tome'], 'magic': ['fireball']},
    'animations': {None}}
PEOPLE['catrina'] = {'name': 'Catrina', 'dead': False, 'protected': True, 'health': 100, 'touch damage': False, 'damage': 0, 'knockback': 2, 'walk speed': (90, 100), 'run speed': 300, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'fwp', 'armed': False, 'dual wield': False,
    'collide': ['walls', 'lava'],
    'gender': 'female', 'race': 'miewdra',
    'colors':  {'hair': MIEWDRA_SKIN_TONES[1], 'skin': MIEWDRA_SKIN_TONES[1]}, 'dialogue': 'CATRINA_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['lantern'], 'hats': [None], 'hair': ['long straight cat'], 'tops': ['red dress top'], 'bottoms': ['blue dress skirt'], 'shoes': ['brown boots'], 'gloves': [None], 'gold': 100, 'items': ['random'], 'magic': [None]},
    'animations': {None}}

PEOPLE['elfvillager'] = {'name': 'Elf Villager', 'protected': True, 'health': 100, 'touch damage': False, 'damage': 0, 'knockback': 2, 'walk speed': (90, 100), 'run speed': 300, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'fwp', 'armed': False, 'dual wield': False,
    'collide': ['walls', 'lava'],
    'gender': 'random', 'race': 'elf',
    'colors':  {'hair': 'random COLOR_PALETTE', 'skin': 'random ELF_SKIN_TONES'}, 'dialogue': 'random ELF_VILLAGER_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['lantern'], 'hats': [None], 'hair': ['random ELFVILLAGER_'], 'tops': ['random ELFVILLAGER_'], 'bottoms': ['random ELFVILLAGER_'], 'shoes': ['random'], 'gloves': [None], 'gold': 100, 'items': ['random'], 'magic': [None]},
    'animations': {None}}
ELFVILLAGER_HAIR = ['elf braids', 'short', 'long pony', 'long side pony']
ELFVILLAGER_TOPS = CASUAL_TOPS_LIST
ELFVILLAGER_BOTTOMS = CASUAL_BOTTOMS_LIST
PEOPLE['elf blacksmith'] = {'name': 'Nelf the Blacksmith', 'dead': False, 'protected': True, 'health': 100, 'touch damage': False, 'damage': 30, 'knockback': 10, 'walk speed': (90, 100), 'run speed': 160, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['obstacles'],
    'gender': 'female', 'race': 'elf',
    'colors':  {'hair': COLOR_PALETTE[17], 'skin': ELF_SKIN_TONES[2]}, 'dialogue': 'BLACKSMITH_DLG', 'store': ELF_BLACKSMITH_STORE,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['smithing hammer', 'lantern'], 'hats': ['elf hat'], 'hair': ['elf braids'], 'tops': ['black racerback tank top'], 'bottoms': ['leather leggings F'], 'shoes': ['brown boots'], 'gloves': ['leather gauntlets'], 'gold': randrange(100, 1000), 'items': ['random'], 'magic': [None]},
    'animations': {None}}

PEOPLE['elfqueen'] = {'name': 'Queen Zeladria', 'dead': False, 'protected': True, 'health': 200, 'touch damage': False, 'damage': 30, 'knockback': 10, 'walk speed': (100, 110), 'run speed': 200, 'detect radius': 500, 'avoid radius': 10, 'aggression': 'sap', 'armed': True, 'dual wield': False,
    'collide': ['obstacles'],
    'gender': 'female', 'race': 'elf',
    'colors':  {'hair': COLOR_PALETTE[1], 'skin': ELF_SKIN_TONES[1]}, 'dialogue': 'ELF_QUEEN_DLG', 'store': None,
    'osidine': {'colors':  {'hair': DEFAULT_HAIR_COLOR, 'skin': DEFAULT_SKIN_COLOR}, 'dialogue': 'ELF_QUEEN_OSIDINE_DLG', 'quest': "Give letter to Zeladria", 'active': True},
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['steel dagger', 'lantern'], 'hats': ['gold paladin crown'], 'hair': ['elf braids'], 'tops': ['wedding dress top'], 'bottoms': ['red mini dress skirt'], 'shoes': ['brown boots'], 'gloves': ['red dress gloves'], 'gold': randrange(100, 1000), 'items': ['random'], 'magic': [None]},
    'animations': {None}}

PEOPLE['elfguard'] = {'name': 'Elf Guard', 'protected': True, 'health': 600, 'touch damage': False, 'damage': 25, 'knockback': 10, 'walk speed': (90, 100), 'run speed': 160, 'detect radius': 200, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['walls', 'water'],
    'gender': 'random', 'race': 'elf',
    'colors':  {'hair': 'random COLOR_PALETTE', 'skin': 'random ELF_SKIN_TONES'}, 'dialogue': 'random ELF_GUARD_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['random GUARD_', 'lantern'], 'hats': [None], 'hair': ['random ELFVILLAGER_'], 'tops': ['steel guard armor'], 'bottoms': ['random GUARD_'], 'shoes': ['steel boots'], 'gloves': ['random GUARD_'], 'gold': 250, 'items': ['random'], 'magic': [None]},
    'animations': {None}}

PEOPLE['dangerman'] = {'name': 'Elron Dangerman', 'dead': False, 'protected': True, 'health': 800, 'touch damage': False, 'damage': 30, 'knockback': 10, 'walk speed': (20, 25), 'run speed': 160, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'sap', 'armed': True, 'dual wield': False,
    'collide': ['obstacles'],
    'gender': 'male', 'race': 'elf',
    'colors':  {'hair': COLOR_PALETTE[19], 'skin': OSIDINE_SKIN_TONES[7]}, 'dialogue': 'DANGERMAN_DLG', 'store': DANGERMAN_STORE,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['lantern'], 'hats': ['red cloak'], 'hair': ['beard'], 'tops': ['red mage robe top M'], 'bottoms': ['red mage robe bottom'], 'shoes': ['bronze boots'], 'gloves': [None], 'gold': randrange(1, 10), 'items': ['potato', 'lock pick'], 'magic': [None]},
    'animations': {None}}


PEOPLE['lacertolianvillager'] = {'name': 'Lacertolian Villager', 'protected': True, 'health': 100, 'touch damage': False, 'damage': 0, 'knockback': 2, 'walk speed': (90, 100), 'run speed': 300, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'fwp', 'armed': False, 'dual wield': False,
    'collide': ['walls', 'lava'],
    'gender': 'random', 'race': 'lacertolian',
    'colors':  {'hair': 'random LACERTOLIAN_SKIN_TONES', 'skin': 'random LACERTOLIAN_SKIN_TONES'}, 'dialogue': 'random LACERTOLIAN_VILLAGER_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['lantern'], 'hats': [None], 'hair': [None], 'tops': ['random VILLAGER_'], 'bottoms': ['random VILLAGER_'], 'shoes': ['random'], 'gloves': [None], 'gold': 100, 'items': ['random'], 'magic': [None]},
    'animations': {None}}
LACERTOLIANVILLAGER_TOPS = CASUAL_TOPS_LIST
LACERTOLIANVILLAGER_BOTTOMS = CASUAL_BOTTOMS_LIST
PEOPLE['lacertolian blacksmith'] = {'name': 'Wendell the Blacksmith', 'dead': False, 'protected': True, 'health': 100, 'touch damage': False, 'damage': 30, 'knockback': 10, 'walk speed': (90, 100), 'run speed': 160, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['obstacles'],
    'gender': 'male', 'race': 'lacertolian',
    'colors':  {'hair': LACERTOLIAN_SKIN_TONES[16], 'skin': LACERTOLIAN_SKIN_TONES[16]}, 'dialogue': 'BLACKSMITH_DLG', 'store': LACERTOLIAN_BLACKSMITH_STORE,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['smithing hammer', 'lantern'], 'hats': [None], 'hair': ['lizard spikes'], 'tops': ['leather armor M'], 'bottoms': ['leather leggings M'], 'shoes': [None], 'gloves': ['leather gauntlets'], 'gold': randrange(100, 1000), 'items': ['random'], 'magic': [None]},
    'animations': {None}}
PEOPLE['liz'] = {'name': 'Liz', 'protected': True, 'dead': False, 'health': 100, 'touch damage': False, 'damage': 20, 'knockback': 10, 'walk speed': (90, 100), 'run speed': 160, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['obstacles'],
    'gender': 'female', 'race': 'lacertolian',
    'colors':  {'hair': LACERTOLIAN_SKIN_TONES[10], 'skin': LACERTOLIAN_SKIN_TONES[10]}, 'dialogue': 'LIZ_DLG', 'store': LIZ_STORE,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['iron dagger', 'lantern'], 'hats': [None], 'hair': [None], 'tops': ['pink dress top'], 'bottoms': ['leather leggings F'], 'shoes': [None], 'gloves': [None], 'gold': randrange(100, 1000), 'items': ['random'], 'magic': ['fireball']},
    'animations': {None}}

PEOPLE['mechanima blacksmith'] = {'name': 'Minimus Prime the Blacksmith', 'dead': False, 'protected': True, 'health': 600, 'touch damage': False, 'damage': 30, 'knockback': 10, 'walk speed': (90, 100), 'run speed': 160, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['obstacles'],
    'gender': 'male', 'race': 'mechanima',
    'colors':  {'hair': MECHANIMA_SKIN_TONES[20], 'skin': MECHANIMA_SKIN_TONES[1]}, 'dialogue': 'BLACKSMITH_DLG', 'store': MECHANIMA_BLACKSMITH_STORE,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['smithing hammer'], 'hats': [None], 'hair': ['full LED skin'], 'tops': ['steel guard armor'], 'bottoms': ['steel chainmail leggings M'], 'shoes': ['black combat'], 'gloves': ['steel gauntlets'], 'gold': randrange(100, 1000), 'items': ['random'], 'magic': [None]},
    'animations': {None}}

PEOPLE['mech suit'] = {'name': 'Mech Suit', 'protected': False, 'health': 600, 'touch damage': False, 'damage': 60, 'knockback': 20, 'walk speed': (100, 110), 'run speed': 480, 'detect radius': 50, 'avoid radius': 10, 'aggression': 'sap', 'armed': True, 'dual wield': False,
    'collide': ['walls', 'water'],
    'gender': 'male', 'race': 'mech_suit',
    'colors':  {'hair': DEFAULT_HAIR_COLOR, 'skin': DEFAULT_SKIN_COLOR}, 'dialogue': None, 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': [None], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 0, 'items': ['machine screws', 'machine screws', 'steel pipe', 'aluminum rod', 'steel wire', 'steel ingot', 'steel ingot'], 'magic': [None]},
    'animations': {None}}

PEOPLE['occupied mech suit'] = {'name': 'Mech Guard', 'protected': True, 'health': 600, 'touch damage': False, 'damage': 60, 'knockback': 20, 'walk speed': (300, 310), 'run speed': 480, 'detect radius': 600, 'avoid radius': 30, 'aggression': 'sap', 'armed': True, 'dual wield': False,
    'collide': ['walls', 'water'],
    'gender': 'male', 'race': 'mech_suit',
    'colors':  {'hair': DEFAULT_HAIR_COLOR, 'skin': DEFAULT_SKIN_COLOR}, 'dialogue': None, 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': RACE_TYPE_LIST, 'weapons': ['mech peacekeeper'], 'hats': [None], 'hair': [None], 'tops': [None], 'bottoms': [None], 'shoes': [None], 'gloves': [None], 'gold': 0, 'items': ['machine screws', 'machine screws', 'steel pipe', 'aluminum rod', 'steel wire', 'steel ingot', 'steel ingot'], 'magic': [None]},
    'animations': {None}}

#Animation patterns:
BASIC3 = [1, 2, 3, 2]
FLY4 = [1, 2, 3, 4, 3, 2]
ANIMAL_ANIMATIONS = {}
ANIMAL_ANIMATIONS['garden lizard'] = {'walk': BASIC3}
ANIMAL_ANIMATIONS['goldfish'] = {'walk':[1, 4, 2, 3, 2, 4]}
ANIMAL_ANIMATIONS['bluefish'] = {'walk':[1, 4, 2, 3, 2, 4]}
ANIMAL_ANIMATIONS['leopard shark'] = {'walk':[1, 2, 3, 2, 1, 4, 5, 4]}
ANIMAL_ANIMATIONS['rabbit'] = {'walk':BASIC3, 'run': [2, 4, 5, 4]}
ANIMAL_ANIMATIONS['chicken'] = {'walk':BASIC3, 'run': [4, 5, 6, 5]}
ANIMAL_ANIMATIONS['pink moth'] = {'walk':BASIC3}
ANIMAL_ANIMATIONS['green moth'] = {'walk':BASIC3}
ANIMAL_ANIMATIONS['brown bird'] = {'walk':BASIC3}
ANIMAL_ANIMATIONS['giant ant'] = {'walk':[1, 2, 3, 2, 1, 4, 5, 6, 5, 4]}
ANIMAL_ANIMATIONS['queen ant'] = {'walk':[1, 2, 3, 2, 1, 4, 5, 6, 5, 4]}
ANIMAL_ANIMATIONS['butterfly ideopsis'] = {'walk':BASIC3}
ANIMAL_ANIMATIONS['sheep'] = {'walk':[1, 2, 3, 2, 1, 4, 5, 4]}
ANIMAL_ANIMATIONS['bighorn sheep'] = {'walk':[1, 2, 3, 2, 1, 4, 5, 4]}
ANIMAL_ANIMATIONS['snake'] = {'walk':[1, 2, 3, 4, 5, 6, 7, 8]}
ANIMAL_ANIMATIONS['horse'] = {'walk':[1, 2, 3, 2, 1, 5, 6, 5], 'run': [1, 2, 3, 4, 3, 2, 1, 5, 6, 7, 6, 5]}
ANIMAL_ANIMATIONS['spider'] = {'walk':BASIC3}
ANIMAL_ANIMATIONS['squid'] = {'walk':BASIC3}
ANIMAL_ANIMATIONS['flying goldfix'] = {'walk':BASIC3}
ANIMAL_ANIMATIONS['marlin'] = {'walk':BASIC3}
ANIMAL_ANIMATIONS['hawk'] = {'walk':BASIC3}
ANIMAL_ANIMATIONS['sea turtle'] = {'walk':BASIC3}
ANIMAL_ANIMATIONS['red wyvern'] = {'walk':FLY4}
ANIMAL_ANIMATIONS['blue wyvern'] = {'walk':FLY4}
ANIMAL_ANIMATIONS['dolphin'] = {'walk':[1, 2, 3, 4, 5, 6, 5, 4, 3, 2]}
ANIMAL_ANIMATIONS['sfix'] = {'walk':[1, 2, 3, 4, 5, 6, 7]}
ANIMAL_ANIMATIONS['pig'] = {'walk': BASIC3}

ANIMALS = {}
ANIMALS['garden lizard'] = {'name': 'garden lizard', 'corpse': None, 'mountable': False, 'touch damage': False, 'protected': False, 'hit rect': SMALL_HIT_RECT, 'grabable': True, 'run speed': 300, 'walk speed': 250, 'walk animate speed': 80, 'run animate speed': 180, 'detect radius': 500, 'avoid radius': 45,'aggression': 'fwd', 'health': 10, 'damage': 0, 'knockback': 0, 'item type': 'items', 'item': 'live garden lizard', 'dropped items': ['dead garden lizard'], 'collide': ['obstacles']}
ANIMALS['rabbit'] = {'name': 'rabbit', 'corpse': None, 'mountable': False, 'touch damage': False, 'protected': False, 'hit rect': SMALL_HIT_RECT, 'grabable': True, 'run speed': 400, 'walk speed': 100, 'walk animate speed': 400, 'run animate speed': 240, 'detect radius': 400, 'avoid radius': 100,'aggression': 'fwd', 'health': 10, 'damage': 0, 'knockback': 0, 'item type': 'weapons', 'item': 'live rabbit', 'dropped items': ['dead rabbit'], 'collide': ['obstacles']}
ANIMALS['chicken'] = {'name': 'chicken', 'corpse': None, 'mountable': False, 'touch damage': False, 'protected': True, 'hit rect': SMALL_HIT_RECT, 'grabable': True, 'run speed': 350, 'walk speed': 50, 'walk animate speed': 400, 'run animate speed': 200, 'detect radius': 300, 'avoid radius': 80, 'aggression': 'fwd', 'health': 20, 'damage': 0, 'knockback': 0, 'item type': 'weapons', 'item': 'live chicken', 'dropped items': ['dead chicken', 'feather', 'feather', 'feather'], 'collide': ['obstacles']}
ANIMALS['bighorn sheep'] = {'name': 'bighorn sheep', 'corpse': 1, 'mountable': False, 'climbing': True, 'touch damage': True, 'protected': False, 'hit rect': LARGE_HIT_RECT, 'grabable': False, 'run speed': 480, 'walk speed': 100, 'walk animate speed': 300, 'run animate speed': 120, 'detect radius': 300, 'avoid radius': 300,'aggression': 'fup', 'health': 100, 'damage': 8, 'knockback': 25, 'item type': 'items', 'item': 'sheep meat', 'dropped items': ['sheep meat', 'sheep skin', 'sheep horn', 'sheep horn'], 'collide': ['walls', 'water']}
ANIMALS['sheep'] = {'name': 'sheep', 'corpse': 3, 'mountable': True, 'touch damage': False, 'protected': True, 'hit rect': LARGE_HIT_RECT, 'grabable': False, 'run speed': 200, 'walk speed': 100, 'walk animate speed': 300, 'run animate speed': 200, 'detect radius': 300, 'avoid radius': 300,'aggression': 'fwd', 'health': 50, 'damage': 0, 'knockback': 0, 'item type': 'items', 'item': 'sheep meat', 'dropped items': ['sheep meat', 'sheep skin'], 'collide': ['obstacles']}
ANIMALS['horse'] = {'name': 'horse', 'corpse': 4, 'mountable': True, 'touch damage': False, 'protected': False, 'hit rect': LARGE_HIT_RECT, 'grabable': False, 'run speed': 480, 'walk speed': 100, 'walk animate speed': 300, 'run animate speed': 100, 'detect radius': 300, 'avoid radius': 300,'aggression': 'fwp', 'health': 280, 'damage': 8, 'knockback': 25, 'item type': 'items', 'item': 'sheep meat', 'dropped items': ['horse skin', 'horse meat'], 'collide': ['walls', 'water']}
ANIMALS['pig'] = {'name': 'pig', 'corpse': 20, 'mountable': True, 'touch damage': False, 'protected': True, 'hit rect': MEDIUM_HIT_RECT, 'grabable': False, 'run speed': 300, 'walk speed': 150, 'walk animate speed': 220, 'run animate speed': 200, 'detect radius': 300, 'avoid radius': 300,'aggression': 'fwd', 'health': 49, 'damage': 0, 'knockback': 0, 'item type': 'items', 'item': 'pig meat', 'dropped items': ['pig meat', 'pig skin'], 'collide': ['obstacles']}


ANIMALS['sfix'] = {'name': 'sfix', 'corpse': None, 'death action': 'explode', 'mountable': False, 'touch damage': False, 'protected': False, 'hit rect': LARGE_HIT_RECT, 'grabable': False, 'run speed': 200, 'walk speed': 180, 'walk animate speed': 180, 'run animate speed': 170, 'detect radius': 500, 'avoid radius': 200,'aggression': 'awd', 'health': 500, 'damage': 25, 'knockback': 0, 'item type': 'items', 'item': 'red crystal', 'dropped items': ['red crystal'], 'collide': ['obstacles'], 'magic': ['fireball']}


ANIMALS['red wyvern'] = {'name': 'red wyvern', 'flying': True, 'magic': ['fireball'], 'corpse': 13, 'mountable': False, 'touch damage': False, 'protected': False, 'hit rect': MEDIUM_HIT_RECT, 'grabable': False, 'run speed': 300, 'walk speed': 180, 'walk animate speed': 80, 'run animate speed': 60, 'detect radius': 500, 'avoid radius': 200,'aggression': 'awd', 'health': 260, 'damage': 0, 'knockback': 0, 'item type': 'items', 'item': 'live brown bird', 'dropped items': ['dragon spit', 'red wyvern skin', 'wyvern meat'], 'collide': ['walls']}
ANIMALS['blue wyvern'] = {'name': 'blue wyvern', 'flying': True, 'magic': ['fireball'], 'corpse': 12, 'mountable': False, 'touch damage': False, 'protected': False, 'hit rect': MEDIUM_HIT_RECT, 'grabable': False, 'run speed': 300, 'walk speed': 180, 'walk animate speed': 80, 'run animate speed': 60, 'detect radius': 500, 'avoid radius': 200,'aggression': 'awd', 'health': 260, 'damage': 0, 'knockback': 0, 'item type': 'items', 'item': 'live brown bird', 'dropped items': ['dragon spit', 'blue wyvern skin', 'wyvern meat'], 'collide': ['walls']}
ANIMALS['brown bird'] = {'name': 'brown bird', 'flying': True, 'corpse': None, 'mountable': False, 'touch damage': False, 'protected': False, 'hit rect': SMALL_HIT_RECT, 'grabable': True, 'run speed': 400, 'walk speed': 220, 'walk animate speed': 80, 'run animate speed': 60, 'detect radius': 200, 'avoid radius': 80,'aggression': 'fwd', 'health': 6, 'damage': 0, 'knockback': 0, 'item type': 'items', 'item': 'live brown bird', 'dropped items': ['dead brown bird', 'feather', 'feather'], 'collide': ['walls']}
ANIMALS['hawk'] = {'name': 'hawk', 'flying': True, 'corpse': None, 'mountable': False, 'touch damage': False, 'protected': False, 'hit rect': SMALL_HIT_RECT, 'grabable': False, 'run speed': 400, 'walk speed': 350, 'walk animate speed': 180, 'run animate speed': 160, 'detect radius': 600, 'avoid radius': 80,'aggression': 'fwd', 'health': 6, 'damage': 0, 'knockback': 0, 'item type': 'items', 'item': 'live brown bird', 'dropped items': ['dead hawk', 'feather', 'feather', 'feather'], 'collide': ['walls']}
ANIMALS['pink moth'] = {'name': 'pink moth', 'flying': True, 'corpse': None, 'mountable': False, 'touch damage': False, 'protected': False, 'hit rect': SMALL_HIT_RECT, 'grabable': True, 'run speed': 300, 'walk speed': 80, 'walk animate speed': 100, 'run animate speed': 80, 'detect radius': 200, 'avoid radius': 80,'aggression': 'fwd', 'health': 5, 'damage': 0, 'knockback': 0, 'item type': 'items', 'item': 'live pink moth', 'dropped items': ['dead pink moth'], 'collide': ['walls']}
ANIMALS['green moth'] = {'name': 'green moth', 'flying': True, 'corpse': None, 'mountable': False, 'touch damage': False, 'protected': False, 'hit rect': SMALL_HIT_RECT, 'grabable': True, 'run speed': 300, 'walk speed': 80, 'walk animate speed': 100, 'run animate speed': 80, 'detect radius': 200, 'avoid radius': 80,'aggression': 'fwd', 'health': 5, 'damage': 0, 'knockback': 0, 'item type': 'items', 'item': 'live green moth', 'dropped items': ['dead green moth'], 'collide': ['walls']}
ANIMALS['butterfly ideopsis'] = {'name': 'butterfly ideopsis', 'flying': True, 'corpse': None, 'mountable': False, 'touch damage': False, 'protected': False, 'hit rect': SMALL_HIT_RECT, 'grabable': True, 'run speed': 300, 'walk speed': 80, 'walk animate speed': 100, 'run animate speed': 80, 'detect radius': 200, 'avoid radius': 80,'aggression': 'fwd', 'health': 5, 'damage': 0, 'knockback': 0, 'item type': 'items', 'item': 'live butterfly ideopsis', 'dropped items': ['dead butterfly ideopsis'], 'collide': ['walls']}
ANIMALS['flying goldfix'] = {'name': 'flying goldfix', 'flying': True, 'corpse': None, 'mountable': False, 'touch damage': False, 'protected': False, 'hit rect': SMALL_HIT_RECT, 'grabable': True, 'run speed': 300, 'walk speed': 100, 'walk animate speed': 80, 'run animate speed': 70, 'detect radius': 200, 'avoid radius': 80,'aggression': 'fwd', 'health': 5, 'damage': 0, 'knockback': 0, 'item type': 'weapons', 'item': 'live goldfish', 'dropped items': ['dead goldfish'], 'collide': ['walls']}

ANIMALS['giant ant'] = {'name': 'giant ant', 'corpse': None, 'mountable': False, 'touch damage': True, 'protected': False, 'hit rect': SMALL_HIT_RECT, 'grabable': False, 'run speed': 400, 'walk speed': 100, 'walk animate speed': 150, 'run animate speed': 100, 'detect radius': 180, 'avoid radius': 60,'aggression': 'awd', 'health': 70, 'damage': 8, 'knockback': 2, 'item type': 'items', 'item': 'dead giant ant', 'dropped items': ['dead giant ant'], 'collide': ['obstacles']}
ANIMALS['queen ant'] = {'name': 'queen ant', 'corpse': None, 'mountable': False, 'touch damage': True, 'protected': False, 'hit rect': MEDIUM_HIT_RECT, 'grabable': False, 'run speed': 600, 'walk speed': 200, 'walk animate speed': 150, 'run animate speed': 100, 'detect radius': 512, 'avoid radius': 150,'aggression': 'awd', 'health': 1500, 'damage': 25, 'knockback': 6, 'item type': 'items', 'item': 'dead giant ant', 'dropped items': ['ant exoskeleton shell','queen ant leg','queen ant leg','queen ant leg','queen ant leg','queen ant leg','queen ant leg', 'ant helmet', 'giant ant eggs'], 'collide': ['obstacles']}
ANIMALS['snake'] = {'name': 'snake', 'corpse': None, 'mountable': False, 'climbing': True, 'touch damage': True, 'protected': False, 'hit rect': SMALL_HIT_RECT, 'grabable': False, 'run speed': 280, 'walk speed': 50, 'walk animate speed': 300, 'run animate speed': 90, 'detect radius': 140, 'avoid radius': 60,'aggression': 'fup', 'health': 12, 'damage': 10, 'knockback': 1, 'item type': 'items', 'item': 'dead snake', 'dropped items': ['dead snake'], 'collide': ['walls']}
ANIMALS['spider'] = {'name': 'spider', 'corpse': 6, 'mountable': True, 'climbing': True, 'touch damage': True, 'protected': False, 'hit rect': MEDIUM_HIT_RECT, 'grabable': False, 'run speed': 300, 'walk speed': 150, 'walk animate speed': 150, 'run animate speed': 100, 'detect radius': 280, 'avoid radius': 80,'aggression': 'awp', 'health': 200, 'damage': 15, 'knockback': 10, 'item type': 'items', 'item': 'dead giant ant', 'dropped items': ['spider venom'], 'collide': ['walls', 'water']}

ANIMALS['goldfish'] = {'name': 'goldfish', 'corpse': None, 'aquatic': True, 'mountable': False, 'touch damage': False, 'protected': False, 'hit rect': SMALL_HIT_RECT,'grabable': True, 'run speed': 350, 'walk speed': 50, 'walk animate speed': 400, 'run animate speed': 180, 'detect radius': 400, 'avoid radius': 40, 'aggression': 'fwd', 'health': 10, 'damage': 0, 'knockback': 0, 'item type': 'weapons', 'item': 'live goldfish', 'dropped items': ['dead goldfish'], 'collide': ['walls', 'shallows', 'lava', 'long_grass']}
ANIMALS['bluefish'] = {'name': 'bluefish', 'corpse': None, 'aquatic': True, 'mountable': False, 'touch damage': False, 'protected': False, 'hit rect': SMALL_HIT_RECT,'grabable': True, 'run speed': 400, 'walk speed': 60, 'walk animate speed': 400, 'run animate speed': 160, 'detect radius': 400, 'avoid radius': 40, 'aggression': 'fwd', 'health': 13, 'damage': 0, 'knockback': 0, 'item type': 'weapons', 'item': 'live bluefish', 'dropped items': ['dead bluefish'], 'collide': ['walls', 'shallows', 'lava', 'long_grass']}
ANIMALS['leopard shark'] = {'name': 'leopard shark', 'corpse': None, 'aquatic': True, 'mountable': False, 'touch damage': True, 'protected': False, 'hit rect': MEDIUM_HIT_RECT,'grabable': False, 'run speed': 400, 'walk speed': 100, 'walk animate speed': 200, 'run animate speed': 100, 'detect radius': 400, 'avoid radius': 40, 'aggression': 'awd', 'health': 55, 'damage': 4, 'knockback': 1, 'item type': 'items', 'item': 'dead leopard shark', 'dropped items': ['dead leopard shark'], 'collide': ['walls', 'shallows', 'lava', 'long_grass']}
ANIMALS['squid'] = {'name': 'squid', 'corpse': 5, 'mountable': True, 'aquatic': True, 'touch damage': True, 'protected': False, 'hit rect': MEDIUM_HIT_RECT,'grabable': False, 'run speed': 400, 'walk speed': 100, 'walk animate speed': 200, 'run animate speed': 100, 'detect radius': 400, 'avoid radius': 40, 'aggression': 'awp', 'health': 250, 'damage': 18, 'knockback': 15, 'item type': 'items', 'item': 'dead leopard shark', 'dropped items': ['squid ink', 'squid eye', 'squid tentacle'], 'collide': ['walls', 'shallows', 'lava', 'long_grass']}
ANIMALS['marlin'] = {'name': 'marlin', 'corpse': 7, 'mountable': False, 'aquatic': True, 'touch damage': True, 'protected': False, 'hit rect': MEDIUM_HIT_RECT,'grabable': False, 'run speed': 450, 'walk speed': 250, 'walk animate speed': 200, 'run animate speed': 100, 'detect radius': 400, 'avoid radius': 40, 'aggression': 'awp', 'health': 150, 'damage': 15, 'knockback': 50, 'item type': 'items', 'item': 'dead leopard shark', 'dropped items': ['marlin meat', 'marlin meat'], 'collide': ['walls', 'shallows', 'lava', 'long_grass']}
ANIMALS['sea turtle'] = {'name': 'sea turtle', 'corpse': None, 'aquatic': True, 'mountable': True, 'touch damage': False, 'protected': False, 'hit rect': MEDIUM_HIT_RECT,'grabable': False, 'run speed': 200, 'walk speed': 100, 'walk animate speed': 200, 'run animate speed': 100, 'detect radius': 400, 'avoid radius': 100, 'aggression': 'fwp', 'health': 350, 'damage': 18, 'knockback': 0, 'item type': 'items', 'item': 'dead leopard shark', 'dropped items': [None], 'collide': ['walls', 'lava']}
ANIMALS['dolphin'] = {'name': 'dolphin', 'corpse': 14, 'aquatic': True, 'mountable': True, 'touch damage': False, 'protected': False, 'hit rect': LARGE_HIT_RECT,'grabable': False, 'run speed': 600, 'walk speed': 300, 'walk animate speed': 80, 'run animate speed': 60, 'detect radius': 400, 'avoid radius': 200, 'aggression': 'fwp', 'health': 200, 'damage': 18, 'knockback': 0, 'item type': 'items', 'item': 'dead leopard shark', 'dropped items': ['dolphin meat', 'dolphin meat', 'whale oil', 'whale oil', 'whale oil'], 'collide': ['walls', 'lava', 'shallows', 'long_grass']}


MOUNTAIN_ANIMALS = ['blue wyvern', 'brown bird', 'goblin', 'rabbit', 'pink moth', 'green moth', 'butterfly ideopsis', 'giant ant', 'bighorn sheep', 'snake', 'garden lizard']
FOREST_ANIMALS = ['blue wyvern', 'red wyvern', 'brown bird', 'goblin', 'rabbit', 'pink moth', 'green moth', 'butterfly ideopsis', 'giant ant', 'garden lizard', 'spider', 'hawk']
GRASSLAND_ANIMALS = ['red wyvern', 'goblin', 'brown bird', 'rabbit', 'pink moth', 'green moth', 'butterfly ideopsis', 'giant ant', 'garden lizard', 'hawk']
BEACH_ANIMALS = ['brown bird', 'vadashay', 'bluefish', 'butterfly ideopsis', 'leopard shark', 'pink moth', 'garden lizard', 'flying goldfix', 'sea turtle']
OCEAN_ANIMALS = ['dolphin', 'vadashay', 'bluefish', 'leopard shark', 'squid', 'marlin', 'sea turtle']
ZOMBIELAND_ANIMALS = ['brown bird', 'immortui', 'immortui', 'immortui', 'rabbit', 'pink moth', 'green moth', 'giant ant', 'chicken', 'garden lizard']
TOWN_ANIMALS = ['brown bird', 'rabbit', 'pink moth', 'green moth', 'butterfly ideopsis', 'garden lizard']
TUNDRA_ANIMALS = ['rabbit', 'ice golem', 'sheep', 'bighorn sheep', 'brown bird', 'hawk']
ICEBEACH_ANIMALS = ['ice golem', 'bluefish', 'hawk']
DESERT_ANIMALS = ['red wyvern', 'demon', 'giant ant', 'snake', 'garden lizard', 'spider', 'hawk']
ANT_TUNNEL_ANIMALS = ['giant ant', 'rabbit']
CAVE_ANIMALS = ['giant ant', 'rabbit', 'snake', 'spider', 'skeleton', 'immortui']

# Created using the NPC designer
PEOPLE['sandy'] = {'name': 'Sandy', 'dead': False, 'protected': True, 'health': 150, 'touch damage': False, 'damage': 30, 'knockback': 10, 'walk speed': (80, 120), 'run speed': (280, 320), 'detect radius': 400, 'avoid radius': 100, 'aggression': 'awp', 'armed': False, 'dual wield': False, 'collide': ['walls', 'lava'], 'gender': 'male', 'race': 'shaktele', 'colors':  {'hair': COLOR_PALETTE[23], 'skin': SHAKTELE_SKIN_TONES[13]}, 'dialogue': 'random VILLAGER_DLG', 'store': None, 'inventory': {'weapons': ['steel dagger'], 'weapons2': [None], 'tops': ['pink dress top'], 'bottoms': ['steel chainmail leggings F'], 'hats': ['grey baseball hat'], 'hair': ['dreadlocks'], 'shoes': ['black combat'], 'gloves': [None], 'items': ['brick'], 'magic': ['fireball'], 'gold': 10}, 'animations': {None}, 'guarded': False}
PEOPLE['demon priest'] = {'name': 'Demon Priest', 'dead': False, 'protected': False, 'health': 250, 'touch damage': True, 'damage': 30, 'knockback': 15, 'walk speed': (130, 170), 'run speed': (180, 220), 'detect radius': 500, 'avoid radius': 80, 'aggression': 'awd', 'armed': False, 'dual wield': False, 'collide': ['walls'], 'gender': 'male', 'race': 'demon', 'colors':  {'hair': DEFAULT_HAIR_COLOR, 'skin': DEFAULT_SKIN_COLOR}, 'dialogue': None, 'store': None, 'inventory': {'weapons': ['ancient viking sword'], 'weapons2': [None], 'tops': ['black mage robe top M'], 'bottoms': ['black mage robe bottom'], 'hats': [None], 'hair': ['demon horns'], 'shoes': ['demon boots'], 'gloves': ['demon gauntlets'], 'items': ['potion of major healing', 'Zhara Talisman'], 'magic': ['fireball'], 'gold': 345}, 'animations': {None}, 'guarded': False}
PEOPLE['zhaway'] = {'name': 'Zhaway', 'dead': False, 'protected': True, 'health': 1000, 'touch damage': False, 'damage': 100, 'knockback': 25, 'walk speed': (100, 140), 'run speed': (180, 220), 'detect radius': 600, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False, 'collide': ['lava'], 'gender': 'male', 'race': 'whitewraith', 'colors':  {'hair': WHITEWRAITH_SKIN_TONES[0], 'skin': WHITEWRAITH_SKIN_TONES[0]}, 'dialogue': 'ZHAWAY_DLG', 'store': None, 'inventory': {'weapons': ['bone club'], 'weapons2': [None], 'tops': ['blue mage robe top M'], 'bottoms': ['blue mage robe bottom'], 'hats': ['white wizard cloak'], 'hair': [None], 'shoes': [None], 'gloves': [None], 'items': ['potion of feminization'], 'magic': ['healing', 'fireball'], 'gold': 0}, 'animations': {None}, 'guarded': True, 'quest': 'Cleanse the Temple of Zhara'}
PEOPLE['king spirit guard'] = {'name': 'King Spirit Guard', 'protected': True, 'health': 700, 'touch damage': False, 'damage': 15, 'knockback': 10, 'walk speed': (80, 120), 'run speed': (180, 220), 'detect radius': 400, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False, 'collide': ['lava'], 'gender': 'female', 'race': 'whitewraith', 'colors':  {'hair': 'random WHITEWRAITH_SKIN_TONES', 'skin': 'random WHITEWRAITH_SKIN_TONES'}, 'dialogue': None, 'store': None, 'inventory': {'weapons': ['iron battleaxe'], 'weapons2': [None], 'tops': ['iron plate armor'], 'bottoms': [None], 'hats': ['steel crown'], 'hair': ['long wraith'], 'shoes': ['steel boots'], 'gloves': ['iron gauntlets'], 'items': ['potion of major healing'], 'magic': ['healing', 'fireball'], 'gold': 0}, 'animations': {None}, 'guarded': True}
PEOPLE['little red riding kitting'] = {'name': 'Little Red Riding Kitty', 'dead': False, 'protected': True, 'health': 125, 'touch damage': False, 'damage': 28, 'knockback': 15, 'walk speed': (80, 120), 'run speed': (180, 220), 'detect radius': 400, 'avoid radius': 100, 'aggression': 'awp', 'armed': False, 'dual wield': False, 'collide': ['walls', 'lava', 'water'], 'gender': 'female', 'race': 'miewdra', 'colors':  {'hair': MIEWDRA_SKIN_TONES[14], 'skin': MIEWDRA_SKIN_TONES[14]}, 'dialogue': None, 'store': None, 'inventory': {'weapons': ['wood cutting axe'], 'weapons2': [None], 'tops': ['red dress top'], 'bottoms': ['red mini dress skirt'], 'hats': ['red cloak'], 'hair': ['long straight cat'], 'shoes': ['brown boots'], 'gloves': [None], 'items': ['french bread'], 'magic': ['healing'], 'gold': 32}, 'animations': {None}, 'guarded': False}
PEOPLE['jaz'] = {'name': 'Jaz', 'dead': False, 'protected': True, 'health': 100, 'touch damage': False, 'damage': 15, 'knockback': 10, 'walk speed': (80, 120), 'run speed': (180, 220), 'detect radius': 400, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False, 'collide': ['walls', 'lava'], 'gender': 'female', 'race': 'lacertolian', 'colors':  {'hair': LACERTOLIAN_SKIN_TONES[25], 'skin': LACERTOLIAN_SKIN_TONES[25]}, 'dialogue': 'JAZ_DLG', 'store': None, 'inventory': {'weapons': ['iron dagger'], 'weapons2': [None], 'tops': ['leather armor F'], 'bottoms': ['leather leggings F'], 'hats': [None], 'hair': ['lizard spikes'], 'shoes': [None], 'gloves': [None], 'items': ['potion of minor healing'], 'magic': [None], 'gold': 123}, 'animations': {None}, 'guarded': False, 'quest': 'Turtle Armor for Jaz'}
PEOPLE['jamal'] = {'name': 'Jamal', 'dead': False, 'protected': True, 'health': 223, 'touch damage': False, 'damage': 15, 'knockback': 15, 'walk speed': (80, 120), 'run speed': (180, 220), 'detect radius': 400, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False, 'collide': ['walls', 'lava'], 'gender': 'male', 'race': 'shaktele', 'colors':  {'hair': COLOR_PALETTE[21], 'skin': SHAKTELE_SKIN_TONES[11]}, 'dialogue': 'JAMAL_DLG', 'store': None, 'inventory': {'weapons': ['shotgun'], 'weapons2': [None], 'tops': ['shaktele guard armor'], 'bottoms': ['jeans M'], 'hats': [None], 'hair': ['beard'], 'shoes': ['green combat'], 'gloves': [None], 'items': ['potion of major healing'], 'magic': ['healing'], 'gold': 23}, 'animations': {None}, 'guarded': False, 'quest': 'Jamal the body guard'}
PEOPLE['hagitha'] = {'name': 'Hagitha', 'dead': False, 'protected': False, 'health': 100, 'touch damage': False, 'damage': 15, 'knockback': 20, 'walk speed': (80, 120), 'run speed': (180, 220), 'detect radius': 400, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False, 'collide': ['walls', 'lava'], 'gender': 'female', 'race': 'goblin', 'colors':  {'hair': DEFAULT_HAIR_COLOR, 'skin': DEFAULT_SKIN_COLOR}, 'dialogue': 'HAGITHA_DLG', 'store': None, 'inventory': {'weapons': ['pickaxe'], 'weapons2': [None], 'tops': ['orange decayed shirt F'], 'bottoms': ['leather leggings F'], 'hats': [None], 'hair': ['elf braids'], 'shoes': ['brown boots'], 'gloves': ['leather gauntlets'], 'items': ['candle'], 'magic': ['healing'], 'gold': 13}, 'animations': {None}, 'guarded': False, 'quest': 'Find gold ore for Hagitha'}
PEOPLE['john'] = {'name': 'John', 'protected': True, 'dead': False, 'health': 250, 'touch damage': False, 'damage': 23, 'knockback': 10, 'walk speed': (80, 120), 'run speed': (280, 320), 'detect radius': 400, 'avoid radius': 100, 'aggression': 'awp', 'armed': False, 'dual wield': False, 'collide': ['walls', 'lava'], 'gender': 'male', 'race': 'osidine', 'colors':  {'hair': COLOR_PALETTE[0], 'skin': OSIDINE_SKIN_TONES[2]}, 'dialogue': 'JOHN_DLG', 'store': None, 'inventory': {'weapons': [None], 'weapons2': [None], 'tops': ['green decayed shirt M'], 'bottoms': ['jeans M'], 'hats': [None], 'hair': ['beard'], 'shoes': ['brown boots'], 'gloves': [None], 'items': ['potion of major healing'], 'magic': ['fireball'], 'gold': 100}, 'animations': {None}, 'guarded': False, 'quest': 'Harvest the potatoes'}
PEOPLE['king draconius'] = {'name': 'King Draconius', 'dead': False, 'protected': True, 'health': 645, 'touch damage': False, 'damage': 56, 'knockback': 10, 'walk speed': (130, 170), 'run speed': (230, 270), 'detect radius': 300, 'avoid radius': 100, 'aggression': 'sap', 'armed': True, 'dual wield': False, 'collide': ['obstacles'], 'gender': 'male', 'race': 'osidine', 'colors':  {'hair': COLOR_PALETTE[10], 'skin': OSIDINE_SKIN_TONES[4]}, 'dialogue': 'KING_DRACONIUS_DLG', 'store': None, 'inventory': {'weapons': ['steel broadsword'], 'weapons2': [None], 'tops': ['gold plated royal armor'], 'bottoms': ['bronze chainmail leggings M'], 'hats': ['golden crown'], 'hair': ['beard'], 'shoes': ['bronze boots'], 'gloves': ['bronze gauntlets'], 'items': ['Angel Talisman'], 'magic': ['healing'], 'gold': 324}, 'animations': {None}, 'guarded': True, 'quest': 'Deliver a letter to the Elf Queen'}
PEOPLE['alex'] = {'name': 'Alex', 'protected': True, 'dead': False, 'health': 100, 'touch damage': False, 'damage': 15, 'knockback': 10, 'walk speed': (80, 120), 'run speed': (180, 220), 'detect radius': 400, 'avoid radius': 100, 'aggression': 'sap', 'armed': False, 'dual wield': False, 'collide': ['obstacles'], 'gender': 'other', 'race': 'osidine', 'colors':  {'hair': COLOR_PALETTE[16], 'skin': OSIDINE_SKIN_TONES[5]}, 'dialogue': None, 'store': None, 'inventory': {'weapons': ['steel mace'], 'weapons2': ['steel shield'], 'tops': ['steel guard armor'], 'bottoms': ['steel chainmail leggings M'], 'hats': ['steel helmet'], 'hair': ['short combed'], 'shoes': ['steel boots'], 'gloves': ['steel gauntlets'], 'items': ['empty bottle', 'book of demon secrets', 'garlic', 'Guide book to Arroshay', 'letter from Alex', 'letter from Loella'], 'magic': [None], 'gold': 13}, 'animations': {None}, 'guarded': False}
PEOPLE['max'] = {'name': 'Max', 'protected': True, 'health': 200, 'touch damage': False, 'damage': 15, 'knockback': 10, 'walk speed': (180, 220), 'run speed': (330, 370), 'detect radius': 400, 'avoid radius': 100, 'aggression': 'sap', 'armed': False, 'dual wield': False, 'collide': ['obstacles'], 'gender': 'male', 'race': 'elf', 'colors':  {'hair': COLOR_PALETTE[19], 'skin': ELF_SKIN_TONES[7]}, 'dialogue': 'MAX_DLG', 'store': MAX_STORE, 'inventory': {'weapons': [None], 'weapons2': [None], 'tops': ['leather armor M'], 'bottoms': ['steel chainmail leggings M'], 'hats': [None], 'hair': ['beard'], 'shoes': ['brown boots'], 'gloves': [None], 'items': ['empty bottle'], 'magic': [None], 'gold': 10}, 'animations': {None}, 'guarded': True}
PEOPLE['demon queen'] = {'name': 'Demon Queen', 'protected': True, 'health': 666, 'touch damage': False, 'damage': 15, 'knockback': 15, 'walk speed': (80, 120), 'run speed': (180, 220), 'detect radius': 400, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False, 'collide': ['walls', 'lava'], 'gender': 'female', 'race': 'demon', 'colors': {'hair': (19, 19, 19, 255), 'skin': (129, 128, 188, 255)}, 'dialogue': 'DEMON_QUEEN_DLG', 'store': None, 'inventory': {'weapons': ['mini wgun'], 'weapons2': [None], 'tops': ['red dress top'], 'bottoms': ['red mini dress skirt'], 'hats': ['silver crown'], 'hair': ['demon horns'], 'shoes': ['demon boots'], 'gloves': ['leather gauntlets'], 'items': ['Angel Talisman'], 'magic': ['fire spray'], 'gold': 666}, 'animations': {None}, 'guarded': False}
PEOPLE['bill'] = {'name': 'Bill', 'protected': True, 'health': 1000, 'touch damage': False, 'damage': 15, 'knockback': 10, 'walk speed': (80, 120), 'run speed': (180, 220), 'detect radius': 400, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False, 'collide': ['walls'], 'gender': 'male', 'race': 'mech_suit', 'colors': {'hair': (138, 54, 15), 'skin': (224, 224, 4, 255)}, 'dialogue': 'BILL_DLG', 'store': None, 'inventory': {'weapons': ['assault rifle'], 'weapons2': [None], 'tops': [None], 'bottoms': [None], 'hats': [None], 'hair': [None], 'shoes': [None], 'gloves': [None], 'items': ['oregano'], 'magic': [None], 'gold': 1}, 'animations': {None}, 'guarded': False, 'quest': "Bill\'s fish"}
PEOPLE['jeff'] = {'name': 'Jeff', 'protected': True, 'health': 300, 'touch damage': False, 'damage': 15, 'knockback': 10, 'walk speed': (80, 120), 'run speed': (280, 320), 'detect radius': 400, 'avoid radius': 100, 'aggression': 'awp', 'armed': False, 'dual wield': False, 'collide': ['obstacles', 'walls', 'lava'], 'gender': 'male', 'race': 'immortui', 'colors': {'hair': (191, 157, 122, 255), 'skin': (255, 255, 255)}, 'dialogue': 'JEFF_DLG', 'store': None, 'inventory': {'weapons': [None], 'weapons2': [None], 'tops': ['grey decayed shirt M'], 'bottoms': ['jeans M'], 'hats': [None], 'hair': ['short messy'], 'shoes': ['brown boots'], 'gloves': [None], 'items': ['plate'], 'magic': [None], 'gold': 0}, 'animations': {None}, 'guarded': False, 'quest': 'Find a chicken'}
PEOPLE['cindy'] = {'name': 'Cindy', 'protected': True, 'health': 600, 'touch damage': False, 'damage': 15, 'knockback': 10, 'walk speed': (20, 60), 'run speed': (180, 220), 'detect radius': 400, 'avoid radius': 100, 'aggression': 'fwp', 'armed': False, 'dual wield': False, 'collide': ['obstacles', 'walls', 'vehicles', 'lava', 'water', 'shallows'], 'gender': 'female', 'race': 'shaktele', 'colors': {'hair': (138, 54, 15), 'skin': (98, 48, 21)}, 'dialogue': 'CINDY_DLG', 'store': CINDY_STORE, 'inventory': {'weapons': [None], 'weapons2': [None], 'tops': ['blue tshirt F'], 'bottoms': ['red mini dress skirt'], 'hats': [None], 'hair': ['medium messy'], 'shoes': ['brown boots'], 'gloves': [None], 'items': ['chop sticks'], 'magic': ['healing'], 'gold': 250}, 'animations': {None}, 'guarded': True}