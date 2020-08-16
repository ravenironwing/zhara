from chests import *

# Items
ITEMS = {}
# First aid
ITEMS['first aid kit'] = {'health': 50, 'stamina': 50, 'image': 1, 'weight': 1.5, 'value': 150}

# Jewelry
ITEMS['Angel Talisman'] = {'image': 134, 'weight': 0.1, 'reinforce health': 100, 'armor': 20}
ITEMS['Zhara Talisman'] = {'image': 144, 'weight': 0}

# Potions
ITEMS['potion of minor healing'] = {'alchemy': True, 'health': 20, 'image': 4, 'weight': 0.5, 'materials': {'dead pink moth':1, 'empty bottle':1}, 'value': 50}
ITEMS['potion of moderate healing'] = {'alchemy': True, 'health': 40, 'image': 3, 'weight': 0.7, 'materials': {'oregano':1, 'dead pink moth':1, 'empty bottle':1}, 'value': 100}
ITEMS['potion of major healing'] = {'alchemy': True, 'health': 75, 'image': 2, 'weight': 1, 'materials': {'garlic':1, 'yarrow':1, 'empty bottle':1}, 'value': 170}
ITEMS['potion of minor magica'] = {'alchemy': True, 'magica': 20, 'image': 4, 'weight': 0.5, 'materials': {'dead green moth':1, 'empty bottle':1}, 'value': 40}
ITEMS['potion of moderate magica'] = {'alchemy': True, 'magica': 40, 'image': 3, 'weight': 0.7, 'materials': {'dead pink moth':1, 'rosemary':1, 'empty bottle':1}, 'value': 90}
ITEMS['potion of major magica'] = {'alchemy': True, 'magica': 75, 'image': 2, 'weight': 1, 'materials': {'dead butterfly ideopsis':1, 'sage':1, 'empty bottle':1}, 'value': 150}
ITEMS['potion of minor stamina'] = {'alchemy': True, 'stamina': 20, 'image': 5, 'weight': 0.5, 'materials': {'rosemary':1, 'empty bottle':1}, 'value': 30}
ITEMS['potion of moderate stamina'] = {'alchemy': True, 'stamina': 40, 'image': 6, 'weight': 0.7, 'materials': {'dead green moth':1, 'oregano':1, 'empty bottle':1}, 'value': 60}
ITEMS['potion of major stamina'] = {'alchemy': True, 'stamina': 75, 'image': 7, 'weight': 1, 'materials': {'dead snake':1, 'dead butterfly ideopsis':1, 'empty bottle':1}, 'value': 120}
ITEMS['humanize potion'] = {'alchemy': True, 'change race': 'human', 'image': 9, 'weight': 0.5, 'materials': {'zombie extract':1, 'sage':1, 'sulfur':1, 'empty bottle':1}, 'value': 1000}
ITEMS['potion of feminization'] = {'alchemy': True, 'change sex': 'female', 'image': 8, 'weight': 0.5, 'materials': {'dead pink moth':1, 'giant ant eggs':1, 'rosemary':1, 'empty bottle':1}, 'value': 5000}
ITEMS['potion of masculinization'] = {'alchemy': True, 'change sex': 'male', 'image': 7, 'weight': 0.5, 'materials': {'dead bluefish':1, 'sulphur':1, 'dead snake':1, 'empty bottle':1}, 'value': 5000}

ITEMS['ale'] = {'alchemy': True, 'stamina': 40, 'health': -10, 'image': 146, 'weight': 0.7, 'materials': {'hops':1, 'barley':1, 'bottled water':1, 'empty mug':1}, 'value': 10}
ITEMS['ale of the gods'] = {'alchemy': True, 'stamina': 40, 'health': 15, 'image': 146, 'weight': 0.7, 'materials': {'hops':1, 'barley':1, 'living water':1, 'empty mug':1}, 'value': 20}

# Tools
ITEMS['lock pick'] = {'image': 11, 'hp': 50, 'weight': 0.2, 'forgeable': True, 'materials': {'steel rod': 1}, 'value': 120}

