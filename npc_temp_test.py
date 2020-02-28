def avoid_mobs(self):
    for mob in self.game.mobs_on_screen:
        if mob != self:
            dist = self.pos - mob.pos
            if 0 < dist.length() < self.avoid_radius:
                self.acc += dist.normalize()


def seek_random_target(self):
    if self.race not in ['mechanima', 'mech_suit']:
        if self.game.night:
            if self not in self.game.lights:
                if randrange(0, 2) == 1:
                    lamp_check(self)
        elif self in self.game.lights:
            if randrange(0, 2) == 1:
                lamp_check(self)
    self.target = choice(list(self.game.random_targets))
    self.detect_radius = self.game.map.height / 2
    temp_dist = self.target.pos - self.pos
    temp_dist = temp_dist.length()
    if temp_dist > self.detect_radius:
        self.target = choice(list(self.game.random_targets))
    if randrange(0, 5) == 1:  # Makes it so NPCs randomly target nearby doors.
        last_dist = 3000
        for entry in self.game.entryways_on_screen:
            dist = self.pos - entry.pos
            dist = dist.length()
            if last_dist > dist:  # Finds closest door
                self.target = entry
                self.approach_vector = vec(1, 0)
                last_dist = dist
    if temp_dist < 200:
        self.target = choice(list(self.game.random_targets))


def seek_mobs(self):
    last_dist = 100000
    non_targets = 0

    if self.guard:
        for mob in self.game.moving_targets_on_screen:
            if mob != self:
                if not mob.invisible:
                    if mob.aggression == 'awd':
                        if mob.kind != self.kind:
                            dist = self.pos - mob.pos
                            dist = dist.length()
                            if 0 < dist < self.detect_radius:
                                if last_dist > dist:  # Finds closest mob
                                    self.target = mob
                                    self.detect_radius = self.default_detect_radius
                                    self.approach_vector = vec(1, 0)
                                    self.offensive = True
                                    last_dist = dist
                            else:
                                non_targets += 1
                        else:
                            non_targets += 1
                    else:
                        non_targets += 1
                else:
                    non_targets += 1

    elif self.aggression == 'awd':
        for mob in self.game.moving_targets_on_screen:  # Only looks at mobs that are on screen
            if mob != self:
                if not mob.invisible:
                    if mob.kind != self.kind:
                        self.offensive = True
                        dist = self.pos - mob.pos
                        dist = dist.length()
                        if 0 < dist < self.detect_radius:
                            if last_dist > dist:  # Finds closest NPC and sets to target
                                self.target = mob
                                self.detect_radius = self.default_detect_radius
                                self.approach_vector = vec(1, 0)
                                last_dist = dist
                        else:
                            non_targets += 1
                    else:
                        non_targets += 1
                else:
                    non_targets += 1
    # Seeks a random target if there are no target mobs in range.
    if non_targets == len(self.game.moving_targets_on_screen) - 1:
        self.seek_random_target()


def is_moving(self):
    # This checks to see if the NPC has moved since the last check.
    dist = self.pos - self.last_pos
    if dist.length() < 10:
        self.last_pos = self.rect.center
        return False
    else:
        self.last_pos = self.rect.center
        return True


def accelerate(self):
    if self.in_player_vehicle:
        pass
    else:
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        collide(self)
        self.talk_rect.center = self.pos


