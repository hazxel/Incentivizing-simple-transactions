import random
import player

TX_OTS_SIZE_MIN = 5
TX_OTS_SIZE_MAX = 20


def generate_transactions(players, shared_obj_num, uniquely_owned_obj_num):
    txs = []
    risks = []

    for p in players:
        if p == player.PLAYER_TYPE_NAIVE:
            txs.append([random.randrange(1, uniquely_owned_obj_num), random.randrange(1, uniquely_owned_obj_num)])
            risks.append([])
        elif p == player.PLAYER_TYPE_TRADER:
            txs.append([random.randrange(1, uniquely_owned_obj_num), random.randrange(1, uniquely_owned_obj_num)])
            risks.append([])
        elif p == player.PLAYER_TYPE_OTS_BEST or p == player.PLAYER_TYPE_OTS_WORST or p == player.PLAYER_TYPE_OTS_EXP:
            t, r = generate_random_ots_tx(shared_obj_num, uniquely_owned_obj_num)
            txs.append(t)
            risks.append(r)
        else:
            txs.append([])
            risks.append([])
    
    return txs, risks

def generate_random_ots_tx(shared_obj_num, uniquely_owned_obj_num):
    obj_total = uniquely_owned_obj_num + shared_obj_num
    tx = [random.randrange(1, obj_total+1)]
    risk = []
    len = 1

    while len < TX_OTS_SIZE_MAX:
        tx.append(random.randrange(1, obj_total+1))
        if random.random() > 0.9:
            risk.append(random.random())
        else:
            risk.append(1)
        len = len + 1
        if (len > TX_OTS_SIZE_MIN and random.random() > 0.9):
            break

    return tx, risk