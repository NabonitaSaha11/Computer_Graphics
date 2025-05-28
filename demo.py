from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math


#dice_rolling = False
FOVY = 40
# Game Constants
GRID_SIZE = 10  # 10x10 grid
CELL_SIZE = 60  # Size of each grid cell
GRID_LENGTH = CELL_SIZE * GRID_SIZE  # Length of entire grid
PLAYER_SCALE = 2.0
SNAKE_SPEED_BASE = 0.5
SNAKE_SPEED_INCREMENT = 0.1
SNAKE_SPEED_INTERVAL = 20  # Seconds between speed increases
DICE_ROLL_DELAY = 20  # Frames between automated dice rolls
LADDER_HEIGHT = 80  # Height of ladders

# Window Dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

# Camera Settings
camera_mode = "default"  # or "follow"
camera_angle = 45
camera_height = 500
camera_radius = 800
camera_pos = (camera_radius * math.cos(math.radians(camera_angle)),
              camera_radius * math.sin(math.radians(camera_angle)),
              camera_height)

# Game State Variables
player_pos = [0, 0, 0]  # Starting position (x, y, z)
player_grid_pos = [0, 0]  # Grid position (row, col)
player_elevated = False
player_moving = False
player_move_frames = 0
player_move_steps = 0
player_move_target = None
player_lives = 3
player_angle = 0

snake_pos = [CELL_SIZE * 5, CELL_SIZE * 1, 0]  # Snake starts in the middle of the second row
snake_grid_pos = [1, 5]  # Snake grid position (row, col)
snake_direction = 0  # 0: up, 1: right, 2: down, 3: left
snake_speed = SNAKE_SPEED_BASE
snake_active = False
snake_timer = 0

dice_value = 0
dice_roll_timer = 0
dice_rolling = False

game_over = False
game_won = False
game_time = 0

# Ladders - format: [start_grid_x, start_grid_y, end_grid_x, end_grid_y]
ladders = [
    [1, 3, 3, 5],  # Ladder from (1,3) to (3,5)
    [2, 8, 4, 9],  # Ladder from (2,8) to (4,9)
    [5, 2, 7, 4],  # Ladder from (5,2) to (7,4)
    [6, 6, 8, 8],  # Ladder from (6,6) to (8,8)
    [0, 5, 2, 7]  # Ladder from (0,5) to (2,7)
]


def grid_to_world(grid_x, grid_y):
    """Convert grid coordinates to world coordinates"""
    return grid_x * CELL_SIZE, grid_y * CELL_SIZE


def world_to_grid(world_x, world_y):
    """Convert world coordinates to grid coordinates"""
    grid_x = int(world_x / CELL_SIZE)
    grid_y = int(world_y / CELL_SIZE)
    return grid_x, grid_y


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    """Draw text at screen position (x,y)"""
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


def draw_grid():
    """Draw the 10x10 game grid"""
    # Draw grid cells
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # Set color alternating between light blue and white
            if (row + col) % 2 == 0:
                glColor3f(0.8, 0.8, 1.0)  # Light blue
            else:
                glColor3f(1.0, 1.0, 1.0)  # White

            # Calculate world coordinates
            x, y = grid_to_world(row, col)

            # Draw cell as quad
            z_platform = -7
            glBegin(GL_QUADS)
            glVertex3f(x, y, z_platform)
            glVertex3f(x + CELL_SIZE, y, z_platform)
            glVertex3f(x + CELL_SIZE, y + CELL_SIZE, z_platform)
            glVertex3f(x, y + CELL_SIZE, z_platform)
            glEnd()

            # Draw cell number
            glColor3f(0.2, 0.2, 0.2)
            cell_number = row * GRID_SIZE + col + 1
            glRasterPos3f(x + CELL_SIZE / 2 - 5, y + CELL_SIZE / 2, 0.1)
            for ch in str(cell_number):
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))


