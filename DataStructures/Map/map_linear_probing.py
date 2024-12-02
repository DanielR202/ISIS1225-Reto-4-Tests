from DataStructures.Map import map_functions as mf
from DataStructures.Map import map_entry as me
from DataStructures.List import array_list as lt

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
    
def find_slot1(my_map, hash_value):
    while hash_value < my_map["table"]["size"]:
        if my_map["table"]["elements"][hash_value]["key"] == "__EMPTY__":
            return True, hash_value
        hash_value += 1
    return False, None

def find_slot(my_map, key, hash_value):
    start = hash_value
    while True:
        current_key = my_map["table"]["elements"][hash_value]["key"]
        # Verifica si la posición está vacía o contiene la key que buscas
        if current_key == "__EMPTY__":
            return False, hash_value
        elif current_key == key:
            return True, hash_value
        # Avanza a la siguiente posición
        hash_value = (hash_value + 1) % my_map["capacity"]
        # Si volvemos al punto de inicio, hemos recorrido toda la tabla
        if hash_value == start:
            return False, None

    
    
def default_compare(key, element):
    if key == element["key"]:
        return 0
    elif key > element["key"]:
        return 1
    elif key < element["key"]:
        return -1
    
    
def put(my_map, key, value):
    value_hash = mf.hash_md5(my_map,key)
    if my_map["table"]["elements"][value_hash]["key"] != "__EMPTY__":
        if my_map["table"]["elements"][value_hash]["key"] == key:
            my_map["table"]["elements"][value_hash]["value"] = value
            return my_map
        con, idx = find_slot1(my_map, value_hash + 1)
        if con == True:
            my_map["table"]["elements"][idx]["key"] = key
            my_map["table"]["elements"][idx]["value"] = value
            my_map["size"] += 1
            my_map["current_factor"] = my_map["size"]/my_map["capacity"]
            if my_map["current_factor"] > my_map["limit_factor"]:
                rehash(my_map)
            return my_map
        else:
            my_map["capacity"] == my_map["capacity"]/2
            rehash(my_map)
            put(my_map, key, value)
    my_map["table"]["elements"][value_hash]["key"] = key
    my_map["table"]["elements"][value_hash]["value"] = value
    my_map["size"] += 1
    my_map["current_factor"] = my_map["size"]/my_map["capacity"]
    if my_map["current_factor"] > my_map["limit_factor"]:
        rehash(my_map)
    return my_map
    
def get(my_map, key):
    value_hash = mf.hash_md5(my_map,key)
    if my_map["table"]["elements"][value_hash]["key"] == key:
        return my_map["table"]["elements"][value_hash]["value"]
    return linear_search(my_map, value_hash, key)

def linear_search(my_map, value_hash, key):
    for i in range(value_hash+1,my_map["table"]["size"]):
        if my_map["table"]["elements"][i]["key"] == key:
            return my_map["table"]["elements"][i]["value"]

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
    if my_map["table"]["elements"][value_hash]["key"] == key:
        return True
    if linear_search(my_map, value_hash, key):
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
            keys["elements"].append(i["key"])
            keys["size"] += 1
    return keys

def value_set(my_map):
    values = {"elements":[],"size":0}
    for i in my_map["table"]["elements"]:
        if i["value"] != "__EMPTY__":
            values["elements"].append(i["value"])
            values["size"] += 1
    return values

def is_available(table, pos):
    centinela = False
    if 0 <= pos <= table["size"]-1:
        if table["elements"][pos]["key"] is None or table["elements"][pos]["key"] == "__EMPTY__":
            centinela = True
    return centinela


def rehash(my_map):
    cap = mf.next_prime(my_map["capacity"]*2)
    my_map["capacity"] = cap
    my_map["current_factor"] = 0
    my_map["size"] = 0
    cope = [[],[]]
    for ele in my_map["table"]["elements"]:
        cope[0].append(ele["key"])
        cope[1].append(ele["value"])
    my_map["table"] = {"elements":tabler(cap),"size":cap}
    for i in range(len(cope[0])):
        if cope[0][i] != "__EMPTY__":
            put(my_map, cope[0][i], cope[1][i])
    return my_map