# Forgeable
ITEMS['flint and steel'] = {'image': 150, 'hp': 20, 'weight': 1, 'materials': {'steel ingot': 1, 'flint stone':1}, 'forgeable': True, 'value': 75}

# Craftable
ITEMS['fire pit'] = {'craftable': True, 'image': 135, 'weight': 23, 'materials': {'cut dry wood':4, 'ordinary rock':10}, 'random drop': 100}
ITEMS['wood block'] = {'craftable': True, 'material': 'wood', 'image': 27, 'weight': 2.1, 'value': 10, 'materials': {'cut green wood':2}}
ITEMS['flint block'] = {'craftable': True, 'material': 'stone', 'image': 29, 'weight': 3.5, 'value': 5, 'materials': {'flint stone':2}}

# Containers/bowls
ITEMS['large plate'] = {'image': 34, 'weight': 0.5, 'value': 2}
ITEMS['plate'] = {'image': 37, 'weight': 0.3, 'value': 1}
ITEMS['jar'] = {'image': 63, 'weight': 0.3, 'value': 50, 'value': 2, 'random drop': 60}
ITEMS['empty bottle'] = {'image': 64, 'weight': 0.2, 'value': 10, 'random drop': 25}
#ITEMS['empty blue bottle'] = {'image': 65, 'weight': 0.2}
ITEMS['pedestal and mortar'] = {'image': 60, 'weight': 1, 'value': 200}
ITEMS['coffee pot'] = {'image': 108, 'weight': 1, 'value': 5}
ITEMS['empty barrel'] = {'image': 131, 'weight': 10, 'value': 100}
ITEMS['empty mug'] = {'image': 147, 'weight': 0.4, 'value': 1}

# Misc items
ITEMS['candle burner'] = {'image': 61, 'weight': 1, 'value': 250, 'brightness': 100, 'light mask': 1, 'materials': {'candle':1, 'steel pipe': 1, 'steel wire': 1}, 'forgeable': True}
ITEMS['candle'] = {'image': 62, 'weight': 0.3, 'value': 25, 'brightness': 100, 'light mask': 1}
ITEMS['chop sticks'] = {'image': 106, 'weight': 0.1, 'value': 1}

ITEMS['airship fuel'] = {'alchemy': True, 'image': 130, 'weight': 25, 'materials': {'empty barrel':1, 'whale oil':3, 'distilled alcohol':5}, 'value': 2000}
ITEMS['horse bridle'] = {'image': 132, 'weight': 1, 'value': 300}

# Building Materials
ITEMS['ordinary rock'] = {'image': 115, 'weight': 1.5, 'value': 0, 'random drop': 2}
ITEMS['palm leaf'] = {'image': 137, 'weight': 0.6, 'value': 3}
ITEMS['pine branch'] = {'image': 138, 'weight': 0.6, 'value': 3}
ITEMS['brick'] = {'image': 97, 'weight': 1, 'value': 0, 'random drop': 60}

