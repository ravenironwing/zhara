UPDATE:
This project has been discontinued do to performance issues with some of the underlying code, which made it impossible to get the level of performance out of the game
that I desired. So, I have been busy reworking the code for better performance. In many aspects it will be like a very different and better game, but with reduced tile
and sprite size for faster rendering. The new project is called Sky Realm - Legends of Arroshay.... People didn't seem to know how to pronouce Zhara- Sky Realm is the English translation of the same name.

Intro:
Legends of Zhara is a 2D open world action RPG that utilizes many game play aspects of modern 3D RPGs.
The world is about 12 kilometers accross if it were to scale. It is made from over 17000 64 by 64 tile maps. 
It has been called by some "2D Skyrim with guns" 
Here are a few of the features: lots of different playable races with different abilities and starting locations, quests, weapon/armor forging, enchanting, alchemy, spell casting, hunting, cooking, followers, dual weilding, minning ore, chopping down dead trees, ridding horses and other large animals, vehicles (tank, airship, boat, etc.), complex NPCs, stores (buying/selling), looting, chests, lock picking, sleeping, using toilets, you can transform into a dragon and breathe fire, etc.
   

Setup:
To Play this game you must first have the following installed:
Python 3.5 or higher
Pygame (if you experience intermittent fatal errors make sure you are running from the python consol or IDLE3 as this game uses a lot of memory [about 1GB in some parts]).

This game has been tested on pygame 2.0.0dev3 and a bunch of the older versions. I reccommend pygame2 as it runs a LOT faster.

You also need the following libraries:
pytmx
pyscroll
To install run these commands in the command prompt/terminal:
  pip3 install pygame==2.0.0dev4
	pip3 install pytmx
  pip3 install pyscroll
Game Play:
Run main.py to play (open in IDLE3 [right click "open with Idle3" press F5 to run or use another IDE, or use the python consol)

﻿Controlls:
W - forward
S - backwards
A - rotate left
D - rotate right
Z - Strafe left
C - Strafe right
arrow keys - rotate and move in NSEW directions
B - Use Equipped Item
G - throw grenade
Q - Use equipped magic
T - Transform into dragon form
R - Reload weapon
F - Breathe fire while in dragon form
E - Loot objects/Exit menus/Activate things/Talk/Mount animal/Enter vehicle
V - Climb obstacles (walls, boulders, mountains, etc.)
N - Nightmode, this is just for testing. In the future day and night will be timed.
I - To access inventory, or exit menus
K - Stats menu
P - Pause
J - Quest menu
L - Crafting menu (used for making various items that don't require a special location: like making fire pits)
M - toggles mini map and compass (+/- changes size of mini map)
O - toggles overworld map.
TAB - Melee attack
SPACE - Jump
LSHIFT - run
Escape - to quit  game while in  menu (currently the only way to end the game when in full screen)
ALT + ENTER - toggle fullscreen mode [Fullscreen may have issues on your particular hardware, so it is off be default]


Mouse:
Move Mouse - rotate/aim
Left Button - Left arm attack
Right Button - Right arm attack
Middle button - Forward (only works with some mice)

Vehicle Controls:
E - enter vehicle
X - exit vehicle/dismount animal
Z/C - rotate turret
U - toggle mini map view in airship.

Ctrl + S - Saves your game. Each save is given a timestamp and organized by the character's race
Ctrl + L - Loads saved games (it's a bit buggy right now, so I reccommend just pressing C at the start instead of loading while in game).

#Notes
The word map is set with the north pole at the center and the south pole wrapped around it (because it is a sphere mapped to a flat surface). This allows you to travel around the world. Since north is towards the center there is a compass on the HUD minimap to show you which way north is.

Npc animations were created using position_editor.py. This file is not needed to run the game.

You can access the NPC creation tool by pressing Ctrl N at the title screen
NPCs are automatically added to npc.py and can be added into new Tiled maps

