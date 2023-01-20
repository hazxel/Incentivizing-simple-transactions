from enum import Enum
import random

import gas

class Player(Enum):
    NAIVE = 1
    TRADER = 2
    OTS_WORST = 3
    OTS_BEST = 4
    OTS_EXP = 5

NUMBER_OF_PLAYER_TYPES = 5

UTILITY_SUCC = 900
UTILITY_FAIL = 0

# randomly generate players
def generate_ots_player(n):
    return generate_mixed_player(n)

def generate_mixed_player(n, ots_portion = 1.0):
    players = []
    for _ in range(n):
        if (random.random() > ots_portion): 
            players.append(Player.NAIVE)
        else:
            players.append(Player.OTS_EXP)
    return players

def generate_rand_player(n):
    players = []
    for _ in range(n):
        players.append(random.choice(list(Player)))
    return players

def dummy_simplify(original_tx):
    new_tx = []
    for tx in original_tx:
        gas_fee = gas.calc_gas_old(tx)
        if UTILITY_SUCC > gas_fee:
            new_tx.append(tx)
    return new_tx


def simplify(players, original_tx, tx_risk, gas_price):
    new_tx = []
    n = len(players)
    for i in range(n):
        match players[i]:
            case Player.OTS_BEST:
                tx_len = len(original_tx[i])
                start = 0
                for j in range(tx_len-1):
                    if tx_risk[i][j] < 1:
                        new_tx.append(original_tx[i][start:j+1])
                        start = j+1
                new_tx.append(original_tx[i][start:tx_len])
            case Player.OTS_WORST:
                new_tx.append(original_tx[i])
            case Player.OTS_EXP:
                tx_len = len(original_tx[i])
                full_split = [[]]
                for j in range(tx_len-1):
                    if tx_risk[i][j] < 1:
                        l = len(full_split)
                        for k in range(l):
                            full_split.append(full_split[k][:])
                            full_split[k].append(j)
                
                for j in range(len(full_split)):
                    split = full_split[j][:]
                    full_split[j] = []
                    start = 0
                    for s in split:
                        full_split[j].append(original_tx[i][start:s+1])
                        start = s+1
                    if start != tx_len:
                        full_split[j].append(original_tx[i][start:tx_len])

                
                benefit = 0
                split = full_split[-1]
                gas_fee = gas.calc_gas(split[0], gas_price)
                full_split.pop()

                for fs in full_split:
                    interval = len(fs[0]) - 1
                    b = 0
                    for j in range(1,len(fs)):
                        b += gas.calc_saved_gas(fs[j-1], fs[j], gas_price) - (UTILITY_SUCC - UTILITY_FAIL) * tx_risk[i][interval]
                        interval += len(fs[j])

                    if benefit < b:
                        benefit = b
                        split = fs
                
                if UTILITY_SUCC + benefit > gas_fee:
                    for s in split:
                        new_tx.append(s)
                #     print("\n succ: ")
                #     print(UTILITY_SUCC + benefit - gas_fee)
                # else:
                #     print("\ngas: ")
                #     print(gas_fee)
                #     print("util: ")
                #     print(UTILITY_SUCC + benefit)
                #     print(len(split))
            case _:
                new_tx.append(original_tx[i])
    return new_tx

def simplify_recursive():
    pass