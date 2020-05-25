import pygame
pygame.init()
pygame.mixer.init()
import random
import os

pygame.mixer.music.load('back.mp3')
pygame.mixer.music.play()

#color
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
gray = (171, 190, 190)
brown = (229, 49, 24)

# Game window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#Background Image
bgimg = pygame.image.load("background.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
bgimg1 = pygame.image.load("starting.png")
bgimg1 = pygame.transform.scale(bgimg1, (screen_width, screen_height)).convert_alpha()

# Game title
pygame.display.set_caption("Snake Game")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((63, 89, 89 ))
        gameWindow.blit(bgimg1, (0, 0))
        text_screen("Welcome to Snakes", black, 260, 250)
        text_screen("Press Space Bar To Play", black, 230, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('game.mp3')
                    pygame.mixer.music.play(30)
                    gameloop()

        pygame.display.update()
        clock.tick(60)




# Creating a game loop
def gameloop():    
    exit_game = False
    game_over = False
    snake_x = 55
    snake_y = 55
    snake_size = 20
    fps = 60
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    food_x = random.randint(20, screen_width/2)
    food_y = random.randint(20, screen_height/2)
    score = 0
    init_velocity = 6
    if(not os.path.exists("Highscore.txt")):
        with open("Highscore.txt", "w") as f:
            f.write("0")
    with open("Highscore.txt", "r") as f:
        Highscore = f.read()
    while not exit_game:
        if game_over:
            with open("Highscore.txt", "w") as f:
                f.write(str(Highscore))
            gameWindow.fill(white)
            text_screen("Game Over! Press Enter To Continue", red, 100, 250)        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load('game.mp3')
                        pygame.mixer.music.play(30)
                        gameloop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0


            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<9 and abs(snake_y - food_y)<9:
                score = score + 10                
                food_x = random.randint(20, screen_width/2)
                food_y = random.randint(20, screen_height/2)
                snk_length += 4
                if score>int(Highscore):
                    Highscore = score
            gameWindow.fill(gray)
            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: "+ str(score) + "  Highscore: "+ str(Highscore), red, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])
            pygame.draw.rect(gameWindow, black, [snake_x, snake_y, snake_size, snake_size])
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]
            
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()
            
            
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('gameover.mp3')
                pygame.mixer.music.play()
            plot_snake(gameWindow, black, snk_list, snake_size)
        pygame.display.update()    
        clock.tick(fps)
    pygame.quit()
    quit()
welcome()