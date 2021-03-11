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
        self.y = column * length
        self.color = WHITE
        self.neighbors = []
        self.length = length
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.column

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
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE
        print self.color

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.length, self.length))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].is_barrier():
            # found it, the bug was here all this time:DD
            self.neighbors.append(grid[self.row + 1][self.column])

        if self.row > 0 and not grid[self.row - 1][self.column].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.column])

        if self.column < self.total_rows - 1 and not grid[self.row][self.column + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.column + 1])

        if self.column > 0 and not grid[self.row][self.column - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.column - 1])

    def __lt__(self, other):
        return False


def heuristic(point_1, point_2):
    x1, y1 = point_1
    x2, y2 = point_2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):

    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))

    came_from = {}

    g_score = {cell: float("inf") for row in grid for cell in row}
    g_score[start] = 0

    f_score = {cell: float("inf") for row in grid for cell in row}
    f_score[start] = heuristic(start.get_position(), end.get_position())

    open_set_hash = {start}


    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_position(), end.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False

def make_grid(rows, length):

    grid = []
    gap = length // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Cell(i, j, gap, rows)
            grid[i].append(spot)


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
    column = x // gap

    return int(row), int(column)


def main(window, length):
    ROWS = 50
    grid = make_grid(ROWS, length)

    start = None
    end = None

    run = True

    while run:
        draw(window, grid, ROWS, length)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, column = get_clicked_position(position, ROWS, length)
                cell = grid[row][column]
                if not start and cell != end:
                    start = cell
                    start.make_start()
                elif not end and cell != start:
                    end = cell
                    end.make_end()
                elif cell != end and cell != start:
                    cell.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, column = get_clicked_position(position, ROWS, length)
                cell = grid[row][column]
                cell.reset()
                if cell == start:
                    start = None
                elif cell == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbors(grid)
                    algorithm(lambda: draw(window, grid, ROWS, length), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, length)


    pygame.quit()


main(WIN, LENGTH)
