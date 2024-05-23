def kruskal(graph):
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

graph = {("A","B"): 2, ("A", "C"):3, ("A", "D"): 5, ("B", "F"): 1, ("B", "E"): 5, ("B","G"): 4, ("F", "G"): 2, ("G", "E"):2, ("E", "C"): 3, ("F", "D"): 4}
graph2= {("A","B"): 2, ("A", "C"):3, ("B", "C"): 5}

print(kruskal(graph2))