# Foods
ITEMS['barley'] = {'image': 148, 'health': 5, 'stamina': 3, 'hunger': 2, 'weight': 0.6, 'food': True, 'value': 3}
ITEMS['hops'] = {'image': 149, 'health': 3, 'stamina': 6, 'hunger': 1, 'weight': 0.6, 'food': True, 'value': 10}
ITEMS['coconut'] = {'image': 136, 'health': 10, 'stamina': 10, 'hunger': 12, 'weight': 0.9, 'food': True, 'value': 4}
ITEMS['cheese wedge'] = {'image': 38, 'health': 15, 'stamina': 5, 'hunger': 15, 'weight': 0.8, 'food': True, 'value': 5}
ITEMS['roasted chicken'] = {'image': 35, 'health': 20, 'stamina': 15, 'hunger': 30, 'weight': 3, 'materials': {'dead chicken':1}, 'food': True, 'value': 25}
ITEMS['roasted wyvern ribs'] = {'image': 129, 'health': 40, 'stamina': 45, 'hunger': 40, 'weight': 8, 'materials': {'wyvern meat':1}, 'food': True, 'value': 80}
ITEMS['roasted dolphin ribs'] = {'image': 129, 'health': 30, 'stamina': 35, 'hunger': 42, 'weight': 9, 'materials': {'dolphin meat':1}, 'food': True, 'value': 40}
ITEMS['roasted hawk'] = {'image': 35, 'health': 18, 'stamina': 19, 'hunger': 16, 'weight': 2.5, 'materials': {'dead hawk':1}, 'food': True, 'value': 25}
ITEMS['roasted rabbit'] = {'image': 56, 'health': 18, 'stamina': 25, 'hunger': 20, 'weight': 3.5, 'materials': {'dead rabbit':1}, 'food': True, 'value': 20}
ITEMS['roasted goldfish'] = {'image': 57, 'health': 15, 'stamina': 28, 'hunger': 8, 'weight': 3.5, 'materials': {'dead goldfish':1}, 'food': True, 'value': 2}
ITEMS['roasted bluefish'] = {'image': 57, 'health': 18, 'stamina': 30, 'hunger': 15, 'weight': 3.5, 'materials': {'dead bluefish':1}, 'food': True, 'value': 5}
ITEMS['roasted leopard shark'] = {'image': 58, 'health': 26, 'stamina': 32, 'hunger': 37, 'weight': 5, 'materials': {'dead leopard shark':1}, 'food': True, 'value': 45}
ITEMS['roasted lamb'] = {'image': 59, 'health': 50, 'stamina': 17, 'hunger': 50, 'weight': 8, 'materials': {'sheep meat':1}, 'food': True, 'value': 42}
ITEMS['roasted pork'] = {'image': 59, 'health': 48, 'stamina': 10, 'hunger': 48, 'weight': 6, 'materials': {'pig meat':1}, 'food': True, 'value': 40}
ITEMS['roasted marlin'] = {'image': 111, 'health': 45, 'stamina': 35, 'hunger': 47, 'weight': 4, 'materials': {'marlin meat':1}, 'food': True, 'value': 70}
ITEMS['roasted giant squid'] = {'image': 100, 'health': 70, 'stamina': 26, 'hunger': 30, 'weight': 5, 'materials': {'giant squid meat':1}, 'food': True, 'value': 62}
ITEMS['roasted horse'] = {'image': 59, 'health': 45, 'stamina': 20, 'hunger': 40, 'weight': 10, 'materials': {'horse meat':1}, 'food': True, 'value': 44}
ITEMS['chicken soup'] = {'image': 81, 'health': 110, 'stamina': 100, 'hunger': 32, 'weight': 1.5, 'materials': {'dead chicken':1, 'potato':1, 'carrot': 2, 'garlic':1, 'rosemary':1, 'sage':1}, 'food': True, 'value': 150}
ITEMS['baked potato'] = {'image': 83, 'health': 12, 'stamina': 15, 'hunger': 10, 'weight': 0.2, 'materials': {'potato':1}, 'food': True, 'value': 7}
ITEMS['french bread'] = {'image': 36, 'health': 10, 'stamina': 10, 'hunger': 10, 'weight': 0.6, 'food': True, 'value': 6}
ITEMS['potato'] = {'image': 82, 'health': 2, 'hunger': 2, 'weight': 0.2, 'food': True, 'value': 1}
ITEMS['garlic'] = {'image': 76, 'health': 5, 'hunger': 1, 'stamina': 1, 'weight': 0.1, 'food': True, 'value': 2, 'random drop': 30}
ITEMS['oregano'] = {'image': 77, 'health': 2, 'hunger': 1, 'weight': 0.1, 'food': True, 'value': 2, 'random drop': 50}
ITEMS['sage'] = {'image': 79, 'health': 1, 'hunger': 1, 'weight': 0.1, 'food': True, 'value': 3, 'random drop': 40}
ITEMS['rosemary'] = {'image': 80, 'stamina': 4, 'hunger': 1, 'weight': 0.1, 'food': True, 'value': 4, 'random drop': 45}
ITEMS['carrot'] = {'image': 98, 'health': 2, 'hunger': 6, 'stamina': 2, 'weight': 0.1, 'food': True, 'value': 1}
ITEMS['california roll'] = {'image': 103, 'hunger': 11, 'health': 10, 'stamina': 3, 'weight': 0.1, 'food': True, 'value': 35}
ITEMS['salmon sushi'] = {'image': 104, 'hunger': 12, 'health': 12, 'stamina': 4, 'weight': 0.1, 'food': True, 'value': 40}
ITEMS['shrimp sushi'] = {'image': 105, 'hunger': 13, 'health': 8, 'stamina': 6, 'weight': 0.1, 'food': True, 'value': 28}
ITEMS['radioactive pizza'] = {'image': 151, 'health': 150, 'stamina': 150, 'hunger': -15, 'weight': 0.1, 'food': True, 'value': 200, 'brightness': 100, 'light mask': 1}

