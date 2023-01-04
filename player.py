import random

PLAYER_TYPE_NAIVE = 1
PLAYER_TYPE_TRADER = 2
PLAYER_TYPE_OTS = 3

# randomly generate players
def generate_player(n):
    players = []
    for _ in range(n):
        players.append(random.randrange(1,4))
    return players

def simplify(original_tx, tx_risk, tx_util, gas_price):
    return original_tx