def update(self):
    # This parts sincs the body sprite with the NPC's soul.
    self.body.rot = self.rot
    self.body.image = pg.transform.rotate(self.body.body_surface, self.rot)
    self.body.rect = self.body.image.get_rect()
    self.body.rect.center = self.pos

    if self.living:
        if self.driver != None:
            self.pos = self.driver.pos
            self.rect.center = self.pos
            self.hit_rect.center = self.pos
            if self.health <= 0:
                self.depossess()
                self.death()
        else:
            if not self.needs_move:
                if self.target != self.game.player:
                    if not self.target.living:  # Makes it so NPC switches target after it kills one.
                        self.offensive = False
                        self.seek_mobs()
                    if self.aggression in ['awp', 'sap', 'fup']:
                        if self.provoked:
                            if not self.game.player.invisible:
                                self.target = self.game.player
                                self.offensive = True
                elif self.aggression in ['awp', 'sap', 'fup']:
                    if not self.provoked:
                        self.offensive = False
                    if self.race in ['osidine', 'shaktele', 'elf']:  # Makes it so humans and elves attack you if you are zombie or skeleton.
                        if self.target == self.game.player:
                            if self.game.player.race in ['immortui', 'skeleton']:
                                self.provoked = True
                                self.offensive = True
                                self.approach_vector = vec(1, 0)

            if self in self.game.companions:
                if self.target == self.game.player:
                    self.offensive = False

            if self.melee_playing:
                self.melee()
            elif self.reloading:
                self.reload()

            ora = pg.time.get_ticks()  # Makes it so the NPCs don't stay in one place too long.
            if not self.offensive:
                if not self.needs_move:
                    if ora - self.last_move_check > randrange(1000, 2000):
                        if not self.is_moving():
                            self.seek_random_target()
                            self.needs_move = True
                        self.last_move_check = ora
                else:
                    if ora - self.last_move_check > randrange(3000, 6000):
                        self.needs_move = False
                        self.last_move_check = ora

            if ora - self.last_hit > 3000:  # Used to set the time NPCs flee for after being attacked.
                if self.running:
                    if self.aggression == 'fwp':
                        self.approach_vector = vec(-1, -1)
                    self.running = False

            if not self.needs_move:
                if ora - self.last_seek > 1000:  # Checks for the closest target
                    self.seek_mobs()
                    self.last_seek = ora

            # Stops them from climbing after a certain time if they aren't on an object that requires you climb on it.
            if self.climbing:
                if ora - self.last_climb > CLIMB_TIME:
                    if not pg.sprite.spritecollide(self, self.game.climbs, False):
                        self.climbing = False

            target_dist = self.target.pos - self.pos
            if True not in [self.melee_playing, self.animating_reload]:  # Only moves character if not attacking or reloading
                if not self.offensive and target_dist.length_squared() < 100 ** 2 and self.approach_vector != vec(-1, 0) and (self.target not in self.game.entryways):
                    self.vel = vec(0, 0)
                    self.rot = target_dist.angle_to(vec(1, 0))

                elif target_dist.length_squared() < self.detect_radius ** 2:
                    # Animates Character's Walking
                    if self.speed == 0:
                        temp_animate_speed = 500
                    else:
                        if self.running:
                            temp_animate_speed = 20000 / self.run_speed
                        else:
                            temp_animate_speed = 20000 / self.speed

                    if self.swimming:
                        self.body.animate(self.body.swim_anim, temp_animate_speed)
                    elif self.in_shallows:
                        self.body.animate(self.body.shallows_anim, temp_animate_speed)
                    elif self.in_grass:
                        self.body.animate(self.body.shallows_anim, temp_animate_speed)
                    elif self.running:
                        self.body.animate(self.body.run_anim, temp_animate_speed)
                    elif self.climbing:
                        self.body.animate(self.body.climbing_anim, temp_animate_speed)
                    elif self.jumping:
                        self.jump()
                    else:
                        self.body.animate(self.body.walk_anim, temp_animate_speed)

                    if random() < 0.002:  # This makes different sounds for each type of npc
                        if self.equipped['race'] == 'immortui':
                            choice(self.game.zombie_moan_sounds).play()
                        if 'wraith' in self.equipped['race']:
                            choice(self.game.wraith_sounds).play()

                    # This part makes the NPC avoid walls
                    now = pg.time.get_ticks()
                    if not self.immaterial:
                        hits = pg.sprite.spritecollide(self, self.game.walls_on_screen, False)
                        if hits:
                            if hits[0] not in self.game.door_walls:
                                self.hit_wall = True
                                if now - self.last_wall_hit > 1000:
                                    self.last_wall_hit = now
                                    self.rot = (self.rot + (randrange(90, 180) * choice([-1, 1]))) % 360
                        elif now - self.last_wall_hit > randrange(3000, 5000):
                            self.last_wall_hit = now
                            self.hit_wall = False
                    if not self.hit_wall:
                        self.rot = target_dist.angle_to(self.approach_vector)

                    self.rect.center = self.pos
                    if self in self.game.lights:
                        if self.race in ['mechanima', 'mech_suit']:
                            self.light_mask_rect.center = self.rect.center
                        elif self.lamp_hand == 'weapons':
                            self.light_mask_rect.center = self.body.melee_rect.center
                        else:
                            self.light_mask_rect.center = self.body.melee2_rect.center
                        if self.mask_kind in DIRECTIONAL_LIGHTS:
                            new_image = self.game.flashlight_masks[int(self.rot / 3)]
                            old_center = self.light_mask_rect.center
                            self.light_mask = new_image
                            self.light_mask_rect = self.light_mask.get_rect()
                            self.light_mask_rect.center = old_center

                    self.acc = vec(1, 0).rotate(-self.rot)
                    self.avoid_mobs()
                    try:  # prevents scaling a vector of 0 length
                        if self.running:
                            speed = self.run_speed
                        else:
                            speed = self.speed
                        self.acc.scale_to_length(speed)
                    except:
                        self.acc = vec(0, 0)
                    if self.target == self.game.player:
                        self.accelerate()
                    elif target_dist.length() > 40:  # Stops mobs from occupying the same space as you.
                        self.accelerate()

                    if self.offensive:
                        if self.aggression not in ['fwd', 'fwp']:
                            if target_dist.length_squared() < self.melee_range ** 2:
                                self.approach_vector = vec(1, 0)
                                now = pg.time.get_ticks()
                                if now - self.last_melee > randrange(1000, 3000):
                                    self.last_melee = now
                                    self.pre_melee()
                            elif True not in [self.reloading, self.hit_wall, self.swimming]:
                                if self.gun:
                                    if target_dist.length_squared() < self.weapon_range ** 2:
                                        if self.bow:
                                            if self.arrow != None:
                                                self.shoot()
                                                self.arrow.kill()
                                                self.arrow = None
                                            else:
                                                self.reloading = True
                                                self.animating_reload = True
                                        else:
                                            self.shoot()
                                        if self.bullets_shot >= self.mag_size:
                                            self.bullets_shot = 0
                                            self.reloading = True
                                            self.animating_reload = True
                                else:
                                    if target_dist.length_squared() < self.detect_radius ** 2:
                                        magic_chance = randrange(0, 100)
                                        if magic_chance == 1:
                                            self.cast_spell()
                            if self.game.player.in_vehicle:
                                if target_dist.length_squared() < 3 * self.melee_range ** 2:
                                    now = pg.time.get_ticks()
                                    if now - self.last_melee > randrange(1000, 3000):
                                        self.last_melee = now
                                        self.pre_melee()
                        elif not self.running:  # Non agressive but provoked NPCs
                            if target_dist.length_squared() < self.melee_range ** 2:
                                self.approach_vector = vec(1, 0)
                                now = pg.time.get_ticks()
                                if self.last_melee != 0:
                                    if now - self.last_melee > 20000:  # Makes it so the villagers stop attacking you if you've left them alone for 20 seconds.
                                        self.offensive = False
                                        self.last_melee = 0
                                if self.offensive:
                                    if now - self.last_melee > 3000:
                                        self.last_melee = now
                                        self.pre_melee()
            if self.health <= 0:
                self.death()