def draw_ladders():
    """Draw ladders on the grid"""
    for ladder in ladders:
        start_x, start_y = grid_to_world(ladder[0], ladder[1])
        end_x, end_y = grid_to_world(ladder[2], ladder[3])

        # Draw ladder base (starting position)
        # glColor3f(0.6, 0.4, 0.2)  # Brown color for ladder base
        # glPushMatrix()
        # glTranslatef(start_x + CELL_SIZE / 2, start_y + CELL_SIZE / 2, 0)
        # glutSolidCube(20)
        # glPopMatrix()

        # Draw ladder top (ending position)
        glColor3f(0.8, 0.6, 0.3)  # Lighter brown for ladder top
        glPushMatrix()
        glTranslatef(end_x + CELL_SIZE / 2, end_y + CELL_SIZE / 2, LADDER_HEIGHT)
        glutSolidCube(20)
        glPopMatrix()

        # Draw ladder rungs
        glColor3f(0.7, 0.5, 0.3)  # Medium brown for ladder rungs

        # Draw vertical supports
        glPushMatrix()
        glTranslatef(end_x + CELL_SIZE / 2 - 10, end_y + CELL_SIZE / 2 - 10, LADDER_HEIGHT / 2)
        glScalef(5, 5, LADDER_HEIGHT)
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(end_x + CELL_SIZE / 2 + 10, end_y + CELL_SIZE / 2 + 10, LADDER_HEIGHT / 2)
        glScalef(5, 5, LADDER_HEIGHT)
        glutSolidCube(1)
        glPopMatrix()

        # Draw horizontal rungs
        for i in range(1, 5):
            height = LADDER_HEIGHT * i / 5
            glPushMatrix()
            glTranslatef(end_x + CELL_SIZE / 2, end_y + CELL_SIZE / 2, height)
            glScalef(30, 30, 3)
            glutSolidCube(1)
            glPopMatrix()


def draw_player():
    """Draw the player character"""
    glPushMatrix()

    # Position player
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(player_angle, 0, 0, 1)

    # Body
    glColor3f(0.2, 0.4, 0.8)  # Blue
    glPushMatrix()
    glTranslatef(0, 0, 10 * PLAYER_SCALE)
    glScalef(10 * PLAYER_SCALE, 10 * PLAYER_SCALE, 20 * PLAYER_SCALE)
    glutSolidCube(1)
    glPopMatrix()

    # Head
    glColor3f(0.8, 0.6, 0.5)  # Skin tone
    glPushMatrix()
    glTranslatef(0, 0, 30 * PLAYER_SCALE)
    glutSolidSphere(7 * PLAYER_SCALE, 20, 20)
    glPopMatrix()

    # Arms
    glColor3f(0.2, 0.4, 0.8)  # Blue

    # Left arm
    glPushMatrix()
    glTranslatef(-12 * PLAYER_SCALE, 0, 15 * PLAYER_SCALE)
    glScalef(5 * PLAYER_SCALE, 5 * PLAYER_SCALE, 10 * PLAYER_SCALE)
    glutSolidCube(1)
    glPopMatrix()

    # Right arm
    glPushMatrix()
    glTranslatef(12 * PLAYER_SCALE, 0, 15 * PLAYER_SCALE)
    glScalef(5 * PLAYER_SCALE, 5 * PLAYER_SCALE, 10 * PLAYER_SCALE)
    glutSolidCube(1)
    glPopMatrix()

    # Legs
    glColor3f(0.3, 0.3, 0.7)  # Darker blue

    # Left leg
    glPushMatrix()
    glTranslatef(-6 * PLAYER_SCALE, 0, 0)
    glScalef(6 * PLAYER_SCALE, 6 * PLAYER_SCALE, 10 * PLAYER_SCALE)
    glutSolidCube(1)
    glPopMatrix()

    # Right leg
    glPushMatrix()
    glTranslatef(6 * PLAYER_SCALE, 0, 0)
    glScalef(6 * PLAYER_SCALE, 6 * PLAYER_SCALE, 10 * PLAYER_SCALE)
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()


