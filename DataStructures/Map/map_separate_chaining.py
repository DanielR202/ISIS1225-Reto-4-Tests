from DataStructures.Map import map_functions as mf
from DataStructures.List import single_linked_list as sl
from random import randint

def new_map(num_elements, load_factor, prime=109345121):
    np = mf.next_prime(num_elements/load_factor)
    new_map = {
        "prime":prime,
        "capacity":np,
        "scale":randint(1,prime-1),
        "shift":randint(0,prime-1),
        "table":{"elements":tabler(np),"size":np},
        "current_factor":0,
        "limit_factor":load_factor,
        "size":0,
        "type":"PROBING",
    }
    return new_map

def tabler(capacity):
    ret = []
    for i in range(capacity):
        ret.append({"key":"__EMPTY__","value":"__EMPTY__"})
    return ret
    
def element_add(my_map):
    my_map["size"] += 1
    my_map["current_factor"] = my_map["size"]/my_map["capacity"]
    if my_map["current_factor"] > my_map["limit_factor"]:
        rehash(my_map)
    return my_map
    
def put(my_map, key, value):
    value_hash = mf.hash_md5(my_map,key)
    elements = my_map["table"]["elements"]
    if elements[value_hash]["key"] != "__EMPTY__":
        pos = sl.is_present(elements[value_hash]["key"], key)
        if pos != -1:
            sl.change_info(elements[value_hash]["value"], pos, value)
            return my_map
        sl.add_last(elements[value_hash]["key"], key)
        sl.add_last(elements[value_hash]["value"], value)
        element_add(my_map)
        return my_map
    elements[value_hash]["key"] = sl.new_list()
    sl.add_last(elements[value_hash]["key"], key)
    elements[value_hash]["value"] = sl.new_list()
    sl.add_last(elements[value_hash]["value"], value)
    element_add(my_map)
    return my_map
    
def get(my_map, key):
    value_hash = mf.hash_md5(my_map,key)
    if my_map["table"]["elements"][value_hash]["key"] != "__EMPTY__":
        idx = sl.is_present(my_map["table"]["elements"][value_hash]["key"], key)
        if idx != -1:
            return sl.get_element(my_map["table"]["elements"][value_hash]["value"], idx)

def remove(my_map, key):
    value_hash = mf.hash_md5(my_map,key)
    if my_map["table"]["elements"][value_hash]["key"] == key:
        my_map["table"]["elements"][value_hash]["key"] = "__EMPTY__"
        my_map["table"]["elements"][value_hash]["value"] = "__EMPTY__"
        my_map["size"] -= 1
    for i in range(value_hash+1,my_map["size"]):
        if my_map["table"]["elements"][i]["key"] == key:
            my_map["table"]["elements"][i]["key"] = "__EMPTY__"
            my_map["table"]["elements"][value_hash]["value"] = "__EMPTY__"
            my_map["size"] -= 1
    return my_map

def contains(my_map, key):
    value_hash = mf.hash_md5(my_map,key)
    idx = sl.is_present(my_map["table"]["elements"][value_hash]["key"], key)
    if idx != -1:
        return True

def size(my_map):
    return my_map["size"]

def is_empty(my_map):
    if my_map["size"] == 0:
        return True

def key_set(my_map):
    keys = {"elements":[],"size":0}
    for i in my_map["table"]["elements"]:
        if i["key"] != "__EMPTY__":
            for a in range(i["key"]["size"]):
                keys["elements"].append(sl.get_element(i["key"],a))
                keys["size"] += 1
    return keys

def value_set(my_map):
    values = {"elements":[],"size":0}
    for i in my_map["table"]["elements"]:
        if i["value"] != "__EMPTY__":
            for a in range(i["value"]["size"]):
                values["elements"].append(sl.get_element(i["value"], a))
                values["size"] += 1
    return values

def is_available(table, pos):
    centinela = False
    if 0 <= pos <= len(table["elements"])-1:
        if table["elements"][pos] is None or table["elements"][pos] == "__EMPTY__":
            centinela = True
    return centinela

def rehash(my_map):
    cap = mf.next_prime(my_map["capacity"]*2)
    my_map["capacity"] = cap
    my_map["current_factor"] = 0
    my_map["size"] = 0
    cope = [[],[]]
    for ele in my_map["table"]["elements"]:
        if ele["key"] != "__EMPTY__":
            for i in range(ele["key"]["size"]):
                cope[0].append(sl.get_element(ele["key"],i))
                cope[1].append(sl.get_element(ele["value"],i))
    my_map["table"] = {"elements":tabler(cap),"size":cap}
    for i in range(len(cope[0])):
        put(my_map, cope[0][i], cope[1][i])
    return my_map
