HATS = {}
HATS['steel crown'] = {'armor': 10, 'image': 0, 'weight': 0.3, 'materials': {'steel ingot': 2}, 'upgrade': {'steel ingot': 1, 'green crystal': 1}, 'value': 100}
HATS['grey baseball hat'] = {'armor': 1, 'image': 1, 'weight': 0.1, 'upgrade': {'leather': 1}, 'value': 10}
HATS['tactical helmet'] = {'armor': 20, 'image': 2, 'weight': 1.5, 'upgrade': {'steel ingot': 1}, 'value': 100}
HATS['military helmet'] = {'armor': 18, 'image': 3, 'weight': 0.9, 'value': 75}
HATS['guard helmet'] = {'armor': 15, 'image': 4, 'weight': 1, 'materials': {'steel ingot': 2, 'leather': 1}, 'upgrade': {'steel ingot': 2}, 'value': 50}
HATS['royal guard helmet'] = {'armor': 18, 'image': 5, 'weight': 1.3, 'upgrade': {'steel ingot': 2}, 'value': 150}
HATS['steel helmet'] = {'armor': 25, 'image': 6, 'weight': 2, 'materials': {'steel ingot': 3}, 'upgrade': {'steel ingot': 2}, 'value': 250}
HATS['steel knight helmet'] = {'armor': 25, 'image': 7, 'weight': 3, 'materials': {'steel ingot': 3, 'leather': 1},  'upgrade': {'steel ingot': 2}, 'value': 270}
HATS['skull helmet'] = {'armor': 15, 'image': 8, 'weight': 2, 'value': 150}
HATS['demon helmet'] = {'armor': 35, 'image': 9, 'weight': 4, 'value': 666}
HATS['dragon mask'] = {'armor': 30, 'image': 10, 'weight': 3, 'fire enhance': {'after effect': 'fire', 'damage': 20, 'life time': 1000, 'speed': 50, 'rate reduction': 300}, 'reinforce magica': 200, 'reinforce health': 200, 'reinforce stamina': 200, 'value': 1050}
HATS['elf hat'] = {'armor': 3, 'image': 11, 'weight': 0.2, 'reinforce magica': 20, 'value': 20}
HATS['paladin crown'] = {'armor': 30, 'image': 12, 'weight': 1, 'value': 2000}
HATS['ant helmet'] = {'armor': 30, 'image': 13, 'weight': 0.5, 'value': 550}
HATS['golden crown'] = {'armor': 2, 'image': 14, 'weight': 2, 'value': 1000, 'materials': {'gold ingot': 2}, 'upgrade': {'gold ingot': 1, 'red crystal': 1}}
HATS['silver crown'] = {'armor': 2, 'image': 14, 'weight': 0.8, 'value': 700, 'materials': {'silver ingot': 2}, 'upgrade': {'silver ingot': 1, 'blue crystal': 1}}
HATS['blue cloak'] = {'armor': 3, 'image': 16, 'weight': 0.7, 'reinforce magica': 30, 'value': 200}
HATS['black cloak'] = {'armor': 3, 'image': 17, 'weight': 0.7, 'reinforce magica': 100, 'value': 800}
HATS['dark wizard cloak'] = {'armor': 3, 'image': 18, 'weight': 0.7, 'reinforce magica': 300, 'value': 3000}
HATS['cloak of invisibility'] = {'armor': 3, 'image': 19, 'weight': 0.7, 'reinforce magica': 50, 'property': 'invisibility', 'value': 10000}
HATS['white wizard cloak'] = {'armor': 3, 'image': 20, 'weight': 0.7, 'reinforce magica': 200, 'value': 1000}
HATS['red cloak'] = {'armor': 3, 'image': 21, 'weight': 0.7, 'reinforce magica': 70, 'value': 500}
HATS['turtle plate helmet'] = {'armor': 34, 'image': 22, 'weight': 3.5, 'materials': {'turtle shell plate': 4, 'leather': 1}, 'upgrade': {'steel ingot': 1, 'leather strips': 1}, 'value': 170}
HATS['dark wizard hood'] = {'armor': 3, 'image': 23, 'weight': 0.7, 'reinforce magica': 200, 'value': 3000}

HAIR = {}
HAIR['long blond pony'] = {'races': ['osidine', 'shaktele', 'elf'], 'weight': 0.4,
                                'image': 0}
HAIR['long straight brown'] = {'races': ['osidine', 'shaktele', 'immortui'], 'weight': 0.3,
                                'image': 1}
HAIR['long curly brown'] = {'races': ['osidine', 'shaktele'], 'weight': 0.3,
                                'image': 2}
