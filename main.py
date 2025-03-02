import pygame
from fighter import fighter
from pygame import mixer
from typing import Dict, List, Tuple
from network import NetworkClient
from network import PlayerState
# Add this import with your other imports
from UI import MenuButton, ArenaCard, MenuManager

from server import GameServer
# At the start of your game, after pygame initialization:
network = NetworkClient()
if not network.connect():
    print("Could not connect to server!")
    pygame.quit()
    exit()

WIDTH, HEIGHT = 1000, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

# Initialize menu manager
menu_manager = MenuManager(WIDTH, HEIGHT)



# Initialize Pygame
mixer.init()
pygame.init()
clock = pygame.time.Clock()
FPS = 60

# Game states
MENU, PLAYING, PAUSED, GAME_OVER, ARENA_SELECT= "menu", "playing", "paused", "game_over","arena_select"
current_state = MENU

# Setup display
pygame.display.set_caption("BattleForge")
icon = pygame.image.load('gun.png')
pygame.display.set_icon(icon)

# Music setup
pygame.mixer.music.load("music/bgmusic.mp3")
pygame.mixer.music.set_volume(0.01)
mixer.music.play(-1)

# Sound effects
intro_count = 0  # Change from 4 to 0
last_count = 0
countdown_started = False  # Add this new variable
score = [0, 0]
round_over = False
Round_Over_CoolDown = 2000
introsound = pygame.mixer.Sound("music/321fight.mp3")
m,n=1,5



victory1 = pygame.image.load("P1.png").convert_alpha()
victory2 = pygame.image.load("P2.png").convert_alpha()
walk = pygame.mixer.Sound("music/walk.mp3")
deathsound=pygame.mixer.Sound("music/death.mp3")
deathsound.set_volume(1.0)


# Attack sounds based on character type (m and n should be defined)
if m in (1, 2, 3, 4):
    p1sound = pygame.mixer.Sound("music/swordattack.wav")
    p1soundmiss = pygame.mixer.Sound("music/swordmissattack.flac")
else:
    p1sound = pygame.mixer.Sound("music/fireattack.wav")
    p1soundmiss = pygame.mixer.Sound("music/firemissattack.wav")

if n in (1, 2, 3, 4):
    p2sound = pygame.mixer.Sound("music/swordattack.wav")
    p2soundmiss = pygame.mixer.Sound("music/swordmissattack.flac")
else:
    p2sound = pygame.mixer.Sound("music/fireattack.wav")
    p2soundmiss = pygame.mixer.Sound("music/firemissattack.wav")

sound1=[p1sound,p1soundmiss,pygame.mixer.Sound("music/jumppp11.ogg"),
pygame.mixer.Sound("music/land1.mp3"),walk
]
sound2=[p2sound,p2soundmiss,pygame.mixer.Sound("music/jumppp22.ogg"),pygame.mixer.Sound("music/land1.mp3"),walk]
# Screen setup
WIDTH, HEIGHT = 1000, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

def drawtimer(timer,width,height):
    cdimg=pygame.image.load(f"intro/{timer}.png").convert_alpha()
    screen.blit(pygame.transform.scale(cdimg,(width,height)),(0,0))

# Colors
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fighter setup
char1_data = [162, 4, [72, 56]]  # size, scale, offset
char2_data = [250, 3, [112, 107]]

# Background setup
scroll = 240
vertical_scroll = 0
scroll_speed = 3
return_speed = 2




# Load fighters

Mcharacter=[1,3,4,2,5]
if(m==1):
    SIZE=180
    SCALE=3
    OFSET=[220,150]
    char1_data=[SIZE,SCALE,OFSET]
    char1_sheet=pygame.image.load("Good Fighter/knight moves.png").convert_alpha()
    char1_anim=[11,8,3,7,7,4,11,3]

elif(m==2):
    SIZE=180
    SCALE=3
    OFSET=[232,150]
    char1_data=[SIZE,SCALE,OFSET]
    char1_sheet=pygame.image.load("Good Fighter/martial 1 moves.png").convert_alpha()
    char1_anim=[8,8,2,6,6,4,6,2]

elif(m==3):
    SIZE=180
    SCALE=3
    OFSET=[220,150]
    char1_data=[SIZE,SCALE,OFSET]
    char1_sheet=pygame.image.load("Good Fighter/martial 2 moves.png").convert_alpha()
    char1_anim=[4,8,2,4,4,3,7,2]

