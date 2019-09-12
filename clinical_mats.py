import pygame
import pyautogui
import RPi.GPIO as gpio
import random
from random import choice, randint

from game_manager import Game_Manager
from mat import Mat

# Game clock
clock = pygame.time.Clock()
FPS = 20

# Setup GPIO
gpio.setmode(gpio.BCM)
TOP_LEFT = 10
TOP_RIGHT = 22
BOT_LEFT = 27
BOT_RIGHT = 17

# Defining pins
gpio.setup(TOP_LEFT, gpio.IN)
gpio.setup(TOP_RIGHT, gpio.IN)
gpio.setup(BOT_LEFT, gpio.IN)
gpio.setup(BOT_RIGHT, gpio.IN)

# Screen dimensions
DISPLAY_WIDTH, DISPLAY_HEIGHT = pyautogui.size()
cw = DISPLAY_WIDTH / 2  # Center width of screen 
ch = DISPLAY_HEIGHT / 2 # Center height of screen
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((1600,1200))

# Game manager
gm = Game_Manager(running=True, game_state=1)

# List of Mats
mats = [
        Mat("Top Left", screen, cw - 420, ch - 420),
        Mat("Top Right", screen, cw, ch - 420),
        Mat("Bottom Left", screen, cw - 420, ch),
        Mat("Bottom Right", screen, cw, ch)
        ]

# Initialize pygame
pygame.init()

### GUI ###
# Fonts
small_font = pygame.font.SysFont("quicksand", 12)
medium_font = pygame.font.SysFont("quicksand", 20)
large_font = pygame.font.SysFont("quicksand", 28)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (185, 185, 185)

# Global exit button
exit_rect = pygame.draw.rect(screen, WHITE, (DISPLAY_WIDTH - 200, DISPLAY_HEIGHT - 100,200,100))
exit_text = medium_font.render("Exit", True, BLACK)
exit_text_rect = exit_text.get_rect()
exit_text_rect.center = exit_rect.center



def intro():

    ### Logic ###

    ### Drawing ###
    screen.fill(BLACK)

    # Choice text
    intro_text = large_font.render("Choose which type of trial to run...", False, WHITE)
    screen.blit(intro_text, (cw-200, ch-250))

    # Front to Back Button
    fb_rect = pygame.draw.rect(screen, WHITE, (cw-100, ch-150,200,100))
    fb_text = medium_font.render("Front to Back", True, BLACK)
    fb_text_rect = fb_text.get_rect()
    fb_text_rect.center = fb_rect.center
    screen.blit(fb_text, fb_text_rect)

    # Left to Right Button
    lr_rect = pygame.draw.rect(screen, WHITE, (cw-100, ch,200,100))
    lr_text = medium_font.render("Left to Right", True, BLACK)
    lr_text_rect = lr_text.get_rect()
    lr_text_rect.center = lr_rect.center
    screen.blit(lr_text, lr_text_rect)

    # Random Button
    r_rect = pygame.draw.rect(screen, WHITE, (cw-100,ch+150,200,100))
    r_text = medium_font.render("Random", True, BLACK)
    r_text_rect = r_text.get_rect()
    r_text_rect.center = r_rect.center
    screen.blit(r_text, r_text_rect)

    # Exit Button
    exit_rect = pygame.draw.rect(screen, WHITE, (DISPLAY_WIDTH - 200, DISPLAY_HEIGHT - 100,200,100))
    screen.blit(exit_text, exit_text_rect)

    ### Event System ###
    for event in pygame.event.get():
        
        # Exit window
        if event.type == pygame.QUIT:
            gm.running = False

        # ESC exit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gm.running = False

        # Button collision checks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
           
            # 'Front to Back' button
            if fb_rect.collidepoint(mouse_pos):
                gm.start_ticks = pygame.time.get_ticks()
                gm.game_state = 2
                gm.trial_type = 1
                gm.target_mat = random.randint(0,3)
                
                # Front
                if gm.target_mat == 0 or gm.target_mat == 1:
                    gm.switch = True
                # Back
                else:
                    gm.switch = False

            # 'Left to Right' button
            if lr_rect.collidepoint(mouse_pos):
                gm.start_ticks = pygame.time.get_ticks()
                gm.game_state = 2
                gm.trial_type = 2
                gm.target_mat = random.randint(0,3)
                

                # Left
                if gm.target_mat == 1 or gm.target_mat == 3:
                    gm.switch = True
                # Right
                else:
                    gm.switch = False

            # 'Random' button
            if r_rect.collidepoint(mouse_pos):
                gm.start_ticks = pygame.time.get_ticks()
                gm.game_state = 2
                gm.trial_type = 3
                gm.target_mat = random.randint(0,3)

            # 'Exit' button
            if exit_rect.collidepoint(mouse_pos):
                gm.running = False