def draw_snake():
    """Draw the snake enemy"""
    if not snake_active:
        return

    glPushMatrix()

    # Position snake
    glTranslatef(snake_pos[0], snake_pos[1], snake_pos[2])

    # Draw snake body segments
    num_segments = 5

    # Head
    glColor3f(0.1, 0.6, 0.1)  # Dark green
    glPushMatrix()
    glTranslatef(0, 0, 15)
    glutSolidSphere(15, 20, 20)

    # Eyes
    glColor3f(1, 1, 0)  # Yellow eyes
    glTranslatef(8, 8, 5)
    glutSolidSphere(3, 10, 10)
    glTranslatef(-16, 0, 0)
    glutSolidSphere(3, 10, 10)
    glPopMatrix()

    # Body segments
    glColor3f(0.2, 0.8, 0.2)  # Lighter green
    for i in range(num_segments):
        offset = -25 * i
        # Calculate position based on snake direction
        if snake_direction == 0:  # Up
            segment_x = 0
            segment_y = offset
        elif snake_direction == 1:  # Right
            segment_x = offset
            segment_y = 0
        elif snake_direction == 2:  # Down
            segment_x = 0
            segment_y = -offset
        else:  # Left
            segment_x = -offset
            segment_y = 0

        glPushMatrix()
        glTranslatef(segment_x, segment_y, 10)
        glTranslatef(segment_x, segment_y, 10)
        glutSolidSphere(12 - i, 20, 20)
        glPopMatrix()

    glPopMatrix()


