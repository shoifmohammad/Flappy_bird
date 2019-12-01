import pygame
import random
import time

pygame.init()

# Basic colours
white = (255, 255, 255)
black = (0, 0, 0)
light_green = (0, 200, 100)
magenta = (128, 0, 128)
pink = (255, 20, 145)

# Game constants ---
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird by Shoif Mohammad")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
player_img = pygame.image.load('bird.png')
player_img = pygame.transform.scale(player_img, (45, 45))
player_width = player_img.get_width()
player_height = player_img.get_height()
background_img = pygame.image.load('mountain.jpg')
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))
background_img_full = pygame.image.load('mountain.jpg')
background_img_full1 = pygame.transform.scale(background_img_full, (background_img_full.get_width(), screen_height))
background_img_full2 = pygame.transform.scale(background_img_full, (background_img_full.get_width(), screen_height))
pipe_img = pygame.image.load('pipe-green.png')
pipe_width = pipe_img.get_width()
pipe_img = pygame.transform.scale(pipe_img, (pipe_width, screen_height))
pipe_img_rev = pygame.transform.rotate(pipe_img, 180)
pipe_width = pipe_img.get_width()
pipe_height = pipe_img.get_height()
right = pygame.image.load('right.png')
right_dark = pygame.image.load('right_dark.png')
left = pygame.transform.rotate(right, 180)
left_dark = pygame.transform.rotate(right_dark, 180)
right_width = right.get_width()
right_height = right.get_height()
pos = 0
pos_next = pos + background_img_full.get_width()

# Parameters
gap = 0     # Difference between upper and lower pipe.
diff = 0    # Difference between two consecutive pipes.
lower = 0
upper = 0

# Player attributes
playerX = screen_width*0.2 - player_width/2
playerY = screen_height*0.5 - player_height/2
g = 3
player_acc = g

# Box details for introduction part
box_width = 275
box_height = 75
boxX = (screen_width-box_width)/2
boxY = (screen_height-box_height)/2
box_speed = 20
text_width = 0
text_height = 0
var = 0
level = ["Easy", "Moderate", "Difficult"]

# Pipes
pipeX = []
upper_pipeY = []
lower_pipeY = []
pipe_speed = -3
num_of_pipes = 0

# Score
score = 0
high_score = 0

# Drawing rectangle
def draw_rect(x, y, width, height, color):
    pygame.draw.rect(screen, color, [x, y, width, height])

# Setting parameters according to difficulty level
def Set(x):
    global gap
    global diff
    global lower
    global upper
    global num_of_pipes
    global pipeX
    global upper_pipeY
    global lower_pipeY
    pipeX.append(random.randint(screen_width*0.4, screen_width))
    if x == 0:
        gap = 200
        diff = 325
        lower = 200
        upper = 300
    elif x == 1:
        gap = 175 
        diff = 300
        lower = 200
        upper = 350
    else:
        gap = 150
        diff = 275
        lower = 100
        upper = 400

    upper_pipeY.append(random.randint(lower, upper))
    lower_pipeY.append(upper_pipeY[0] + gap)
    num_of_pipes = (screen_width/diff) + 3
    
    for i in range(1, int(num_of_pipes), 1):
        pipeX.append(pipeX[i-1] + diff)
        upper_pipeY.append(random.randint(lower, upper))
        lower_pipeY.append(upper_pipeY[i] + gap)
    
    return()