HAIR['long black pony'] = {'races': ['osidine', 'shaktele', 'elf'], 'weight': 0.4,
                                'image': 3}
HAIR['medium messy brown'] = {'races': ['osidine', 'shaktele', 'immortui'], 'weight': 0.2,
                                'image': 4}
HAIR['long brown side pony'] = {'races': ['osidine', 'shaktele', 'elf'], 'weight': 0.4,
                                'image': 5}
HAIR['short messy'] = {'races': ['osidine', 'shaktele', 'immortui'], 'weight': 0.1,
                                'image': 6}
HAIR['short brown'] = {'races': ['osidine', 'shaktele', 'elf', 'immortui'], 'weight': 0.1,
                                'image': 7}
HAIR['long blond side pony'] = {'races': ['osidine', 'shaktele', 'elf'], 'weight': 0.4,
                                'image': 8}
HAIR['short blond'] = {'races': ['osidine', 'shaktele', 'elf', 'immortui'], 'weight': 0.1,
                                'image': 9}
HAIR['dreadlocks'] = {'races': ['osidine', 'shaktele', 'immortui'], 'weight': 0.5,
                                'image': 16}
HAIR['long blond'] = {'races': ['osidine', 'shaktele', 'immortui'], 'weight': 0.3,
                                'image': 10}
HAIR['brown elf braids'] = {'races': ['elf'], 'weight': 0.3,
                                'image': 11}
HAIR['white elf braids'] = {'races': ['elf', 'demon'], 'weight': 0.3,
                                'image': 14}
HAIR['blond elf braids'] = {'races': ['elf'], 'weight': 0.3,
                                'image': 15}
HAIR['lizard hornes'] = {'races': ['lacertolian'], 'weight': 0.2,
                                'image': 12}
HAIR['lizard spikes'] = {'races': ['lacertolian', 'demon'], 'weight': 0.1,
                                'image': 13}
HAIR['cat tufts'] = {'races': ['miewdra'], 'weight': 0.1,
                                'image': 17}
HAIR['frizzy cat'] = {'races': ['miewdra'], 'weight': 0.2,
                                'image': 18}
HAIR['fluffy cat'] = {'races': ['miewdra'], 'weight': 0.2,
                                'image': 19}
HAIR['blond cat'] = {'races': ['miewdra'], 'weight': 0.3,
                                'image': 20}
HAIR['brown cat'] = {'races': ['miewdra'], 'weight': 0.3,
                                'image': 21}
HAIR['blue cat'] = {'races': ['miewdra'], 'weight': 0.3,
                                'image': 22}
HAIR['white cat'] = {'races': ['miewdra'], 'weight': 0.3,
                                'image': 23}
HAIR['bald'] = {'races': ['osidine', 'shaktele', 'elf', 'lacertolian', 'miewdra', 'immortui', 'mechanima', 'blackwraith', 'whitewraith', 'skeleton', 'demon', 'vadashay'], 'weight': 0,
                                'image': 24}
HAIR['ram horns'] = {'races': ['skeleton', 'demon'], 'weight': 0.5,
                                'image': 25}
HAIR['demon horns'] = {'races': ['skeleton', 'demon'], 'weight': 0.4, 'value': 666,
                                'image': 26}
HAIR['short horns'] = {'races': ['skeleton', 'demon'], 'weight': 0.2,
                                'image': 27}
HAIR['long black wraith'] = {'races': ['blackwraith'], 'weight': 0,
                                'image': 28}
HAIR['long white wraith'] = {'races': ['whitewraith'], 'weight': 0,
                                'image': 29}
HAIR['medium white droid'] = {'races': ['mechanima'], 'weight': 0.1,
                                'image': 30}
HAIR['medium black droid'] = {'races': ['mechanima'], 'weight': 0.1,
                                'image': 31}
HAIR['medium blue droid'] = {'races': ['mechanima'], 'weight': 0.1,
                                'image': 32}
HAIR['cable mohawk'] = {'races': ['mechanima'], 'weight': 0.1,
                                'image': 33}
HAIR['medium cable dreads'] = {'races': ['mechanima'], 'weight': 0.1,
                                'image': 34}
HAIR['long cable dreads'] = {'races': ['mechanima'], 'weight': 0.1,
                                'image': 35}
HAIR['LED skin'] = {'races': ['mechanima'], 'weight': 0,
                                'image': 36}
HAIR['light strips'] = {'races': ['mechanima'], 'weight': 0,
                                'image': 37}