# Live animals
ITEMS['live green moth'] = {'image': 41, 'weight': 0.1, 'value': 2}
ITEMS['live butterfly ideopsis'] = {'image': 42, 'weight': 0.1, 'value': 5}
ITEMS['live pink moth'] = {'image': 39, 'weight': 0.1, 'value': 3}
ITEMS['live brown bird'] = {'image': 92, 'weight': 0.4, 'value': 6}
ITEMS['live garden lizard'] = {'image': 107, 'weight': 0.2, 'value': 5}

# Dead animals (also used for alchemy and enchanting)
ITEMS['marlin meat'] = {'image': 110, 'weight': 5, 'value': 20}
ITEMS['dolphin meat'] = {'image': 128, 'weight': 10, 'value': 28}
ITEMS['sheep meat'] = {'image': 31, 'weight': 12, 'value': 34}
ITEMS['pig meat'] = {'image': 31, 'weight': 10, 'value': 30}
ITEMS['horse meat'] = {'image': 31, 'weight': 15, 'value': 35}
ITEMS['wyvern meat'] = {'image': 128, 'weight': 10, 'value': 65}
ITEMS['giant squid meat'] = {'image': 99, 'weight': 6, 'value': 45}
ITEMS['dead pink moth'] = {'image': 39, 'weight': 0.1, 'value': 2}
ITEMS['dead giant ant'] = {'image': 40, 'weight': 3}
ITEMS['dead green moth'] = {'image': 41, 'weight': 0.1, 'value': 2}
ITEMS['dead butterfly ideopsis'] = {'image': 42, 'weight': 0.1, 'value': 5}
ITEMS['dead bluefish'] = {'image': 48, 'weight': 1, 'value': 2}
ITEMS['dead leopard shark'] = {'image': 49, 'weight': 6, 'value': 10}
ITEMS['dead snake'] = {'image': 50, 'weight': 1, 'value': 10}
ITEMS['dead rabbit'] = {'image': 14, 'weight': 5, 'value': 12}
ITEMS['dead chicken'] = {'image': 15, 'weight': 4, 'value': 20}
ITEMS['dead hawk'] = {'image': 109, 'weight': 3, 'value': 15}
ITEMS['dead goldfish'] = {'image': 16, 'weight': 0.8, 'value': 1}
ITEMS['dead brown bird'] = {'image': 91, 'weight': 0.4, 'value': 1, 'random drop': 46}
ITEMS['dead garden lizard'] = {'image': 107, 'weight': 0.2, 'value': 5, 'random drop': 34}

