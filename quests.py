QUESTS = {}
QUESTS['A fish for Loella'] = {'accepted': False, 'completed': False, 'rewarded': False, 'inventory check': False,
                               'description': 'Catch a goldfish for Loella\'s fish tank in the town of Dewcastle.',
                               'accept text': ['Oh, thank you so much! I\'m so excited!'],
                               'deny text': ['Oh... ok. I hope my daddy will get home soon to help me.'],
                               'completed text': ['I love my new fish!'],
                               'waiting text': ['Have you found a fish for me yet? I hope you find one soon. I\'m so excited. Please hurry.'],
                               'reward': ['potion of major healing'],
                               'reward text': ['Thank you so much for the fish. Please take this healing potion as a token of my appreciation.'],
                               'next quest': 'A friend for Loella',
                               'next dialogue': 'LOELLA_DLG2'}

QUESTS['A friend for Loella'] = {'accepted': False, 'completed': False, 'rewarded': False, 'inventory check': False,
                               'description': 'Loella needs help finding a friend in the town of Dewcastle.',
                               'accept text': ['Oh, thank you so much! I\'m so excited to meet my new friend!'],
                               'deny text': ['Oh... ok. I guess I\'ll have to go out and make friends like a normal kid.'],
                               'completed text': ['I\'m really enjoying playing with Kimmy!'],
                               'waiting text': ['Have you found a friend for me yet? I hope you find one soon. I\'m so excited. Please hurry.'],
                               'reward': ['potion of major stamina'],
                               'reward text': ['Thank you so much for introducing me to Kimmy! Please take this stamina potion as a token of my appreciation.'],
                               'next quest': None,
                               'next dialogue': None}

QUESTS['A mace for Steve'] = {'accepted': False, 'completed': False, 'rewarded': False, 'inventory check': True, 'needed item': 'mace',
                               'description': 'Steve is a slacker and lost his mace. He needs help finding a new one in the town of Dewcastle.',
                               'accept text': ['Oh, thank you so much! You\'re a life saver.'],
                               'deny text': ['Thanks okay. I can see you\'re busy.'],
                               'completed text': ['This new mace is awesome. You really saved my neck.'],
                               'waiting text': ['Have you found that mace for me yet? The captain will have my head for this. Please hurry.'],
                               'has item text': ['I see you brought me a mace. May I have it?YN'],
                               'refuse to give text': ['That\'s not at all what we agreed to. How rude.'],
                               'reward': ['baked potato', 'cheese wedge', 'gold:12'],
                               'reward text': ['Thanks so much. Sorry, I don\'t have much to reward you with, but here\'s my lunch and what\'s left of yesterday\'s wages.'],
                               'next quest': None,
                               'next dialogue': 'STEVE_DLG2'}

QUESTS['Ant eggs for Tamolin'] = {'accepted': False, 'completed': False, 'rewarded': False, 'inventory check': True, 'needed item': 'giant ant eggs',
                               'description': 'Tamolin of Dewcastle wants you to find giant ant eggs so he can create powerful new potions. Search the ant tunnels to the south and see if you can find any eggs.',
                               'accept text': ['Oh, thank you. I would have gone myself, but I\'d have no one to watch the shop for me.'],
                               'deny text': ['Not up to it huh? Perhaps I can find someone else who is brave enough.'],
                               'completed text': ['These eggs are beautiful. They are much larger than I expected.'],
                               'waiting text': ['Any luck finding those ant eggs for me?'],
                               'has item text': ['Wonderful! I see you found some giant ant eggs. May I have them?YN'],
                               'refuse to give text': ['Oh, so you want them for yourself huh? Ok, good luck figuring out what to do with them.'],
                               'reward': ['gold:2000'],
                               'reward text': ['Amazing! I can tell you are a brave adventurer.'],
                               'next quest': 'Clay for Tamolin',
                               'next dialogue': 'TAMOLIN_DLG2'}

