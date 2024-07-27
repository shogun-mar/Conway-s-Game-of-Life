import pygame
from random import randrange

# Constants
TILE_SIZE = 20
WIDTH, HEIGHT = TILE_SIZE * 40, TILE_SIZE * 40
GRID_WIDTH, GRID_HEIGHT = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE
MAX_FPS = 60

BACKGROUND_COLOR = 'grey'
CELL_COLOR = 'purple'
GRID_COLOR = 'black'

# Set up pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

cell_positions = set()

def handle_grid_key_event(key):
    global cell_positions #Global keyword is used to modify the global variable (must be at the top of the function)

    if key == pygame.K_SPACE: playing_simulation = not playing_simulation
    elif key == pygame.K_c: cell_positions.clear()
    elif key == pygame.K_r: cell_positions = gen_random_grid(randrange(2, 5) * GRID_WIDTH)

def gen_random_grid(num_cells):
    return set([(randrange(0, GRID_HEIGHT), randrange(0, GRID_WIDTH)) for _ in range(num_cells)])

def handle_grid_mouse_event(mouse_pos):
    x, y = mouse_pos
    cell_pos = (x // TILE_SIZE, y // TILE_SIZE)

    if cell_pos in cell_positions: cell_positions.remove(cell_pos)
    else: cell_positions.add(cell_pos)

def draw_grid():
    for x in range(0, WIDTH, TILE_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))

    for y in range(0, HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))

def draw_cells():
    for cell_pos in cell_positions:
        x, y = cell_pos
        pygame.draw.rect(screen, CELL_COLOR, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def start_simulation():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN: 
                handle_grid_mouse_event(pygame.mouse.get_pos()) #Adds or removes cell based on the mouse position

            elif event.type == pygame.KEYDOWN:
                handle_grid_key_event(event.key)

        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        draw_cells()

        pygame.display.flip()
        clock.tick(MAX_FPS)

if __name__ == "__main__":
    start_simulation()