# Alchemy materials
ITEMS['yarrow'] = {'image': 78, 'health': 2, 'weight': 0.1, 'value': 5, 'random drop': 36}
ITEMS['ant exoskeleton shell'] = {'image': 46, 'weight': 6, 'value': 250}
ITEMS['giant ant eggs'] = {'image': 47, 'weight': 1, 'value': 90, 'random drop': 60}
ITEMS['spider egg sack'] = {'image': 133, 'weight': 1, 'value': 250, 'random drop': 80}
ITEMS['zombie extract'] = {'change race': 'immortui', 'image': 10, 'weight': 0.5, 'value': 34}
ITEMS['spider venom'] = {'health': -30, 'image': 9, 'weight': 0.5, 'value': 20}
ITEMS['dragon spit'] = {'image': 2, 'weight': 0.5, 'value': 1000}
ITEMS['sulphur'] = {'image': 73, 'weight': 0.5, 'value': 45, 'random drop': 65}
ITEMS['charcoal'] = {'image': 74, 'weight': 0.2, 'value': 10, 'random drop': 35}
ITEMS['coal'] = {'image': 74, 'weight': 0.3, 'value': 15, 'random drop': 200}
ITEMS['potassium nitrate crystals'] = {'image': 75, 'weight': 0.3, 'value': 54, 'random drop': 78}
ITEMS['squid tentacle'] = {'image': 101, 'weight': 2, 'value': 28}
ITEMS['squid eye'] = {'image': 102, 'weight': 0.5, 'value': 65}
ITEMS['squid ink'] = {'health': 5, 'image': 10, 'weight': 0.5, 'value': 25}
ITEMS['living water'] = {'health': 15, 'image': 7, 'weight': 0.2, 'value': 50, 'brightness': 30}
ITEMS['bottled water'] = {'health': 5, 'image': 7, 'weight': 0.2, 'value': 2}
ITEMS['distilled alcohol'] = {'health': -20, 'image': 6, 'weight': 0.2, 'value': 100}
ITEMS['whale oil'] = {'image': 4, 'weight': 0.2, 'value': 100}
ITEMS['sea turtle shell'] = {'image': 112, 'weight': 200, 'value': 300}
ITEMS['turtle shell plate'] = {'image': 113, 'weight': 3, 'value': 150}
ITEMS['demon dust'] = {'image': 121, 'weight': 0.1, 'value': 52}
ITEMS['ectoplasm'] = {'image': 122, 'weight': 0.1, 'value': 52}
ITEMS['clay'] = {'image': 123, 'weight': 1, 'value': 30, 'random drop': 20}
ITEMS['feather'] = {'image': 141, 'weight': 0.1, 'value': 1, 'random drop': 18}
ITEMS['yellow rose'] = {'image': 143, 'weight': 0.1, 'value': 6, 'random drop': 90}

