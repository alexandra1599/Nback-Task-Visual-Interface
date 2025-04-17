import pygame
import random
import time
import pyautogui

# Initialize Pygame
pygame.init()

# Screen settings
# Screen settings
screen_tmp = pyautogui.size();
screen_width = screen_tmp[0];
screen_height = screen_tmp[1];

BACKGROUND_COLOR = (0, 0, 0)
GREEN_CROSS_COLOR = (0, 255, 0)
CROSS_COLOR = (255, 255, 255)
DOT_COLOR = (255, 255, 255)

CROSS_SIZE = 20
DOT_RADIUS = 10
FIXATION_TIME = 1  # Seconds
DOT_TIME = 1 # Seconds
RUNS = 15  # Number of repetitions
BLINK_TIME = 10  # Seconds

# Define positions
CENTER = (screen_width // 2, screen_height // 2)
DOT_POSITIONS = [
    (CENTER[0], CENTER[1] - 400),  # Top
    (CENTER[0], CENTER[1] + 400),  # Bottom
    (CENTER[0] - 400, CENTER[1]),  # Left
    (CENTER[0] + 400, CENTER[1])   # Right
]

# Create screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("EOG Calibration")
clock = pygame.time.Clock()

def draw_fixation_cross(color):
    """Draws a white fixation cross at the center of the screen."""
    pygame.draw.line(screen, color, (CENTER[0] - CROSS_SIZE, CENTER[1]), 
                     (CENTER[0] + CROSS_SIZE, CENTER[1]), 3)
    pygame.draw.line(screen, color, (CENTER[0], CENTER[1] - CROSS_SIZE), 
                     (CENTER[0], CENTER[1] + CROSS_SIZE), 3)

def draw_dot(position):
    """Draws a white dot at the specified position."""
    pygame.draw.circle(screen, DOT_COLOR, position, DOT_RADIUS)

def main():
    running = True
    num_repeats = RUNS // len(DOT_POSITIONS)  # Ensure even distribution
    dot_sequence = DOT_POSITIONS * num_repeats
    random.shuffle(dot_sequence)  # Shuffle order randomly
    
    for dot_position in dot_sequence:
        screen.fill(BACKGROUND_COLOR)
        draw_fixation_cross(CROSS_COLOR)
        pygame.display.flip()
        time.sleep(FIXATION_TIME)

        screen.fill(BACKGROUND_COLOR)
        draw_dot(dot_position)
        pygame.display.flip()
        time.sleep(DOT_TIME)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
      
            
            
    # Display green fixation cross for blinking phase
    screen.fill(BACKGROUND_COLOR)
    draw_fixation_cross(GREEN_CROSS_COLOR)
    pygame.display.flip()
    time.sleep(BLINK_TIME)
            
    

    pygame.quit()


if __name__ == "__main__":
    main()

