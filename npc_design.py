from tkinter import *
from armor import *
from items import *
from weapons import *

class Npc_Info_Designer(Tk):
    """PEOPLE['generic'] = {'name': 'generic', 'protected': True, 'health': 100, 'touch damage': False, 'damage': 0, 'knockback': 2, 'walk speed': (90, 100), 'run speed': 300, 'detect radius': 300, 'avoid radius': 100, 'aggression': 'awp', 'armed': True, 'dual wield': False,
    'collide': ['vehicles', 'walls', 'jumpables', 'climbables', 'lava'],
    'gender': 'male', 'race': 'osidine',
    'dialogue': 'random VILLAGER_DLG', 'store': None,
    'inventory': {'gender': list(GENDER.keys()), 'race': list(RACE.keys()), 'weapons': list(WEAPONS.keys()), 'hats': list(HATS.keys()), 'hair': list(HAIR.keys()), 'tops': list(TOPS.keys()), 'bottoms': list(BOTTOMS.keys()), 'shoes': list(SHOES.keys()), 'gloves': list(GLOVES.keys()), 'gold': 100, 'items': ['random'], 'magic': list(MAGIC.keys())},
    'animations': {None}}"""

    def __init__(self, npc_menu, character):
        Tk.__init__(self)
        self.title("Zhara NPC Infor Designer (press Alt if it doesn't load)")
        self.character = character
        self.npc_menu = npc_menu
        Label(self, text="Aggression Type:", font="none 12 bold").grid(row=1, column=0, sticky=W)
        self.aggression_var = IntVar()
        Radiobutton(self, text="Flee when provoked", variable=self.aggression_var, value=1).grid(row=2, column=0, sticky=W)
        Radiobutton(self, text="Attack when provoked", variable=self.aggression_var, value=2).grid(row=2, column=1, sticky=W)
        Radiobutton(self, text="Flee until provoked", variable=self.aggression_var, value=3).grid(row=2, column=2, sticky=W)
        Radiobutton(self, text="Stationary aggressive when provoked", variable=self.aggression_var, value=4).grid(row=2, column=3, sticky=W)
        Radiobutton(self, text="Flee when detected", variable=self.aggression_var, value=5).grid(row=2, column=4, sticky=W)
        Radiobutton(self, text="Attack when detected", variable=self.aggression_var, value=6).grid(row=2, column=5, sticky=W)

        Label(self, text="Collides With:", font="none 12 bold").grid(row=3, column=0, sticky=W)
        self.obstaclesvar = IntVar()
        Checkbutton(self, text="obstacles", variable=self.obstaclesvar).grid(row=4, column=0, sticky=W)
        self.wallvar = IntVar()
        Checkbutton(self, text="walls", variable=self.wallvar).grid(row=4, column=1, sticky=W)
        self.jumpvar = IntVar()
        Checkbutton(self, text="jumpables", variable=self.jumpvar).grid(row=4, column=2, sticky=W)
        self.climbvar = IntVar()
        Checkbutton(self, text="climbables", variable=self.climbvar).grid(row=4, column=3, sticky=W)
        self.vehiclevar = IntVar()
        Checkbutton(self, text="vehicles", variable=self.vehiclevar).grid(row=4, column=4, sticky=W)
        self.lavavar = IntVar()
        Checkbutton(self, text="lava", variable=self.lavavar).grid(row=4, column=5, sticky=W)
        self.watervar = IntVar()
        Checkbutton(self, text="water", variable=self.watervar).grid(row=4, column=6, sticky=W)
        self.shallowsvar = IntVar()
        Checkbutton(self, text="shallows", variable=self.shallowsvar).grid(row=4, column=7, sticky=W)

        Label(self, text="Attributes:", font="none 12 bold").grid(row=5, column=0, sticky=W)
        self.protectvar = IntVar()
        Checkbutton(self, text="guard protected", variable=self.protectvar).grid(row=6, column=0, sticky=W)
        self.touchvar = IntVar()
        Checkbutton(self, text="does touch damage", variable=self.touchvar).grid(row=6, column=1, sticky=W)
        self.armedvar = IntVar()
        Checkbutton(self, text="armed", variable=self.armedvar).grid(row=6, column=2, sticky=W)
        self.dualvar = IntVar()
        Checkbutton(self, text="dual wield", variable=self.dualvar).grid(row=6, column=3, sticky=W)
        vcmd = (self.register(self.callback))

        Label(self, text="Health:", font="none 12 bold").grid(row=7, column=0, sticky=W)
        self.health_entry = Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.health_entry.grid(row=7, column=1, sticky=W)
        self.health_entry.insert(END, '100')
        #health_entry.bind('<Return>', self.store_value)
        Label(self, text="Damage:", font="none 12 bold").grid(row=7, column=2, sticky=W)
        self.damage_entry = Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.damage_entry.grid(row=7, column=3, sticky=W)
        self.damage_entry.insert(END, '15')
        Label(self, text="Knockback:", font="none 12 bold").grid(row=7, column=4, sticky=W)
        self.knockback_entry = Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.knockback_entry.grid(row=7, column=5, sticky=W)
        self.knockback_entry.insert(END, '10')

        Label(self, text="Detect Radius:", font="none 12 bold").grid(row=8, column=0, sticky=W)
        self.detect_entry = Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.detect_entry.grid(row=8, column=1, sticky=W)
        self.detect_entry.insert(END, '400')
        Label(self, text="Avoid Radius:", font="none 12 bold").grid(row=8, column=2, sticky=W)
        self.avoid_entry = Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.avoid_entry.grid(row=8, column=3, sticky=W)
        self.avoid_entry.insert(END, '100')

        Label(self, text="Walk Speed:", font="none 12 bold").grid(row=9, column=0, sticky=W)
        self.walk_entry = Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.walk_entry.grid(row=9, column=1, sticky=W)
        self.walk_entry.insert(END, '100')
        Label(self, text="Run Speed:", font="none 12 bold").grid(row=9, column=2, sticky=W)
        self.run_entry = Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.run_entry.grid(row=9, column=3, sticky=W)
        self.run_entry.insert(END, '200')

        Label(self, text="Character Name:", font="none 12 bold").grid(row=10, column=0, sticky=W)
        self.name_entry = Entry(self)
        self.name_entry.grid(row=10, column=1, sticky=W)
        Label(self, text="Key Name:", font="none 12 bold").grid(row=10, column=2, sticky=W)
        self.key_name_entry = Entry(self)
        self.key_name_entry.grid(row=10, column=3, sticky=W)
        Label(self, text="Gold:", font="none 12 bold").grid(row=10, column=4, sticky=W)
        self.gold_entry = Entry(self, validate='all', validatecommand=(vcmd, '%P'))
        self.gold_entry.grid(row=10, column=5, sticky=W)
        self.gold_entry.insert(END, '10')
        Label(self, text="1st Dialogue:", font="none 12 bold").grid(row=11, column=0, sticky=W)
        self.dialogue_entry = Entry(self, width=195)
        self.dialogue_entry.grid(row=12, column=0, columnspan=8, sticky=W)
        Label(self, text="2nd Dialogue:", font="none 12 bold").grid(row=13, column=0, sticky=W)
        self.dialogue2_entry = Entry(self, width=195)
        self.dialogue2_entry.grid(row=14, column=0, columnspan=8, sticky=W)


        Label(self, text="Quest Name:", font="none 12 bold").grid(row=15, column=0, sticky=W)
        self.quest1_name_entry = Entry(self)
        self.quest1_name_entry.grid(row=16, column=0, sticky=W)
        Label(self, text="Needed Item:", font="none 12 bold").grid(row=15, column=1, sticky=W)
        self.needed_item1_entry = Entry(self)
        self.needed_item1_entry.grid(row=16, column=1, sticky=W)
        Label(self, text="Rewards (Separate items with commas. Example: steel sword, 100gold):", font="none 12 bold").grid(row=15, column=2, columnspan=5, sticky=W)
        self.reward1_item = Entry(self)
        self.reward1_item.grid(row=16, column=2, sticky=W)
        Label(self, text="Description", font="none 12 bold").grid(row=17, column=0, sticky=W)
        self.quest1_des_entry = Entry(self, width=195)
        self.quest1_des_entry.grid(row=18, column=0, columnspan=8, sticky=W)
        Label(self, text="Accept Text", font="none 12 bold").grid(row=19, column=0, sticky=W)
        self.accept_text1 = Entry(self, width=195)
        self.accept_text1.grid(row=20, column=0, columnspan=8, sticky=W)
        Label(self, text="Deny Text", font="none 12 bold").grid(row=21, column=0, sticky=W)
        self.deny_text1 = Entry(self, width=195)
        self.deny_text1.grid(row=22, column=0, columnspan=8, sticky=W)
        Label(self, text="Waiting Text", font="none 12 bold").grid(row=23, column=0, sticky=W)
        self.waiting_text1 = Entry(self, width=195)
        self.waiting_text1.grid(row=24, column=0, columnspan=8, sticky=W)
        Label(self, text="Has Item Text", font="none 12 bold").grid(row=25, column=0, sticky=W)
        self.has_item_text1 = Entry(self, width=70)
        self.has_item_text1.grid(row=26, column=0, columnspan=3, sticky=W)
        Label(self, text="Refuse give txt", font="none 12 bold").grid(row=25, column=4, sticky=W)
        self.refuse_text1 = Entry(self, width=70)
        self.refuse_text1.grid(row=26, column=4, columnspan=3, sticky=W)
        Label(self, text="Reward Text", font="none 12 bold").grid(row=27, column=0, sticky=W)
        self.reward1_text1 = Entry(self, width=195)
        self.reward1_text1.grid(row=28, column=0, columnspan=8, sticky=W)
        Label(self, text="Completed Text", font="none 12 bold").grid(row=29, column=0, sticky=W)
        self.completed_text1 = Entry(self, width=90)
        self.completed_text1.grid(row=30, column=0, columnspan=4, sticky=W)

        self.autocomplete_var = IntVar()
        Checkbutton(self, text="autocomplete", variable=self.autocomplete_var).grid(row=31, column=0, sticky=W)
        self.autoaccept_var = IntVar()
        Checkbutton(self, text="autoaccept", variable=self.autoaccept_var).grid(row=31, column=1, sticky=W)
        Button(self, text="Submit and Close", width=20, command=self.end_edits).grid(row=34, column=4, sticky=W)
        Button(self, text="Submit and Create Another", width=25, command=self.submit).grid(row=34, column=5, sticky=W)
        self.mainloop()

    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    def submit(self):
        self.npc_menu.running = True
        self.end_edits()

    def end_edits(self):
        self.character.kind['name'] = self.name_entry.get()
        self.character.species = self.key_name_entry.get()
        gold = int(self.gold_entry.get())
        self.character.kind['inventory']['gold'] = gold
        health = int(self.health_entry.get())
        self.character.kind['health'] = health
        damage = int(self.damage_entry.get())
        self.character.kind['damage'] = damage
        knockback = int(self.knockback_entry.get())
        self.character.kind['knockback'] = knockback
        detect_radius = int(self.detect_entry.get())
        self.character.kind['detect radius'] = detect_radius
        avoid_radius = int(self.avoid_entry.get())
        self.character.kind['avoid radius'] = avoid_radius
        walk_speed = int(self.walk_entry.get())
        self.character.kind['walk speed'] = (walk_speed - 20, walk_speed + 20)
        run_speed = int(self.run_entry.get())
        self.character.kind['run speed'] = (run_speed - 20, run_speed + 20)
        aggression_num = self.aggression_var.get()
        if aggression_num ==1:
            aggression = 'fwp'
        elif aggression_num ==2:
            aggression = 'awp'
        elif aggression_num ==3:
            aggression = 'fup'
        elif aggression_num ==4:
            aggression = 'sap'
        elif aggression_num ==5:
            aggression = 'fwd'
        elif aggression_num ==6:
            aggression = 'awd'
        else:
            aggression = 'fwp'
        self.character.kind['aggression'] = aggression
        collide_list = []
        if self.obstaclesvar.get():
            collide_list.append('obstacles')
        if self.wallvar.get():
            collide_list.append('walls')
        if self.jumpvar.get():
            collide_list.append('jumpables')
        if self.climbvar.get():
            collide_list.append('climbables')
        if self.vehiclevar.get():
            collide_list.append('vehicles')
        if self.lavavar.get():
            collide_list.append('lava')
        if self.watervar.get():
            collide_list.append('water')
        if self.shallowsvar.get():
            collide_list.append('shallows')
        self.character.kind['collide'] = collide_list
        guarded = self.protectvar.get()
        self.character.kind['guarded'] = bool(guarded)
        touch_damage = self.touchvar.get()
        self.character.kind['touch damage'] = bool(touch_damage)
        armed = self.armedvar.get()
        self.character.kind['armed'] = bool(armed)
        dual_wield = self.dualvar.get()
        self.character.kind['dual wield'] = bool(dual_wield)
        autocomplete = str(bool(self.autocomplete_var.get()))
        autoaccept = str(bool(self.autoaccept_var.get())   )
        rewards = self.reward1_item.get().split(", ")
        rewards_string = '["' + '", "'.join(rewards) + '"]'
        dialogue = self.dialogue_entry.get()
        dialogue2 = self.dialogue2_entry.get()
        dialogue2_name = 'None'
        if dialogue2 != '':
            dialogue2_name = self.character.species.upper() + '_DLG2'
        if self.key_name_entry.get() != '': # This makes it so it doesn't write unfinished NPCs
            file = open("dialogue.py", "a")
            if dialogue != '':
                self.character.kind['dialogue'] = self.character.species.upper() + '_DLG'
                file.write("\n")
                file.write(self.character.species.upper() + '_DLG = ' + '["' + dialogue + '"]')
            if dialogue2 != '':
                file.write("\n")
                file.write(self.character.species.upper() + '_DLG2 = ' + '["' + dialogue2 + '"]')
            file.close()

        inv_check = "False"
        needed_item = "None"
        if self.needed_item1_entry.get() != '':
            inv_check = "True"
            needed_item = self.needed_item1_entry.get()
        if self.quest1_name_entry.get() != '':
            # Add checks for complete flields.
            self.character.kind['quest'] = self.quest1_name_entry.get()
            file = open("quests.py", "a")
            file.write("\n")
            file.write("QUESTS['" + self.quest1_name_entry.get() + "'] = " + '{"accepted": False, "completed": False, "rewarded": False, "inventory check": ' + inv_check + ', "needed item": ' + '"' + needed_item + '"' + ', "autocomplete": ' + autocomplete + ', "autoaccept": ' + autoaccept + ', "description": ' + '"' + self.quest1_des_entry.get() + '"' + ', "accept text": ' + '["' + self.accept_text1.get() + '"]' + ', "deny text": ' + '["' + self.deny_text1.get() + '"]' + ', "completed text": ' + '["' + self.completed_text1.get() + '"]' + ', "waiting text": ' + '["' + self.waiting_text1.get() + '"]' + ', "has item text": ' + '["' + self.has_item_text1.get() + '"]' + ', "refuse to give text": ' + '["' + self.refuse_text1.get() + '"]' + ', "reward text": ' + '["' + self.reward1_text1.get() + '"]' + ', "next quest": None, "next dialogue": "' + dialogue2_name + '", "reward": ' + rewards_string + '}')
            file.close()

        self.destroy()