# Forging Materials (some are also used for enchanting)
ITEMS['steel pipe'] = {'image': 84, 'weight': 2, 'materials': {'steel ingot': 1}, 'forgeable': True, 'value': 50}
ITEMS['springs'] = {'image': 85, 'weight': 0.1, 'materials': {'steel wire': 1}, 'forgeable': True, 'value': 45}
ITEMS['steel wire'] = {'image': 86, 'weight': 0.5, 'materials': {'steel ingot': 1}, 'forgeable': True, 'value': 46}
ITEMS['machine screws'] = {'image': 87, 'weight': 0.2, 'materials': {'aluminum rod': 1}, 'forgeable': True, 'value': 55}
ITEMS['aluminum rod'] = {'image': 88, 'weight': 0.3, 'materials': {'aluminum ingot': 1}, 'forgeable': True, 'value': 40}
ITEMS['steel rod'] = {'image': 88, 'weight': 0.3, 'materials': {'steel ingot': 1}, 'forgeable': True, 'value': 40}
ITEMS['brass tubing'] = {'image': 89, 'weight': 0.3, 'materials': {'brass ingot': 1}, 'forgeable': True, 'value': 30}
ITEMS['gun powder'] = {'alchemy': True, 'image': 72, 'weight': 1, 'materials': {'sulphur': 1, 'charcoal': 1, 'potassium nitrate crystals': 1, 'sheep horn': 1, 'leather strips': 1}, 'value': 100}
ITEMS['sheep horn'] = {'image': 32, 'weight': 1, 'value': 10}
ITEMS['sheep skin'] = {'image': 33, 'weight': 2, 'value': 15}
ITEMS['pig skin'] = {'image': 33, 'weight': 1.7, 'value': 12}
ITEMS['horse skin'] = {'image': 55, 'weight': 2, 'value': 17}
ITEMS['bear skin'] = {'image': 52, 'weight': 3, 'value': 22}
ITEMS['wolf skin'] = {'image': 53, 'weight': 2, 'value':19}
ITEMS['deer skin'] = {'image': 54, 'weight': 2, 'value': 18}
ITEMS['red wyvern skin'] = {'image': 126, 'weight': 1, 'value': 45}
ITEMS['blue wyvern skin'] = {'image': 127, 'weight': 1, 'value': 45}
ITEMS['gold ingot'] = {'material': 'metal', 'image': 17, 'weight': 5.5, 'value': 300, 'materials': {'gold ore': 2}}
ITEMS['lead ingot'] = {'material': 'metal', 'image': 20, 'weight': 8, 'value': 150, 'materials': {'lead ore': 2}}
ITEMS['iron ingot'] = {'material': 'metal', 'image': 18, 'weight': 4, 'value': 12, 'materials': {'iron ore': 2}}
ITEMS['silver ingot'] = {'material': 'metal', 'image': 19, 'weight': 4.5, 'value': 210, 'materials': {'silver ore': 2}}
ITEMS['steel ingot'] = {'material': 'metal', 'image': 20, 'weight': 3.5, 'value': 40, 'materials': {'iron ore': 2, 'charcoal': 2}}
ITEMS['copper ingot'] = {'material': 'metal', 'image': 21, 'weight': 5, 'value': 14, 'materials': {'copper ore': 2}}
ITEMS['bronze ingot'] = {'material': 'metal', 'image': 22, 'weight': 4.8, 'value': 18, 'materials': {'copper ore': 1, 'tin ore': 1}}
ITEMS['brass ingot'] = {'material': 'metal','image': 23, 'weight': 4.7, 'value': 16, 'materials': {'copper ore': 1, 'zinc ore': 1}}
ITEMS['tin ingot'] = {'material': 'metal', 'image': 24, 'weight': 3, 'value': 20, 'materials': {'tin ore': 2}}
ITEMS['aluminum ingot'] = {'material': 'metal', 'image': 24, 'weight': 3, 'value': 40, 'materials': {'aluminum ore': 2}}
ITEMS['ebony block'] = {'material': 'wood', 'image': 25, 'weight': 2, 'value': 60}
ITEMS['ironwood block'] = {'material': 'wood', 'image': 25, 'weight': 2.5, 'value': 100}
ITEMS['olive wood block'] = {'material': 'wood', 'image': 27, 'weight': 2.1, 'value': 70}
ITEMS['rosewood block'] = {'material': 'wood', 'image': 28, 'weight': 1.8, 'value': 80}
ITEMS['flint stone'] = {'material': 'stone', 'image': 30, 'weight': 1, 'value': 2, 'random drop': 14}
ITEMS['leather'] = {'material': 'fabric', 'image': 43, 'weight': 0.7, 'value': 20}
ITEMS['leather strips'] = {'material': 'fabric', 'image': 51, 'weight': 0.4, 'value': 20}
ITEMS['iron ore'] = {'material': 'metal', 'image': 0, 'weight': 5, 'value': 5}
ITEMS['gold ore'] = {'material': 'metal', 'image': 90, 'weight': 8, 'value': 130}
ITEMS['tin ore'] = {'material': 'metal', 'image': 93, 'weight': 3, 'value': 9}
ITEMS['copper ore'] = {'material': 'metal', 'image': 94, 'weight': 4, 'value': 6}
ITEMS['silver ore'] = {'material': 'metal', 'image': 95, 'weight': 4.5, 'value': 90}
ITEMS['aluminum ore'] = {'material': 'metal', 'image': 94, 'weight': 3, 'value': 18}
ITEMS['lead ore'] = {'material': 'metal', 'image': 95, 'weight': 10, 'value': 25}
ITEMS['zinc ore'] = {'material': 'metal', 'image': 95, 'weight': 3, 'value': 24}
ITEMS['cut dry wood'] = {'material': 'metal', 'image': 114, 'weight': 2, 'value': 5}
ITEMS['cut green wood'] = {'material': 'metal', 'image': 114, 'weight': 2.2, 'value': 5}