def countdown(): 
    
    ### Logic ###
    seconds = (pygame.time.get_ticks() - gm.start_ticks) / 1000
    seconds = gm.timer - seconds
    
    if seconds <= 1:
        gm.game_state = 3
        gm.trial_timer_start_ticks = pygame.time.get_ticks()

    ### Drawing ###
    timer_text = large_font.render("{:0.0f}".format(abs(seconds)), False, WHITE)
    screen.blit(timer_text, (cw, ch))

    # Exit Button
    exit_rect = pygame.draw.rect(screen, WHITE, (DISPLAY_WIDTH - 200, DISPLAY_HEIGHT - 100,200,100))
    screen.blit(exit_text, exit_text_rect)

    ### Event System ###
    for event in pygame.event.get():
        # Exit window
        if event.type == pygame.QUIT:
            gm.running = False

        # ESC exit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gm.running = False

        # Button collision checks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
           
            # Exit button
            if exit_rect.collidepoint(mouse_pos):
                gm.running = False


def trial():
   
    
    ### User input ###
    # GPIO pressed checks
    if gpio.input(TOP_LEFT):
        mats[0].state = 1

    if gpio.input(TOP_RIGHT):
        mats[1].state = 1

    if gpio.input(BOT_LEFT):
        mats[2].state = 1

    if gpio.input(BOT_RIGHT):
        mats[3].state = 1

    # GPIO unpressed checks
    if gpio.input(TOP_LEFT) == 0 and mats[0].state == 1:
        mats[0].state = 0

    if gpio.input(TOP_RIGHT) == 0 and mats[1].state == 1:
        mats[1].state = 0

    if gpio.input(BOT_LEFT) == 0 and mats[2].state == 1:
        mats[2].state = 0

    if gpio.input(BOT_RIGHT) == 0 and mats[3].state == 1:
        mats[3].state = 0
    
    
    ### Logic ###
    # Front to back
    if gm.trial_type == 1:
        
        # Front
        if gm.switch:

            # Target mat was pressed
            if mats[gm.target_mat].state == 1:
                pressed = []
                gm.steps += 1

                # Iterate through front mats
                for x in range(0,2):
                    if mats[x].state == 1 or mats[x].state == 2:
                        pressed.append(x)

                # Grab a unique non used, random mat
                if len(pressed) < 2:
                    gm.target_mat = choice([i for i in range(2,4) if i not in pressed])

                # Switch to back
                gm.switch = False
                
        
        # Back
        else:

            # Target mat was pressed
            if mats[gm.target_mat].state == 1:
                pressed = []
                gm.steps += 1

                # Iterate through back mats
                for x in range(2,4):
                    if mats[x].state == 1 or mats[x].state == 2:
                        pressed.append(x)

                # Grab a uniqe non used, random mat
                if len(pressed) < 2:
                    gm.target_mat = choice([i for i in range(0,2) if i not in pressed])

                # Switch to top
                gm.switch = True 
        
        # Set new target mat
        mats[gm.target_mat].state = 2


    # Left to right
    if gm.trial_type == 2:
     
        # Left
        if gm.switch:

            # Target mat was pressed
            if mats[gm.target_mat].state == 1:
                pressed = []
                gm.steps += 1

                # Iterate through left  mats
                for x in [y for y in range(0,4) if y != 0  and y != 2]:
                    if mats[x].state == 1 or mats[x].state == 2:
                        pressed.append(x)

                # Grab a unique non used, random mat
                if len(pressed) < 2:
                    gm.target_mat = choice([i for i in range(0,4) if i not in pressed and i != 1 and i != 3])
                
                # Switch to right
                gm.switch = False

        # Right
        else:

            # Target Mat was pressed
            if mats[gm.target_mat].state == 1:
                pressed = []
                gm.steps += 1

                # Iterate through back mats
                for x in [y for y in range(0,4) if y != 1 and y != 3]:
                    if mats[x].state == 1 or mats[x].state == 2:
                        pressed.append(x)

                # Grab a unique non used, random mat
                if len(pressed) < 2:
                    gm.target_mat = choice([i for i in range(0,4) if i not in pressed and i != 0 and i != 2])
                
                # Switch to left
                gm.switch = True
        
        # Set new target mat
        mats[gm.target_mat].state = 2


    # Random
    if gm.trial_type == 3:
       
        # Target mat was pressed
        if mats[gm.target_mat].state == 1:
            gm.steps += 1
            
            
            # Choose a new mat
            mats[gm.target_mat].state = 1

            # Select a non used random mat
            pressed = []

            # Get the state of all mats
            for x in range(0,4):
                if mats[x].state == 1 or mats[x].state == 2:
                    pressed.append(x)

            # Grab a unique non used, random mat
            if len(pressed) < 4:
                gm.target_mat = choice([i for i in range(0,4) if i not in pressed])

        # Set current target mat
        mats[gm.target_mat].state = 2


    ### Drawing ###
    # Exit Button
    exit_rect = pygame.draw.rect(screen, WHITE, (DISPLAY_WIDTH - 200, DISPLAY_HEIGHT - 100,200,100))
    screen.blit(exit_text, exit_text_rect)
    
    # Iterate through mats and draw them    
    for mat in mats:
        mat.draw()
 
    ### Event System ###
    for event in pygame.event.get():
        
        # Exit window
        if event.type == pygame.QUIT:
            gm.running = False

        # ESC exit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gm.running = False

        # Button collision checks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
           
            # Exit button
            if exit_rect.collidepoint(mouse_pos):
                gm.running = False

