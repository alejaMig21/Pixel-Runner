import pygame

def get_current_second() :
    return int(pygame.time.get_ticks() / 1000)

def display_score() :
    current_time = get_current_second() - start_time
    score_surface = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center = (SCREEN_WIDTH / 2, 50))
    pygame.draw.rect(screen, '#c0e8ec', score_rect)
    pygame.draw.rect(screen, '#c0e8ec', score_rect.inflate(10,10), border_radius=10)
    screen.blit(score_surface, score_rect)

pygame.init()

# game data
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
TARGET_FRAMERATE = 60
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
mouse_pos = (0, 0)
game_active = False
start_time = 0
game_name = test_font.render('Pixel Runner', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (SCREEN_WIDTH / 2, 80))
game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (SCREEN_WIDTH / 2, 340))

# enviroment area
sky_surface = pygame.image.load('graphics/Sky.png').convert_alpha()
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
ground_y_pos = 300
# text area
score_surface = test_font.render('2D Endless Runner', False, (64, 64, 64))
score_rect = score_surface.get_rect(center = (SCREEN_WIDTH / 2, 50))
# characters area - snail
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_x_original_pos = 800
snail_x_speed = 5
snail_y_original_pos = ground_y_pos
snail_rect = snail_surface.get_rect(bottomright = (snail_x_original_pos, snail_y_original_pos))
# characters area - player
player_run_surface = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha() # in game player state
player_stand_surface = pygame.image.load('graphics/player/player_stand.png').convert_alpha() # in menu player state
player_stand_scaled = pygame.transform.scale2x(player_stand_surface)
player_x_original_pos = 80
player_x_speed = 0
player_y_original_pos = ground_y_pos
player_y_current_pos = ground_y_pos
player_y_speed = -20 # jump force
player_run_rect = player_run_surface.get_rect(midbottom = (player_x_original_pos, player_y_current_pos)) # in game player rect
player_stand_rect = player_stand_scaled.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)) # in menu player rect
player_gravity = 0

isGameRunning = True

while isGameRunning:
    # ensure proper surface renderings
    screen.fill('Black')
    
    # events loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameRunning = False
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE :
                if player_run_rect.bottom >= ground_y_pos :
                    player_gravity = player_y_speed
                if not game_active :
                    game_active = True
                    snail_rect.left = snail_x_original_pos
                    player_run_rect.left = player_x_original_pos
                    start_time = get_current_second()
    
    if game_active :
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, ground_y_pos))
        display_score()
        
        # snail behaviour
        snail_rect.left -= snail_x_speed
        if snail_rect.left <= -snail_surface.get_width():
            snail_rect.left = snail_x_original_pos
        screen.blit(snail_surface, snail_rect)
        
        # player behaviour
        player_gravity += 1
        player_run_rect.top += player_gravity
        
        if player_run_rect.bottom > ground_y_pos :
            player_run_rect.bottom = ground_y_pos
        
        player_run_rect.left += player_x_speed
        screen.blit(player_run_surface, player_run_rect)
        
        # collision
        if snail_rect.colliderect(player_run_rect) :
            game_active = False
    else :
        screen.fill((94, 129, 162))
        screen.blit(player_stand_scaled, player_stand_rect)
        screen.blit(game_name, game_name_rect)
        screen.blit(game_message, game_message_rect)
    
    # refresh screen at a given framerate
    pygame.display.update()
    clock.tick(TARGET_FRAMERATE)

pygame.quit()