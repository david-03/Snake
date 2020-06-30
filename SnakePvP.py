import pygame
from random import randint

# Length in pixels of each square
BOX = 32
# Colors used
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 160, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

# Default grid dimensions
num_col = 17
num_row = 15
# Width and Height of the game grid in pixels
game_w = num_col * BOX
game_h = num_row * BOX
# Width and Height of the window in pixels (changes depending on window mode)
win_width = game_w
win_height = game_h + 75
# Initial apple position
applec = 3 * num_col // 4
appler = num_row // 2

# Initialize pygame
pygame.init()
# Create fonts
FONT = pygame.font.SysFont('comicsans', 30)
FONT_50 = pygame.font.SysFont('comicsans', 50)


# Drawing the grid
def grid(win):
    # Grid dimensions depend on window size
    w, h = win.get_size()
    x = w / 2 - game_w / 2
    y = (h - 75) / 2 - game_h / 2
    # Draw a rectangle which is the outline of the entire game grid
    r1 = pygame.Rect((int(x), int(y)), (game_w, game_h))
    pygame.draw.rect(win, (255, 255, 255), r1, 1)

    # Draw a rectangle for every two columns (one rectangle = two lines = two columns drawn)
    for n in range(1, num_col // 2 + 1):
        r_x = x + (2 * n - 1) * BOX
        r_n = pygame.Rect((int(r_x), int(y)), (BOX, game_h))
        pygame.draw.rect(win, (255, 255, 255), r_n, 1)

    # Draw a rectangle for every two rows (one rectangle = two lines = two rows drawn)
    for n in range(1, num_row // 2 + 1):
        r_y = y + (2 * n - 1) * BOX
        r_n = pygame.Rect((int(x), int(r_y)), (game_w, BOX))
        pygame.draw.rect(win, (255, 255, 255), r_n, 1)


# General function for drawing a solid square based on column and row alone (no need to calculate pixels every time)
def square(win, color, col, row, width=0):
    w, h = win.get_size()
    x = w / 2 - game_w / 2
    y = (h - 75) / 2 - game_h / 2
    # Important to put int(x) and int(y) to round them to the nearest integer (pixel number)
    square1 = pygame.Rect((int(x) + col * BOX, int(y) + row * BOX), (BOX, BOX))
    pygame.draw.rect(win, color, square1, width)


# Draw the window
def draw(win):
    win.fill(BLACK)
    grid(win)


# Create a class for the snake object (every snake has the same attributes)
class Snake:
    # Declare the attributes that each snake has
    def __init__(self, start_col, start_row, color):
        # Snake body is a list that contains the position of each body part as tuples (column, row)
        self.body = [(start_col, start_row), (start_col - 1, start_row), (start_col - 2, start_row)]
        # Dictionary that stores the position at which each body part has to turn and the turn itself
        # (column, row) = (right, left, up or down)
        self.turns = {}
        # Each body part has a speed on the x axis and on the y axis
        # Index of speeds is the same as index of body parts
        self.speed_x = [0, 0, 0]
        self.speed_y = [0, 0, 0]
        # Temporary variable that stores the turn at one precise moment
        self.dir = 0
        # Snakes have different colors
        self.color = color

    # Moving the snake by one box
    def move_snake(self):
        # For each body part on the snake
        for i in range(len(self.body)):
            # Reverse the order to move tail first, in order to remove turns that are not in body anymore
            ind = -i - 1
            (col, row) = self.body[ind]
            # Check if the body part position corresponds to a turn
            if (col, row) in self.turns.keys():
                # Get the turn and change speed accordingly
                self.dir = self.turns.get((col, row))
                if self.dir == 'r':
                    self.speed_x[ind] = 1
                    self.speed_y[ind] = 0
                if self.dir == 'l':
                    self.speed_x[ind] = -1
                    self.speed_y[ind] = 0
                if self.dir == 'u':
                    self.speed_x[ind] = 0
                    self.speed_y[ind] = -1
                if self.dir == 'd':
                    self.speed_x[ind] = 0
                    self.speed_y[ind] = 1

            # Change position of body part based on speed
            col += self.speed_x[ind]
            row += self.speed_y[ind]
            self.body[ind] = (col, row)

            # Delete turns that are gone (turns that are outside of the snake body)
            for (col, row) in list(self.turns):
                if (col, row) not in self.body:
                    self.turns.pop((col, row))

    # Draw a square for every body part of the snake
    def draw_snake(self, win):
        for (col, row) in self.body:
            square(win, self.color, col, row)

    # Check if snake lost (boolean function -> if snake dies, returns True, otherwise, False)
    def lose(self):
        # Check if snake head is outside of game grid
        (col, row) = self.body[0]
        if (col, row) in self.body[1:]:
            return True
        if col < 0 or row < 0 or col >= num_col or row >= num_row:
            return True
        # Default return value of function
        return False

    # Check collision between snake head and apple (boolean function)
    def check_eat(self, win):
        # Get window dimensions
        w, h = win.get_size()
        x = w / 2 - game_w / 2
        y = (h - 75) / 2 - game_h / 2
        # Get snake head position
        (col, row) = self.body[0]
        # Get rectangles that represent the snake head and the apple
        head = pygame.Rect((int(x) + col * BOX, int(y) + row * BOX), (BOX, BOX))
        apple1 = pygame.Rect((int(x) + applec * BOX, int(y) + appler * BOX), (BOX, BOX))
        # If the two rectangles overlap, there is collision
        if head.colliderect(apple1):
            # Add one body part to the tail depending on the tail's current speed
            (col, row) = self.body[-1]
            # Add new tail one square behind current tail
            self.body.append((col - self.speed_x[-1], row - self.speed_y[-1]))
            # Add the current tail speed at the end of the speed list for the new tail
            self.speed_x.append(self.speed_x[-1])
            self.speed_y.append(self.speed_y[-1])
            return True
        # If no collision, function returns False
        return False


# Create new apple
def apple(win, body1, body2):
    while True:
        # Change the apple position globally, not just locally
        global applec, appler
        applec = randint(0, num_col - 1)
        appler = randint(0, num_row - 1)
        # Get a position that is not already in a snake
        if (applec, appler) not in body1 and (applec, appler) not in body2:
            break
    # Draw red apple square and update display
    square(win, RED, applec, appler)


# Main function
def main():
    global num_col, num_row, game_w, game_h, win_width, win_height, applec, appler

    # Create window
    pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("Snake")
    icon = pygame.image.load('data/snake.png')
    pygame.display.set_icon(icon)

    # Width and Height of the game grid in pixels
    game_w = num_col * BOX
    game_h = num_row * BOX
    # Width and Height of the window in pixels (changes depending on window mode)
    win_width = game_w
    win_height = game_h + 75
    # Initial apple position
    applec = 3 * num_col // 4
    appler = num_row // 2

    # Make resizable window
    win = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)

    # Initialize each score as 0
    b_score = 0
    g_score = 0

    # Game loop
    game = True
    while game:

        # Create snakes
        snakes = [Snake(4, num_row // 2 - 1, BLUE), Snake(4, num_row // 2 + 1, GREEN)]

        # Create list of losers in case of tie
        loser = []

        # Initialize a clock that will regulate number of frames per second
        clock = pygame.time.Clock()
        # Draw window (black background + grid)
        draw(win)

        # Loops activated
        run = True
        start = True
        # Both players are not ready to play
        p1 = False
        p2 = False

        # While starting loop is active
        while start:
            # Set maximum of 60 frames per second
            clock.tick(60)
            # Get window size
            w, h = win.get_size()
            x = w / 2 - game_w / 2
            y = (h - 75) / 2 - game_h / 2
            # Print the score based on window size
            score_y = y + game_h + 20
            score1_x = x + 20
            score1_text = FONT_50.render("BLUE : " + str(b_score), True, BLUE)
            score2_x = x + (num_col - 6) * BOX
            score2_text = FONT_50.render("GREEN : " + str(g_score), True, GREEN)
            win.blit(score2_text, (int(score2_x), int(score_y)))
            win.blit(score1_text, (int(score1_x), int(score_y)))

            # If player 1 not ready
            if not p1:
                # Draw text box
                ready_x = x + BOX
                ready1_y = y + (num_row // 2 - 3) * BOX
                text_box1 = pygame.Rect((int(ready_x) - 5, int(ready1_y) - 5), (230, 30))
                pygame.draw.rect(win, YELLOW, text_box1)
                ready1_text = FONT.render('When ready, press "d"', True, BLUE)
                win.blit(ready1_text, (int(ready_x), int(ready1_y)))
            # Same as player 1
            if not p2:
                ready_x = x + BOX
                ready2_y = y + (num_row // 2 + 3) * BOX
                text_box2 = pygame.Rect((int(ready_x) - 5, int(ready2_y) - 5), (340, 30))
                pygame.draw.rect(win, YELLOW, text_box2)
                ready2_text = FONT.render('When ready, press the right arrow', True, GREEN)
                win.blit(ready2_text, (int(ready_x), int(ready2_y)))

            # Draw apple
            square(win, RED, applec, appler)
            # Draw each snake
            for snake in snakes:
                snake.draw_snake(win)
            # Scan for events
            for event in pygame.event.get():
                # Quit
                if event.type == pygame.QUIT:
                    # All loops are false, so main function finishes and program reaches pygame.quit()
                    game = False
                    run = False
                    start = False
                # Get new window size if window is maximized or minimized and not when window is fullscreen
                if event.type == pygame.VIDEORESIZE and win.get_flags() != -2147483648:
                    scrsize = event.size
                    win = pygame.display.set_mode(scrsize, pygame.RESIZABLE)
                    draw(win)
                # If a key is pressed
                if event.type == pygame.KEYDOWN:
                    # Fullscreen when F11 is pressed
                    if event.key == pygame.K_F11 and win.get_flags() != -2147483648:
                        win = pygame.display.set_mode((win_width, win_height), pygame.FULLSCREEN)
                        draw(win)
                    # Escape -> resize window out of fullscreen
                    if event.key == pygame.K_ESCAPE and win.get_flags() == -2147483648:
                        win = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)
                        draw(win)

                    # If player is ready, draw a transparent rectangle (multiplayer)
                    if event.key == pygame.K_d and not p1:
                        s = pygame.Surface((game_w, game_h // 2))
                        s.set_alpha(128)
                        s.fill(BLUE)
                        win.blit(s, (w // 2 - game_w // 2, (h - 75) // 2 - game_h // 2))
                        p1 = True
                    if event.key == pygame.K_RIGHT and not p2:
                        s = pygame.Surface((game_w, game_h // 2))
                        s.set_alpha(128)
                        s.fill(GREEN)
                        win.blit(s, (w // 2 - game_w // 2, (h - 75) // 2))
                        p2 = True

                # If both players are ready
                if p1 and p2:
                    # 3 second countdown
                    for i in range(3):
                        count = FONT_50.render(str(3 - i), True, WHITE)
                        win.blit(count, (w // 2 - 10, (h - 175 + i * 75) // 2))
                        pygame.display.flip()
                        pygame.time.delay(750)

                    # Set all body part horizontal speeds to 1 and make everyone go to the right
                    (col1, row1) = snakes[0].body[0]
                    snakes[0].turns[(col1, row1)] = 'r'
                    snakes[0].speed_x[0] = 1
                    snakes[0].speed_x[1] = 1
                    snakes[0].speed_x[2] = 1

                    (col2, row2) = snakes[1].body[0]
                    snakes[1].turns[(col2, row2)] = 'r'
                    snakes[1].speed_x[0] = 1
                    snakes[1].speed_x[1] = 1
                    snakes[1].speed_x[2] = 1

                    # Break from start loop
                    start = False
            # Update display every loop
            pygame.display.flip()

        # Redraw window to get rid of previous text boxed and transparent rectangles
        draw(win)
        # Run loop (where game is playable)
        while run:
            # Set maximum of 5 frames per second
            clock.tick(5)

            # Re-draw window to cover previous frame
            draw(win)
            # Draw apple
            square(win, RED, applec, appler)

            # Get window size
            w, h = win.get_size()
            x = w / 2 - game_w / 2
            y = (h - 75) / 2 - game_h / 2

            # Print the score based on window size
            score_y = y + game_h + 20
            score1_x = x + 20
            score1_text = FONT_50.render("BLUE : " + str(b_score), True, BLUE)
            score2_x = x + (num_col - 6) * BOX
            score2_text = FONT_50.render("GREEN : " + str(g_score), True, GREEN)
            win.blit(score2_text, (int(score2_x), int(score_y)))
            win.blit(score1_text, (int(score1_x), int(score_y)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                    run = False
                if event.type == pygame.VIDEORESIZE and win.get_flags() != -2147483648:
                    scrsize = event.size
                    win = pygame.display.set_mode(scrsize, pygame.RESIZABLE)
                    draw(win)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE and win.get_flags() == -2147483648:
                        win = pygame.display.set_mode((win_width, win_height), pygame.RESIZABLE)
                        draw(win)
                    elif event.key == pygame.K_F11 and win.get_flags() != -2147483648:
                        win = pygame.display.set_mode((win_width, win_height), pygame.FULLSCREEN)
                        draw(win)

                    # Check if player one turns (keys w a s d)
                    if event.key == pygame.K_d and snakes[0].speed_x[0] == 0:
                        (col, row) = snakes[0].body[0]
                        snakes[0].turns[(col, row)] = 'r'
                    elif event.key == pygame.K_a and snakes[0].speed_x[0] == 0:
                        (col, row) = snakes[0].body[0]
                        snakes[0].turns[(col, row)] = 'l'
                    if event.key == pygame.K_w and snakes[0].speed_y[0] == 0:
                        (col, row) = snakes[0].body[0]
                        snakes[0].turns[(col, row)] = 'u'
                    elif event.key == pygame.K_s and snakes[0].speed_y[0] == 0:
                        (col, row) = snakes[0].body[0]
                        snakes[0].turns[(col, row)] = 'd'
                    # Check if player two turns (keys u l d r)
                    if event.key == pygame.K_RIGHT and snakes[1].speed_x[0] == 0:
                        (col, row) = snakes[1].body[0]
                        snakes[1].turns[(col, row)] = 'r'
                    elif event.key == pygame.K_LEFT and snakes[1].speed_x[0] == 0:
                        (col, row) = snakes[1].body[0]
                        snakes[1].turns[(col, row)] = 'l'
                    if event.key == pygame.K_UP and snakes[1].speed_y[0] == 0:
                        (col, row) = snakes[1].body[0]
                        snakes[1].turns[(col, row)] = 'u'
                    elif event.key == pygame.K_DOWN and snakes[1].speed_y[0] == 0:
                        (col, row) = snakes[1].body[0]
                        snakes[1].turns[(col, row)] = 'd'

            # Move the snake both at the same time to get true ties
            for snake in snakes:
                snake.move_snake()

            # Actions to do for each snake
            for ind, snake in enumerate(snakes):
                snake.draw_snake(win)

                # Try/Except block to avoid index errors when snakes lose
                try:
                    if snake.lose():
                        # Check which snake lost
                        loser.append(ind)
                # If there's an IndexError, don't terminate the program, just ignore it
                except IndexError:
                    pass

                # Check if the snake ate
                if snake.check_eat(win):
                    apple(win, snakes[0].body, snakes[1].body)

            try:
                # Check if the snakes head has the same position as any of the two snakes' body parts
                for a in range(len(snakes[0].body)):
                    if snakes[1].body[0] == snakes[0].body[a]:
                        loser.append(1)
                for b in range(len(snakes[1].body)):
                    if snakes[0].body[0] == snakes[1].body[b]:
                        loser.append(0)
            except IndexError:
                pass

            # Game over
            if len(loser) != 0:
                # Check for tie
                if len(loser) == 2:
                    # Draw turquoise square on both heads if they collided with each other
                    (head_x, head_y) = snakes[0].body[0]
                    (head2_x, head2_y) = snakes[1].body[0]
                    if (head_x, head_y) == (head2_x, head2_y):
                        square(win, (0, 200, 150), head_x, head_y)
                    # Display text box
                    text_box = pygame.Rect((w // 2 - 50, (h - 100) // 2 - 15), (80, 60))
                    pygame.draw.rect(win, YELLOW, text_box)
                    text = FONT_50.render('TIE', True, RED)
                    win.blit(text, (w // 2 - 40, (h - 100) // 2))
                # If no tie
                elif len(loser) == 1:
                    # Check who lost, increase score of opponent and display text box
                    if loser[0] == 0:
                        text_box = pygame.Rect((w // 2 - 115, (h - 100) // 2 - 15), (255, 60))
                        pygame.draw.rect(win, YELLOW, text_box)
                        text = FONT_50.render('GREEN WINS', True, GREEN)
                        win.blit(text, (w // 2 - 100, (h - 100) // 2))
                        g_score += 1
                    elif loser[0] == 1:
                        text_box = pygame.Rect((w // 2 - 115, (h - 100) // 2 - 15), (225, 60))
                        pygame.draw.rect(win, YELLOW, text_box)
                        text = FONT_50.render('BLUE WINS', True, BLUE)
                        win.blit(text, (w // 2 - 100, (h - 100) // 2))
                        b_score += 1
                # Wait 3 seconds and reset the game
                pygame.display.flip()
                pygame.time.delay(2500)
                applec = 3 * num_col // 4
                appler = num_row // 2
                snakes = []
                run = False

            # Update display for every frame
            pygame.display.flip()


# Quitting without error messages
try:
    main()
except pygame.error:
    pass

pygame.quit()
