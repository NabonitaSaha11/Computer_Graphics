from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Constants and Globals
GRID_LENGTH = 600
PLAYER_SCALE = 2.5
ENEMY_SCALE = 2.1
BULLET_SPEED = 8
ENEMY_SPEED = 0.1/2
FOVY = 120


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

camera_mode = "default"  # or "follow"
camera_angle = 0
camera_height = 600
camera_radius = 500
cheat_mode = False
cheat_vision = False

player_pos = [0, 0, 0]
player_angle = 0
life = 5
score = 0
missed_bullets = 0
game_over = False
missed_bullets_in_a_row =0



# Define gun offset (relative to player)  # bullet player er bodyr upor spawn korbe, bhitore na
gun_offset = [0, 5 * PLAYER_SCALE, 17 * PLAYER_SCALE]  


bullets = []
enemies = []   # active bullet ar active enemy hold korbe 

rand_var = 423


class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.z = 30  # height from ground
        self.angle = angle
        self.active = True   # false hoile bullet disappear hoy
        self.hit= False

    def move(self):
        self.x += BULLET_SPEED * math.cos(math.radians(self.angle)) # bullet shamne niye jay 
        self.y += BULLET_SPEED * math.sin(math.radians(self.angle))
        if abs(self.x) > GRID_LENGTH or abs(self.y) > GRID_LENGTH: # playing field er moddhe rakhe 
            self.active = False

    def draw(self):
        glPushMatrix()
        glColor3f(1, 0.647, 0)  # Orange color
        glTranslatef(self.x, self.y, self.z+38)
        glScalef(3,3,3)
        glutSolidCube(5)
        glPopMatrix()


class Enemy:
    def __init__(self):
        self.reset()

    def reset(self):# random position e enemy chole ashe
        while True:
            self.x = random.randint(-GRID_LENGTH + 50, GRID_LENGTH - 50)
            self.y = random.randint(-GRID_LENGTH + 50, GRID_LENGTH - 50)
            if abs(self.x) > 200 or abs(self.y) > 200:
                break
        self.scale = 3
        self.growing = True





    def move(self):
        dx = player_pos[0] - self.x
        dy = player_pos[1] - self.y
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist != 0:
            self.x += ENEMY_SPEED * dx / dist
            self.y += ENEMY_SPEED * dy / dist
        # enemy size boro choto hoy
        if self.growing:
            self.scale += 0.005
            if self.scale >= 8:
                self.growing = False
        else:
            self.scale -= 0.005
            if self.scale <= 5:
                self.growing = True




     # enemy aka
    def draw(self):
     glPushMatrix()
     glColor3f(1, 0, 0) 
     glTranslatef(self.x, self.y, 20)  
     glutSolidSphere(self.scale * ENEMY_SCALE * 4, 20, 20)  # Increased size of the body
     glColor3f(0, 0, 0)  # Black color for head
     glTranslatef(0, 0, self.scale * ENEMY_SCALE * 4.5)  
     
     glutSolidSphere(self.scale * ENEMY_SCALE * 2, 20, 20)  
     glPopMatrix()
 


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)





def setupCamera():  # mouse right click e jei perspective view ta dey eta ekhane handle kori 
    global camera_angle
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


    if camera_mode == "follow": # camera player er mathay boshay player er vision er dike face kora thake 
        cx = player_pos[0] - camera_radius/3 * math.cos(math.radians(player_angle-90)) 
        cy = player_pos[1] - camera_radius/3 * math.sin(math.radians(player_angle-90))
        cz= player_pos[2]+290
        gluLookAt(cx, cy, cz,
                  player_pos[0]+50, player_pos[1], cz,
                  0, 0, 2)
    else:
        cx = camera_radius * math.cos(math.radians(camera_angle))
        cy = camera_radius * math.sin(math.radians(camera_angle))
        gluLookAt(cx, cy, camera_height,
                  0, 0, 0,
                  0, 0, 1)






PLAYER_SCALE = 4.5  # Scale player to make it larger


