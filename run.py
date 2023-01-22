import sys
import numpy as np

import player
import gas
import transaction as tx
import rigidscheduler as skdr
import plot

rounds = 25                     # each round forms a new block
samples = 40                    # samples in a block
shared_obj_num = 200            # id from 1 to shared_obj_num are shared objs
uniquely_owned_obj_num = 300    # id from shared_obj_num+1 to shared_obj_num+uniquely_owned_obj_num are uniquely owned objs
player_num = 100                # every player has one tx each round

def run_with_OTS(ots_portion):
    players = player.generate_mixed_player(player_num, ots_portion)
    gas_price = gas.init_gas_price(shared_obj_num)
    hot_objects = tx.generate_hot_obj(shared_obj_num)

    original_exec_time = []
    simplified_exec_time = []
    original_throughput = []
    simplified_throughput = []

    typical_tx_price = []
    original_operations = []
    simplified_operations = []

    for i in range(rounds):
        original_throughput.append([])
        simplified_throughput.append([])
        original_total_op = []
        simplified_total_op = []

        for _ in range(samples):
            original_tx, tx_risk = tx.generate_transactions(players, shared_obj_num, uniquely_owned_obj_num, hot_objects)
            
            simplified_tx = player.simplify(players, original_tx, tx_risk, gas_price)
            original_tx = player.dummy_simplify(original_tx)

            original_total_op.append(sum([len(tx) for tx in original_tx]))
            simplified_total_op.append(sum([len(tx) for tx in simplified_tx]))
            
            original_exec_time.append(skdr.schedule(original_tx, shared_obj_num))
            simplified_exec_time.append(skdr.schedule(simplified_tx, shared_obj_num))

            typical_tx_price.extend(gas.calc_typical_gas(list(filter(lambda t : len(t) == tx.TYPICAL_TX_LEN, simplified_tx)), gas_price))

            original_throughput[i].append(tx.calc_throughput(original_tx, original_exec_time[-1]))
            simplified_throughput[i].append(tx.calc_throughput(simplified_tx, simplified_exec_time[-1]))
        
        gas_price = gas.next_block_gas(gas_price, simplified_tx, shared_obj_num)

        original_operations.append(original_total_op)
        simplified_operations.append(simplified_total_op)

    return original_throughput, simplified_throughput, typical_tx_price, original_operations, simplified_operations

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"One argument expected, got {len(sys.argv) - 1}")
        raise SystemExit(2)
    
    match sys.argv[1]:
        case "single":
            original_throughput, simplified_throughput, typical_tx_price, _, _ = run_with_OTS(1)
            plot.plot_single(original_throughput, simplified_throughput)
            print(sum(typical_tx_price) / len(typical_tx_price)) # we need this to be equal to un-simplified tx with same length
        case "scan":
            original_throughput = []
            simplified_throughput = []
            for ots_portion in np.arange(0, 1.0001, 0.05):
                o, s, _, _, _ = run_with_OTS(ots_portion)
                original_throughput.append(o)
                simplified_throughput.append(s)
            plot.plot_scan(original_throughput, simplified_throughput)
        case "operation":
            _, _, _, original_op, simplified_op = run_with_OTS(1)
            plot.plot_operation(original_op, simplified_op)
        case _:
            print("valid modes are single, scan and operation!")
