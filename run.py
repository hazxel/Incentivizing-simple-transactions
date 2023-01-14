import player
import gas
import transaction as tx
import rigidscheduler as skdr

rounds = 5                      # each round forms a new block
shared_obj_num = 100            # id from 1 to shared_obj_num are shared objs
uniquely_owned_obj_num = 100    # id from shared_obj_num+1 to shared_obj_num+uniquely_owned_obj_num are uniquely owned objs
player_num = 100                # every player has one tx each round

def calc_throughput(txs, time):
    count = 0.0
    for tx in txs:
        count += len(tx)
    return count / time

if __name__ == '__main__':
    players = player.generate_player(player_num)
    gas_price = gas.init_gas_price(shared_obj_num)

    original_exec_time = []
    simplified_exec_time = []
    original_throughput = []
    simplified_throughput = []

    for _ in range(rounds):
        original_tx, tx_risk = tx.generate_transactions(players, shared_obj_num, uniquely_owned_obj_num)
        
        simplified_tx = player.simplify(players, original_tx, tx_risk, gas_price)
        original_tx = player.dummy_simplify(original_tx, gas_price)
        
        original_exec_time.append(skdr.schedule(original_tx, shared_obj_num))
        simplified_exec_time.append(skdr.schedule(simplified_tx, shared_obj_num))

        original_throughput.append(calc_throughput(original_tx, original_exec_time[-1]))
        simplified_throughput.append(calc_throughput(simplified_tx, simplified_exec_time[-1]))
        
        gas_price = gas.next_block_gas(simplified_tx, shared_obj_num)

    # plot
    print(original_exec_time)
    print(simplified_exec_time)
    print(original_throughput)
    print(simplified_throughput)