HAIR['LED stripes'] = {'races': ['mechanima'], 'weight': 0,
                                'image': 38}
HAIR['The Golden Toupee'] = {'races': ['goblin'], 'weight': 3,
                                'image': 39, 'value': 1000}
HAIR['brown beard'] = {'races': ['osidine', 'shaktele', 'elf', 'immortui'], 'weight': 0.2,
                                'image': 40}
HAIR['white beard'] = {'races': ['osidine', 'shaktele', 'elf', 'immortui'], 'weight': 0.2,
                                'image': 41}

# Makes a dictionary containing the hairstyles appropriate for each race.
temp_race_list = ['demon', 'osidine', 'shaktele', 'elf', 'lacertolian', 'miewdra', 'immortui', 'mechanima', 'blackwraith', 'whitewraith', 'skeleton']
RACE_HAIR = {}
for race in temp_race_list:
    RACE_HAIR[race] = []
for item in HAIR:
    for race in temp_race_list:
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
SHOES['bronze boots'] = {'armor': 8, 'weight': 1.2, 'image': 0, 'materials': {'bronze ingot': 2, 'leather': 2},  'upgrade': {'bronze ingot': 1, 'leather': 1}, 'value': 120}
SHOES['black combat'] = {'armor': 2, 'weight': 0.8, 'image': 1, 'materials': {'steel ingot': 1, 'leather': 2}, 'upgrade': {'leather': 1}, 'value': 45}
SHOES['green combat'] = {'armor': 2, 'weight': 0.8, 'image': 2, 'materials': {'steel ingot': 1, 'leather': 2}, 'upgrade': {'leather': 1}, 'value': 45}
SHOES['brown boots'] = {'armor': 1, 'weight': 0.3, 'image': 3, 'materials': {'leather': 2}, 'upgrade': {'leather': 1}, 'value': 5}
SHOES['steel boots'] = {'armor': 10, 'weight': 2, 'image': 4, 'materials': {'steel ingot': 2, 'leather': 2},  'upgrade': {'steel ingot': 2, 'leather': 1}, 'value': 150}
SHOES['demon boots'] = {'armor': 46, 'weight': 2.1, 'image': 5, 'value': 150}

GLOVES = {}
GLOVES['bronze gauntlets'] = {'armor': 8, 'weight': 1.6, 'image': 0, 'materials': {'bronze ingot': 2, 'leather': 1}, 'upgrade': {'bronze ingot': 1, 'leather': 1}, 'value': 110}
GLOVES['demon gauntlets'] = {'armor': 45, 'weight': 2, 'value': 666,
                              'image': 1}
GLOVES['leather gauntlets'] = {'armor': 5, 'weight': 0.4, 'image': 2, 'materials': {'leather': 2}, 'value': 55}
GLOVES['dress gloves'] = {'armor': 1, 'weight': 0.1,
                              'image': 3}
GLOVES['steel gauntlets'] = {'armor': 11, 'weight': 2.3, 'image': 4, 'materials': {'steel ingot': 2, 'leather': 1}, 'upgrade': {'steel ingot': 1, 'leather': 1}, 'value': 140}
GLOVES['iron gauntlets'] = {'armor': 9, 'weight': 4, 'image': 5, 'materials': {'iron ingot': 2, 'leather': 1}, 'upgrade': {'iron ingot': 1, 'leather': 1}, 'value': 50}