# Ammo
ITEMS['arrow'] = {'ammo': 1, 'type': 'bow', 'image': 139, 'weight': 0.1, 'value': 1, 'craftable': True, 'materials': {'cut green wood': 1, 'feather': 1, 'flint stone': 1}}
ITEMS['small arrow quiver'] = {'ammo': 30, 'type': 'bow', 'image': 140, 'weight': 1.5, 'value': 70, 'craftable': True, 'materials': {'cut green wood': 1, 'feather': 2, 'flint stone': 1}}
ITEMS['large arrow quiver'] = {'ammo': 60, 'type': 'bow', 'image': 140, 'weight': 1.5, 'value': 70, 'craftable': True, 'materials': {'cut green wood': 2, 'feather': 6, 'flint stone': 2}}
ITEMS['large pistol ammo case'] = {'ammo': 100, 'type': 'pistol', 'image': 12, 'weight': 7, 'value': 80}
ITEMS['large shotgun ammo case'] = {'ammo': 100, 'type': 'shotgun', 'image': 12, 'weight': 10, 'value': 100}
ITEMS['large rifle ammo case'] = {'ammo': 100, 'type': 'rifle', 'image': 12, 'weight': 9, 'value': 120}
ITEMS['medium pistol ammo case'] = {'ammo': 50, 'type': 'pistol', 'image': 13, 'weight': 5, 'materials': {'brass tubing':2, 'gun powder':2, 'lead ingot':1}, 'forgeable': True, 'value': 40}
ITEMS['medium shotgun ammo case'] = {'ammo': 50, 'type': 'shotgun', 'image': 13, 'weight': 6, 'materials': {'brass tubing':2, 'gun powder':2, 'lead ingot':1}, 'forgeable': True, 'value': 50}
ITEMS['medium rifle ammo case'] = {'ammo': 50, 'type': 'rifle', 'image': 13, 'weight': 6, 'materials': {'brass tubing':2, 'gun powder':2, 'lead ingot':1}, 'forgeable': True, 'value': 60}
ITEMS['medium laser ammo module'] = {'ammo': 50, 'type': 'laser', 'image': 45, 'weight': 3, 'value': 70}
ITEMS['large laser ammo module'] = {'ammo': 100, 'type': 'laser', 'image': 44, 'weight': 5, 'value': 140}
# Crystals
ITEMS['black crystal'] = {'image': 71, 'weight': 0.5, 'ammo': 150, 'type': 'crystals', 'value': 500}
ITEMS['white crystal'] = {'image': 68, 'weight': 0.5, 'ammo': 100, 'type': 'crystals', 'value': 500}
ITEMS['blue crystal'] = {'image': 66, 'weight': 0.5, 'ammo': 80, 'type': 'crystals', 'value': 200}
ITEMS['green crystal'] = {'image': 69, 'weight': 0.5, 'ammo': 70, 'type': 'crystals', 'value': 170}
ITEMS['yellow crystal'] = {'image': 70, 'weight': 0.5, 'ammo': 50, 'type': 'crystals', 'value': 135}
ITEMS['red crystal'] = {'image': 67, 'weight': 0.5, 'ammo': 25, 'type': 'crystals', 'value': 100}

ITEMS['diamond'] = {'image': 152, 'weight': 0.5, 'value': 300}

# Books
ITEMS['old book'] = {'image': 117, 'weight': 1, 'value': 0, 'author': '', 'heading': '', 'spell words': '', 'font': 'SCRIPT_FONT'}
ITEMS['book: War of the Worlds'] = {'image': 117, 'weight': 0.2, 'value': 5, 'author': 'H. G. Wells', 'heading': 'War of the Worlds', 'spell words': '', 'font': 'SCRIPT_FONT'}
ITEMS['book: A Tale of Two Cities'] = {'image': 117, 'weight': 0.3, 'value': 5, 'author': 'Charles Dickens', 'heading': 'A Tale of Two Cities', 'spell words': '', 'font': 'SCRIPT_FONT'}
ITEMS['book of basic enchantments'] = {'image': 117, 'weight': 1, 'value': 5, 'author': 'Olrond Magarfindrel', 'heading': 'Book of Basic Enchantments', 'spell words': '', 'font': 'SCRIPT_FONT'}
ITEMS['Guide book to Arroshay'] = {'image': 117, 'weight': 1, 'value': 0, 'author': 'King Dent', 'heading': "Hitchhiker's Guide to Arroshay" , 'spell words': '', 'font': 'SCRIPT_FONT'}

