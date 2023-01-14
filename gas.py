BASE_GAS = 1.0
ADD_GAS = 100.0

def init_gas_price(shared_obj_num):
    return [BASE_GAS + ADD_GAS / shared_obj_num] * shared_obj_num

def calc_saved_gas(left, right, gas_price):
    shared_obj_num = len(gas_price)
    saved = 0
    set_left = set()
    for obj in left:
        # not shared obj
        if obj > shared_obj_num or obj in set_left:
            continue
        
        saved += gas_price[obj-1] * len(right)
        set_left.add(obj)

    set_right = set()
    for obj in right:
        # not shared obj
        if obj > shared_obj_num or obj in set_right:
            continue
        
        if obj in set_left:
            saved -= gas_price[obj-1] * len(right)
        else:
            saved += gas_price[obj-1] * len(left)

        set_right.add(obj)

    return saved



def next_block_gas(simplified_tx, shared_obj_num):
    load = [0] * shared_obj_num
    for tx in simplified_tx:
        length = len(tx)
        obj_set = set()
        for obj in tx:
            if obj > shared_obj_num or obj in obj_set:
                continue
            load[obj-1] += length
            obj_set.add(obj)
    
    load_total = sum(load) 
    return [BASE_GAS + ADD_GAS * l / load_total for l in load]