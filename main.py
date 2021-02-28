
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

    # continue here