# Letters
ITEMS['letter to Zeladria'] = {'image': 145, 'weight': 0.1, 'value': 0, 'author': 'King Draconius', 'heading': 'to Queen Zeladria', 'spell words': '', 'font': 'WRITING_FONT'}
ITEMS['letter from Zeladria'] = {'image': 145, 'weight': 0.1, 'value': 0, 'author': 'Queen Zeladria', 'heading': 'to King Draconius', 'spell words': '', 'font': 'WRITING_FONT'}
ITEMS['letter from Loella'] = {'image': 145, 'weight': 0.1, 'value': 0, 'author': 'Loella', 'heading': 'to Daddy', 'spell words': '', 'font': 'WRITING_FONT'}
ITEMS['letter from Alex'] = {'image': 145, 'weight': 0.1, 'value': 0, 'author': 'Daddy', 'heading': 'to Loella', 'spell words': '', 'font': 'WRITING_FONT'}

# Spell books
ITEMS['book of demon secrets'] = {'image': 142, 'spell': 'demonic possession', 'weight': 1, 'sound': 'enchant', 'value': 9000, 'author': 'Lucious Captivarian', 'heading': "The Book of Demon Secrets", 'font': 'SCRIPT_FONT',
                                  'spell words': 'wE SPka  sepUka wE  wE famas aka  ka epa wE'}
ITEMS['elementary healing tome'] = {'image': 118, 'spell': 'healing', 'weight': 1, 'sound': 'casting healing', 'value': 2000, 'author': 'Tamolin Abara', 'heading': 'Elementary Healing Magic', 'spell words': 'beUma wE samawaha P UwaRa', 'font': 'SCRIPT_FONT'}
ITEMS['fireball tome'] = {'image': 119, 'spell': 'fireball', 'weight': 1, 'sound': 'fire blast', 'value': 700, 'author': 'Draconius Elandrom', 'heading': 'Casting Fireballs', 'spell words': 'eTU ba yEda', 'font': 'SCRIPT_FONT'}
ITEMS['fire spray tome'] = {'image': 120, 'spell': 'fire spray', 'sound': 'fire blast', 'weight': 1, 'value': 3000, 'author': 'Draconius Elandrom', 'heading': 'Conjouring Zharan Flames', 'spell words': 'ba ayEda eJarE', 'font': 'SCRIPT_FONT'}
ITEMS['summon golem tome'] = {'image': 124, 'spell': 'summon golem', 'weight': 1, 'sound': 'casting healing', 'value': 4000, 'author': 'Tamolin Abara', 'heading': 'The Art of Creating Life', 'spell words': 'heyeba ruhEged', 'font': 'SCRIPT_FONT'}
ITEMS['summon rabbit tome'] = {'image': 125, 'spell': 'summon rabbit', 'weight': 1, 'sound': 'casting healing', 'value': 1100, 'author': 'Tamolin Abara', 'heading': 'Practicing Summoning', 'spell words': 'yeba vidUru', 'font': 'SCRIPT_FONT'}


# Misc Keys for vehicles and such
ITEMS['airship key'] = {'image': 116, 'weight': 0.1, 'value': 10000}

# Generates keys for all chests
for chest in CHESTS:
    key_name = chest + " chest key"
    ITEMS[key_name] = {'image': 116, 'weight': 0.1, 'value': 100}


NAMED_DOOR_LIST = ["Kevin's house"]
# Generates keys for all doors in the list.
for door in NAMED_DOOR_LIST:
    key_name = door + " key"
    ITEMS[key_name] = {'image': 116, 'weight': 0.1, 'value': 100}


FORGEITEMS = ['gold ingot', 'iron ingot', 'silver ingot', 'steel ingot', 'copper ingot', 'bronze ingot', 'brass ingot', 'tin ingot', 'ebony block', 'ironwood block', 'olive wood block', 'rosewood block', 'flint block', 'flint stone', 'leather', 'leather strips']
FLOAT_LIST = ['fish', 'wood', 'shark', 'butterfly', 'bread', 'moth']

UPGRADED_ITEMS = {}