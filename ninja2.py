import pygame
import sys
import random

# Initialize Pygame once at the very beginning of the script.
# This ensures all Pygame modules (like font) are ready before being used.
pygame.init()

class ninja(object):
    def __init__(self):
        self.length = 1
        self.positions = [(Width // 2, Height // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = Blue

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        # Prevent turning 180 degrees into itself if length > 1
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        current = self.get_head_position()
        x, y = self.direction
        # Calculate new position, wrapping around the screen
        new = (((current[0] + (x * grid_size)) % Width), (current[1] + (y * grid_size)) % Height)

        # Check for self-collision (if the head hits any part of its body except the immediate next segment)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset() # Reset the game if collision occurs
        else:
            self.positions.insert(0, new) # Add new head position
            if len(self.positions) > self.length:
                self.positions.pop() # Remove tail if length exceeds current limit

    def reset(self):
        # Reset ninja to initial state
        self.length = 1
        self.positions = [(Width // 2, Height // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        # Draw each segment of the ninja
        for pos in self.positions:
            rect = pygame.Rect((pos[0], pos[1]), (grid_size, grid_size))
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, black, rect, 1)  # Draw border for segments

    def handle_keys(self):
        # Event handling for player input (keyboard and quitting)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)


class enemy(object):
    def __init__(self):
        self.position = (0, 0)
        self.color = red
        self.randomize_position() # Place enemy randomly on creation

    def randomize_position(self):
        # Place the enemy at a random grid position
        self.position = (random.randint(0, gridwidth - 1) * grid_size, random.randint(0, gridheight - 1) * grid_size)

    def draw(self, surface):
        # Draw the enemy
        rect = pygame.Rect(self.position[0], self.position[1], grid_size, grid_size)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, black, rect, 1)

def drawgrid(surface):
    # Draws a checkerboard grid pattern on the surface
    for y in range(0, int(gridheight)):
        for x in range(0, int(gridwidth)):
            if ((x + y) % 2) == 0:
                rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
                pygame.draw.rect(surface, gray1, rect)
            else:
                rect = pygame.Rect(x * grid_size, y * grid_size, grid_size, grid_size)
                pygame.draw.rect(surface, gray2, rect)

# --- Game Variables Library ---
# Screen dimensions and grid settings
Width = 800
Height = 600
grid_size = 20 # Size of each 'block' in pixels
gridwidth = Width // grid_size
gridheight = Height // grid_size

# Color definitions (RGB tuples)
gray1 = (120, 120, 120)
gray2 = (200, 200, 200)
Blue = (0, 0, 255)
black = (0, 0, 0)
red = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230) # New background color

# Direction vectors
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Font for displaying text (like score).
# Assumes 'freesansbold.ttf' is in the same directory, or use None for default font.
font = pygame.font.Font('freesansbold.ttf', 30)

def main():
    clock = pygame.time.Clock() # Manages game timing
    screen = pygame.display.set_mode((Width, Height)) # Set up the display window

    surface = pygame.Surface(screen.get_size()) # Create a surface to draw on
    surface = surface.convert() # Optimize surface for faster blitting

    ninja_obj = ninja() # Create the ninja object
    enemy_obj = enemy() # Create the enemy object

    score = 0 # Initialize player score

    # --- NEW VARIABLES FOR SPEED CONTROL (within main) ---
    ninja_speed = 10  # Controls how often the ninja moves.
                      # A higher number means the ninja moves every 'ninja_speed' frames.
                      # At 60 FPS, ninja_speed = 10 means 6 moves per second.
                      # ninja_speed = 1 means it moves every frame (fastest).
    move_counter = 0  # Counter to track frames until the next ninja move.

    # --- Main Game Loop ---
    while True:
        # Limit frame rate to 60 frames per second.
        # This keeps the game running smoothly regardless of CPU speed.
        clock.tick(60)

        # Handle keyboard input and quit events.
        ninja_obj.handle_keys()

        # --- SPEED CONTROL LOGIC FOR NINJA MOVEMENT ---
        move_counter += 1 # Increment the counter each frame
        if move_counter >= ninja_speed:
            ninja_obj.move() # Only call move() when the counter reaches the desired speed
            # Check for collision immediately after the ninja moves
            if ninja_obj.get_head_position() == enemy_obj.position:
                ninja_obj.length += 1 # Increase ninja length
                score += 1 # Increase score
                enemy_obj.randomize_position() # Place new enemy
            move_counter = 0 # Reset the counter for the next movement cycle

        # --- Drawing Operations ---
        # Fill the entire surface with the chosen background color each frame
        surface.fill(LIGHT_BLUE)

        # Optionally draw the grid on top of the background.
        # Uncomment the line below if you want the checkerboard grid.
        # drawgrid(surface)

        # Draw the ninja and enemy
        ninja_obj.draw(surface)
        enemy_obj.draw(surface)

        # Render and display the score
        text = font.render("score {0}".format(score), True, black)
        surface.blit(text, (5, 10))

        # Update the entire screen to show what has been drawn on the 'surface'
        screen.blit(surface, (0, 0))
        pygame.display.update()

# Ensures main() runs only when the script is executed directly
if __name__ == "__main__":
    main()