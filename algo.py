from queue import PriorityQueue
import pygame

class Algo:

    def __init__(self, runscreen):
        self.runscreen = runscreen

    def a_star(self, draw, grid, start, end):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, start))
        came_from = {}
        g_score = {spot: float("inf") for row in grid for spot in row}
        g_score[start] = 0
        runscreen = self.runscreen

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
                path_weight = runscreen.reconstruct_path(came_from, end, draw)[1]
                path = runscreen.reconstruct_path(came_from, end, draw)[0]
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