def results():

    ### Logic ###

    ### Drawing ###
    # Trial complete text
    finish_text = large_font.render("Trial Complete!", False, WHITE)
    screen.blit(finish_text, (cw-100, ch-100))
    
    # Step count text
    step_text = large_font.render("Steps: {}".format(gm.steps), False, WHITE)
    screen.blit(step_text, (cw-70, ch-50))
    
    # Timer text
    timer_text = large_font.render("Time: {}".format(gm.trial_timer), False, WHITE)
    screen.blit(timer_text, (cw-80, ch))

    # New Trial Button
    nt_rect = pygame.draw.rect(screen, WHITE, (cw-100, ch+150,200,100))
    nt_text = medium_font.render("New Trial?", True, BLACK)
    nt_text_rect = nt_text.get_rect()
    nt_text_rect.center = nt_rect.center
    screen.blit(nt_text, nt_text_rect)

    # Exit Button
    exit_rect = pygame.draw.rect(screen, WHITE, (DISPLAY_WIDTH - 200, DISPLAY_HEIGHT - 100,200,100))
    screen.blit(exit_text, exit_text_rect)


    ### Event System ###
    for event in pygame.event.get():

        # Exit window
        if event.type == pygame.QUIT:
            gm.running = False

        # ESC exit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                gm.running = False
        
        # Button collision checks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            # New trial button
            if nt_rect.collidepoint(mouse_pos):
                # Reset all game manager variables
                gm.reset()
                # Reset all mats to default grey state
                for mat in mats: 
                    mat.state = 0

            # Exit button
            if exit_rect.collidepoint(mouse_pos):
                gm.running = False


### Game Loop ###
while gm.running:
    screen.fill(BLACK)

    # Intro State
    if gm.game_state == 1:
        intro()

    # Countdown State
    if gm.game_state == 2:
        countdown()

    # Trial State
    if gm.game_state == 3:
        
        # Run until 20 steps are counted
        if gm.steps < 20:
            trial()
        else:
            gm.trial_timer = (pygame.time.get_ticks() - gm.trial_timer_start_ticks) / 1000
            gm.game_state = 4

    # Results State
    if gm.game_state == 4:
        results()
    
    # Update screen
    pygame.display.update()
    
    # Define fps
    clock.tick(FPS)

# Exit game
pygame.quit()