def draw_player():
    glPushMatrix()  
    glTranslatef(player_pos[0], player_pos[1], 0)

    if game_over :
        glRotatef(-90, 1, 0, 0) # shuye pore player = dead 
    else:
     glRotatef(player_angle, 0, 0, 1)



    
    # Head (sphere)
    glPushMatrix() 
    glTranslatef(0, 0, 24 * PLAYER_SCALE) 
    glColor3f(0, 0, 0)  
    glScalef( 1,1,1) 
    glutSolidSphere(6 * PLAYER_SCALE, 20, 20)  
    glPopMatrix() 




    # Body (rectangular cuboid)
    glPushMatrix()  
    glTranslatef(0,0, 10 * PLAYER_SCALE)  
    glColor3f(0.5, 0.5, 0.0)  # Olive Green color for body
    glScalef(17 * PLAYER_SCALE, 12 * PLAYER_SCALE, 22.8 * PLAYER_SCALE)  
    glutSolidCube(0.85)  
    glPopMatrix()  
    


    # Legs (cylinders)
    glPushMatrix()  
    glColor3f(0.0, 0.0, 0.4)  
    

    glPushMatrix()
    glTranslatef(-6.5 * PLAYER_SCALE, 3, -5 * PLAYER_SCALE)  
    gluCylinder(gluNewQuadric(), 4.5 * PLAYER_SCALE, 2.5 * PLAYER_SCALE, 16 * PLAYER_SCALE, 10, 10)
    glPopMatrix()  
   
    glPushMatrix()
    glTranslatef(6.5 * PLAYER_SCALE, 3, -5 * PLAYER_SCALE)  
    gluCylinder(gluNewQuadric(), 4.5 * PLAYER_SCALE, 2.5 * PLAYER_SCALE, 16 * PLAYER_SCALE, 10, 10)
    glPopMatrix()
    
    glPopMatrix()  
    


   #armsss
    glPushMatrix()  
    glColor3f(1, 0.8, 0.6)  
    
    glPushMatrix()
    glTranslatef(-5 * PLAYER_SCALE, 5 * PLAYER_SCALE, 17 * PLAYER_SCALE)  
    glScalef(2 , 1.7 , 2.7 ) 
    glRotatef(90, 1, 0, 0)  
    gluCylinder(gluNewQuadric(), 1 * PLAYER_SCALE, 1 * PLAYER_SCALE, 10 * PLAYER_SCALE, 10, 10)
    glPopMatrix()  
    
    
    glPushMatrix()
    glTranslatef(5 * PLAYER_SCALE, 5 * PLAYER_SCALE, 17 * PLAYER_SCALE)  
    glScalef(2 , 1.7, 2.7 )  
    glRotatef(90, 1, 0, 0)  
    gluCylinder(gluNewQuadric(), 1 * PLAYER_SCALE, 1 * PLAYER_SCALE, 10 * PLAYER_SCALE, 10, 10)
    glPopMatrix()  # End transformations for right arm
    



    # Gun (middle cylinder through which bullet will be shot)
    glPushMatrix()  
    glColor3f(0.8, 0.8, 0.8)  


    # Gun (middle cylinder) on the body
    glTranslatef(2, 5 * PLAYER_SCALE, 17 * PLAYER_SCALE)  
    glScalef(2.5 , 1.7 , 2.3 ) 
    glRotatef(90, 1, 0, 0)  
    gluCylinder(gluNewQuadric(), 1 * PLAYER_SCALE, 1 * PLAYER_SCALE, 15 * PLAYER_SCALE, 10, 10)
    glPopMatrix()  
    
    glPopMatrix()  
    glPopMatrix()  




def check_collisions():  # this is where we collect a point for hitting the enemy 
    global score, missed_bullets, life, game_over, missed_bullets_in_a_row
    for bullet in bullets:
        for enemy in enemies:
            dist = math.sqrt((bullet.x - enemy.x) ** 2 + (bullet.y - enemy.y) ** 2)
            if dist < 30:
                score += 1
                bullet.hit=True
                bullet.active = False
                enemy.reset()
                #missed_bullets_in_a_row=0


    for enemy in enemies:   # enemy too close to player 
        dist = math.sqrt((enemy.x - player_pos[0]) ** 2 + (enemy.y - player_pos[1]) ** 2)
        if dist < 50:
            life -= 1
            enemy.reset()
            if life <= 0:
                game_over = True







def draw_grid():
    num_squares = 20 # 20x20 grid
    square_size = (2 * GRID_LENGTH) / num_squares

    #  chessboard-style grid
    for i in range(num_squares): # x axis
        for j in range(num_squares): # y axis
          
            if (i + j) % 2 == 0:
                glColor3f(1.0, 1.0, 1.0) 
            else:
                glColor3f(0.8, 0.7, 1.0)  

            x = -GRID_LENGTH + i * square_size
            y = -GRID_LENGTH + j * square_size  # Starting from the boundary (bottom)

            glBegin(GL_QUADS)   # floor shuru korsi -40 theke 
            glVertex3f(x, y, -40)
            glVertex3f(x + square_size, y, -40)
            glVertex3f(x + square_size, y + square_size, -40)
            glVertex3f(x, y + square_size, -40)
            glEnd()

    


    # floor er boundary :
    thickness = 50
    z = 0
    boundary_height = 100 



    glColor3f(0, 1, 1)  # cyan
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, z-40)                  
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, z-40)                   
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, boundary_height)     
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, boundary_height)   
    glEnd()

    
    glColor3f(1, 1, 1) # white
    glBegin(GL_QUADS)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, z-40)                   
    glVertex3f(GRID_LENGTH, GRID_LENGTH, z-40)                   
    glVertex3f(GRID_LENGTH, GRID_LENGTH, boundary_height)     
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, boundary_height)     
    glEnd()


    
    glColor3f(0.5, 1.0, 0.5)  # Light Bright Green
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, z-40)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, z-40)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, boundary_height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, boundary_height)
    glEnd()

    

    glColor3f(0, 0, 1)  # blue
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, z-40)  
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, z-40)   
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, boundary_height)  
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, boundary_height)  
    glEnd()