QUESTS['Clay for Tamolin'] = {'accepted': False, 'completed': False, 'rewarded': False, 'inventory check': True, 'needed item': 'clay&4', 'action': 'summon:clay golem guard',
                               'description': 'Tamolin of Dewcastle wants your help finding clay so he can create a golem.',
                               'accept text': ["Thank's again. You're the type of person I know I can count on. They say the Lacertolians sell fine clay, but you might also just find some lying around if you search hard enough."],
                               'deny text': ["Well, I suppose you've done enough for me already. I'll find someone else to help."],
                               'completed text': ["Now that we know have to summon a golem we can protect ourselves and our city."],
                               'waiting text': ["Any luck finding thay clay yet?"],
                               'has item text': ["It looks like you found that clay. May I have it?YN"],
                               'refuse to give text': ['So you want them for yourself huh? Ok, good luck figuring out what to do with it. Maybe you can make a pot or something!'],
                               'reward': ['summon golem tome'],
                               'reward text': ["This clay will do nicely. Now let's try to summon a golem. I just need to put the finishing touches in my spell Tome. I always make two copies of my work. You can have one as a reward for all of your help."],
                               'next quest': None,
                               'next dialogue': 'TAMOLIN_DLG3'}

QUESTS['Fuel for Felius'] = {'accepted': False, 'completed': False, 'rewarded': False, 'inventory check': True, 'needed item': 'airship fuel', 'action': 'companion',
                               'description': 'Find some fuel for Felius\' airship, so he can go back home.',
                               'accept text': ['Oh, thank you so much! Please take as many of those empty barrels by my house as you can carry. You\'ll need them to bring the fuel back in.', 'Good luck my friend!'],
                               'deny text': ['Oh, I hope you change your mind. I\'m not sure how much longer I can survive out here.'],
                               'completed text': ['This is perfect! You really saved my life. You won\'t regret this!'],
                               'waiting text': ['Any luck finding airship fuel? I could probably make some if I had an alchemy lab.', 'An alchemist friend of mine made the fuel, using oil and alcohol.'],
                               'has item text': ['Wonderful! You found the fuel. May I have it?YN'],
                               'refuse to give text': ['Oh, well that\'s cruel of you to bring it all this way just to taunt me.'],
                               'reward': [],
                               'reward text': ['Thank you so much! Now I can be with my family again. I don\'t have anything to offer except for my airship. I think I\'ve done enough exploring for one lifetime. Accompany me home and the key is yours.'],
                               'next quest': 'Take Felius Home',
                               'next dialogue': 'FELIUS_DLG2'}

QUESTS['Take Felius Home'] = {'accepted': False, 'completed': False, 'rewarded': False, 'inventory check': False, 'autoaccept': True,
                               'description': 'Escort Felius back to his home in Norwald.',
                               'completed text': ['I\'m so happy to be home.'],
                               'waiting text': ['I hope it doesn\'t take us too much longer to get home.', 'It\'s a long way home to Norwald. I\'m glad to have a warrior like you accompanying me.', 'I\'ll fight for you so long as we are together friend.'],
                               'reward': ['airship key'],
                               'reward text': ['Thank you so much! I\'m so happy to be with my family again. Here\'s the key to my airship. Please take good care of her.'],
                               'next quest': None,
                               'next dialogue': 'FELIUS_DLG2'}

