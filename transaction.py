import random
from player import Player

TX_OTS_SIZE_MIN = 8
TX_OTS_SIZE_MAX = 20
TYPICAL_TX_LEN = 10

HOT_OBJ_PORTION = 0.1
POSSIBILITY_CHOOSE_FROM_HOT = 0.5


def generate_transactions(players, shared_obj_num, uniquely_owned_obj_num, hot_obj_num):
    txs = []
    risks = []

    for p in players:
        match p:
            case Player.NAIVE:
                t, _ = generate_random_ots_tx(shared_obj_num, uniquely_owned_obj_num, hot_obj_num)
                txs.append(t)
                risks.append([])
            case Player.TRADER:
                txs.append([random.randrange(1, uniquely_owned_obj_num), random.randrange(1, uniquely_owned_obj_num)])
                risks.append([])
            case Player.OTS_BEST | Player.OTS_EXP | Player.OTS_WORST:
                t, r = generate_random_ots_tx(shared_obj_num, uniquely_owned_obj_num, hot_obj_num)
                txs.append(t)
                risks.append(r)
            case _:
                txs.append([])
                risks.append([])
    return txs, risks

def generate_random_ots_tx(shared_obj_num, uniquely_owned_obj_num, hot_obj_num):
    obj_total = uniquely_owned_obj_num + shared_obj_num
    tx = [random.randrange(1, obj_total+1)]
    risk = []
    len = 1

    while len < TX_OTS_SIZE_MAX:
        if random.random() > 0.5:
            tx.append(random.randrange(1, obj_total+1))
        else:
            tx.append(random.choice(hot_obj_num))
        if random.random() > 0.9:
            risk.append(random.random())
        else:
            risk.append(1)
        len = len + 1
        if (len > TX_OTS_SIZE_MIN and random.random() > 0.9):
            break

    return tx, risk

def calc_throughput(txs, time):
    if time == 0:
        return 0
    count = 0.0
    for tx in txs:
        count += len(tx)
    # print(count)
    return count / time

def generate_hot_obj(shared_obj_num):
    hot_obj_num = int(shared_obj_num * HOT_OBJ_PORTION)
    return random.sample(range(1, shared_obj_num+1), hot_obj_num)
