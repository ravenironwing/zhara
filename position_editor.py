import pygame as pg
import random
from os import path
from character_positions import *
vec = pg.math.Vector2

WING1_OFFSET = (35, 121)
WING2_OFFSET = (35, 74)

WIDTH = 480
HEIGHT = 600
FPS = 60

default = CP_STANDING_ARMS_OUT0
animation = ROW


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
# Player body image settings
PLAYER_IMAGES = []
for i in range(1, 12):
    filename = 'player_layer{}.png'.format(i)
    PLAYER_IMAGES.append(filename)

# initialize pg and create window
pg.mixer.pre_init(44100, -16, 1, 512) #reduces the delay in playing sounds
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Position Editor")
clock = pg.time.Clock()


def draw_text(surf, text, size, x, y, color = WHITE):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color) #True tells whether or not text is anti-aliased (smothed) or not
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y) #midtop centers the text xy at the middle top of the text
    surf.blit(text_surface, text_rect)

class Character(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.surface_width = 200
        self.surface_height = 200
        self.body_surface = pg.Surface((self.surface_width, self.surface_height))
        self.body_surface.set_colorkey(BLACK)
        self.rect = self.body_surface.get_rect()
        # The body part list includes first the placement then the rotation of each part
        self.part_placement = default
        torso_pos = []
        for i, part in enumerate(self.part_placement):
            if i not in [9, 10, 11]:
                if i == 7:
                    torso_pos = part
                image = pg.transform.rotate(player_images[i], part[2])
                rect = image.get_rect()
                self.body_surface.blit(image, (self.rect.centerx - (rect.centerx - part[0]), self.rect.centery - (rect.centery - part[1])))
            elif i in [9, 10]:
                image = pg.transform.rotate(arrow_img, part[2])
                rect = image.get_rect()
                self.body_surface.blit(image, (self.rect.centerx - (rect.centerx - part[0]), self.rect.centery - (rect.centery - part[1])))
            elif i == 11:
                wing1_pos = vec(WING1_OFFSET).rotate(-torso_pos[2])
                wing2_pos = vec(WING2_OFFSET).rotate(-torso_pos[2])
                image = pg.transform.rotate(player_images[9], part[0] + torso_pos[2])
                temp_rect = image.get_rect()
                self.body_surface.blit(image, (rect.centerx - (temp_rect.centerx - (torso_pos[0] + wing1_pos.x)), rect.centery - (temp_rect.centery - (torso_pos[1] + wing1_pos.y))))

                image = pg.transform.rotate(player_images[10], part[1] + torso_pos[2])
                temp_rect = image.get_rect()
                self.body_surface.blit(image, (rect.centerx - (temp_rect.centerx - (torso_pos[0] + wing2_pos.x)), rect.centery - (temp_rect.centery - (torso_pos[1] + wing2_pos.y))))


        self.image = self.body_surface
        self.rect = self.image.get_rect()
        self.rot = 0
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.index = 0
        self.frame = 0
        self.last_step = 0

    def change_postion(self):
        self.body_surface.fill((0, 0, 0))
        self.rect = self.body_surface.get_rect()

        torso_pos = []
        for i, part in enumerate(self.part_placement):
            if i not in [9, 10, 11]:
                if i == 7:
                    torso_pos = part
                image = pg.transform.rotate(player_images[i], part[2])
                rect = image.get_rect()
                self.body_surface.blit(image, (self.rect.centerx - (rect.centerx - part[0]), self.rect.centery - (rect.centery - part[1])))
            elif i in [9, 10]:
                image = pg.transform.rotate(arrow_img, part[2])
                rect = image.get_rect()
                self.body_surface.blit(image, (self.rect.centerx - (rect.centerx - part[0]), self.rect.centery - (rect.centery - part[1])))
            elif i == 11:
                wing1_pos = vec(WING1_OFFSET).rotate(-torso_pos[2])
                wing2_pos = vec(WING2_OFFSET).rotate(-torso_pos[2])
                image = pg.transform.rotate(player_images[9], part[0] + torso_pos[2])
                temp_rect = image.get_rect()
                self.body_surface.blit(image, (rect.centerx - (temp_rect.centerx - (torso_pos[0] + wing1_pos.x)), rect.centery - (temp_rect.centery - (torso_pos[1] + wing1_pos.y))))

                image = pg.transform.rotate(player_images[10], part[1] + torso_pos[2])
                temp_rect = image.get_rect()
                self.body_surface.blit(image, (rect.centerx - (temp_rect.centerx - (torso_pos[0] + wing2_pos.x)), rect.centery - (temp_rect.centery - (torso_pos[1] + wing2_pos.y))))

    def get_keys(self):
        global text_output, save_pressed, default, animation
        keys = pg.key.get_pressed()
        # Select Parts
        if keys[pg.K_1]:
            self.index = 0
            text_output = "Right Foot"
        if keys[pg.K_2]:
            self.index = 1
            text_output = "Left Foot"
        if keys[pg.K_3]:
            self.index = 2
            text_output = "Butt/Hips"
        if keys[pg.K_4]:
            self.index = 3
            text_output = "Right Forearm"
        if keys[pg.K_5]:
            self.index = 4
            text_output = "Left Forearm"
        if keys[pg.K_6]:
            self.index = 5
            text_output = "Right Upper Arm"
        if keys[pg.K_7]:
            self.index = 6
            text_output = "Left Upper Arm"
        if keys[pg.K_8]:
            self.index = 7
            text_output = "Upper Body"
        if keys[pg.K_9]:
            self.index = 8
            text_output = "Head"
        if keys[pg.K_MINUS]:
            self.index = 9
            text_output = "Right Weapon"
        if keys[pg.K_EQUALS]:
            self.index = 10
            text_output = "Left Weapon"
        if keys[pg.K_q]:
            self.index = 11
            text_output = "Right Wing"
        if keys[pg.K_w]:
            self.index = 12
            text_output = "Left Wing"
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_step > 200:
                self.last_step = now
                self.frame += 1
                if self.frame  + 1 > len(animation):
                    self.frame = 0
                self.part_placement = animation[self.frame]
                self.change_postion()
                text_output = "Frame: " + str(self.frame + 1)



        # Move Parts
        if self.index not in [11, 12]:
            if keys[pg.K_UP]:
                self.part_placement[self.index][1] -= 1
                self.change_postion()
            if keys[pg.K_DOWN]:
                self.part_placement[self.index][1] += 1
                self.change_postion()
            if keys[pg.K_RIGHT]:
                self.part_placement[self.index][0] += 1
                self.change_postion()
            if keys[pg.K_LEFT]:
                self.part_placement[self.index][0] -= 1
                self.change_postion()

        # Rotate Parts
            if keys[pg.K_a]:
                self.part_placement[self.index][2] += 1
                self.change_postion()
            if keys[pg.K_d]:
                self.part_placement[self.index][2] -= 1
                self.change_postion()

        elif self.index == 11:
            if keys[pg.K_a]:
                self.part_placement[self.index][0] += 1
                self.change_postion()
            if keys[pg.K_d]:
                self.part_placement[self.index][0] -= 1
                self.change_postion()
        elif self.index == 12:
            if keys[pg.K_a]:
                self.part_placement[11][1] += 1
                self.change_postion()
            if keys[pg.K_d]:
                self.part_placement[11][1] -= 1
                self.change_postion()

        # Save Position Profile:
        if keys[pg.K_s]:
            mods = pg.key.get_mods()
            if mods & pg.KMOD_CTRL:
                save_pressed = True

    def save(self):
        file = open("character_positions.txt", "a")
        file.write("\n")
        file.write(str(self.part_placement))
        file.close()

    def update(self):
        self.get_keys()
        self.image = pg.transform.rotate(self.body_surface, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)


text_output = ""
save_pressed = False
font_name = pg.font.match_font('arial') #python looks for closest match to arial on whatever computer
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'img')
body_parts_folder = path.join(img_folder, 'female_osidinedragon_parts')
hair_folder = path.join(img_folder, 'hair')
tops_folder = path.join(img_folder, 'tops')
bottoms_folder = path.join(img_folder, 'bottoms')
shoes_folder = path.join(img_folder, 'shoes')
weapons_folder = path.join(img_folder, 'weapons')
player_images = []
for i in range(11):
    img = pg.image.load(path.join(body_parts_folder, PLAYER_IMAGES[i])).convert_alpha()
    player_images.append(img)
arrow_img = pg.image.load(path.join(img_folder, "dot_arrow.png")).convert_alpha()
all_sprites = pg.sprite.Group()
character = Character()
all_sprites.add(character)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pg.event.get():
        # check for closing window
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYUP:
            if save_pressed == True:
                character.save()
                text_output = "Profile Saved"
                save_pressed = False

    # Update
    all_sprites.update()

    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, text_output, 14, WIDTH / 2, HEIGHT - 100)
    # *after* drawing everything, flip the display
    pg.display.flip()

pg.quit()