TOPS = {}
TOPS['bronze armor'] = {'armor': 26, 'image': 0, 'gender': 'other', 'weight': 7, 'materials': {'bronze ingot': 5, 'leather': 2}, 'upgrade': {'bronze ingot': 3, 'leather strips': 1}, 'value': 250}
TOPS['grey racerback tank top'] = {'armor': 2,'image': 1,'gender': 'female', 'weight': 0.3, 'value': 5}
TOPS['black racerback tank top'] = {'armor': 2, 'image': 2,'gender': 'female', 'weight': 0.3, 'value': 5}
TOPS['decayed shirt F'] = {'armor': 1, 'image': 3, 'gender': 'female', 'weight': 0.4, 'value': 1}
TOPS['decayed shirt M'] = {'armor': 1, 'image': 4, 'gender': 'male', 'weight': 0.4, 'value': 1}
TOPS['tshirt M'] = {'armor': 1, 'image': 5, 'gender': 'male', 'weight': 0.4, 'value': 5}
TOPS['tshirt F'] = {'armor': 1, 'image': 14, 'gender': 'female', 'weight': 0.4, 'value': 5}
TOPS['wedding dress top'] = {'armor': 1, 'image': 6, 'gender': 'female', 'weight': 0.3, 'value': 200}
TOPS['pink dress top'] = {'armor': 1, 'image': 7, 'gender': 'female', 'weight': 0.2, 'value': 74}
TOPS['blue dress top'] = {'armor': 1, 'image': 8, 'gender': 'female', 'weight': 0.2, 'value': 70}
TOPS['red dress top'] = {'armor': 1, 'image': 9, 'gender': 'female', 'weight': 0.2, 'value': 78}
TOPS['green elf dress top'] = {'armor': 2, 'image': 10, 'gender': 'female', 'weight': 0.1, 'value': 55}
TOPS['red elf dress top'] = {'armor': 1, 'image': 11, 'gender': 'female', 'weight': 0.1, 'value': 56}
TOPS['dark tshirt M'] = {'armor': 1, 'image': 12, 'gender': 'male', 'weight': 0.4, 'value': 5}
TOPS['dark tshirt F'] = {'armor': 1, 'image': 13, 'gender': 'female', 'weight': 0.4, 'value': 5}
TOPS['guard armor'] = {'armor': 30, 'image': 15, 'gender': 'other', 'weight': 10, 'materials': {'steel ingot': 4, 'iron ingot': 1, 'leather': 2}, 'upgrade': {'steel ingot': 2, 'iron ingot': 1, 'leather strips': 1}, 'value': 250}
TOPS['knight armor'] = {'armor': 45, 'image': 16, 'gender': 'other', 'weight': 15, 'materials': {'steel ingot': 7, 'leather': 3}, 'upgrade': {'steel ingot': 4, 'leather strips': 1}, 'value': 400}
TOPS['demon armor F'] = {'armor': 60, 'image': 17, 'gender': 'female', 'weight': 17, 'value': 2250}
TOPS['demon armor M'] = {'armor': 60, 'image': 18, 'gender': 'male', 'weight': 17, 'value': 2250}
TOPS['leather armor F'] = {'armor': 10, 'image': 19, 'gender': 'female', 'weight': 4, 'materials': {'leather': 4}, 'upgrade': {'leather': 2, 'leather strips': 1}, 'upgrade': {'steel ingot': 1, 'leather': 1}, 'value': 100}
TOPS['leather armor M'] = {'armor': 10, 'image': 20, 'gender': 'male', 'weight': 4, 'materials': {'leather': 4}, 'upgrade': {'leather': 2, 'leather strips': 1}, 'upgrade': {'steel ingot': 1, 'leather': 1}, 'value': 100}
TOPS['shaktele guard armor'] = {'armor': 25, 'image': 21, 'gender': 'other', 'weight': 7, 'materials': {'steel ingot': 2, 'leather': 3}, 'upgrade': {'steel ingot': 1, 'leather strips': 1, 'leather': 1}, 'value': 260}
TOPS['steel plate armor'] = {'armor': 40, 'image': 22, 'gender': 'other', 'weight': 15, 'materials': {'steel ingot': 6, 'iron ingot': 1, 'leather': 3}, 'upgrade': {'steel ingot': 3, 'leather strips': 1}, 'value': 300}
TOPS['iron plate armor'] = {'armor': 27, 'image': 22, 'gender': 'other', 'weight': 20, 'materials': {'iron ingot': 6, 'leather': 2}, 'upgrade': {'iron ingot': 3, 'leather strips': 1}, 'value': 100}
TOPS['turtle plate armor'] = {'armor': 38, 'image': 24, 'gender': 'other', 'weight': 7, 'materials': {'turtle shell plate': 8, 'leather': 2}, 'upgrade': {'steel ingot': 2, 'leather strips': 1}, 'value': 360}
TOPS['blue mage robe top M'] = {'armor': 10, 'image': 25, 'gender': 'male', 'weight': 0.6, 'reinforce magica': 70, 'value': 70}
TOPS['red mage robe top M'] = {'armor': 8, 'image': 26, 'gender': 'male', 'weight': 0.6, 'reinforce magica': 50, 'value': 50}
TOPS['blue mage robe top F'] = {'armor': 10, 'image': 27, 'gender': 'female', 'weight': 0.6, 'reinforce magica': 70, 'value': 70}
TOPS['red mage robe top F'] = {'armor': 8, 'image': 28, 'gender': 'female', 'weight': 0.6, 'reinforce magica': 50, 'value': 50}
TOPS['black mage robe top M'] = {'armor': 38, 'image': 30, 'gender': 'male', 'weight': 0.6, 'reinforce magica': 150, 'value': 1000}
TOPS['black mage robe top F'] = {'armor': 38, 'image': 29, 'gender': 'female', 'weight': 0.6, 'reinforce magica': 150, 'value': 1000}
TOPS['melerous armor'] = {'armor': 38, 'image': 31, 'gender': 'male', 'weight': 0.6, 'reinforce magica': 150, 'value': 1000}

