"""
FOR BEST RESULTS, SET PROCESSING MAX MEMORY TO 1024MB OR HIGHER
"""

from welcomescreen import*
from platformer import*
import time
from random import randint
from random import uniform
add_library('minim')

def setup():
    #######################################################################
    # Function Name: setup
    # Function Purpose: setup the background and all global variables
    # Parameters: none
    # Variables (Locally defined): step_fcount, key_states, welcome_screen, bg(1 - 4), img_list, temp, img_height_list, sound_array, minim, intro, outro, pos_array, player, player_array, count, img_file, img_file_load, player_temp
    # Return: none
    #######################################################################

    
    global player_array, game_stage, welcome_screen, key_states, img_height_list, step_fcount, assist, sound_array
    
    size(800, 600)
    frameRate(60)
    
    # Timing variable based off frameCount differences
    step_fcount = 0
    
    # Makes holding down a key work correctly
    key_states = {}
    for char in "abcdefghijklmnopqrstuvwxyz":
        key_states[char] = False
    
    # loads our friendly buffalo assistant for board screens    
    assist = loadImage('buf.png')
    assist.resize(80, 0)
    
    # create intro/outro screens
    welcome_screen = []
    welcome_screen.append(WelcomeScreen("Mythic Origins: Echoes of the First Dawn"))
    welcome_screen.append(WelcomeScreen("Thank you for playing and creating harmony!"))
    game_stage = 'welcome'
    
    # background images, plus other important info
    bg1 = loadImage('bg1.png')
    bg1.resize(800, 0)
    bg2 = loadImage('bg2.png')
    bg2.resize(800, 0)
    bg3 = loadImage('bg3.png')
    bg3.resize(800, 0)
    bg4 = loadImage('bg4.png')
    bg4.resize(800, 0)
    
    img_list = [bg1, bg2, bg3, bg4]
    img_height_list = []
    
    n = 0
    while n < 4:
        temp = [img_list[n], 800 - img_list[n].height]
        img_height_list.append(temp)
        n += 1
    
    # sounds to be send to main
    sound_array = []
    minim = Minim(this)
    intro = minim.loadFile('intro.mp3')
    sound_array.append(intro)
    outro = minim.loadFile('outro.mp3') # if you're fine with swearing keep as outro.mp3, otherwise change to outro_alt.mp3
    sound_array.append(outro)

    # positions of the platforms
    pos_array = [
        [Platform(0, 600, 800, 1), Platform(200, 150, 100, 10),
        Platform(350, 200, 100, 10), Platform(500, 250, 100, 10),
        Platform(650, 300, 100, 10), Platform(200, 350, 100, 10),
        Platform(50, 400, 100, 10), Platform(350, 450, 100, 10),
        Platform(500, 500, 100, 10), Platform(650, 550, 100, 10),
        Platform(200, 100, 100, 10), Platform(50, 250, 100, 10),
        Platform(350, 300, 100, 10), Platform(500, 350, 100, 10),
        Platform(650, 400, 100, 10), Platform(200, 450, 100, 10),
        Platform(50, 500, 100, 10)],
        [Platform(0, 600, 800, 1), Platform(100, 500, 100, 10),
        Platform(250, 450, 100, 10), Platform(400, 400, 100, 10),
        Platform(550, 350, 100, 10), Platform(700, 300, 100, 10),
        Platform(150, 250, 100, 10), Platform(300, 200, 100, 10),
        Platform(450, 150, 100, 10), Platform(600, 100, 100, 10),
        Platform(50, 550, 100, 10), Platform(200, 480, 100, 10),
        Platform(350, 420, 100, 10), Platform(500, 360, 100, 10),
        Platform(650, 300, 100, 10), Platform(100, 240, 100, 10),
        Platform(250, 180, 100, 10)],
        [Platform(0, 600, 800, 1), Platform(50, 550, 100, 10),
        Platform(200, 500, 100, 10), Platform(75, 450, 100, 10),
        Platform(300, 400, 100, 10), Platform(450, 450, 100, 10),
        Platform(600, 500, 100, 10), Platform(750, 550, 100, 10),
        Platform(400, 350, 100, 10), Platform(550, 300, 100, 10),
        Platform(700, 250, 100, 10), Platform(350, 200, 100, 10),
        Platform(100, 350, 100, 10), Platform(250, 300, 100, 10),
        Platform(400, 250, 100, 10), Platform(550, 200, 100, 10),
        Platform(700, 150, 100, 10)]
    ]
    
    # creating each game
    player = loadImage("player.png")
    player.resize(60, 0)
    player_array = []
    count = 0
    for I in pos_array:
        img_file = str(count) + "_image.png"
        img_file_load = loadImage(img_file)
        player_temp = Player(100, 500, I, player, minim, img_file_load)
        player_array.append(player_temp)
        count += 1
        

def draw():
    #######################################################################
    # Function Name: draw
    # Function Purpose: call the main function for the game to run
    # Parameters: none
    # Variables (Locally defined): none
    # Return: none
    #######################################################################
    main()
    
