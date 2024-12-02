from DataStructures.Graph import edge as ed
from DataStructures.List import array_list as al
from DataStructures.Map import map_linear_probing as mp

def new_graph(size=15, directed=False):
    graph = {
        "vertices":mp.new_map(size, 0.5),
        "information":mp.new_map(size, 0.5),
        "in_degree":None,
        "edges":0,
        "directed":directed,
        "type":"ADJ_LIST"
    }
    return graph

def insert_vertex(graph, key_vertex, info_vertex):
    ext = mp.get(graph["vertices"], key_vertex)
    if ext == None:
        mp.put(graph["vertices"], key_vertex, al.new_list())
        mp.put(graph["information"], key_vertex, info_vertex)
    
def num_vertices(graph):
    return mp.size(graph["vertices"])

def num_edges(graph):
    return graph["edges"]

def vertices(graph):
    return mp.key_set(graph["vertices"])

def edges(graph):
    ret = al.new_list()
    val = mp.value_set(graph["vertices"])
    for v in val["elements"]:
        for edge in v["elements"]:
            if not (edge in ret["elements"] or ed.new_edge(edge["vertex_b"],edge["vertex_a"],edge["weight"]) in ret["elements"]):
                al.add_last(ret, edge)
    return ret

def degree(graph, key_vertex):
    ret = mp.get(graph["vertices"], key_vertex)
    if ret != None:
        return al.size(ret)
    
def in_degree(graph, key_vertex):
    num = 0
    val = mp.value_set(graph["vertices"])
    for v in val["elements"]:
        for edge in v["elements"]:
            if edge["vertex_b"] == key_vertex:
                num += 1
    if num == 0:
        return None
    return num

def add_edge(graph, vertex_a, vertex_b, weight=0):
    work = graph["vertices"]
    p1 = mp.get(work, vertex_a)
    p2 = mp.get(work, vertex_b)
    if p1 == None or p2 == None:
        return None
    al.add_last(p1, ed.new_edge(vertex_a, vertex_b, weight))
    al.add_last(p2, ed.new_edge(vertex_b, vertex_a, weight))
    graph["edges"] += 1

def adjacents(graph, vertex):
    adj = mp.get(graph["vertices"], vertex)
    ret = al.new_list()
    for i in adj["elements"]:
        al.add_last(ret, i["vertex_b"])
    return ret
    