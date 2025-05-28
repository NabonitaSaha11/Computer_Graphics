
######################################### TASK 01 ############################################


from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# ekhane global variables for rainfall exists
rain_drops = [(random.randint(-1000, 1800), random.randint(700, 2000)) for _ in range(500)]  
rain_direction = 0  #  bending of rain e help kore (-10 to 10 range)
day_night_factor = 1.0  # day=1, night=0

def draw_points(x, y):
    glPointSize(5) #pixel size. by default 1 thake

    
    glBegin(GL_QUADS)  # SKY EKHANEEEE
    glColor3f(0.3 * day_night_factor, 0.55 * day_night_factor, 0.9 * day_night_factor)
    glVertex2f(0, 300)
    glColor3f(0.25 * day_night_factor, 0.5 * day_night_factor, 0.85 * day_night_factor)
    glVertex2f(800, 300)
    glColor3f(0.2 * day_night_factor, 0.45 * day_night_factor, 0.8 * day_night_factor)
    glVertex2f(800, 800)
    glColor3f(0.25 * day_night_factor, 0.5 * day_night_factor, 0.85 * day_night_factor)
    glVertex2f(0, 800)
    glEnd()





    glBegin(GL_LINES)   # CREATES GAP BETWEEN ASMAN AR JOMIN 
    glColor3f(0*day_night_factor,0.9*day_night_factor,0.7*day_night_factor)
    glVertex2f(0,300) 
    glColor3f(0*day_night_factor,0.6*day_night_factor,0.7*day_night_factor)
    glVertex2f(800,300)
    glEnd()

    glBegin(GL_TRIANGLES)   # BUSHHHHH
    glColor3f(0.1*day_night_factor,0.5*day_night_factor,0.1*day_night_factor)
    glVertex2f(540,300) 
    glColor3f(0.1*day_night_factor,0.5*day_night_factor,0.1*day_night_factor)
    glVertex2f(640,300)
    glColor3f(1*day_night_factor,1*day_night_factor,0.2*day_night_factor)
    glVertex2f(590,400)
    glEnd()
    glBegin(GL_TRIANGLES)   
    glColor3f(0.1*day_night_factor,0.5*day_night_factor,0.1*day_night_factor)
    glVertex2f(540,350) 
    glColor3f(0.1*day_night_factor,0.5*day_night_factor,0.1*day_night_factor)
    glVertex2f(640,350)
    glColor3f(1*day_night_factor,1*day_night_factor,0.2*day_night_factor)
    glVertex2f(590,450)
    glEnd()
    glBegin(GL_TRIANGLES)   
    glColor3f(0.1*day_night_factor,0.5*day_night_factor,0.1*day_night_factor)
    glVertex2f(540,420) 
    glColor3f(0.1*day_night_factor,0.5*day_night_factor,0.1*day_night_factor)
    glVertex2f(640,420)
    glColor3f(1*day_night_factor,1*day_night_factor,0.2*day_night_factor)
    glVertex2f(590,500)
    glEnd()


    glBegin(GL_TRIANGLES)   # HOUSE ROOF BANAISI
    glColor3f(0*day_night_factor,0.1*day_night_factor,0.7*day_night_factor)
    glVertex2f(x,y) 
    glColor3f(0*day_night_factor,0.1*day_night_factor,0.7*day_night_factor)
    glVertex2f(550,400)
    glColor3f(1*day_night_factor,1*day_night_factor,1*day_night_factor)
    glVertex2f(400,500)
    glEnd()

    glBegin(GL_QUADS)  #MATI EKHANE
    glColor3f(0.8*day_night_factor, 0.4*day_night_factor, 0.3*day_night_factor)
    glVertex2f(0, 299)
    glColor3f(0.6*day_night_factor, 0.4*day_night_factor, 0.2*day_night_factor)
    glVertex2f(0, 0)
    glColor3f(0.8*day_night_factor, 0.3*day_night_factor, 0.1*day_night_factor)
    glVertex2f(800, 0)
    glColor3f(0.7*day_night_factor, 0.3*day_night_factor, 0.2*day_night_factor)
    glVertex2f(800, 299)
    glEnd()


 

    glBegin(GL_TRIANGLES)  # WALLS OF THE HOUSE 
    glColor3f(1*day_night_factor, 0.2*day_night_factor, 0*day_night_factor) 
    glVertex2f(300, 400)
    glColor3f(0*day_night_factor, 0.1*day_night_factor, 0.7*day_night_factor) 
    glVertex2f(300, 250)
    glColor3f(1*day_night_factor, 0.7*day_night_factor, 0.2*day_night_factor) 
    glVertex2f(500, 250)
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(1*day_night_factor, 0.2*day_night_factor, 0*day_night_factor) 
    glVertex2f(300, 400)
    glColor3f(1*day_night_factor, 0.7*day_night_factor, 0.2*day_night_factor) 
    glVertex2f(500, 250)
    glColor3f(1*day_night_factor, 0.8*day_night_factor, 0.2*day_night_factor) 
    glVertex2f(500, 400)
    glEnd()




    glBegin(GL_TRIANGLES)   # HOUSE ER DORJA 
    glColor3f(1*day_night_factor, 0.71*day_night_factor, 0*day_night_factor) 
    glVertex2f(375, 250)
    glColor3f(0.8*day_night_factor, 0.6*day_night_factor, 0.7*day_night_factor) 
    glVertex2f(425, 250)
    glColor3f(1*day_night_factor, 1*day_night_factor, 0.2*day_night_factor) 
    glVertex2f(425, 350)
    glEnd()

    glBegin(GL_TRIANGLES)
    glColor3f(1*day_night_factor, 0.71*day_night_factor, 0*day_night_factor) 
    glVertex2f(375, 250)
    glColor3f(1*day_night_factor, 1*day_night_factor, 0.2*day_night_factor) 
    glVertex2f(425, 350)
    glColor3f(1*day_night_factor, 0.8*day_night_factor, 0.2*day_night_factor) 
    glVertex2f(375, 350)
    glEnd()



    
    glBegin(GL_QUADS)   # TREEEEEEEEEE TRUNKKKK
    glColor3f(0.3*day_night_factor,0.15*day_night_factor,0.07*day_night_factor)
    glVertex2f(150,250) 
    glColor3f(0.4*day_night_factor,0.2*day_night_factor,0.1*day_night_factor)
    glVertex2f(170,250)
    glColor3f(0.2*day_night_factor,0.2*day_night_factor,0.051*day_night_factor)
    glVertex2f(170,530)
    glColor3f(0.4*day_night_factor,0.2*day_night_factor,0.1*day_night_factor)
    glVertex2f(150,530)
    glEnd()

    glBegin(GL_QUADS)   # TREEEEEEEEEE 
    glColor3f(0*day_night_factor,0.4*day_night_factor,0.07*day_night_factor)
    glVertex2f(100,430) 
    glColor3f(0.1*day_night_factor,0.5*day_night_factor,0.1*day_night_factor)
    glVertex2f(220,430)
    glColor3f(0.2*day_night_factor,0.8*day_night_factor,0.351*day_night_factor)
    glVertex2f(220,460)
    glColor3f(0.1*day_night_factor,1*day_night_factor,0.1*day_night_factor)
    glVertex2f(100,460)
    glEnd()
    glBegin(GL_QUADS)   
    glColor3f(0*day_night_factor,0.4*day_night_factor,0.07*day_night_factor)
    glVertex2f(115,460) 
    glColor3f(0.1*day_night_factor,0.5*day_night_factor,0.1*day_night_factor)
    glVertex2f(205,460)
    glColor3f(0.2*day_night_factor,0.8*day_night_factor,0.351*day_night_factor)
    glVertex2f(205,490)
    glColor3f(0.1*day_night_factor,1*day_night_factor,0.1*day_night_factor)
    glVertex2f(115,490)
    glEnd()
    glBegin(GL_QUADS)   
    glColor3f(0*day_night_factor,0.4*day_night_factor,0.07*day_night_factor)
    glVertex2f(130,490) 
    glColor3f(0.1*day_night_factor,0.5*day_night_factor,0.1*day_night_factor)
    glVertex2f(190,490)
    glColor3f(0.2*day_night_factor,0.8*day_night_factor,0.351*day_night_factor)
    glVertex2f(190,520)
    glColor3f(0.1*day_night_factor,1*day_night_factor,0.1*day_night_factor)
    glVertex2f(130,520)
    glEnd()
    glBegin(GL_QUADS)   
    glColor3f(0*day_night_factor,0.4*day_night_factor,0.07*day_night_factor)
    glVertex2f(145,520) 
    glColor3f(0.1*day_night_factor,0.5*day_night_factor,0.1*day_night_factor)
    glVertex2f(170,520)
    glColor3f(0.2*day_night_factor,0.8*day_night_factor,0.351*day_night_factor)
    glVertex2f(170,550)
    glColor3f(0.1*day_night_factor,1*day_night_factor,0.1*day_night_factor)
    glVertex2f(145,550)
    glEnd()
    glBegin(GL_QUADS)  
    glColor3f(0*day_night_factor,0.4*day_night_factor,0.07*day_night_factor)
    glVertex2f(115,400) 
    glColor3f(0.1*day_night_factor,0.5*day_night_factor,0.1*day_night_factor)
    glVertex2f(205,400)
    glColor3f(0.2*day_night_factor,0.8*day_night_factor,0.351*day_night_factor)
    glVertex2f(205,430)
    glColor3f(0.1*day_night_factor,1*day_night_factor,0.1*day_night_factor)
    glVertex2f(115,430)
    glEnd()