def main():
    #######################################################################
    # Function Name: main
    # Function Purpose: Main game loop
    # Parameters: None
    # Variables (Locally defined): bottom_height, y_pos
    # Return: None
    #######################################################################

    global player_array, game_stage, welcome_screen, key_states, img_height_list, step_fcount, assist, sound_array
    
    # system for determining when to display what
    if game_stage == 'welcome': # 10 seconds at 60 fps
        # display welcome screen, play music
        if frameCount < 600: 
            welcome_screen[0].update()
            welcome_screen[0].display()
            sound_array[0].play()
            
        else:
            sound_array[0].pause()
            clear()
            game_stage = 'board1'
            step_fcount = frameCount

    elif game_stage == 'board1':
        if frameCount - step_fcount < 450:  # 7.5 seconds at 60 fps
            image(img_height_list[0][0], 0, 0)
            bottom_height = img_height_list[0][1]
            y_pos = img_height_list[0][0].height
            fill('#804322')
            rect(0, y_pos, 800, bottom_height)
            image(assist, 0, 520)
            textSize(20)
            fill('#ffffff')
            text("The plains are empty, just mountains. It's up to you to create!", 400, (bottom_height + (y_pos / 2) - 60))
            text("Use A and D to move left and right,\n W to jump, and triple jump to attack!", 400, (bottom_height + (y_pos / 2) - 10))
        else:
            clear()
            game_stage = 'game1'
            step_fcount = frameCount

    elif game_stage == 'game1':
        # non jump movement logic
        if key_states['a']:
            player_array[0].acc.add(PVector(-1, 0))
        if key_states['d']:
            player_array[0].acc.add(PVector(1, 0))
        
        player_array[0].check_platform_collision()
        player_array[0].update()
        player_array[0].check_platform_collision()
        player_array[0].display()
        
        # check if all enemies have died
        if player_array[0].are_all_enemies_dead():
            game_stage = 'board2'
            step_fcount = frameCount
            player_array[0] = "done"

    elif game_stage == 'board2':
        if frameCount - step_fcount < 450: # 7.5 seconds at 60 fps
            image(img_height_list[1][0], 0, 0)
            bottom_height = img_height_list[1][1]
            y_pos = img_height_list[1][0].height
            fill('#804322')
            rect(0, y_pos, 800, bottom_height)
            image(assist, 0, 520)
            textSize(20)
            fill('#ffffff')
            text("Good job, we have the forest, rivers, and plains now!", 400, (bottom_height + (y_pos / 2) - 60))
            text("Beat the next wave to create the buffalos!", 400, (bottom_height + (y_pos / 2) - 10))
        else:
            clear()
            game_stage = 'game2'
            step_fcount = frameCount

    elif game_stage == 'game2':
        # non jump movement logic
        if key_states['a']:
            player_array[1].acc.add(PVector(-1, 0))
        if key_states['d']:
            player_array[1].acc.add(PVector(1, 0))

        player_array[1].check_platform_collision()
        player_array[1].update()
        player_array[1].check_platform_collision()
        player_array[1].display()
        
        # check if all enemies are dead
        if player_array[1].are_all_enemies_dead():
            game_stage = 'board3'
            step_fcount = frameCount
            player_array[1] = "done"

    elif game_stage == 'board3':
        if frameCount - step_fcount < 450: # 7.5 seconds at 60 fps
            image(img_height_list[2][0], 0, 0)
            bottom_height = img_height_list[2][1]
            y_pos = img_height_list[2][0].height
            fill('#804322')
            rect(0, y_pos, 800, bottom_height)
            image(assist, 0, 520)
            textSize(20)
            fill('#ffffff')
            text("We are almost done creating!", 400, (bottom_height + (y_pos / 2) - 60))
            text("Finish the last wave to create humans, allowing the Earth to exist in harmony!", 400, (bottom_height + (y_pos / 2) - 10))
        else:
            clear()
            game_stage = 'game3'
            step_fcount = frameCount

    elif game_stage == 'game3':
        # non jump movement logic
        if key_states['a']:
            player_array[2].acc.add(PVector(-1, 0))
        if key_states['d']:
            player_array[2].acc.add(PVector(1, 0))

        player_array[2].check_platform_collision()
        player_array[2].update()
        player_array[2].check_platform_collision()
        player_array[2].display()

        # check if all enemies are dead
        if player_array[2].are_all_enemies_dead():
            game_stage = 'board4'
            step_fcount = frameCount
            player_array[2] = "done"

    elif game_stage == 'board4':
        if frameCount - step_fcount < 450: # 7.5 seconds at 60 fps
            image(img_height_list[3][0], 0, 0)
            bottom_height = img_height_list[3][1]
            y_pos = img_height_list[3][0].height
            fill('#804322')
            rect(0, y_pos, 800, bottom_height)
            image(assist, 0, 520)
            textSize(20)
            fill('#ffffff')
            text("All has been created.", 400, (bottom_height + (y_pos / 2) - 60))
            text("From this day on, everything and everyone will live in harmony!", 400, (bottom_height + (y_pos / 2) - 10))
        else:
            clear()
            game_stage = 'exit'
            step_fcount = frameCount

    elif game_stage == 'exit':
        # display exit screen, play music
        welcome_screen[1].update()
        welcome_screen[1].display()
        sound_array[1].play()

def keyPressed():
    #######################################################################
    # Function Name: keyPressed (Processing default name)
    # Function Purpose: handle key presses through key_states dictionary, and jumping internally (for triple jump to work)
    # Parameters: none
    # Variables (Locally defined): none
    # Return: none
    #######################################################################

    global key_states, player_array, game_stage
    key_states[key] = True
    
    # string methods for handling which object to jump in
    if key == 'w' and game_stage.startswith('game'):
        if game_stage.endswith('1'):
            player_array[0].jump()
        elif game_stage.endswith('2'):
            player_array[1].jump()
        elif game_stage.endswith('3'):
            player_array[2].jump()
    
def keyReleased():
    #######################################################################
    # Function Name: keyReleased (Processing default name)
    # Function Purpose: handle key releases through key_states dictionary
    # Parameters: none
    # Variables (Locally defined): none
    # Return: none
    #######################################################################

    global key_states
    key_states[key] = False