elif(m==4):
    SIZE=180
    SCALE=3
    OFSET=[220,150]
    char2_data=[SIZE,SCALE,OFSET]
    char1_sheet=pygame.image.load("Good Fighter/martial 3 moves.png").convert_alpha()
    char1_anim=[10,8,3,7,9,3,11,3]

elif(m==5):
    SIZE=180
    SCALE=2
    OFSET=[120,129]
    char2_data=[SIZE,SCALE,OFSET,]
    char1_sheet=pygame.image.load("Good Fighter/wiz 2 moves.png").convert_alpha()
    char1_anim=[6,8,2,8,8,5,7,2]

#----------------player 2 selection------------------------------------------------------

Ncharacter=[5,2,4,1,3]
Ncharacter.remove(m) #makes sure both player don't get the same character

if(n==1):
    SIZE=180
    SCALE=3
    OFSET=[220,150]
    char2_data=[SIZE,SCALE,OFSET]
    char2_sheet=pygame.image.load("Good Fighter/knight moves.png").convert_alpha()
    char2_anim=[11,8,3,7,7,4,11,3]

elif(n==2):
    SIZE=180
    SCALE=3
    OFSET=[220,150]
    char2_data=[SIZE,SCALE,OFSET]
    char2_sheet=pygame.image.load("Good Fighter/martial 1 moves.png").convert_alpha()
    char2_anim=[8,8,2,6,6,4,6,2]

elif(n==3):
    SIZE=180
    SCALE=3
    OFSET=[220,150]
    char2_data=[SIZE,SCALE,OFSET]
    char2_sheet=pygame.image.load("Good Fighter/martial 2 moves.png").convert_alpha()
    char2_anim=[4,8,2,4,4,3,7,2]

elif(n==4):
    SIZE=180
    SCALE=3
    OFSET=[220,150]
    char2_data=[SIZE,SCALE,OFSET]
    char2_sheet=pygame.image.load("Good Fighter/martial 3 moves.png").convert_alpha()
    char2_anim=[10,8,3,7,9,3,11,3]

elif(n==5):
    SIZE=180
    SCALE=2
    OFSET=[120,129]
    char2_data=[SIZE,SCALE,OFSET]
    char2_sheet=pygame.image.load("Good Fighter/wiz 2 moves.png").convert_alpha()
    char2_anim=[6,8,2,8,8,5,7,2]

# Health bar
original_health = pygame.image.load("health bar.png").convert_alpha()
health = original_health.copy()

# Zoom settings
current_zoom = 1.1
target_zoom = 0.9


# Font setup
pixelfont = pygame.font.Font("CosmicAlien.ttf.", 30)
title_text = pixelfont.render("BattleForge", True, WHITE)
start_text = pixelfont.render("Press ENTER to Start", True, WHITE)
pause_text = pixelfont.render("Paused - Press ESC to Resume", True, WHITE)
game_over_text = pixelfont.render("Game Over - Press ENTER to Restart", True, WHITE)


class BackgroundManager:
    def __init__(self, bg_images: List[pygame.Surface], width: int, height: int):
        self.original_images = bg_images
        self.width = width
        self.height = height
        self.zoom_cache: Dict[float, List[pygame.Surface]] = {}
        self.cache_precision = 3  # Increased precision for smoother transitions
        self.target_zoom = 1.0
        self.current_zoom = 1.1
        self.zoom_speed = 0.2 # Slower for smoother animation
        self.center_x = width // 2
        self.center_y = height // 2

    def update_zoom(self):
        if abs(self.current_zoom - self.target_zoom) > 0.001:  # Smaller threshold
            self.current_zoom += (self.target_zoom - self.current_zoom) * self.zoom_speed

    def set_target_zoom(self, target: float):
        self.target_zoom = max(0.1, min(2.0, target))

    def get_scaled_backgrounds(self, zoom_factor: float) -> List[pygame.Surface]:
        zoom_factor = round(zoom_factor, self.cache_precision)
        if zoom_factor in self.zoom_cache:
            return self.zoom_cache[zoom_factor]

        scaled_images = []

        for bg in self.original_images:
            scaled_width = int(bg.get_width() * (zoom_factor))
            scaled_height = int(bg.get_height() * (zoom_factor))
            scaled_bg = pygame.transform.smoothscale(bg, (scaled_width, scaled_height))
            scaled_images.append(scaled_bg)


        self.zoom_cache[zoom_factor] = scaled_images
        if len(self.zoom_cache) > 15:  # Increased cache size
            oldest_zoom = sorted(self.zoom_cache.keys())[0]
            del self.zoom_cache[oldest_zoom]
        return scaled_images

    def draw_backgrounds(self, screen: pygame.Surface, scroll: float, layers: int):
        self.update_zoom()
        scaled_bgs = self.get_scaled_backgrounds(self.current_zoom)
        bg_width = scaled_bgs[0].get_width()

        for i, bg in enumerate(scaled_bgs):
            speed_sc = 1 + (i * 0.1)
            x_pos = (scroll * speed_sc) * self.current_zoom

            # Calculate center offsets
            x_center_offset = (bg.get_width() - bg_width) // 2
            y_center_offset = (bg.get_height() - self.original_images[i].get_height()) // 2

            positions = [
                (-bg_width - x_pos - x_center_offset, -y_center_offset),
                (-x_pos - x_center_offset, -y_center_offset),
                (bg_width - x_pos - x_center_offset, -y_center_offset)
            ]

            for pos_x, pos_y in positions:
                screen.blit(bg, (pos_x, pos_y))