# Introduction part of game
def game_intro():
    global var
    pipeX.clear()
    upper_pipeY.clear()
    lower_pipeY.clear()
    state_left = "stable"
    state_right = "stable"
    boxX = (screen_width-box_width)/2
    boxY = (screen_height-box_height)/2
    var = 0
    while True:
        screen.fill(light_green)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        text = pygame.font.Font('into_deep.otf', 50)
        text_font = text.render("Choose level", True, black)
        text_width = text_font.get_width()
        screen.blit(text_font, ((screen_width-text_width)/2, 75))
        text = pygame.font.Font('into_deep.otf', 30)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_RIGHT:
                    state_left = "stable"
                    if var == 0 or var == 1:
                        state_right = "moving"
                if event.key == pygame.K_LEFT:
                    state_right = "stable"
                    if var == 1 or var == 2:
                        state_left = "moving"
                if event.key == pygame.K_KP_ENTER:
                    Set(var)
                    return()

        # Action for right click.
        if screen_width-right_width-50 < mouse[0] < screen_width-50 and (screen_height-right_height)/2 < mouse[1] < (screen_height+right_height)/2 :
            if click[0] == 1:
                if var == 0 or var == 1:
                    state_right = "moving"

        # Action for left click.                
        if 50 < mouse[0] < 50+right_width and (screen_height-right_height)/2 < mouse[1] < (screen_height+right_height)/2 :
            if click[0] == 1:
                if var == 1 or var == 2:
                    state_left = "moving"

        # Action for choosing.
        if (screen_width-box_width)/2 <= mouse[0] <= (screen_width+box_width)/2 and (screen_height-box_height)/2 < mouse[1] < (screen_height+box_height)/2 :
            if click[0] == 1:
                Set(var)
                return()

        # Action for right arrow
        if state_right is "moving":
            boxX -= box_speed
            if(boxX < (0 - box_width)):
                var += 1
                boxX = screen_width
            if((screen_width-box_width)/2 <= boxX <= (screen_width+box_width)/2+box_speed):
                boxX = (screen_width-box_width)/2
                state_right = "stable"
            draw_rect(boxX, boxY, box_width, box_height, magenta)
            text_font = text.render(level[var], True, black)
            text_width = text_font.get_width()
            text_height = text_font.get_height()
            screen.blit(text_font, ((boxX+box_width-text_width), (screen_height-text_height)/2))
        
        # Action for left arrow
        if state_left is "moving":
            boxX += box_speed
            if(boxX > screen_width):
                var -= 1
                boxX = 0-box_width
            if((screen_width-box_width)/2-box_speed <= boxX <= (screen_width-box_width)/2):
                boxX = (screen_width-box_width)/2
                state_left = "stable"
            draw_rect(boxX, boxY, box_width, box_height, magenta)
            text_font = text.render(level[var], True, black)
            text_width = text_font.get_width()
            text_height = text_font.get_height()
            screen.blit(text_font, ((boxX+box_width-text_width), (screen_height-text_height)/2))

        # Displaying objects in stable position        
        else:
            if boxX < mouse[0] < boxX + box_width and boxY < mouse[1] < boxY + box_height:
                draw_rect(boxX, boxY, box_width, box_height, pink)
            else:
                draw_rect(boxX, boxY, box_width, box_height, magenta)
            
            for i in range(3):
                if var == i:
                    text_font = text.render(level[i], True, black)
                    text_width = text_font.get_width()
                    text_height = text_font.get_height()
                    screen.blit(text_font, ((screen_width-text_width)/2, (screen_height-text_height)/2))
            if var == 0 or var == 1:
                if screen_width-right_width-50 < mouse[0] < screen_width-50 and (screen_height-right_height)/2 < mouse[1] < (screen_height+right_height)/2 :
                    screen.blit(right_dark, ((screen_width-right_width-50), (screen_height-right_height)/2))
                else:
                    screen.blit(right, ((screen_width-right_width-50), (screen_height-right_height)/2))
            if var == 1 or var == 2:
                if 50 < mouse[0] < 50+right_width and (screen_height-right_height)/2 < mouse[1] < (screen_height+right_height)/2 :
                    screen.blit(left_dark, (50, (screen_height-right_height)/2))
                else:
                    screen.blit(left, (50, (screen_height-right_height)/2))

        pygame.display.update()

# Checking collision function
def collision(up, low, x, playerX, playerY):
    if abs(playerX - x) < pipe_width:
        if playerY < up or playerY > low:
            return True
    return False

