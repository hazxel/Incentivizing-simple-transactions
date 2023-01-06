import random
import gas

PLAYER_TYPE_NAIVE = 1
PLAYER_TYPE_TRADER = 2
PLAYER_TYPE_OTS_WORST = 3
PLAYER_TYPE_OTS_BEST = 4
PLAYER_TYPE_OTS_EXP = 5

NUMBER_OF_PLAYER_TYPES = 5

UTILITY_SUCC = 100
UTILITY_FAIL = 0

# randomly generate players
def generate_player(n):
    players = []
    for _ in range(n):
        players.append(random.randrange(1, NUMBER_OF_PLAYER_TYPES+1))
    return players


def simplify(players, original_tx, tx_risk, gas_price):
    new_tx = []
    n = len(players)
    for i in range(n):
        if players[i] == PLAYER_TYPE_OTS_BEST:
            tx_len = len(original_tx[i])
            start = 0
            for j in range(tx_len-1):
                if tx_risk[i][j] < 1:
                    new_tx.append(original_tx[i][start:j+1])
                    start = j+1
            new_tx.append(original_tx[i][start:tx_len])
        elif players[i] == PLAYER_TYPE_OTS_WORST:
            new_tx.append(original_tx[i])
        elif players[i] == PLAYER_TYPE_OTS_EXP:
            tx_len = len(original_tx[i])

            full_split = []
            start = 0
            for j in range(tx_len-1):
                if tx_risk[i][j] < 1:
                    full_split.append(original_tx[i][start:j+1])
                    start = j+1
            full_split.append(original_tx[i][start:tx_len])

            if (not full_split):
                continue

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

        else:
            new_tx.append(original_tx[i])
    return new_tx

def simplify_recursive():
    pass