def initialize_background_manager(background_set: int, width: int, height: int) -> BackgroundManager:
    layers = 4 if background_set in (1, 2) else 7

    bg_images = []

    for i in range(layers, 0, -1):
        bg_image = pygame.image.load(f"assets/Background/bg{background_set}/img {i}.png").convert_alpha()
        scaled_image = pygame.transform.smoothscale(bg_image, (width + 420, height))
        bg_images.append(scaled_image)

    return BackgroundManager(bg_images, width, height)



def healthbar(health_value, x, y, screen_width):
    bar_width = int(screen_width * 0.3)
    bar_height = 30
    ratio = health_value / 100
    pygame.draw.rect(screen, WHITE, (x, y, bar_width, bar_height))
    pygame.draw.rect(screen, RED, (x, y, bar_width * ratio, bar_height))

# Initialize background manager
x = 1  # Background set number
c = 4 if x in (1, 2) else 7
bg_manager = initialize_background_manager(x, WIDTH, HEIGHT)



def resize_images(width, height):
    global health, bg_manager
    health = pygame.transform.smoothscale(original_health, (width, 500))
    bg_manager = initialize_background_manager(x, width, height)


# Create fighters
fighter_1 = fighter(1, 200, 300, False, char1_data, char1_sheet, char1_anim,sound1)
fighter_2 = fighter(2, 600, 300, True, char2_data, char2_sheet, char2_anim,sound2)

player_id = network.get_player_id()
# Adjust initial positions based on player ID
if player_id == 1:
    fighter_1, fighter_2 = fighter_2, fighter_1  # Swap fighters for player 2


def update_network_state(fighter, network):
    # Create current player state
    player_state = PlayerState(
        x=fighter.rect.x,
        y=fighter.rect.y,
        health=fighter.health,
        animation_index=fighter.action,
        animation_frame=fighter.frame_index,
        attacking=fighter.attacking,
        attack_type=fighter.attack_type,
        jump=fighter.jump,
        flip=fighter.flip,
        run=fighter.running
    )

    # Send state and get both players' states
    game_state = network.send(player_state)

    if game_state is None:
        return None

    # Update opponent's state
    opponent_id = 1 if network.get_player_id() == 0 else 0
    return game_state.get(opponent_id)


