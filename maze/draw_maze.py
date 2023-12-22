import pygame
import time
import sys
from read_file import read_file
from config import *
from position import position_cheese, position_mouse

pygame.init()

maze_file = read_file('maze4.txt')

# Images
mouse_img = pygame.image.load('assets/img/mouse.png')
cheese_img = pygame.image.load('assets/img/cheese.png')

# Screen and Cell sizes
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rat in Maze")
rows = len(maze_file)
columns = len(maze_file[0]) if maze_file else 0
cell_size = min((WIDTH - MARGIN) // columns, (HEIGHT - MARGIN) // rows)

# mouse and cheese sizes
mouse = pygame.transform.scale(mouse_img, (cell_size, cell_size))
cheese = pygame.transform.scale(cheese_img, (cell_size, cell_size))

mouse_start_x, mouse_start_y = position_mouse(maze_file)
cheese_position = position_cheese(maze_file)
cheese_end_x, cheese_end_y = cheese_position if cheese_position is not None else (None, None)

def draw_maze(screen, maze_file, mouse_x, mouse_y, cheese_x, cheese_y, mouse):

    screen.fill(WHITE)
    for row in range(len(maze_file)):
        for column in range(len(maze_file[row])):
            cell = maze_file[row][column]

            if cell == '1':  # walls
                pygame.draw.rect(screen, WALL, (column * cell_size, row * cell_size, cell_size, cell_size))

            elif cell == '0':  # paths
                pygame.draw.rect(screen, CELL_COLOR, (column * cell_size, row * cell_size, cell_size, cell_size))

            elif cell == 'm':  # mouse
                screen.blit(mouse, (mouse_x * cell_size, mouse_y * cell_size))

            elif cell == 'e':  # cheese
                if cheese_x is not None and cheese_y is not None:
                    screen.blit(cheese, (cheese_x * cell_size, cheese_y * cell_size))

def valid_position(location_x, location_y, maze_file):
    return 0 <= location_x < len(maze_file[0]) and 0 <= location_y < len(maze_file)

def backtracking(maze_file, mouse_x, mouse_y, cheese_x, cheese_y):
    paths_visited = []
    correct_path = []

    while (mouse_x, mouse_y) != (cheese_x, cheese_y):
        position = (mouse_x, mouse_y)

        mouse_right = mouse_x + 1
        mouse_left = mouse_x - 1
        mouse_top = mouse_y - 1
        mouse_bottom = mouse_y + 1

        # MOVE RIGHT
        if valid_position(mouse_right , mouse_y, maze_file) and maze_file[mouse_y][mouse_right ] in ['0', 'e'] and (mouse_right , mouse_y) not in paths_visited:
            mouse_x += 1
            paths_visited.append((mouse_x, mouse_y))
            correct_path.append(position)

        # MOVE LEFT
        elif valid_position(mouse_left , mouse_y, maze_file) and maze_file[mouse_y][mouse_left ] in ['0', 'e'] and (mouse_left , mouse_y) not in paths_visited:
            mouse_x -= 1
            paths_visited.append((mouse_x, mouse_y))
            correct_path.append(position)

        # MOVE BOTTOM
        elif valid_position(mouse_x, mouse_bottom, maze_file) and maze_file[mouse_bottom][mouse_x] in ['0', 'e'] and (mouse_x, mouse_bottom) not in paths_visited:
            mouse_y += 1
            paths_visited.append((mouse_x, mouse_y))
            correct_path.append(position)

        # MOVE TOP
        elif valid_position(mouse_x, mouse_top, maze_file) and maze_file[mouse_top][mouse_x] in ['0', 'e'] and (mouse_x, mouse_top) not in paths_visited:
            mouse_y -= 1
            paths_visited.append((mouse_x, mouse_y))
            correct_path.append(position)

        else:
            if not correct_path:
                print("\n -------------------------------------------------\n There's no correct path \n -------------------------------------------------\n ")
                break

            last_position = correct_path.pop()
            mouse_x, mouse_y = last_position

    return correct_path, paths_visited

def draw_path(screen, path, cell_color, cell_size, mouse_x, mouse_y, mouse_img, cheese_x, cheese_y, cheese_img):

    for position in path:
        pygame.draw.rect(screen, cell_color, (mouse_x * cell_size, mouse_y * cell_size, cell_size, cell_size))

        if cheese_x is not None and cheese_y is not None and (position[0], position[1]) != (cheese_x, cheese_y):
            pygame.draw.rect(screen, CELL_COLOR, (cheese_x * cell_size, cheese_y * cell_size, cell_size, cell_size))
            screen.blit(cheese_img, (cheese_x * cell_size, cheese_y * cell_size))

        if mouse_x is not None and mouse_y is not None:
            screen.blit(mouse_img, (position[0] * cell_size, position[1] * cell_size))
            pygame.display.flip()

        mouse_x, mouse_y = position
    
# Run
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if running:
        draw_maze(screen=screen, maze_file=maze_file, mouse_x=mouse_start_x, mouse_y=mouse_start_y, mouse=mouse, cheese_x=cheese_end_x, cheese_y=cheese_end_y)

        pygame.display.flip()
        
        
        running = False

    correct_path, visited_path = backtracking(maze_file, mouse_start_x, mouse_start_y, cheese_end_x, cheese_end_y)

    if len(correct_path) > 0 or len(visited_path) > 0:

        for path in visited_path:
            draw_path(screen, [path], WRONG, cell_size, mouse_start_x, mouse_start_y, mouse, cheese_end_x, cheese_end_y, cheese)
            pygame.display.flip()
            time.sleep(0.05)
            mouse_start_x, mouse_start_y = path
    
        for path in correct_path:
            draw_path(screen, [path], CORRECT, cell_size, mouse_start_x, mouse_start_y, mouse, cheese_end_x, cheese_end_y, cheese)
            pygame.display.flip()
            time.sleep(0.05)
            mouse_start_x, mouse_start_y = path

        
        if correct_path:
            print("\n -------------------------------------------------\n Found the cheese! \n -------------------------------------------------\n ")
        
    

pygame.quit()
sys.exit()
