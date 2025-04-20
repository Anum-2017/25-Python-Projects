import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 300
screen_height = 600
block_size = 30

# Set up display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris with Pause & Restart")

# Define shapes
shapes = [
    [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']],

    [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']],

    [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']],

    [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']],

    [['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....']],

    [['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']],

    [['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]
]

shape_colors = [
    (0, 255, 255),
    (255, 165, 0),
    (0, 255, 0),
    (255, 0, 0),
    (128, 0, 128),
    (255, 255, 0),
    (0, 0, 255)
]

class Piece:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x,y) in locked_positions:
                grid[y][x] = locked_positions[(x,y)]
    return grid

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    return positions

def valid_space(piece, grid):
    accepted_pos = [[(x, y) for x in range(10) if grid[y][x] == (0,0,0)] for y in range(20)]
    accepted_pos = [x for row in accepted_pos for x in row]

    formatted = convert_shape_format(piece)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_grid(screen, grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            pygame.draw.rect(screen, grid[y][x], (x*block_size, y*block_size, block_size, block_size), 0)

    for y in range(len(grid)):
        pygame.draw.line(screen, (128,128,128), (0, y*block_size), (screen_width, y*block_size))
        for x in range(len(grid[y])):
            pygame.draw.line(screen, (128,128,128), (x*block_size, 0), (x*block_size, screen_height))

def clear_rows(grid, locked):
    increment = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            increment += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if increment > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                new_key = (x, y + increment)
                locked[new_key] = locked.pop(key)
    return increment

def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (screen_width//2 - label.get_width()//2, screen_height//2 - label.get_height()//2))

def draw_window(screen, grid):
    screen.fill((0,0,0))
    draw_grid(screen, grid)
    pygame.display.update()

def main():
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    paused = False

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if not paused and fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_r:
                    main()
                    return

                if not paused:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not valid_space(current_piece, grid):
                            current_piece.x += 1
                    elif event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not valid_space(current_piece, grid):
                            current_piece.x -= 1
                    elif event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not valid_space(current_piece, grid):
                            current_piece.y -= 1
                    elif event.key == pygame.K_UP:
                        current_piece.rotation = (current_piece.rotation + 1) % len(current_piece.shape)
                        if not valid_space(current_piece, grid):
                            current_piece.rotation = (current_piece.rotation - 1) % len(current_piece.shape)

        shape_pos = convert_shape_format(current_piece)

        for x, y in shape_pos:
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            clear_rows(grid, locked_positions)

        draw_window(screen, grid)
        if paused:
            draw_text_middle("PAUSED", 60, (255, 255, 0), screen)
            pygame.display.update()

        if check_lost(locked_positions):
            draw_text_middle("YOU LOST", 80, (255, 0, 0), screen)
            pygame.display.update()
            pygame.time.delay(2000)
            run = False

def run_game():
    main()

run_game()
