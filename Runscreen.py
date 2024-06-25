import pygame
import math
from queue import PriorityQueue
# from Spot_obj import Spot
import Spot_obj
import Constants
from algo import Algo
import random

WIN = pygame.display.set_mode((Constants.GAME_WIDTH, Constants.GAME_WIDTH))
pygame.display.set_caption("Welcome To The Neightborhood game")


pygame.init()
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
    

    def make_grid(self, rows, width):
        grid = []
        gap = width // rows
        for i in range(rows):
            grid.append([])
            for j in range(rows):
                spot = Spot_obj.Spot(i, j, gap, rows)
                grid[i].append(spot)

        return grid

    def draw_grid(self, win, rows, width):
        gap = width // rows
        for i in range(rows):
            pygame.draw.line(win, Constants.GREY, (0, i * gap), (width, i * gap))
            for j in range(rows):
                pygame.draw.line(win, Constants.GREY, (j * gap, 0), (j * gap, width))

    def draw(self, win, grid, rows, width):
        win.fill(Constants.WHITE)

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
        algo = Algo(runscreen=self)

        while run:
            self.draw(self.win, grid, ROWS, self.width)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                #Make start and barrier with left-click
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

                #Erase with right-click
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

                                path, weight, found = algo.a_star(grid=grid, start=start, end=end, draw = lambda: self.draw(self.win, grid, ROWS, self.width))
                            
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
                                        start.color = Constants.ORANGE
                                    else: start.color = Constants.RED
                                
                                
                                pygame.display.update() 

                        print("Path finding done!")
                        
                    #Press M to run Kruskal algorithm (find MST)
                    if event.key == pygame.K_m:
                        total_length = 0
                        mst = algo.kruskal(weight_graph)

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