# Loop for the gameplay.
def game_loop():
    playerY = screen_height*0.5 - player_height/2
    player_acc = 3
    global score
    pos = 0
    pos_next = pos + background_img_full.get_width()
    run = True
    while run:
        screen.blit(background_img_full1, (pos, 0))
        screen.blit(background_img_full2, (pos_next, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_SPACE:
                    player_acc = -5
            if event.type == pygame.KEYUP:
                player_acc = g

        text = pygame.font.Font('mounting.ttf', 20)
        text_font = text.render("Score : " + str(score), True, black)
        screen.blit(text_font, (0, 0))
        text_font = text.render("High Score : " + str(high_score), True, black)
        score_width = text_font.get_width()
        screen.blit(text_font, (screen_width - score_width, 0))
        
        # Checking for background
        pos += pipe_speed
        pos_next += pipe_speed
        if pos < (0 - background_img_full.get_width()):
            pos = 0
            pos_next = pos + background_img_full.get_width()

        # Cheking collision at boundaries
        if playerY < 0 or playerY > (screen_height-player_height):
            return()
        
        # Updating score
        player_mid = (playerX + player_width)/2
        for i in range(int(num_of_pipes)):
            pipe_mid = (pipeX[i] + pipe_width)/2
            if pipe_mid <= player_mid < pipe_mid-pipe_speed/2 :
                score += 5

        # Checking for collision
        for i in range(int(num_of_pipes)):
            if(abs(playerX - pipeX[i]) < diff):
                col = collision(upper_pipeY[i], lower_pipeY[i], pipeX[i], playerX, playerY)
                if col:
                    return()        

        # Removals of pipes out of the screen and adding at end
        store = int(num_of_pipes)
        for i in range(store):
            if pipeX[i] < 0-pipe_width:
                pipeX.append(pipeX[store-1] + diff)
                upper_pipeY.append(random.randint(lower, upper))
                lower_pipeY.append(upper_pipeY[store] + gap)
                del pipeX[i]
                del upper_pipeY[i]
                del lower_pipeY[i]
        
        # Displaying all the objects
        playerY += player_acc
        screen.blit(player_img, (playerX, playerY))
        for i in range(int(num_of_pipes)):
            screen.blit(pipe_img, (pipeX[i], lower_pipeY[i]))
            screen.blit(pipe_img_rev, (pipeX[i], upper_pipeY[i]-pipe_height))
            pipeX[i] += pipe_speed
        pygame.display.update()

# Display game over and ask whether they want to play again
def game_over():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_KP_ENTER:
                    return()
        
        screen.blit(background_img, (0, 0))
        
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        font = pygame.font.Font('mounting.ttf', 50)
        end_font = font.render("-: GAME OVER :-", True, black)
        width = end_font.get_width()
        height = end_font.get_height()
        screen.blit(end_font, ((screen_width-width)/2, (screen_height-height)/4))

        text = pygame.font.Font('mounting.ttf', 20)
        text_font = text.render("Score : " + str(score), True, black)
        screen.blit(text_font, (0, 0))
        text_font = text.render("High Score : " + str(high_score), True, black)
        score_width = text_font.get_width()
        screen.blit(text_font, (screen_width - score_width, 0))
        
        font = pygame.font.Font('mounting.ttf', 25)
        font1 = font.render("Play", True, white)
        width1 = font1.get_width()
        height1 = font1.get_height()
        font2 = font.render("Quit", True, white)
        width2 = font2.get_width()
        height2 = font2.get_height()
        
        pos1 = (screen_height-height1)*0.75
        if 75 < mouse[0] < 125+width1 and pos1-25 < mouse[1] < pos1+height1+25 :
            if click[0] == 1:
                return()
            draw_rect(75, pos1-25, width1+50, height1+50, black)
        screen.blit(font1, (100, pos1))
        
        pos2 = (screen_width - width2) - 100
        pos3 = (screen_height-height2)*0.75
        if pos2 < mouse[0] < pos2+width2+50 and pos3-25 < mouse[1] < pos3+height2+25 :
            if click[0] == 1:
                pygame.quit()
                quit()
            draw_rect(pos2, pos3-25, width2+50, height2+50, black)
        screen.blit(font2, (pos2+25, pos3))

        pygame.display.update()
    

if __name__ == '__main__':
    high_score = 0
    while True:
        game_intro()
        game_loop()
        game_over()
        if score > high_score:
            high_score = score
        score = 0
    quit()
