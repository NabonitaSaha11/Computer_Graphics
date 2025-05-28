import random
import sys
import time 
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18  # works on drawing text 





width, height = 550, 700
catcher_x = width // 2  # CATCHER er position bujhay 
catcher_width = width // 3 # CATCHER er width 
falling_diamonds = []  # currently jei diamond porche 
score = 0
game_over = False
paused = False
diamond_caught_since_last_speedup = 0
new_diamond_ready = True
last_time = time.time()
delta_time = 0.03  # initial fallback/default value
diamond_speed = 14  # pixels per second 







# 8 WAY SYMMETRYYYYYY (identify zone, bring it to zone0 and do necessary calculations, take it back to the zone it belonged )
def draw_line(x1, y1, x2, y2, thickness=2): # 8 way symmetry ( mid point line drawing niye deal kore )

    def find_zone(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        if abs(dx) >= abs(dy):
            if dx >= 0 and dy >= 0:
                return 0
            elif dx >= 0 and dy < 0: 
                return 7
            elif dx < 0 and dy >= 0: 
                return 3
            else: 
                return 4
        else:
            if dx >= 0 and dy >= 0: 
                return 1
            elif dx >= 0 and dy < 0: 
                return 6
            elif dx < 0 and dy >= 0: 
                return 2
            else: 
                return 5

    def convert_to_zone0(x, y, zone):
     if zone == 0:
        return x, y
     elif zone == 1:
        return y, x
     elif zone == 2:
        return y, -x
     elif zone == 3:
        return -x, y
     elif zone == 4:
        return -x, -y
     elif zone == 5:
        return -y, -x
     elif zone == 6:
        return -y, x
     else:
        return x, -y

    def convert_back(x, y, zone):
     if zone == 0:
        return x, y
     elif zone == 1:
        return y, x
     elif zone == 2:
        return -y, x
     elif zone == 3:
        return -x, y
     elif zone == 4:
        return -x, -y
     elif zone == 5:
        return -y, -x
     elif zone == 6:
        return y, -x
     else :
        return x, -y

    zone = find_zone(x1, y1, x2, y2)
    x_1, y_1 = convert_to_zone0(x1, y1, zone)
    x_2, y_2 = convert_to_zone0(x2, y2, zone)

    dx = x_2 - x_1
    dy = y_2 - y_1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    x, y = x_1, y_1
    while x <= x_2:  # ekhane x_1<=x<=x_2
        orig_x, orig_y = convert_back(x, y, zone) # etate kore correct direction e line ta represent kora possible hoy
        # ei part pixel er surrounding e point plot kore thickness baray  
        for dx_offset in range(-thickness, thickness+1 ):
            for dy_offset in range(-thickness, thickness+1):
                glBegin(GL_POINTS)
                glVertex2f(orig_x + dx_offset, orig_y + dy_offset)
                glEnd()

        # next point e jawa :
        if d > 0:
            y += 1
            d += incNE
        else:
            d += incE
        x += 1







def draw_diamond(x, y, w, h, thickness=2): # here, w= half of diamond width , h = half of diamond height 
    draw_line(x, y + h, x + w, y, thickness)
    draw_line(x + w, y, x, y - h, thickness)
    draw_line(x, y - h, x - w, y, thickness)
    draw_line(x - w, y, x, y + h, thickness)








def draw_catcher(thickness=2):
    global catcher_x
    # eta left and right limit niye deal kore catcher er center er (prevents catcher going out of screen)
    max_catcherx = width - catcher_width // 2
    min_catcherx = catcher_width // 2
    if catcher_x > max_catcherx:
        catcher_x = max_catcherx
    elif catcher_x < min_catcherx:
        catcher_x = min_catcherx

    ground_offset = 10
    bottom_y = ground_offset
    top_y = ground_offset + 30

    
    bottom_left = (catcher_x - catcher_width // 2 + 20, bottom_y)
    bottom_right = (catcher_x + catcher_width // 2 - 20, bottom_y)
    top_left = (catcher_x - catcher_width // 2, top_y)
    top_right = (catcher_x + catcher_width // 2, top_y)


    # inner trapezium black color korte: 
    # proti horizontal line e left_x to right_x , row of pixel color korte korte jay 
    glColor3f(0.0, 0.0, 0.0)
    for y in range(bottom_y, top_y):
        right_x = bottom_right[0] + (top_right[0] - bottom_right[0]) * (y - bottom_y) / (top_y - bottom_y) 
        left_x =  bottom_left[0] + (top_left[0] - bottom_left[0]) * (y - bottom_y) / (top_y - bottom_y) 
        for x in range(int(left_x), int(right_x) + 1):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

    if game_over== True : 
        glColor3f(1.0, 0.0, 0.0) 
    else : 
        glColor3f(1.0, 1.0, 1.0)


    draw_line(top_left[0], top_left[1], top_right[0], top_right[1], thickness)
    draw_line(top_right[0], top_right[1], bottom_right[0], bottom_right[1], thickness)
    draw_line(bottom_right[0], bottom_right[1], bottom_left[0], bottom_left[1], thickness)
    draw_line(bottom_left[0], bottom_left[1], top_left[0], top_left[1], thickness)









def draw_buttons(thickness=2):
    

    # pauseeee/ playyyyyy
    glColor3f(1.0, 0.5, 0.0)
    if paused:
        draw_line(width // 2 - 15, height - 5, width // 2 - 15, height - 45, thickness)
        draw_line(width // 2 + 15, height - 5, width // 2 + 15, height - 45, thickness)
    else:
        draw_line(width // 2 - 15, height - 5, width // 2 - 15, height - 45, thickness)
        draw_line(width // 2 - 15, height - 5, width // 2 + 15, height - 25, thickness)
        draw_line(width // 2 - 15, height - 45, width // 2 + 15, height - 25, thickness)


    # restartttttt
    glColor3f(0, 1, 1)
    draw_line(30, height - 25, 60, height - 25, thickness)
    draw_line(30, height - 25, 45, height - 5, thickness)
    draw_line(30, height - 25, 45, height - 45, thickness)

     
    # close kora 
    glColor3f(1, 0, 0)
    draw_line(width - 20, height - 5, width - 40, height - 45, thickness)
    draw_line(width - 20, height - 45, width - 40, height - 5, thickness)









# game e  harle ja dekhabe : 
def draw_game_over(score1):

    glColor3f(1.0, 0.0, 0.0)
    glRasterPos2f(width // 2 - 70, height // 2)
    for c in "GAME OVER":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

    glRasterPos2f((width // 2) - 70, (height // 2) - 30)
    final_scoretext = "FINAL SCORE : " + str(score1)
    for d in final_scoretext:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(d))









def draw_falling_diamonds():
    global falling_diamonds, score, diamond_caught_since_last_speedup, game_over, diamond_speed, new_diamond_ready
    # falling diamond = current diamond er x,y er tuple in list 

    def random_bright_color():
        return (random.uniform(0.5, 1.0), random.uniform(0.5, 1.0), random.uniform(0.5, 1.0))

    
    new_diamonds = [] #diamond jegula ekhono porche   
    for x, y in falling_diamonds:
        if paused== False:
            y = y - diamond_speed  # based on current speed, diamond ke downwards ane 
        else:
            y= y
        if y < 30: # diamond ei kehtre catching level e pouchabe 
            if catcher_x - catcher_width // 2 <= x <= catcher_x + catcher_width // 2:  # catcher er horizontal range  e diamong ache ki nai check kore 
                score += 1
                print(f"Current Score:{score}")
                diamond_caught_since_last_speedup += 1
                if diamond_caught_since_last_speedup == 3:
                    diamond_speed += 4
                    diamond_caught_since_last_speedup = 0
                new_diamond_ready = True
            else:
                game_over = True
                print(f"GAME OVER!!! Final Score:{score}")
                return  # ekhane theke diamond fall, generation shob bondho hoy 
        else:
            glColor3f(*random_bright_color())
            draw_diamond(x, y, 10, 20)  # drawing the diamond in the new position if the diamond hasn't reached the catch level 
            new_diamonds.append((x, y))

    falling_diamonds[:] = new_diamonds # falling_diamond ke updated rakhe with new_diamond er position 








##### eta amar main rendering function #####
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    if not game_over:
        draw_falling_diamonds()
        draw_catcher()
        draw_buttons()
    else:
        draw_game_over(score)
        draw_buttons()
        draw_catcher()
    glutSwapBuffers()







# catcher er left right movement niye deal kore 
def keyboard(key, x, y):
 global catcher_x, paused, game_over

 if paused:
        return   # exits the function immediately ekhane 
 
 if not game_over:
    if key == b'd':
        if catcher_x + catcher_width // 2 < width: # catcher er movemnet er por width jodi screen er baire na jay, tokhon catcher ke right e move korte allow kora hoy by +20 
            catcher_x += 20
    elif key == b'a':
        if catcher_x - catcher_width // 2 > 0:  #  catcher ke left e move korte dewa hoy by -20 if true 
            catcher_x -= 20







# restart button click korle ekhane ashbe 
def restart_game():
    global score, falling_diamonds, game_over, diamond_speed, diamond_caught_since_last_speedup, paused, new_diamond_ready, catcher_x
    print(f"###### NEW GAME ######")
    score = 0
    falling_diamonds.clear()
    game_over = False
    diamond_speed = 12
    diamond_caught_since_last_speedup = 0
    paused = False
    new_diamond_ready = True
    catcher_x = width // 2
    # shob data renew kore initial state e jemon thake temon bhabe include kora hobe 







def mouse(button, state, x, y):
    global paused, game_over

    if state == GLUT_DOWN: # mouse clicked 
        y = height - y

        if paused:
            if width//2- 15 <= x <= width//2+ 15 and height-45 <= y <= height-5:  # unpause kore 
                paused = False

            elif width- 40 <= x <= width- 20 and height-45 <= y <= height-5: # cross = shob bondho kore dey 
                print(f"Goodbye! Score: {score}")
                glutLeaveMainLoop()

            elif 30 <= x <= 60 and height- 45 <= y <= height- 5: # restart button 
                    restart_game()
            return 
            
    
        if not game_over: # restart, cross , pause/ play shob kaaj korbe 
                if width//2 - 15 <= x <= width//2 + 15 and height-45 <= y <= height-5:
                    paused = True

                elif width- 40 <= x <= width- 20 and height- 45 <= y <= height- 5:
                    print(f"Goodbye! Score: {score}")
                    glutLeaveMainLoop()

                elif 30 <= x <= 60 and height- 45 <= y <= height- 5:
                    restart_game()

        else:   # khali cross  ar restart kaaj korbe ( since here gese, pause/play kaaj korbena)
                if 30 <= x <= 60 and height- 45 <= y <= height- 5:
                    restart_game()

                elif width- 40 <= x <= width- 20 and height- 45 <= y <= height- 5:
                    print(f"Goodbye! Score: {score}")
                    glutLeaveMainLoop()









# ei function ta  keeps the game running smoothly in real time 
def update(value):
    global new_diamond_ready, delta_time, last_time , falling_diamonds

    if not paused and not game_over: # if diamonds are moving
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time

        for i in range(len(falling_diamonds)):
            x, y = falling_diamonds[i]
            new_y = y - diamond_speed * delta_time # s=vt, ensures smooth falling of heeraaaa
            falling_diamonds[i] = (x, new_y)

        if new_diamond_ready: # catcher catch korse diamond, next diamond generated hobe 
            if len(falling_diamonds) == 0 :
                falling_diamonds.append((random.randint(30, width - 30), height - 10))
                new_diamond_ready = False
        glutPostRedisplay() # display function trigger kore new position gula show korte 


    elif not game_over: # if game paused but game not over
        last_time = time.time()

    glutTimerFunc(16, update, 0)









glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(width, height)
glutCreateWindow(b"Catch the Diamonds!")
glClearColor(0.0, 0.0, 0.0, 0.0)
glOrtho(0, width, 0, height, -1, 1)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
glutTimerFunc(25, update, 0)  # 25ms porpor update function call diye check kore kono change anar ase naki 
glutMainLoop()
