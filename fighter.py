import pygame

class fighter():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.cooldown_time = 0.3
        self.last_sound_time = 0
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.was_in_air = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit_cooldown = 0  # Invulnerability cooldown
        self.attack_sound = sound[0]
        self.attack_misssound = sound[1]
        self.jumpsound = sound[2]
        self.landsound = sound[3]
        self.walk = sound[4]
        self.hit = False
        self.health = 100
        self.alive = True

    def play_walking_sound(self):
        current_time = pygame.time.get_ticks() / 1000
        if current_time - self.last_sound_time >= self.cooldown_time:
            self.walk.set_volume(0.1)
            self.walk.play()
            self.last_sound_time = current_time

    def reset(self, x, y):
        self.health = 200
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.frame_index = 0
        self.alive = True

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(
                    pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 5
        GRAVITY = 5
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        key = pygame.key.get_pressed()

        if self.alive and not round_over:
            if self.player == 1:
                if key[pygame.K_a]:
                    dx = -SPEED
                    self.play_walking_sound()
                    self.running = True
                    self.flip = True

                if key[pygame.K_d]:
                    dx = SPEED
                    self.play_walking_sound()
                    self.running = True
                    self.flip = False
                if key[pygame.K_w] and not self.jump:
                    self.jumpsound.play()
                    self.vel_y = -35
                    self.jump = True
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2

            if self.player == 2:
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                    self.play_walking_sound()
                    self.running = True
                    self.flip = True

                if key[pygame.K_RIGHT]:
                    dx = SPEED
                    self.flip = False
                    self.play_walking_sound()
                    self.running = True
                if key[pygame.K_UP] and not self.jump:
                    self.jumpsound.play()
                    self.vel_y = -35
                    self.jump = True
                if key[pygame.K_m] or key[pygame.K_l]:
                    self.attack(target)
                    if key[pygame.K_m]:
                        self.attack_type = 1
                    if key[pygame.K_l]:
                        self.attack_type = 2

        self.vel_y += GRAVITY
        dy += self.vel_y

        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            if self.vel_y > 0 and self.was_in_air:
                self.landsound.play()
            self.vel_y = 0
            self.jump = False
            self.was_in_air = False
            dy = screen_height - 110 - self.rect.bottom

        else:
            self.was_in_air = True

        if self.rect.colliderect(target.rect):
            if self.rect.centerx < target.rect.centerx:
                if dx > 0:
                    dx = 0
                    target.rect.x = self.rect.right
            elif self.rect.centerx > target.rect.centerx:
                if dx < 0:
                    dx = 0
                    target.rect.x = self.rect.left - target.rect.width

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        if not self.alive and self.health <= 0:
            self.update_action(6)
        elif self.hit:
            self.update_action(5)
        elif self.attacking:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump:
            self.update_action(2)
        elif self.running:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 50
        current_time = pygame.time.get_ticks()

        if current_time - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = current_time

            if self.frame_index >= len(self.animation_list[self.action]):
                if not self.alive:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0
                    if self.action in [3, 4]:
                        self.attacking = False
                        self.attack_cooldown = 30
                    if self.action == 5:
                        self.hit = False
                        self.attacking = False
                        self.attack_cooldown = 30

            self.image = self.animation_list[self.action][self.frame_index]

    def attack(self, target):
        if self.attack_cooldown == 0 and not self.hit:
            attacking_rect = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip),
                self.rect.y,
                2 * self.rect.width,
                self.rect.height,
            )
            if attacking_rect.colliderect(target.rect) and not self.was_in_air and target.hit_cooldown == 0:
                self.attack_sound.play()
                target.health -= 10
                target.hit = True
                target.hit_cooldown = 20
                if target.rect.centerx < self.rect.centerx:
                    target.rect.x -= 20
                else:
                    target.rect.x += 20
            else:
                self.attack_misssound.play()

            self.attacking = True
            self.attack_cooldown = 30

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] - self.image_scale), self.rect.y - (self.offset[1] - self.image_scale)))
