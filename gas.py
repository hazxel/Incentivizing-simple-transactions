BASE_GAS = 100
ADD_GAS = 100

def init_gas_price(shared_obj_num):
    return [BASE_GAS] * shared_obj_num

def calc_gas(simplified_tx, shared_obj_num):
    return init_gas_price(shared_obj_num)