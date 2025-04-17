import pygame
import random
import time
import socket
#from pylsl import StreamInfo, StreamOutlet

# Press M : yes , Z : no

# Initialize pygame
pygame.init()

# Screen settings
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Visuospatial N-back Task")

# Set up fonts
font = pygame.font.SysFont('Arial', 50)
letter_font = pygame.font.SysFont('Arial', 100)

# Setup UDP
#udp_marker = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
#message1 = "Trial Start"
#message2 = "Button Press Match"
#message3 = "Button Press Nomatch"
#message4 = "Time out"
#message5 = "Trial End"
#ip = '127.0.0.1'
#port = 12345

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# List of possible letters
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

# N-back level
N = 2  # Change to your desired N level

# Set up LSL stream
#info = StreamInfo('NBackMarkers', 'Markers', 1, 0, 'string', 'visual_nback_task_001')
#outlet = StreamOutlet(info)


# Function to display text
def display_text(text, font, color, position, duration=None):
    screen.fill(BLACK)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=position)
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    if duration:
        time.sleep(duration)

# Function to draw fixation cross
def draw_fixation_cross(duration):
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < duration:
        screen.fill(BLACK)
        center = (screen_width // 2, screen_height // 2)
        line_width = 5
        pygame.draw.line(screen, WHITE, (center[0] - 20, center[1]), (center[0] + 20, center[1]), line_width)
        pygame.draw.line(screen, WHITE, (center[0], center[1] - 20), (center[0], center[1] + 20), line_width)
        pygame.display.flip()

# Function to get random peripheral positions
def get_random_position():
    positions = [
        (100, 100), (screen_width - 100, 100), (100, screen_height - 100), (screen_width - 100, screen_height - 100),
        (screen_width // 2, 100), (screen_width // 2, screen_height - 100), (100, screen_height // 2), (screen_width - 100, screen_height // 2)
    ]
    return random.choice(positions)

# Main function
def run_nback_task(version=1):
    sequence = []
    correct_responses = 0
    total_trials = 10
    trial = 0

    # Display "Press any key to start"
    display_text("Press any key to start", font, WHITE, (screen_width // 2, screen_height // 2), 0)
    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting_for_start = False

    while trial < total_trials:
        # Randomly choose a letter and position
        letter = random.choice(letters)
        position = get_random_position()
        sequence.append((letter, position))

        # Display the letter for 1s
        start_time = time.time()
        #send udp command for trial start
        #udp_marker.sendto(message1.encode('utf-8'),(ip,port))
        display_text(letter, letter_font, WHITE, position, duration=1)

        # Display fixation cross for 1500 ms (ISI)
        draw_fixation_cross(1.5)

        if len(sequence) > N:
            correct_letter, correct_position = sequence[-(N + 1)]
            current_letter, current_position = sequence[-1]

            # Scoring logic based on version
            if version == 1:  # Match letters only
                is_match = (current_letter == correct_letter)
            elif version == 2:  # Match letters and positions
                is_match = (current_letter == correct_letter and current_position == correct_position)

            response_time = pygame.time.get_ticks()
            response = None

            while response is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_e:  # Exit the game if 'E' is pressed
                            pygame.quit()
                            exit()
                        if event.key == pygame.K_m:  # M key for Yes
                            response = 'y'  # Yes (match)
                            #send udp command for response
                            #udp_marker.sendto(message2.encode('utf-8'),(ip,port))
                        elif event.key == pygame.K_z:  # Z key for No
                            response = 'n'  # No (no match)
                            #send udp command for response
                            #udp_marker.sendto(message3.encode('utf-8'),(ip,port))

                # Check for timeout (1 second to respond)
                if pygame.time.get_ticks() - response_time > 1000:
                    response = 'timeout'

            # Check response correctness
            if response != 'timeout':
                if (response == 'y' and is_match) or (response == 'n' and not is_match):
                    correct_responses += 1

        trial += 1
        #send udp command for trial end 
        #udp_marker.sendto(message5.encode('utf-8'),(ip,port))

    # Show final score
    display_text(f'You got {correct_responses} out of {total_trials} correct!', font, WHITE, (screen_width // 2, screen_height // 2), 3)
    pygame.quit()

# Ask the user for the version before starting
version_choice = input("Enter '1' for matching letters only or '2' for matching letters and positions: ")
version = 1 if version_choice == '1' else 2

# Run the N-back task
if __name__ == "__main__":
    run_nback_task(version)
