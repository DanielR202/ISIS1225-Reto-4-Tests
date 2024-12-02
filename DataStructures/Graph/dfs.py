from DataStructures.Graph import adj_list_graph as g
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Stack import stack as stk

def depth_first_search(my_graph, source):
    new_dfs = {
        "source":source,
        "visited":mp.new_map(7, 0.5),
    }
    dfs_vertex(new_dfs["visited"], my_graph, source)
    return new_dfs

def dfs_vertex(search, my_graph, vertex):
    if mp.get(search, vertex) == None:
        mp.put(search, vertex, {"marked": True, "edge_to": None})
    lest = g.adjacents(my_graph, vertex)
    for i in lest["elements"]:
        if mp.get(search, i) == None:
            mp.put(search, i, {"marked": True, "edge_to": vertex})
            dfs_vertex(search, my_graph, i)

def has_path_to(my_dfs, vertex):
    if mp.get(my_dfs["visited"], vertex) != None:
        return True
    return False

def path_to(my_dfs, vertex):
    ret = stk.new_stack()
    stk.push(ret, vertex)
    adi = mp.get(my_dfs["visited"], vertex)
    while adi["edge_to"] != None:
        stk.push(ret, adi["edge_to"])
        adi = mp.get(my_dfs["visited"], adi["edge_to"])
    return ret