QUESTS['Cleanse the Temple of Zhara'] = {'accepted': False, 'completed': False, 'rewarded': False, 'inventory check': True, 'needed item': 'Zhara Talisman', 'action': None,
                               'description': 'Find the Temple of Zhara to the southeast, destroy the evil spirits there and bring back any Zharan relics you find.',
                               'accept text': ['You must have been a brave warrior in your past life. The demons must be after something of value there. I bet they are guarding some Zharan relic. Please bring back whatever treasure you find there. I must warn you, the black wraiths can only be destroyed by magic and energy weapons. Please take this magic tome. Read it and you will learn the art of fire magic. GIFTS'],
                               'deny text': ['You really ought to reconsider. I have a feeling you came back to this world for a very important reason and that this quest is only the beginning of your fate.'],
                               'completed text': ['This is perfect! You really saved my life. You won\'t regret this!'],
                               'waiting text': ["I would come with you on your journey, but I must stay here at the Temple of Demos to welcome any new spirit that may arrive.", "I fish you the best of luck on your journey."],
                               'has item text': ["I hear you have cleansed the temple. May I have a look at what you found there?YN"],
                               'refuse to give text': ['It is unwise for you to keep such treasures to yourself. I could give you valuable insight into their purpose and meaning.'],
                               'reward': ['Zhara Talisman'],
                               'gifts': ['fireball tome'],
                               'reward text': ["I don't believe it! You've found the Zhara Talisman. It's been missing since the fall of Zhara. It possesses great power. If the one who wears it has within them the soul of the Yaizhavay then the talisman will bring that dragon soul to life. I have a feeling you found this for a reason. You must take it on your journey. Press T to invoke your dragon soul and F to breathe fire."],
                               'next quest': None,
                               'next dialogue': 'ZHAWAY_DLG2'}

QUESTS['Give letter to Zeladria'] = {'accepted': False, 'completed': False, 'rewarded': False, 'inventory check': True, 'needed item': 'letter to Zeladria',
                               'description': 'Give Zeladria the letter from the king of Dewcastle.',
                               'accept text': ["May I hear it then? YN"],
                               'lie text': ["Why would you lie to me? You don't have anything to tell me from your king. Don't you know we elves can tell when we are being lied to."],
                               'deny text': ['Oh, forget I asked.'],
                               'completed text': ['I am troubled by the growing darkness in our land.'],
                               'waiting text': ['Hello again. You should return to your king in your own land. We have no need for your assistance here.'],
                               'has item text': ['I see you have a letter for me. May I have it?YN'],
                               'refuse to give text': ['Why would you come all this way just to refuse to give it to me?'],
                               'reward': ['letter from Zeladria', 'gold:100'],
                               'reward text': ["This is worse than I thought. Please take this response letter back to your king. Here is some gold for your troubles."],
                               'next quest': None,
                               'next dialogue': 'ELF_QUEEN_DLG'}