def draw_rain():
    glColor3f(0.1 * day_night_factor, 0.1 * day_night_factor, 0.7)
    glPointSize(2)
    glBegin(GL_LINES)
    for i in range(len(rain_drops)):
        x, y = rain_drops[i]
        glVertex2f(x, y)
        glVertex2f(x + rain_direction, y - 20)  # ekhane speed of the raindrops handle korsi 
        
        rain_drops[i] = (x + rain_direction, y - 20)

        # condition rakhsi jodi rainfall goes below the screen, it starts from the top again
        if y < 0:
            rain_drops[i] = (random.randint(0, 800), 800) 

        # If the rain drops move out of the left or right side, bringing them around to the other side-
        if rain_drops[i][0] < 0:
            rain_drops[i] = (800, rain_drops[i][1])  
        elif rain_drops[i][0] > 800:
            rain_drops[i] = (0, rain_drops[i][1]) 
    glEnd()

def keyboard(key, x, y):
    global rain_direction, day_night_factor
    key = key.decode("utf-8")
    if key == "\x1b":
        glutLeaveMainLoop()
    elif key == "l":
        day_night_factor = min(1.0, day_night_factor + 0.1)
    elif key == "d":
        day_night_factor = max(0.2, day_night_factor - 0.1)

def special_keys(key, x, y):
    global rain_direction

    
    if key == GLUT_KEY_LEFT and rain_direction > -10:
        rain_direction -= 1
    elif key == GLUT_KEY_RIGHT and rain_direction < 10:
        rain_direction += 1

