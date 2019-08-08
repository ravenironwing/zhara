Setup:
To Play this game you must first have the following installed:
Python 3.5 or higher
Pygame (if you experience intermittent fatal errors make sure you are running from the python consol or IDLE3 as this game uses a lot of memory [about 1GB in some parts]).

This game has been tested on pygame 2.0.0dev3 and a bunch of the older versions. I reccommend pygame2 as it runs a LOT faster.

You also need the following libraries:
pytmx
pyscroll
To install run these commands in the command prompt/terminal:
  pip3 install pygame 2.0.0dev3
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

Vehicle Controlls:
E - enter vehicle
X - exit vehicle/dismount animal
Z/C - rotate turret
U - toggle mini map view in airship.

Ctrl + S - Saves your game. Each save is given a timestamp and organized by the character's race
Ctrl + L - Loads saved games (it's a bit buggy right now, so I reccommend just pressing C at the start instead of loading while in game).

#Notes
Npc animations were created using position_editor.py. This file is not needed to run the game.