QUESTS['Turtle Armor for Jaz'] = {"accepted": False, "completed": False, "rewarded": False, "inventory check": True, "needed item": "turtle plate armor", "description": "Forge Jaz some turtle plate armor, so she can be ready for her epic quest.", "accept text": ["Oh, thank you so much. I wish I had the smithing skills to make my own armor, but I'm so glad you decided to help me."], "deny text": ["Oh, well that's okay. Maybe I can learn how to make some for myself."], "completed text": ["This new armor is awesome. Thanks so much!"], "waiting text": ["Have you made me that armor yet?"], "has item text": ["I see you made some turtle armor for me. May I have it?YN"], "refuse to give text": ["Oh, you decided to keep it for yourself huh? Well, it is really nice. I don't blame you. I'll just have to make my own."], "reward text": ["Amazing! Here's a little cash for your efforts and some lunch."], "next quest": 'Let Jaz join your quest', "next dialogue": "JAZ_DLG2", "reward": ["roasted bluefish","gold:225"]}
QUESTS['Let Jaz join your quest'] = {'action': 'companion', "autocomplete": True, "accepted": False, "completed": False, "rewarded": False, "inventory check": False, "needed item": None, "description": "Let Jaz join your quest.", "accept text": ["Oh, thank you so much. I'll do my best to make a great companion on your journey."], "deny text": ["Oh, I guess you'd rather travel alone. I'm sure I can find an epic quest myself."], "completed text": ["I'm excited. Lead the way!"], "waiting text": [""], "has item text": [""], "refuse to give text": [""], "reward text": ["Here's some more food for our journey."], "next quest": None, "next dialogue": "JAZ_DLG3", "reward": ['cheese wedge', 'french bread']}
QUESTS['Jamal the body guard'] = {'action': 'companion', "accepted": False, "completed": False, "rewarded": False, "inventory check": True, "needed item": "gold:1000", "autocomplete": False, "autoaccept": False, "description": "Pay Jamal 1000 gold to protect you.", "accept text": ["Great. You won't regret this."], "deny text": ["Well, maybe next time."], "completed text": ["I'll shoot anything that gets in our way."], "waiting text": ["Got that money yet?"], "has item text": ["I see you have the cash. Want to pay me now?YN"], "refuse to give text": ["I'd reconsider if I were you."], "reward text": ["Nice. I've got your back."], "next quest": None, "next dialogue": "JAMAL_DLG2", "reward": [""]}
QUESTS['Find gold ore for Hagitha'] = {"accepted": False, "completed": False, "rewarded": False, "inventory check": True, "needed item": "gold ore", "autocomplete": False, "autoaccept": False, "description": "Find some gold ore for Hagitha. When you do she might tell you some valuable information.", "accept text": ["Excellent. I have an extra pickaxe you can take with you. It's always better to find someone else to do the hard work for you. That's what I always say. GIFTS"], "deny text": ["Suit yourself. I don't share any information with people who aren't willing to help."], "completed text": ["Well, You might notice I'm a goblin, we're not all aggressive like the ones you'd usually run into in the forest. We used to be a race of peaceful wood elves until King Grump took over and used his dark magic to make us all his orange slaves. A few of us have managed to escape his mind control magic, but unfortunately we are still hated and despised by the other elves. I hear King Grump has moved to an island where he surrounded himself with a great wall and guards to keep everyone out. I wish I knew where that island was. Then I'd kill him myself."], "waiting text": ["Have you found that ore yet?"], "has item text": ["I see you found some gold ore. May I have it?YN"], "refuse to give text": ["I ought to eat your face off for taunting me like that."], "reward text": ["This ore is excellent quality. Here's some of my finest liquor and something to eat as a reward."], "next quest": None, "next dialogue": "HAGITHA_DLG2", "gifts": ["pickaxe"], "reward": ["distilled alcohol", "roasted chicken"]}
QUESTS['Harvest the potatoes'] = {"accepted": False, "completed": False, "rewarded": False, "inventory check": True, "needed item": "potato&20", "autocomplete": False, "autoaccept": False, "description": "Uncle John is an old wounded war veteran. He needs your help to harvest twenty potatoes from the garden.", "accept text": ["You're a good kid. Here you'll need this shovel. Press I to access your inventory so you can equip the shovel. GIFTS"], "deny text": ["You had better reconsider. We all need to do our share of the work around here."], "completed text": ["You're such a hard working kid. I'm an old man and we just don't have the money we need to keep living here. You should go up to the king's palace and apply to be one of his guards. They pay very handsomely."], "waiting text": ["Have you harvested the potatoes yet?"], "has item text": ["Nice work kiddo! May I take those potatoes off your hands. YN"], "refuse to give text": ["Well, you can't just carry them around all day. Now, give them here!"], "reward text": ["I have something I've been wanting to give you for some time. I think you are finally old enough. Your mother always wore this necklace. It is an ancient relic called a Zhara Talisman. Before Zhara fell the dragons of noble birth wore them. They are said to possess great magical power. Legend has it that the dragons used their magic to take on human form. Let me tell you a secret: The markings on this talisman are particularly special. I think your mother was a descendant of the Ikthee, the last dragon prince. The legend says that he and Melerous were twin brothers born from the dragon queen and an Osidine father. Melerous was not born with the gift of being able to take on dragon form, and he was jealous that his brother was. So, Melerous decided gain power through the study of magic, a path that lead him to fall into darkness and lust for power. Melerous used his magic to overthrow Zhara, but before Zhara fell into the ocean, Ikthee put an end to Melerous. With the fall of Zhara, Ikthee had no home, so he came here to live among us. That talisman meant a lot to your mother. I think she would want you to have it as a reminder of how much she loved you. You never know, you may have some dragon blood in you as well. If you hold the talisman and press T you will transform into a dragon if you do. Once in dragon form you can breathe fire by pressing F."], "next quest": None, "next dialogue": "JOHN_DLG2", "gifts": ["shovel"], "reward": ["Zhara Talisman"]}
QUESTS['Deliver a letter to the Elf Queen'] = {"accepted": False, "completed": False, "rewarded": False, "inventory check": True, "needed item": "letter from Zeladria", "autocomplete": False, "autoaccept": False, "description": "King Draconius needs you to deliver a letter to Zeladria the elf queen. She lives in a forest village to the west. The king has promissed to make you one of his guards if you do so.", "accept text": ["It's settled then. Take this letter and may the souls of the ancients protect you on your journey.GIFTS"], "deny text": ["Very well then. I see you are not fit to be one of my guards."], "completed text": ["Now that you are one of my guards it is your solemn duty to protect the people of Dewcastle. "], "waiting text": ["Have you delivered that letter yet? It is a time sensitive matter you know."], "has item text": ["Wonderful, you've brought word from Zeladria. May I have the letter? YN"], "refuse to give text": ["I should have you beheaded. You have not right to interfear with royal matters."], "reward text": ["Well, you have done as I asked and has promissed you are now one of my royal guards. Here is your standard issue armor and your wages. Unfortunately, the news from Zeladria is worrisome. She says the goblins haven't been themselves lately and have been attacking their villiage frequently, as if they are under control by a demonic force. She's concerned that Melerous has come back and is once again taking control of the dark forces of Arroshay.  This simply cannot be. Melerous was destroyed long ago and the remaining demons have been subdued. There must be some other dark force at play here. I must hold a conference with the elders at once."], "next quest": None, "next dialogue": "KING_DRACONIUS_DLG2", "gifts": ["letter to Zeladria"], "reward": ["guard armor", "steel sword", "steel helmet", "steel boots", "steel gauntlets", "gold:100"]}
QUESTS["Bill's fish"] = {"accepted": False, "completed": False, "rewarded": False, "inventory check": True, "needed item": "live goldfish", "autocomplete": False, "autoaccept": False, "description": "Bring Bill N. his fish back but alive.", "accept text": ["Thank you! I've always hoped this day would come!GIFTS"], "deny text": ["I'm *%#$ing pissed dude!"], "completed text": ["Thanks for bringing my fish back to life! I'm so glad!"], "waiting text": ["Is it alive yet?"], "has item text": ["It's a miracle! I see you brought my fish back to life. May I have it?YN"], "refuse to give text": ["Well, you're an A-hole."], "reward text": ["Oops! it died. Here, you can have it back!"], "next quest": None, "next dialogue": "BILL_DLG2", "gifts": ["dead goldfish"], "reward": ["dead goldfish"]}
QUESTS["Find a chicken"] = {"accepted": False, "completed": False, "rewarded": False, "inventory check": True, "needed item": "live chicken", "autocomplete": False, "autoaccept": False, "description": "Jeff doesn't know how to steal. Steal a chicken for him.", "accept text": ["Yay!"], "deny text": ["Dang!"], "completed text": ["I love my new chicken!"], "waiting text": ["Have you found it yet?"], "has item text": ["Ooh! Do you have it yet?YN"], "refuse to give text": ["Ughhh!"], "reward text": ["Thanks! Here's a peice of pizza."], "next quest": None, "next dialogue": "JEFF_DLG2", "gifts": [""], "reward": ["radioactive pizza"]}