
import sys
import random
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (200,300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.apply_gravity()

def player_animation():
    global player_surf, player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):
            player_index = 0
        player_surf = player_walk[int(player_index)]

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                bg_music.stop()
                pygame.time.delay(200)
                hit_sound.play()
                return False
    return True

def calculate_speed(current_score):
    base_speed = 8 if hardcore_mode else 5
    max_speed = 18 if hardcore_mode else 14
    speed = base_speed + (current_score // 10)
    if speed > max_speed:
        speed = max_speed
    return speed

def spawn_obstacle(obstacle_list):
    if random.randint(0,2):
        obstacle_list.append(snail_surf.get_rect(bottomright = (random.randint(900,1100),300)))
    else:
        obstacle_list.append(fly_surf.get_rect(bottomright = (random.randint(900,1100),210)))
    return obstacle_list

def obstacle_movement(obstacle_list, speed):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= speed

            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'score: {current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return current_time

def update_high_score(current_score, current_high):
    if current_score > current_high:
        current_high = current_score
    if current_high > 0:
        high_surf = test_font.render(f'high score: {current_high}', False, (100,189,169))
        high_rect = high_surf.get_rect(center = (400,375))
        screen.blit(high_surf, high_rect)
    return current_high

def toggle_pause(toggle_state=False):
    global game_paused, pause_start_time, start_time

    if toggle_state:
        game_paused = not game_paused
        if game_paused:
            pause_start_time = int(pygame.time.get_ticks() / 1000)
            pygame.mixer.pause()
        else:
            paused_duration = int(pygame.time.get_ticks() / 1000) - pause_start_time
            start_time += paused_duration
            pygame.mixer.unpause()

    if game_paused:
        overlay = pygame.Surface((800, 400), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        pause_surf = test_font.render('GAME PAUSED - PRESS P TO RESUME', False, 'White')
        pause_rect = pause_surf.get_rect(center=(400, 180))
        screen.blit(pause_surf, pause_rect)

        update_settings()

def update_settings(key_pressed=None):
    global is_muted, hardcore_mode

    if key_pressed == pygame.K_m:
        is_muted = not is_muted
        bg_music.set_volume(0.0 if is_muted else 0.1)
        hit_sound.set_volume(0.0 if is_muted else 1.0)

    elif key_pressed == pygame.K_d:
        hardcore_mode = not hardcore_mode

    audio_status = "OFF" if is_muted else "ON"
    diff_status = "HARDCORE" if hardcore_mode else "NORMAL"

    settings_surf = settings_font.render(
        f'[M] Audio: {audio_status}   |   [D] Mode: {diff_status}   |   [P] Pause', 
        False, (220, 220, 220)
    )
    settings_rect = settings_surf.get_rect(center=(400, 25))
    screen.blit(settings_surf, settings_rect)

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("snake game")
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
settings_font = pygame.font.Font('font/Pixeltype.ttf', 30)

game_active = False
game_paused = False
is_muted = False
hardcore_mode = False

start_time = 0
pause_start_time = 0
score = 0
high_score = 0

bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.set_volume(0.1)
hit_sound = pygame.mixer.Sound('audio/fahhh.mp3')
hit_sound.set_volume(1.0)

player = pygame.sprite.GroupSingle()

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0 
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_surf = player_walk[player_index]

player_rect = player_surf.get_rect(midbottom = (80,300))

player_gravity = 0
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('pixel runner', False, (100,189,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render('press space to run', False, (100,189,169))
game_message_rect = game_message.get_rect(center = (400,340))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if not game_active or game_paused:
                if event.key in (pygame.K_m, pygame.K_d):
                    update_settings(event.key)

            if game_active and event.key == pygame.K_p:
                toggle_pause(toggle_state=True)

        if game_active and not game_paused:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == obstacle_timer:
                obstacle_rect_list = spawn_obstacle(obstacle_rect_list)

            if event.type == snail_animation_timer:
                snail_frame_index = 1 if snail_frame_index == 0 else 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                fly_frame_index = 1 if fly_frame_index == 0 else 0
                fly_surf = fly_frames[fly_frame_index]

        elif not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                game_paused = False
                obstacle_rect_list.clear()
                player_rect.bottom = 300
                player_gravity = 0
                start_time = int(pygame.time.get_ticks() / 1000)
                bg_music.play(loops=-1)

    if game_active:
        screen.blit(sky_surface, (0,0))
        screen.blit(ground_surface, (0,300))

        if not game_paused:
            score = display_score()

            player_gravity += 1
            player_rect.y += player_gravity
            if player_rect.bottom >= 300: 
                player_rect.bottom = 300
            player_animation()
            screen.blit(player_surf, player_rect)
            player.draw(screen)

            current_speed = calculate_speed(score)
            obstacle_rect_list = obstacle_movement(obstacle_rect_list, current_speed)

            game_active = collisions(player_rect, obstacle_rect_list)
        else:
            score_surf = test_font.render(f'score: {score}', False, (64,64,64))
            screen.blit(score_surf, score_surf.get_rect(center=(400, 50)))
            screen.blit(player_surf, player_rect)
            obstacle_movement(obstacle_rect_list, 0)
            toggle_pause(toggle_state=False)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        player_rect.midbottom = (80,300)
        player_gravity = 0

        score_message = test_font.render(f'your score: {score}', False, (100,189,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name, game_name_rect)

        update_settings()

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
            high_score = update_high_score(score, high_score)

    pygame.display.update()
    clock.tick(60)
"""
today day 2 and 3 created more obstacled a start/end screen a 
non working obstacle collision program , also this project has exceeded
5h of making so i will also be adding my own functions and sound effects
and later making it more better,,,,,,,,,,, day 4 skipped due to some evwnts day 5 :30 am doing nearly an hour
added flies fixed it logic ,,, fixed spawning for both also did added animation 
snd fixed collisions 
fahh 
"""
