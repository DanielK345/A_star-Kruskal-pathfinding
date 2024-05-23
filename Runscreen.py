import pygame
import math
from queue import PriorityQueue
import time
import random

WIDTH = 810 
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Welcome To The Neightborhood game")

pygame.init()

house = pygame.image.load("House_With_Garden.png")
house = pygame.transform.scale(house, (50,70))
tree = pygame.image.load("Tree.png")
tree = pygame.transform.scale(tree, (50,70))

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.image = None
        # self.neighbors = []
        self.close_neighbors = []
        self.far_neighbors = []
        self.weight = 1
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.image == tree

    def is_start(self):
        return self.image == house
    
    def is_path(self):
        return self.color == PURPLE
    
    def is_mst_path(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE
        self.image = None

    def make_start(self):
        self.image = house
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.image = tree


    def make_path(self):
        self.color = PURPLE

    def make_path_mst(self):
        self.color = TURQUOISE

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
class RunScreen:
    def __init__(self, win, width):
        self.win = win
        self.width = width

    def reconstruct_path(self,came_from, current, draw):
        path_weight = 0
        path = []
        while current in came_from:
            if came_from[current] in current.far_neighbors: 
                path_weight += 3
                path.append((current.row, current.col, 3))
            else: 
                path_weight += 1
                path.append((current.row, current.col, 1))
            current = came_from[current] 
            current.make_path()
            draw()
        return [path, path_weight]
    

    def a_star(self, draw, grid, start, end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float("inf") for row in grid for spot in row}
        g_score[start] = 0

        explore = []
        found = False

        path_weight = 0
        path = {}
        open_set_hash = {start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            current = open_set.get()[2]
            open_set_hash.remove(current)
        

            if current == end:
                for spot in explore: spot.reset()
                path_weight = self.reconstruct_path(came_from, end, draw)[1]
                path = self.reconstruct_path(came_from, end, draw)[0]
                found = True
                break


            neighbors = current.close_neighbors + current.far_neighbors
            for neighbor in neighbors:
                if neighbor in current.close_neighbors: temp_g_score = g_score[current] + 1
                elif neighbor in current.far_neighbors: temp_g_score = g_score[current] + 3


                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score = temp_g_score + self.h(neighbor.get_pos(), end.get_pos())

                    if neighbor not in open_set_hash:
                        open_set.put((f_score, count, neighbor))
                        open_set_hash.add(neighbor)
                                
                    if not (neighbor.is_path() or neighbor.is_start()): 
                        neighbor.make_open()
                        explore.append(neighbor)

            draw()
        return [path, path_weight, found]


    def h(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        score = abs(x1 - x2) + abs(y1 - y2)
        if y1 == y2 or x1 == x2: return score - 1.5 #Optimizes search

        return score

    def kruskal(self, graph):
        mst = set()  # Minimum spanning tree
        disjoint_sets = {vertex: {vertex} for edge in graph for vertex in edge}

        # Sort edges by weight
        sorted_edges = sorted(graph, key=lambda x: graph[x])

        for edge in sorted_edges:
            u, v = edge
            set_u = disjoint_sets[u]
            set_v = disjoint_sets[v]

            # If the edge forms a cycle, skip it
            if set_u != set_v:
                mst.add(edge)
                # Union the sets
                new_set = set_u.union(set_v)
                for vertex in new_set:
                    disjoint_sets[vertex] = new_set

        return mst

    def make_grid(self, rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot(i, j, gap, rows)
                grid[i].append(spot)

        return grid

    def draw_grid(self, win, rows, width):
        gap = width // rows
        for i in range(rows):
            pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
            for j in range(rows):
                pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

    def draw(self, win, grid, rows, width):
        win.fill(WHITE)

        for row in grid:
            for spot in row:
                spot.draw(win)

        self.draw_grid(win, rows, width)
    
        pygame.display.update()

    def get_clicked_pos(self, pos, rows, width):
        gap = width // rows
        y, x = pos
        row = y // gap
        col = x // gap
        return row, col


    def run(self):
        ROWS = 30
        grid = self.make_grid(ROWS, self.width)
        
        run = True

        targets =[]
        weight_graph = {}
        path_graph ={}

        num = 2

        while run:
            self.draw(self.win, grid, ROWS, self.width)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                #Make start and barrier by left-click
                if pygame.mouse.get_pressed()[0]:  
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos, ROWS, self.width)
                    spot = grid[row][col]
                    if len(targets) < num :
                        if not spot.is_start():
                            spot.make_start()
                            targets.append(spot)

                    elif len(targets) >= num and not spot.is_start():
                        spot.make_barrier()

                #Erase by right-click
                elif pygame.mouse.get_pressed()[2]: # RIGHT
                    pos = pygame.mouse.get_pos()
                    row, col = self.get_clicked_pos(pos, ROWS, self.width)
                    spot = grid[row][col]
                    spot.reset()
                    if spot in targets:
                        targets.remove(spot)
                        spot = None
                        

                if event.type == pygame.KEYDOWN:
                    #Press r to creat random forrest
                    if event.key == pygame.K_r:
                        for _ in range(300):
                            row = random.randint(0, ROWS-1)
                            col = random.randint(0, ROWS-1)

                            if grid[row][col].is_barrier() or grid[row][col].is_start(): pass
                            else: grid[row][col].make_barrier()

                    if event.unicode.isdigit():
                        num = int(event.unicode)
                        print(f"Number of starting nodes chosen is {num}")

                    #Press space to start A*
                    if event.key == pygame.K_SPACE and targets:
                        for row in grid:
                            for spot in row:
                                spot.update_close_neighbors(grid)
                                spot.update_far_neighbors(grid)
                                if spot.is_path() or spot.is_mst_path(): spot.reset()
                        
                        found_set = set()
                        for i in range(len(targets)):
                            for j in range(i+1, len(targets)):
                                
                                start = targets[i]
                                end = targets[j]

                                
                                path, weight, found = self.a_star(lambda: self.draw(self.win, grid, ROWS, self.width), grid, start, end)
                            
                                if found:
                                    found_set.add(start)
                                    found_set.add(end)
                                    weight_graph[(start.get_pos(), end.get_pos())] = weight
                                    path_graph[(start.get_pos(), end.get_pos())] = path
                                
                                else: 
                                    for row in grid:
                                        for spot in row:
                                            if spot.is_open(): spot.reset()
                                    print(f"There is no path between spot {(start.row, start.col)} and {(end.row, end.col)}")
                                    pass
                                
                                for start in targets: 
                                    
                                    if start in found_set:
                                        start.color = ORANGE
                                    else: start.color = RED
                                
                                
                                pygame.display.update() 

                        print("Path finding done!")
                        
                    #Press M to run Kruskal algorithm (find MST)
                    if event.key == pygame.K_m:
                        total_length = 0
                        mst = self.kruskal(weight_graph)

                        node_set =set() #Use a set to prevent path overlapping
                     
                        for edge in path_graph:
                            if edge in mst:
                                path = path_graph[edge]
                                for node in path: 
                                    node_set.add(node)
                                    row,col = node[:-1]
                                    spot = grid[row][col]
                                    if not spot.is_start(): spot.make_path_mst()
                                    self.draw(self.win, grid, ROWS, self.width)
                        for node in node_set:
                            total_length += node[-1]
                        
                        print(f"Length shortest of path across all nodes is {total_length - num + 1}")

                    #Press C to restart
                    if event.key == pygame.K_c:
                        targets =[]
                        weight_graph = {}
                        path_graph ={}
                        num = 2
                        grid = self.make_grid(ROWS, self.width)
                    


        pygame.quit()

