
import pygame
import math
from queue import PriorityQueue

LENGTH = 1000
WIN = pygame.display.set_mode((LENGTH, LENGTH))
pygame.display.set_caption("A* Path Finding Visualizer")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Cell:
    def __init__(self, row, column, length, total_rows):
        self.row = row
        self.column = column
        self.x = row * length
        self.y = row * length
        self.color = WHITE
        self.length = length
        self.total_rows = total_rows

    def get_postion(self):
        return self.row, self.color

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color == WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.length, self.length))
    # continue here

    def update_neighbors(self, grid):
        return

    def __lt__(self, other):
        return False

def heuristic(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, length):
    # there is something wrong here
    grid = []
    gap = length // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i, j, gap, rows)
            grid[i].append(cell)

    return grid

def draw_grid(window, rows, length):
    gap = length // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap), (length, i * gap))
        for j in range(rows):
            pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, length))

def draw(window, grid, rows, length):
    window.fill(WHITE)
    for row in grid:
        for cell in row:
            cell.draw(window)

    draw_grid(window, rows, length)
    pygame.display.update()

def get_clicked_position(position, rows, length):
    gap = length // rows
    y, x = position

    row = y // gap
    column = x //gap

    return row, column

def main(window, length):
    ROWS = 50
    grid = make_grid(ROWS, length)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(window, grid, ROWS, length)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                # for some reason I can't draw on this grid
                position = pygame.mouse.get_pos()
                row, column = get_clicked_position(position, ROWS, length)
                cell = grid[row][column]
                if not start:
                    start = cell
                    start.make_start()

                elif not end:
                    end = cell
                    end.make_end()

                elif cell != end and cell != start:
                    cell.make_barrier()
            elif pygame.mouse.get_pressed()[2]:
                pass

    pygame.quit()

main(WIN, LENGTH)
# scan line by line side by side w/ tutorial vid for what's wrong.
# smth about type conversions and interations
# int instead of list, list instaed of int
# run to debug
