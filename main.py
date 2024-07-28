import pygame
from random import randrange

# Constants
TILE_SIZE = 15
WIDTH, HEIGHT = TILE_SIZE * 100, TILE_SIZE * 50
GRID_WIDTH, GRID_HEIGHT = WIDTH // TILE_SIZE, HEIGHT // TILE_SIZE
PLACEMENT_PHASE_FPS = 60 #Faster FPS for the placement phase (for mouse drag input to work better)
SIMULATION_FPS = 10

BACKGROUND_COLOR = 'grey'
CELL_COLOR = 'purple'
GRID_COLOR = 'black'

playing_simulation = False

# Set up pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

cell_positions = set() #Could also use an array to represent the grid but a set is more efficient for this use case

def handle_grid_key_event(key):
    global cell_positions, playing_simulation #Global keyword is used to modify the global variable (must be at the top of the function)

    if key == pygame.K_SPACE:
        if playing_simulation: print("Stopping simulation")
        else: print("Starting simulation") 
        playing_simulation = not playing_simulation
    elif key == pygame.K_c: 
        print("Clearing grid")
        cell_positions.clear()
    elif key == pygame.K_r: cell_positions = gen_random_grid(randrange(2, 5) * GRID_WIDTH)

def gen_random_grid(num_cells):
    return set([(randrange(0, GRID_HEIGHT), randrange(0, GRID_WIDTH)) for _ in range(num_cells)])

def handle_grid_mouse_event(mouse_pos):
    x, y = mouse_pos
    cell_pos = (x // TILE_SIZE, y // TILE_SIZE)

    if cell_pos in cell_positions: cell_positions.remove(cell_pos)
    elif is_in_bounds(cell_pos): cell_positions.add(cell_pos) #Extra check necessary only if window is bigger than the grid

def check_mouse_drag_event():
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos() #Had to repeat the logic of handle_grid_mouse_event because it didn't wait for the cell to be removed
        cell_pos = (x // TILE_SIZE, y // TILE_SIZE)

        if cell_pos not in cell_positions and is_in_bounds(cell_pos): cell_positions.add(cell_pos)

def update_grid():
    global playing_simulation

    for cell_pos in cell_positions.copy(): #Copy the set to avoid set change size during iteration error
        update_living_cells(cell_pos)

    #Reproduction: dead cells with exactly 3 neighbors become living cells
    check_reproduction()

    if len(cell_positions) == 0:
        print("Stopping simulation")
        playing_simulation = False 

def update_living_cells(cell_pos):
    column, row = cell_pos
    
    #Count the number of neighbors
    num_neighbors = count_neighbors(cell_pos)

    #Overpopulation
    if num_neighbors > 3: 
        cell_positions.remove(cell_pos)

    #Underpopulation
    elif num_neighbors < 2: 
        cell_positions.remove(cell_pos)

    #Cell survives onto the next generation if neighbors are 2 or 3

def count_neighbors(cell_pos):
    column, row = cell_pos
    num_neighbors = 0

    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0: continue

            neighbor_pos = (column + i, row + j)
            if neighbor_pos in cell_positions: num_neighbors += 1

    return num_neighbors

def check_reproduction():
    for cell_pos in cell_positions.copy(): #Copy the set to avoid set change size during iteration error
        column, row = cell_pos

        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor_pos = (column + i, row + j)

                if neighbor_pos not in cell_positions and count_neighbors(neighbor_pos) == 3 and is_in_bounds(neighbor_pos):
                    cell_positions.add(neighbor_pos)

def is_in_bounds(cell_pos):
    column, row = cell_pos
    return 0 <= column < GRID_HEIGHT and 0 <= row < GRID_WIDTH

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

        #Continuos event handling
        if not playing_simulation: check_mouse_drag_event()

        #Update logic
        if playing_simulation: update_grid()
        #Draw calls
        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        draw_cells()

        #print("Living cells:", len(cell_positions))
        #print("Dead cells:", GRID_WIDTH * GRID_HEIGHT - len(cell_positions))

        pygame.display.flip()
        clock.tick(SIMULATION_FPS if playing_simulation else PLACEMENT_PHASE_FPS) 

if __name__ == "__main__":
    start_simulation()