def draw_dice():
    """Draw the current dice value"""
    # Draw dice in top-right corner of the screen
    glPushMatrix()
    glTranslatef(WINDOW_WIDTH - 80, WINDOW_HEIGHT - 80, 0)
    glColor3f(1, 1, 1)  # White dice

    if dice_rolling:
        # Show animated dice
        random_roll = (game_time // 5) % 6 + 1
        draw_text(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 50, f"Rolling... {random_roll}")
    else:
        # Show fixed dice value
        draw_text(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 50, f"Dice: {dice_value}")

    glPopMatrix()


# def roll_dice():
#     """Roll the dice to get a random value from 1-6"""
#     global dice_value, dice_rolling, dice_roll_timer
#
#     if dice_rolling:
#         dice_roll_timer -= 1
#         if dice_roll_timer <= 0:
#             dice_rolling = False
#             dice_value = random.randint(1, 6)
#             move_player(dice_value)
#     else:
#         dice_rolling = True
#         dice_roll_timer = 30  # Roll for 30 frames
#     #print(dice_roll_timer)

def roll_dice():
    """Roll the dice to get a random value from 1-6"""
    global dice_value, dice_rolling, dice_roll_timer

    if not dice_rolling and not player_moving:
        # Start rolling animation
        dice_rolling = True
        dice_roll_timer = 30  # Roll for 30 frames
    elif dice_rolling:
        # Already rolling, let the animation continue in the idle function
        pass

def move_player(steps):
    """Move the player forward by the given number of steps"""
    global player_moving, player_move_steps, player_grid_pos, player_move_target

    if player_moving:
        return

    player_moving = True
    player_move_steps = steps

    # Calculate target position based on snake and ladder game movement pattern
    current_pos = player_grid_pos[0] * GRID_SIZE + player_grid_pos[1]
    target_pos = min(current_pos + steps, GRID_SIZE * GRID_SIZE - 1)  # Cap at final position

    # Convert to row, col using snake pattern (alternating left-to-right and right-to-left)
    target_row = target_pos // GRID_SIZE
    if target_row % 2 == 0:
        # Even row, moving left to right
        target_col = target_pos % GRID_SIZE
    else:
        # Odd row, moving right to left
        target_col = GRID_SIZE - 1 - (target_pos % GRID_SIZE)

    # Set target position
    player_move_target = [target_row, target_col]


def update_player_movement():
    """Update player movement animation"""
    global player_moving, player_move_frames, player_grid_pos, player_pos, player_elevated, player_move_target

    if not player_moving:
        return

    # Calculate next grid position
    current_pos = player_grid_pos[0] * GRID_SIZE + player_grid_pos[1]
    target_pos = player_move_target[0] * GRID_SIZE + player_move_target[1]

    if current_pos == target_pos:
        player_moving = False
        check_ladder_collision()
        return

    # Move one step at a time (could be improved for smoother movement)
    next_pos = current_pos + 1
    next_row = next_pos // GRID_SIZE

    if next_row % 2 == 0:
        # Even row, moving left to right
        next_col = next_pos % GRID_SIZE
    else:
        # Odd row, moving right to left
        next_col = GRID_SIZE - 1 - (next_pos % GRID_SIZE)

    # Update player grid position
    player_grid_pos = [next_row, next_col]

    # Update player world position
    world_x, world_y = grid_to_world(next_row, next_col)
    player_pos = [world_x + CELL_SIZE / 2, world_y + CELL_SIZE / 2, player_pos[2]]

    # If player was elevated and moving to a new position, check if they need to come down
    if player_elevated:
        on_ladder_top = False
        for ladder in ladders:
            if ladder[2] == player_grid_pos[0] and ladder[3] == player_grid_pos[1]:
                on_ladder_top = True
                break

        if not on_ladder_top:
            player_elevated = False
            player_pos[2] = 0  # Back to ground level


def check_ladder_collision():
    """Check if player is on a ladder and update position accordingly"""
    global player_pos, player_elevated

    # Check for ladder start positions
    for ladder in ladders:
        if ladder[0] == player_grid_pos[0] and ladder[1] == player_grid_pos[1]:
            # Player is at the bottom of a ladder
            player_grid_pos[0] = ladder[2]  # Update to ladder top position
            player_grid_pos[1] = ladder[3]

            # Update world position
            world_x, world_y = grid_to_world(ladder[2], ladder[3])
            player_pos = [world_x + CELL_SIZE / 2, world_y + CELL_SIZE / 2, LADDER_HEIGHT]
            player_elevated = True
            return

    # Check if player is already at the top of a ladder
    for ladder in ladders:
        if ladder[2] == player_grid_pos[0] and ladder[3] == player_grid_pos[1]:
            player_pos[2] = LADDER_HEIGHT
            player_elevated = True
            return


def update_snake():
    """Update snake position and behavior"""
    global snake_pos, snake_grid_pos, snake_direction, snake_active, snake_timer, snake_speed

    # Activate snake only after player reaches the second row
    if not snake_active and player_grid_pos[0] >= 1:
        snake_active = True

    if not snake_active:
        return

    # Update snake speed periodically
    snake_timer += 1
    if snake_timer >= SNAKE_SPEED_INTERVAL * 60:  # 60 frames per second
        snake_speed += SNAKE_SPEED_INCREMENT
        snake_timer = 0

    # Move snake in random directions
    if random.random() < snake_speed / 60:  # Probability based on speed
        # Choose a new random direction
        possible_directions = []

        # Check which directions are valid (within grid)
        if snake_grid_pos[0] > 0:  # Can move up
            possible_directions.append(0)
        if snake_grid_pos[1] < GRID_SIZE - 1:  # Can move right
            possible_directions.append(1)
        if snake_grid_pos[0] < GRID_SIZE - 1:  # Can move down
            possible_directions.append(2)
        if snake_grid_pos[1] > 0:  # Can move left
            possible_directions.append(3)

        if possible_directions:
            snake_direction = random.choice(possible_directions)

            # Update snake grid position based on direction
            if snake_direction == 0:  # Up
                snake_grid_pos[0] -= 1
            elif snake_direction == 1:  # Right
                snake_grid_pos[1] += 1
            elif snake_direction == 2:  # Down
                snake_grid_pos[0] += 1
            else:  # Left
                snake_grid_pos[1] -= 1

            # Update snake world position
            world_x, world_y = grid_to_world(snake_grid_pos[0], snake_grid_pos[1])
            snake_pos = [world_x + CELL_SIZE / 2, world_y + CELL_SIZE / 2, 0]


def check_snake_collision():
    global player_elevated
    """Check if snake collides with player"""
    global player_lives, game_over, player_grid_pos, player_pos

    if not snake_active or player_elevated:
        return

    # Check if snake and player are on the same grid cell
    if snake_grid_pos[0] == player_grid_pos[0] and snake_grid_pos[1] == player_grid_pos[1]:
        player_lives -= 1

        if player_lives <= 0:
            game_over = True
        else:
            # Reset player to starting position
            player_grid_pos = [0, 0]
            world_x, world_y = grid_to_world(0, 0)
            player_pos = [world_x + CELL_SIZE / 2, world_y + CELL_SIZE / 2, 0]
            player_elevated = False


def check_win_condition():
    """Check if player has reached the final cell"""
    global game_won

    if player_grid_pos[0] == GRID_SIZE - 1 and player_grid_pos[1] == GRID_SIZE - 1:
        game_won = True

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
        # cx = camera_radius * math.cos(math.radians(camera_angle))
        # cy = camera_radius * math.sin(math.radians(camera_angle))
        target_x = GRID_LENGTH / 2
        target_y = GRID_LENGTH / 2

        cx = target_x + camera_radius * math.cos(math.radians(camera_angle))
        cy = target_y + camera_radius * math.sin(math.radians(camera_angle))

        gluLookAt(cx, cy, camera_height,
                  target_x, target_y, 0,
                  0, 0, 1)
# def setupCamera():
#     """Configure the camera view"""
#     global camera_pos, camera_angle, camera_height
#
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     gluPerspective(120, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 1500)
#     glMatrixMode(GL_MODELVIEW)
#     glLoadIdentity()
#
#     if camera_mode == "follow":
#         # Camera follows player
#         look_x = player_pos[0]
#         look_y = player_pos[1]
#         look_z = player_pos[2]
#
#         # Position camera behind player
#         camera_dist = 200
#         camera_x = look_x - camera_dist * math.cos(math.radians(player_angle))
#         camera_y = look_y - camera_dist * math.sin(math.radians(player_angle))
#         camera_z = look_z + 150
#
#         gluLookAt(camera_x, camera_y, camera_z,
#                   look_x, look_y, look_z,
#                   0, 0, 1)
#     else:
#         # Top-down isometric view
#         cx = camera_radius * math.cos(math.radians(camera_angle))
#         cy = camera_radius * math.sin(math.radians(camera_angle))
#         gluLookAt(cx, cy, camera_height,
#                   #0, 0, 0,
#                   GRID_LENGTH, GRID_LENGTH, 0,
#                   0, 0, 1)


def keyboardListener(key, x, y):
    """Handle keyboard input"""
    global player_angle, camera_mode, game_over, game_won, player_lives, player_grid_pos, player_pos, player_elevated

    if game_over or game_won:
        # Reset game if R is pressed
        if key == b'r':
            reset_game()
        return

    # Roll dice with space bar
    if key == b' ':
        roll_dice()

    # Toggle camera mode
    if key == b'c':
        camera_mode = "follow" if camera_mode == "default" else "default"


def specialKeyListener(key, x, y):
    """Handle special key input (arrow keys)"""
    global camera_angle, camera_height

    if key == GLUT_KEY_UP:
        camera_height += 10
    elif key == GLUT_KEY_DOWN:
        camera_height -= 10
    elif key == GLUT_KEY_LEFT:
        camera_angle += 5
    elif key == GLUT_KEY_RIGHT:
        camera_angle -= 5


def mouseListener(button, state, x, y):
    """Handle mouse input"""
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        roll_dice()


def reset_game():
    """Reset the game state"""
    global player_pos, player_grid_pos, player_elevated, player_lives
    global snake_pos, snake_grid_pos, snake_active, snake_speed, snake_timer
    global dice_value, dice_rolling, dice_roll_timer
    global game_over, game_won, game_time

    # Reset player
    player_grid_pos = [0, 0]
    world_x, world_y = grid_to_world(0, 0)
    player_pos = [world_x + CELL_SIZE / 2, world_y + CELL_SIZE / 2, 0]
    player_elevated = False
    player_lives = 3

    # Reset snake
    snake_grid_pos = [1, 5]
    world_x, world_y = grid_to_world(1, 5)
    snake_pos = [world_x + CELL_SIZE / 2, world_y + CELL_SIZE / 2, 0]
    snake_active = False
    snake_speed = SNAKE_SPEED_BASE
    snake_timer = 0

    # Reset game state
    dice_value = 0
    dice_rolling = False
    dice_roll_timer = 5
    game_over = False
    game_won = False
    game_time = 0


# def idle():
#     """Idle function for animation"""
#     global game_time, dice_roll_timer
#
#     game_time += 1
#
#     if not game_over and not game_won:
#         # Update game state
#         update_player_movement()
#         update_snake()
#         check_snake_collision()
#         check_win_condition()
#
#         #Auto roll dice if player is not moving
#         if not player_moving and dice_rolling:
#             dice_roll_timer += 1
#             if dice_roll_timer >= DICE_ROLL_DELAY:
#                 roll_dice()
#                 dice_roll_timer = 0
#
#     glutPostRedisplay()

def idle():
    """Idle function for animation"""
    global game_time, dice_roll_timer, dice_rolling, dice_value

    game_time += 1

    if not game_over and not game_won:
        # Update game state
        update_player_movement()
        update_snake()
        check_snake_collision()
        check_win_condition()

        # Handle dice rolling animation
        if dice_rolling:
            dice_roll_timer -= 1
            if dice_roll_timer <= 0:
                # Finish rolling and move player
                dice_rolling = False
                dice_value = random.randint(1, 6)
                move_player(dice_value)

        # Auto roll dice if player is not moving and dice is not currently rolling
        # elif not player_moving and not dice_rolling:
        #     # This part is optional - only needed if you want automatic rolling after some delay
        #     dice_roll_timer += 1
        #     if dice_roll_timer >= DICE_ROLL_DELAY:
        #         roll_dice()
        #         dice_roll_timer = 0

    glutPostRedisplay()

def showScreen():
    """Display function to render the game"""
    global game_time

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

    setupCamera()

    # Draw game elements
    draw_grid()
    draw_ladders()
    draw_player()
    #draw_snake()
    draw_dice()

    # Draw game information
    draw_text(10, 770, f"Lives: {player_lives}")
    draw_text(10, 750, f"Position: {player_grid_pos[0]}, {player_grid_pos[1]}")
    draw_text(10, 730, f"Time: {game_time // 60}")

    if game_over:
        draw_text(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2, "GAME OVER", font=GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(WINDOW_WIDTH / 2 - 150, WINDOW_HEIGHT / 2 - 30, "Press 'R' to restart", font=GLUT_BITMAP_HELVETICA_18)

    if game_won:
        draw_text(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2, "YOU WIN!", font=GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(WINDOW_WIDTH / 2 - 150, WINDOW_HEIGHT / 2 - 30, "Press 'R' to restart", font=GLUT_BITMAP_HELVETICA_18)

    glutSwapBuffers()


def main():
    """Main function to initialize and run the game"""
    global player_pos, player_grid_pos

    # Initialize GLUT
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"3D Snake and Ladder Adventure")

    # Enable depth testing
    glEnable(GL_DEPTH_TEST)

    # Initialize player position
    world_x, world_y = grid_to_world(0, 0)
    player_pos = [world_x + CELL_SIZE / 2, world_y + CELL_SIZE / 2, 0]

    # Register callback functions
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    # Start the game loop
    glutMainLoop()


if __name__ == "__main__":
    main()