# Main game loop
is_fullscreen = False
running = True
while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    if current_state == MENU:
        menu_manager.update()
        menu_manager.draw(screen, pygame.font.Font(None, 36))

        if menu_manager.state == "arena_selection":
            current_state = ARENA_SELECT

    elif current_state == ARENA_SELECT:
        menu_manager.update()
        menu_manager.draw(screen, pygame.font.Font(None, 36))

        if menu_manager.state == "main_menu":
            current_state = MENU
        elif menu_manager.selected_arena:
            # Update background based on selected arena
            arena_name = menu_manager.selected_arena
            if arena_name == "Forest Arena":
                x = 1
            elif arena_name == "Desert Arena":
                x = 2
            elif arena_name == "Ice Arena":
                x = 3
            c = 4 if x in (1, 2) else 7
            print(x)
            bg_manager = initialize_background_manager(x, WIDTH, HEIGHT)


    elif current_state == PLAYING:

        bg_manager.draw_backgrounds(screen, scroll, c)
        healthbar(fighter_1.health, int(WIDTH * 0.07), 25, WIDTH)
        healthbar(fighter_2.health, int(WIDTH * 0.63), 25, WIDTH)
        screen.blit(health, (0, 0))
        fighter_1.draw(screen)
        fighter_2.draw(screen)


        if intro_count <= 0:
            if fighter_1.jump or fighter_2.jump:
                bg_manager.set_target_zoom(1.0)  # Zoom out when jumping
            else:
                bg_manager.set_target_zoom(1.1)  # Normal zoom level

            fighter_1.move(WIDTH, HEIGHT, screen, fighter_2, False)
            fighter_2.move(WIDTH, HEIGHT, screen, fighter_1, False)

            fighter_1.update()  # Update the local player first

            # Send and receive network updates
            opp_state = update_network_state(fighter_1, network)
            if opp_state:
                # Update opponent position and state
                fighter_2.rect.x = opp_state.x
                fighter_2.rect.y = opp_state.y
                fighter_2.health = opp_state.health
                fighter_2.attacking = opp_state.attacking
                fighter_2.attack_type = opp_state.attack_type
                fighter_2.jump = opp_state.jump
                fighter_2.flip = opp_state.flip
                fighter_2.running=opp_state.run
                # Only update the action if it's different
                if fighter_2.action != opp_state.animation_index:
                    fighter_2.action = opp_state.animation_index
                    fighter_2.frame_index = opp_state.animation_frame
                    fighter_2.update_time = pygame.time.get_ticks()

            fighter_2.update()

            if fighter_1.health <= 0 or fighter_2.health <= 0:
                deathsound.play()
                current_state = GAME_OVER

            key = pygame.key.get_pressed()
            if (key[pygame.K_a] or key[pygame.K_LEFT]) and scroll > 0:
                scroll -= 5
            if (key[pygame.K_d] or key[pygame.K_RIGHT]) and scroll < 320:
                scroll += 5
            if (key[pygame.K_w] or key[pygame.K_UP]) and vertical_scroll < 50:
                vertical_scroll += scroll_speed
            elif vertical_scroll > 0:
                vertical_scroll -= return_speed
                vertical_scroll = max(0, vertical_scroll)

        else:
            drawtimer(intro_count, WIDTH, HEIGHT)
            if countdown_started and (pygame.time.get_ticks() - last_count) >= 1000:
                intro_count -= 1
                last_count = pygame.time.get_ticks()
                print(intro_count)

    elif current_state == PAUSED:
        bg_manager.draw_backgrounds(screen, scroll, c)
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        # Draw pause overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Draw pause menu
        pause_text = pygame.font.Font("CosmicAlien.ttf.", 30).render("Paused", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 3))

    elif current_state == GAME_OVER:
        bg_manager.draw_backgrounds(screen, scroll, c)
        fighter_1.draw(screen)
        fighter_2.draw(screen)
        fighter_1.update()
        fighter_2.update()
        # Create a transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)  # Adjust transparency (0-255)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        # Display the Game Over text
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                    WIDTH, HEIGHT = screen.get_size()
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                WIDTH, HEIGHT = screen.get_size()
                resize_images(WIDTH, HEIGHT)
                menu_manager = MenuManager(WIDTH,HEIGHT)  # Recreate menu manager with new dimensions


            elif event.key == pygame.K_RETURN:
                if current_state == MENU:
                    current_state = PLAYING
                    intro_count = 4  # Reset count when starting game
                    last_count = pygame.time.get_ticks()  # Set initial time when starting game
                    countdown_started = True
                    introsound.play()  # Play sound when countdown starts
                elif current_state == GAME_OVER:
                    fighter_1.reset(200, 300)
                    fighter_2.reset(600, 300)
                    current_state = PLAYING
            elif event.key == pygame.K_ESCAPE and current_state in (PLAYING, PAUSED):
                current_state = PAUSED if current_state == PLAYING else PLAYING
        elif event.type == pygame.VIDEORESIZE and not is_fullscreen:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            resize_images(WIDTH, HEIGHT)

        if current_state in (MENU, ARENA_SELECT):
            result = menu_manager.handle_event(event)
            if menu_manager.run:
                current_state= PLAYING
                intro_count = 4  # Reset count when starting game
                last_count = pygame.time.get_ticks()
                countdown_started = True
                introsound.play()
            if not result:  # Quit button pressed
                running = False

    pygame.display.update()

pygame.quit()