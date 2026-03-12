import pygame
import random

scream = 'scream.mp3'
nom = 'nom.mp3'

pygame.init()  #Initialises library
pygame.mixer.init() #initialises the sound module 

window = pygame.display.set_mode((800,800))
pygame.display.set_caption("Snake Game")

def checkered():    #Creates checkered background
     tile_size = 40            
     for row in range(18):
         for col in range(20):
             if (row + col) % 2 == 0:
                color = (160, 160, 160)  # Light grey
             else:
                color = (96, 96, 96)     # Dark grey
             pygame.draw.rect(window, color, (col * tile_size, row * tile_size + 80, tile_size, tile_size))

def load_high_score():
    try: 
        with open("highscore.txt", "r") as file: 
            return int(file.read())
    except:
        return 0 # if file doesn't exist or empty it returns 0.

def game_over_msg():
    window.fill((0, 0, 135), (0, 80, 800, 720))
    font_large = pygame.font.Font(None, 74) 
    text = font_large.render(f"Game Over! Score:{score}", True, (255, 255, 255))
    high_score_text = font_large.render(f"High Score: {high_score}", True, (255, 255, 255))    
    text_rect = text.get_rect(center = (400, 300))
    hstext_rect = high_score_text.get_rect(center = (300, 200))

    window.blit(text, text_rect)
    window.blit(high_score_text, hstext_rect)

    font_small = pygame.font.Font(None, 36)
    restart_text = font_small.render("Press ENTER to restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center = (400,400))
    window.blit(restart_text, restart_rect)

    pygame.display.update()

score = 0
high_score = load_high_score()

snake = [(5, 9), (6, 9), (7, 9)]  #initial snake position
obstacles = [] #coordinates of blocks after scoring stored as list

direction = "RIGHT"      #starting direction
dx, dy = 1, 0 

clock = pygame.time.Clock()    #game clock

game_over = False

#Setting up burger/food item
burger_img = pygame.image.load("burger.png").convert_alpha()
burger_img = pygame.transform.scale(burger_img, (40, 40))
burger_x = random.randint(0, 20)
burger_y = random.randint(0, 18)

running = True        #Main game loop
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                dx, dy = 1, 0
                direction = "RIGHT"
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                dx, dy = -1, 0
                direction = "LEFT"
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                dx, dy = 0, -1
                direction = "UP"
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                dx, dy = 0, 1
                direction = "DOWN"

    checkered()

    font = pygame.font.Font(None, 36)
    font_s = pygame.font.Font(None, 24)
    score_bg = pygame.Rect(0, 0, 800, 80)
    pygame.draw.rect(window, (0, 0, 0), score_bg) 
    score_text = font.render(f"Score: {score}", True, (255,255,255))
    high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
    window.blit(score_text, (20,20))
    window.blit(high_score_text, (240, 20))

    controls = font_s.render("Use Arrows or WASD for movement", True, (255, 255, 255))
    window.blit(controls, (500, 20))

    #draws burger on grid
    window.blit(burger_img, (burger_x * 40, burger_y * 40 + 80))

    for obs_x, obs_y in obstacles:
        pygame.draw.rect(window, (102, 0, 204), (obs_x * 40, obs_y * 40 + 80, 40, 40))

    #Logically --> Movement 1st             
    head_x, head_y = snake[0] #initial head position
    new_head = (head_x + dx, head_y + dy) #new head position
    snake.insert(0, new_head)

    #Allows length of snake to increase by 1 if burger eaten. 
    if not (new_head[0] == burger_x and new_head[1] == burger_y):
        snake.pop()

    #Collision checks for burger (2nd)
    if new_head[0] == burger_x and new_head[1] == burger_y:
        score += 1
        pygame.mixer.music.load(nom)
        pygame.mixer.music.play()
        valid_burger = False    
        while not valid_burger:
            burger_x = random.randint(0, 19)
            burger_y = random.randint(0, 17)
            if (burger_x, burger_y) not in obstacles:
                valid_burger = True

        #spawning of obstacle
        obstacle_spwn = (random.randint(0, 19), random.randint(0, 17))
        obstacles.append(obstacle_spwn)

    #Drawing the snake (3rd)
    for i, (x, y) in enumerate(snake):
        pixel_x = x * 40
        pixel_y = y * 40 + 80

        if i == 0: #head
            color = (0, 204, 102) 
        elif i == len(snake) - 1: #tail
            color = (255, 255, 51)
        else: #body
            color = (51, 255, 51)

        pygame.draw.rect(window, color, (pixel_x, pixel_y, 40, 40))

    #Wall collision check (3rd)
    if (new_head[0] < 0 or new_head[0] >= 20 or new_head[1] < 0 or new_head[1] >= 18):
        pygame.mixer.music.load(scream)
        pygame.mixer.music.play()
        game_over = True
    
    #Obstacle collision check
    if new_head in obstacles:
        game_over = True

    #Gamover due to any collision 
    if game_over:       
        while game_over:
            game_over_msg() 

            #Game over screen loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  #restarts game
                        if score > high_score:
                            with open("highscore.txt", "w") as file:
                                file.write(str(score))
                                high_score = score 
                        snake = [(5,9), (6,9), (7,9)]
                        dx, dy = 1, 0
                        score = 0
                        obstacles = []
                        game_over = False
                         
    pygame.display.update()  #draws entire display

    clock.tick(10) #10 fps for snake movement

pygame.quit()