def showScreen():
    global bullets, missed_bullets, game_over, missed_bullets_in_a_row, player_angle
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    

    setupCamera()
    draw_grid()
    draw_player()

    if not game_over:
        for bullet in bullets:
            bullet.move()  # updating the moves of the bullets
            if bullet.active:
                bullet.draw()
            else:
                if not bullet.hit:  
                  missed_bullets += 1
                  missed_bullets_in_a_row += 1
                  if missed_bullets_in_a_row >= 10:
                        game_over = True
                        print(" 10 bullets missed in a row, game over :( ")
                else: 
                    missed_bullets_in_a_row= 0

        bullets = [b for b in bullets if b.active]

        for enemy in enemies:
            enemy.move()
            enemy.draw()

        if cheat_mode== True :
          player_angle += 4  


        

          
          for enemy in enemies:
             dx = enemy.x - player_pos[0]
             dy = enemy.y - player_pos[1]
             angle_to_enemy = math.degrees(math.atan2(dy, dx))
             angle_diff = (angle_to_enemy - player_angle) % 360
             if angle_diff > 180:
                angle_diff -= 360

             if abs(angle_diff)<= 15:  
                fire_bullet()

                
                #check_collisions()
                #break


        check_collisions()

    
    draw_text(10, 770, f"Player life remaining: {life}")
    draw_text(10, 750, f"Game score: {score}")
    draw_text(10, 730, f"Player bullets missed: {missed_bullets}")


    glutSwapBuffers()


def clamp_player_position():      # helps player to stay within boundary
     player_pos[0] = max(-GRID_LENGTH +15, min(player_pos[0], GRID_LENGTH- 1-15))
     player_pos[1] = max(-GRID_LENGTH+15, min(player_pos[1], GRID_LENGTH- 1-15))




def keyboardListener(key, x, y):
  global player_pos, player_angle, cheat_mode, cheat_vision, life, score, missed_bullets, game_over

  move_speed = 5
  

  if game_over== False:

    if key == b'a':  # Rotate left
        player_angle += 5
    elif key == b'd':  # Rotate right
        player_angle -= 5
    

    elif key == b'c':
        cheat_mode = not cheat_mode
    elif key == b'v':
        if cheat_mode and camera_mode== 'follow' :
           cheat_vision = not cheat_vision


    elif key == b'w':
                player_pos[0] -= move_speed * math.sin(math.radians(-player_angle))
                player_pos[1] -= move_speed * math.cos(math.radians(player_angle))
    elif key == b's':
                player_pos[0] += move_speed * math.sin(math.radians(-player_angle))
                player_pos[1] += move_speed * math.cos(math.radians(player_angle))
    
    clamp_player_position()  # added to restrict within grid
  else: 
    if key == b'r' :
        life = 5
        score = 0
        missed_bullets = 0
        game_over = False
        player_pos = [0, 0, 0]
        bullets.clear()
        enemies.clear()
        for _ in range(5):
            enemies.append(Enemy())




def specialKeyListener(key, x, y):
    global camera_height, camera_angle

    if key == GLUT_KEY_UP:
        camera_height += 10
    elif key == GLUT_KEY_DOWN:
        camera_height -= 10
    elif key == GLUT_KEY_LEFT:
        camera_angle += 5
    elif key == GLUT_KEY_RIGHT:
        camera_angle -= 5


def mouseListener(button, state, x, y):
    global camera_mode
    if game_over== False:
       if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
          fire_bullet()

       elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
         camera_mode = "follow" if camera_mode == "default" else "default"



def fire_bullet():
    bullet_start_x = player_pos[0] + 2
    bullet_start_y = player_pos[1] + (5 * PLAYER_SCALE)
    bullet_start_z = 17 * PLAYER_SCALE  

    bullets.append(Bullet(bullet_start_x, bullet_start_y, player_angle - 90))





def idle():
    glutPostRedisplay()




def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy")

    glEnable(GL_DEPTH_TEST)
    for _ in range(5):
        enemies.append(Enemy())

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()




if __name__ == "__main__":
    main()
