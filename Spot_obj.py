
import pygame
import Constants

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = Constants.WHITE
        self.image = None
        self.close_neighbors = []
        self.far_neighbors = []
        self.weight = 1
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == Constants.RED

    def is_open(self):
        return self.color == Constants.GREEN

    def is_barrier(self):
        return self.image == Constants.tree

    def is_start(self):
        return self.image == Constants.house
    
    def is_path(self):
        return self.color == Constants.PURPLE
    
    def is_mst_path(self):
        return self.color == Constants.TURQUOISE

    def reset(self):
        self.color = Constants.WHITE
        self.image = None

    def make_start(self):
        self.image = Constants.house
        self.color = Constants.ORANGE

    def make_closed(self):
        self.color = Constants.RED

    def make_open(self):
        self.color = Constants.GREEN

    def make_barrier(self):
        self.image = Constants.tree


    def make_path(self):
        self.color = Constants.PURPLE

    def make_path_mst(self):
        self.color = Constants.TURQUOISE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        if self.image: win.blit(self.image, (self.x-15, self.y-25))

    def update_close_neighbors(self, grid):
        self.close_neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
            self.close_neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.close_neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.close_neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.close_neighbors.append(grid[self.row][self.col - 1])

    def update_far_neighbors(self, grid):
        self.far_neighbors = []
        if self.row < self.total_rows - 1:
            if self.col < self.total_rows - 1 and not grid[self.row + 1][self.col+1].is_barrier(): #TOP RIGHT
                self.far_neighbors.append(grid[self.row + 1][self.col+1])
            if  self.col > 0 and not grid[self.row+1][self.col - 1].is_barrier(): #TOP LEFT
                self.far_neighbors.append(grid[self.row + 1][self.col-1])
        if self.row > 0:
            if self.col < self.total_rows - 1 and not grid[self.row - 1][self.col+1].is_barrier(): #BOTTOM RIGHT
                self.far_neighbors.append(grid[self.row - 1][self.col + 1])
            if self.col > 0 and not grid[self.row - 1][self.col-1].is_barrier(): #BOTTOM LEFT
                self.far_neighbors.append(grid[self.row - 1][self.col - 1])
            
    def __lt__(self, other):
        return False