BOTTOMS = {}
BOTTOMS['grey yoga pants'] = {'armor': 1, 'image': 1, 'gender': 'female', 'weight': 0.5, 'value': 10}
BOTTOMS['blue yoga pants'] = {'armor': 1, 'image': 2, 'gender': 'female', 'weight': 0.5, 'value': 10}
BOTTOMS['jeans M'] = {'armor': 1, 'image': 3, 'gender': 'male', 'weight': 0.6, 'value': 12}
BOTTOMS['jeans F'] = {'armor': 1, 'image': 10, 'gender': 'female', 'weight': 0.6, 'value': 12}
BOTTOMS['wedding dress skirt'] = {'armor': 1, 'image': 4, 'gender': 'female', 'weight': 3, 'value': 500}
BOTTOMS['pink dress skirt'] = {'armor': 1, 'image': 5, 'gender': 'female', 'weight': 2, 'value': 100}
BOTTOMS['blue dress skirt'] = {'armor': 1, 'image': 6, 'gender': 'female', 'weight': 1, 'value': 110}
BOTTOMS['red mini dress skirt'] = {'armor': 1, 'image': 7, 'gender': 'female', 'weight': 0.4, 'value': 80}
BOTTOMS['leaf skirt'] = {'armor': 2, 'image': 8, 'gender': 'female', 'weight': 0.4, 'value': 55}
BOTTOMS['green mini dress skirt'] = {'armor': 1, 'image': 9, 'gender': 'female', 'weight': 0.4, 'value': 66}
BOTTOMS['chainmail leggings M'] = {'armor': 15, 'image': 12, 'gender': 'male', 'weight': 8, 'materials': {'steel ingot': 4}, 'upgrade': {'steel ingot': 2}, 'value': 150}
BOTTOMS['chainmail leggings F'] = {'armor': 15, 'image': 11, 'gender': 'female', 'weight': 8, 'materials': {'steel ingot': 4}, 'upgrade': {'steel ingot': 2}, 'value': 150}
BOTTOMS['leather leggings M'] = {'armor': 10, 'image': 14, 'gender': 'male', 'weight': 1, 'materials': {'leather': 4}, 'upgrade': {'leather': 2, 'leather strips': 1}, 'value': 90}
BOTTOMS['leather leggings F'] = {'armor': 10, 'image': 13, 'gender': 'female', 'weight': 1, 'materials': {'leather': 4}, 'upgrade': {'leather': 2, 'leather strips': 1}, 'value': 90}
BOTTOMS['bronze chainmail leggings M'] = {'armor': 13, 'image': 15, 'gender': 'male', 'weight': 6, 'materials': {'bronze ingot': 4}, 'upgrade': {'bronze ingot': 2}, 'value': 150}
BOTTOMS['bronze chainmail leggings F'] = {'armor': 13, 'image': 0, 'gender': 'female', 'weight': 6, 'materials': {'bronze ingot': 4}, 'upgrade': {'bronze ingot': 2}, 'value': 150}
BOTTOMS['blue mage robe bottom'] = {'armor': 6, 'image': 16, 'gender': 'other', 'weight': 0.5, 'reinforce magica': 30, 'value': 40}
BOTTOMS['red mage robe bottom'] = {'armor': 4, 'image': 17, 'gender': 'other', 'weight': 0.5, 'reinforce magica': 30, 'value': 30}
BOTTOMS['black mage robe bottom'] = {'armor': 24, 'image': 18, 'gender': 'other', 'weight': 0.5, 'reinforce magica': 100, 'value': 1000}

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
CASUAL_TOPS_LIST.extend(['grey racerback tank top', 'black racerback tank top', 'tshirt M', 'tshirt F', 'pink dress top', 'blue dress top', 'red dress top', 'green elf dress top', 'red elf dress top', 'dark tshirt M', 'dark tshirt F'])
CASUAL_BOTTOMS_LIST = ['grey yoga pants', 'blue yoga pants', 'jeans M', 'jeans F', 'blue dress skirt', 'red mini dress skirt', 'green mini dress skirt', 'leather leggings M', 'leather leggings F']

UPGRADED_HATS = {}
UPGRADED_TOPS = {}
UPGRADED_GLOVES = {}
UPGRADED_BOTTOMS = {}
UPGRADED_SHOES = {}
