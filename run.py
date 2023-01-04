import player
import gas
import transaction as tx
import rigidscheduler as skdr

rounds = 5                      # each round forms a new block
shared_obj_num = 100            # id from 1 to shared_obj_num are shared objs
uniquely_owned_obj_num = 100    # id from shared_obj_num+1 to shared_obj_num+uniquely_owned_obj_num are uniquely owned objs
player_num = 100                # every player has one tx each round


if __name__ == '__main__':
    # uniquely_owned_objcets, shared_objects = object.generate_objects(uniquely_owned_obj_num, shared_obj_num)
    players = player.generate_player(player_num)
    gas_price = gas.init_gas_price(shared_obj_num)

    original_exec_time = []
    simplified_exec_time = []

    for _ in range(rounds):
        original_tx, tx_risk, tx_util = tx.generate_transactions(players, shared_obj_num, uniquely_owned_obj_num)
        simplified_tx = player.simplify(original_tx, tx_risk, tx_util, gas_price)
        original_exec_time.append(skdr.schedule(original_tx, shared_obj_num, uniquely_owned_obj_num))
        simplified_exec_time.append(skdr.schedule(simplified_tx, shared_obj_num, uniquely_owned_obj_num))
        gas_price = gas.calc_gas(simplified_tx, shared_obj_num) 

    # plot

    print(original_exec_time)
    print(simplified_exec_time)