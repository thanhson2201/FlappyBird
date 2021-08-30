import pygame,sys,random

def draw_floor():
    screen.blit(flo,(flo_x_pos,650))
    screen.blit(flo,(flo_x_pos+432,650))

def creat_pipe():
    random_pipe_height = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_height))
    top_pipe = pipe_surface.get_rect(midtop = (500,random_pipe_height-650))
    return top_pipe,bottom_pipe

def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

def check(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True

def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird

def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100,bird_rect.centery))
    return new_bird,new_bird_rect

def score_display(game_state):
    if game_state == 'main game':
        score_surface = game_font.render(str(int(score)),True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)
    if game_state == 'Game Over':
        score_surface = game_font.render(f'Score :{(int(score))}',True,(255,255,255))
        score_rect = score_surface.get_rect(center = (216,100))
        screen.blit(score_surface,score_rect)

        high_score_surface = game_font.render(f'High Score :{(int(high_score))}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center = (216,610))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score,high_score):
    if score > high_score:
        high_score = score
    return high_score
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.init()
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
game_font = pygame.font.Font('C:/Users/Hi/Documents/Code/Python/Game/04B_19.TTF',40)

gravity = 0.25
bird_movement = 0
game_loop = True
score = 0
high_score = 0
# background
bg = pygame.image.load('C:/Users/Hi/Documents/Code/Python/Game/assets/background-night.png')
bg = pygame.transform.scale2x(bg)
# floor
flo = pygame.image.load('C:/Users/Hi/Documents/Code/Python/Game/assets/floor.png')
flo = pygame.transform.scale2x(flo)
flo_x_pos = 0
# bird
bird_bottom = pygame.image.load('C:/Users/Hi/Documents/Code/Python/Game/assets/yellowbird-upflap.png')
bird_middle = pygame.image.load('C:/Users/Hi/Documents/Code/Python/Game/assets/yellowbird-midflap.png')
bird_top = pygame.image.load('C:/Users/Hi/Documents/Code/Python/Game/assets/yellowbird-downflap.png')
bird_list = [bird_top,bird_middle,bird_bottom]
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center = (100,384))
# timer_bird
bird_flap = pygame.USEREVENT + 1
pygame.time.set_timer(bird_flap,200)
# pipe
pipe_list = []
pipe_surface = pygame.image.load('C:/Users/Hi/Documents/Code/Python/Game/assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_height = [200,300,400]
# timer_pipe
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1200)
#sound
flap_sound = pygame.mixer.Sound('C:/Users/Hi/Documents/Code/Python/Game/sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('C:/Users/Hi/Documents/Code/Python/Game/sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('C:/Users/Hi/Documents/Code/Python/Game/sound/sfx_point.wav')
score_count = 100
# ending
game_over_surface = pygame.image.load('C:/Users/Hi/Documents/Code/Python/Game/assets/message.png')
game_over_rect = game_over_surface.get_rect(center = (216,384))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement = -7
                flap_sound.play() 
            if event.key == pygame.K_SPACE and game_loop == False:
                game_loop = True
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_movement = 0
                score = 0
        if event.type == spawnpipe:
            pipe_list.extend(creat_pipe())
        if event.type == bird_flap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
            
    screen.blit(bg,(0,0))
    if game_loop:
        # bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_loop = check(pipe_list)
        # pipe
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01    
        score_display("main game")
        score_count -= 1
        if score_count <= 0:
            score_sound.play()
            score_count = 100
    else:
        score_display("Game Over")
        high_score = update_score(score,high_score)
        screen.blit(game_over_surface,game_over_rect)
    # floor
    flo_x_pos -= 1
    draw_floor()
    if flo_x_pos <= -432:
        flo_x_pos = 0
    pygame.display.update()
    clock.tick(120)
    