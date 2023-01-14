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

UTILITY_SUCC = 100
UTILITY_FAIL = 0

# randomly generate players
def generate_player(n):
    players = []
    for _ in range(n):
        players.append(random.choice(list(Player)))
    return players


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

                full_split = []
                start = 0
                for j in range(tx_len-1):
                    if tx_risk[i][j] < 1:
                        full_split.append(original_tx[i][start:j+1])
                        start = j+1

                full_split.append(original_tx[i][start:tx_len])

                left = full_split[0]
                interval = len(left) - 1
                for j in range(1, len(full_split)):
                    right = full_split[j]
                    saved_gas = gas.calc_saved_gas(left, right, gas_price)
                    # compare exp of splitting
                    if saved_gas > (UTILITY_SUCC - UTILITY_FAIL) * tx_risk[i][interval]:
                        # split
                        new_tx.append(left)
                        left = right
                    else:
                        # not split
                        left = left + right
                    interval += len(right)
                
                new_tx.append(left)
            case _:
                new_tx.append(original_tx[i])
    return new_tx

def simplify_recursive():
    pass