def iterate():
    glViewport(0, 0, 800, 800)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 800, 0.0, 800, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClearColor(0.1 * day_night_factor, 0.2 * day_night_factor, 0.3 * day_night_factor, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_points(250, 400)
    draw_rain()
    glutSwapBuffers()

def update(value):
    glutPostRedisplay()
    glutTimerFunc(30, update, 0)

if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(800, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Rain Animation")
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutTimerFunc(30, update, 0)
    glutMainLoop()










######################################## TASK 02 ############################################################

# from OpenGL.GL import *
# from OpenGL.GLUT import *
# from OpenGL.GLU import *
# import random


# WINDOW_WIDTH, WINDOW_HEIGHT = 700, 700
# MAX_DOTS = 450  # just to reduce obstacle jam
# FRAME_RATE = 60



# COLOR_PALETTE = [ (1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), (1.0, 1.0, 0.0),
#     (1.0, 0.0, 1.0), (0.0, 1.0, 1.0), (0.5, 0.0, 0.0), (0.0, 0.5, 0.0),
#     (0.0, 0.0, 0.5), (0.5, 0.5, 0.0), (0.5, 0.0, 0.5), (0.0, 0.5, 0.5),
#     (1.0, 0.5, 0.0), (0.5, 1.0, 0.0), (0.0, 1.0, 0.5), (0.0, 0.5, 1.0),
#     (0.5, 0.0, 1.0), (1.0, 0.0, 0.5), (0.75, 0.25, 0.5), (0.25, 0.75, 0.5)]



# class MovingDot:

#     def __init__(self, x, y): #here I initialized dot positioning , color , speed and blink status
#         self.x = x
#         self.y = y
#         self.blinking = False
#         self.blink_visible = True
#         self.color = random.choice(COLOR_PALETTE)
#         self.dx = random.choice([-1, 1]) * random.uniform(1, 3)
#         self.dy = random.choice([-1, 1]) * random.uniform(1, 3)
#         self.stored_dx = 0
#         self.stored_dy = 0



#     def update_position(self): # In case it reaches edge of the window, direction reverse hoye jabe 
#         self.x = self.x+ self.dx
#         self.y = self.y+ self.dy

#         if  self.x >= WINDOW_WIDTH or self.x <= 0 :
#             self.dx *= -1
#         if  self.y >= WINDOW_HEIGHT or self.y <= 0 :
#             self.dy *= -1



#     def toggle_blink(self): #ekhane blinking state on/off korte pari 
#         self.blinking = not self.blinking
#         self.blink_visible = True



#     def render(self): # Defines kokhon dot draw korte parbo 
#         if self.blinking and not self.blink_visible:
#             return
#         glPointSize(8)
#         glColor3f(*self.color) # basically equivalents to glColor3f(R, G, B)
#         glBegin(GL_POINTS)
#         glVertex2f(self.x, self.y)
#         glEnd()

    

#     def adjust_speed(self, factor):
#         self.dx *= factor
#         self.dy *= factor # here it maintains the speed of my dots either faster or slower but within the range 
#         self.dx = max(0.5, min(abs(self.dx), 10.0)) * (1 if self.dx > 0 else -1)
#         self.dy = max(0.5, min(abs(self.dy), 10.0)) * (1 if self.dy > 0 else -1)



#     def freeze(self): #ekhane amar dot freezed hole oder oder freeze howar ag muhurter position stored rakhi
#         if self.dx == 0 and self.dy == 0:
#             return
#         self.stored_dx = self.dx
#         self.stored_dy = self.dy
#         self.dx = 0
#         self.dy = 0



#     def unfreeze(self):  #unfreeze kore position gula restore kore with the last stored speed 
#         if self.dx == 0 and self.dy == 0:
#             self.dx = self.stored_dx
#             self.dy = self.stored_dy




# dots = [] # shob dot er config store kore 
# is_paused = False
# frame_counter = 0



# def initialize():
#     glClearColor(0.0, 0.0, 0.0, 1.0)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT) #ekhane 2D setup create kora hoy 



# def render_scene():
#     glClear(GL_COLOR_BUFFER_BIT)
#     for val in dots:
#         val.render()
#     glutSwapBuffers() #smooth animation ensure kore ekhane



# def update_frame(value):
#     global is_paused, frame_counter
#     if not is_paused:
#         for dot in dots:
#             dot.update_position() #position update kori paused na thakle 
#         frame_counter += 1 #timing of blinking effect handle kore 
#         if frame_counter % FRAME_RATE == 0: 
#             for dot in dots:
#                 if dot.blinking:
#                     dot.blink_visible = not dot.blink_visible
#     glutPostRedisplay() 
#     glutTimerFunc(1000 // FRAME_RATE, update_frame, 0)



# def handle_mouse(button, state, x, y):
#     global is_paused
#     y = WINDOW_HEIGHT - y  # screen to opengl coordinate convert korsi to match
#     if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not is_paused:
#         if len(dots) < MAX_DOTS:
#             dots.append(MovingDot(x, y))
#     elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not is_paused:
#         for dot in dots:
#             dot.toggle_blink() #eta shob dot ke blinking er accesibility dey 



# def handle_keyboard(key, x, y):
#     global is_paused, dots
#     if key == b'\x1b':  # exit kore
#         glutLeaveMainLoop()
#     elif key == b' ':  # Spacebar= pause ar unpause
#         is_paused = not is_paused
#         for dot in dots:
#             dot.freeze() if is_paused else dot.unfreeze()
    


# def handle_special_keys(key, x, y):
    
#     if key == GLUT_KEY_DOWN and not is_paused:
#         for dot in dots:
#             dot.adjust_speed(0.9) #FACTOR 0.9 kore slow hoy
#     elif key == GLUT_KEY_UP and not is_paused:
#         for dot in dots:
#             dot.adjust_speed(1.5) #factor 1.5 kore fast hoy 



# glutInit()
# glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
# glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
# glutCreateWindow(b"Magic Box")
# initialize()
# glutDisplayFunc(render_scene)
# glutMouseFunc(handle_mouse)
# glutKeyboardFunc(handle_keyboard)
# glutSpecialFunc(handle_special_keys)
# glutTimerFunc(1000 // FRAME_RATE, update_frame, 0)
# glutMainLoop()
