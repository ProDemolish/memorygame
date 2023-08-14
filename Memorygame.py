import pygame
import random

pygame.init()

# Screen properties
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)
LEFT_MARGIN = 35

# Button properties
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
BUTTON_X = (SCREEN_WIDTH - BUTTON_WIDTH) // 2
BUTTON_Y = SCREEN_HEIGHT - 70  # Positioned 70 pixels from the bottom
BUTTON_COLOR = (50, 150, 50)
BUTTON_TEXT_COLOR = (255, 255, 255)
FONT = pygame.font.SysFont('Arial', 20)

# Card properties
CARD_SIZE = 100
SPACING = 10
GRID_SIZE = 4

# Load and prepare the images
# Place your images in the specified location
images = [pygame.transform.scale(pygame.image.load(f"Icons\\{i + 1}.jpg"), (CARD_SIZE, CARD_SIZE)) for i in
          range(GRID_SIZE * GRID_SIZE // 2)]
images *= 2  # Double the images for pairs
random.shuffle(images)

# Create a screen/window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Memory Matching Game")

# Initialization
revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
matched = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
first_card = None
hide_on_next_click = None


# Function to reset the game
def reset_game():
    global images, revealed, matched, first_card, hide_on_next_click
    random.shuffle(images)
    revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    matched = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    first_card = None
    hide_on_next_click = None


# Game loop
running = True
while running:
    screen.fill(BACKGROUND_COLOR)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Check if the reset button was clicked
            if BUTTON_X <= x <= BUTTON_X + BUTTON_WIDTH and BUTTON_Y <= y <= BUTTON_Y + BUTTON_HEIGHT:
                reset_game()
                continue

            col = x // (CARD_SIZE + SPACING)
            row = y // (CARD_SIZE + SPACING)


            # If there are cards to hide, hide them first
            if hide_on_next_click:
                revealed[hide_on_next_click[0][0]][hide_on_next_click[0][1]] = False
                revealed[hide_on_next_click[1][0]][hide_on_next_click[1][1]] = False
                hide_on_next_click = None
                first_card = None

            # If the clicked card is already revealed, hide it
            elif revealed[row][col]:
                revealed[row][col] = False
                if first_card == (row, col):
                    first_card = None

            # If the card is not matched and not revealed
            elif not matched[row][col]:
                if not first_card:
                    first_card = (row, col)
                    revealed[row][col] = True
                else:
                    revealed[row][col] = True
                    if images[first_card[1] + first_card[0] * GRID_SIZE] != images[col + row * GRID_SIZE]:
                        hide_on_next_click = [first_card, (row, col)]
                    else:
                        matched[row][col] = True
                        matched[first_card[0]][first_card[1]] = True
                        first_card = None

    # Drawing logic

    # Draw the cards
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            card_x = LEFT_MARGIN + col * (CARD_SIZE + SPACING)
            card_y = row * (CARD_SIZE + SPACING)
            if revealed[row][col]:
                screen.blit(images[col + row * GRID_SIZE], (card_x, card_y))
            else:
                pygame.draw.rect(screen, (50, 150, 50), (card_x, card_y, CARD_SIZE, CARD_SIZE))

    # Draw the reset button
    pygame.draw.rect(screen, BUTTON_COLOR, (BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT))
    text = FONT.render("Reset Game", True, BUTTON_TEXT_COLOR)
    screen.blit(text, (
    BUTTON_X + (BUTTON_WIDTH - text.get_width()) // 2, BUTTON_Y + (BUTTON_HEIGHT - text.get_height()) // 2))

    pygame.display.flip()

pygame.quit()