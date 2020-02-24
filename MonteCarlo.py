import Easy21
import numpy as np
import pickle
import random

random.seed(1)

# Heavily reliant on timbmg's code for mc.py https://github.com/timbmg/easy21-rl/blob/master/mc.py

# Action space, 0 is hit, 1 is stick
action_space = [0, 1]

# Constant
N0 = 100
# Number of times an action a has been selected from state s.
# Note, this keeps the number of times a state has been visited as well.
NSA = np.zeros((10, 10, 2))

# Q-table mirroring NSA to plug into our action function
Q = np.zeros((10, 10, 2))

# The number of times that a state is visited
# Found by summing the number of times each action has been taken for a given state."
NS = lambda ns_dealer, ns_player: np.sum(NSA[ns_dealer-1, ns_player-12])

# Time-varying scalar step-size alpha_t
alpha_t = lambda alpha_dealer, alpha_player, action: 1 / (NSA[alpha_dealer-1, alpha_player-12, action])


def eGreedy(eps_dealer, eps_player):
    debugAction = ["Greedy Action", "Argmax Action"]

    epsilon = N0 / (N0 + NS(eps_dealer, eps_player))  # could also define this outside function
    if random.random() < epsilon:  # FIXME: check randomness
        eps_action = random.randint(0, 1)
        print(debugAction[0] + " " + repr(eps_action))

    else:
        eps_action = np.argmax([Q[eps_dealer-1, eps_player-12, action] for action in action_space])
        print(debugAction[1] + " " + repr(eps_action))

    return eps_action


env = Easy21

episodes = 10000
avgReturn = 0
wins = 0

for episode in range(episodes):
    done = False
    SAR = list()
    state_now = env.begin_game()
    while not done:

        action = eGreedy(state_now.dealer_first, state_now.player_total)
        NSA[state_now.dealer_first - 1, state_now.player_total - 12, action] += 1

        next_state, r = env.step(state_now, action)

        SAR.append([state_now.dealer_first, state_now.player_total, action, r])
        state_now = next_state

    G = sum([sar[-1] for sar in SAR])  # sum all rewards
    for (state_now.dealer_first, state_now.player_total, action, _) in SAR:
        Q[state_now.dealer_first, state_now.player_total, action] += alpha_t(state_now.dealer_first, state_now.player_total, action) * (G - Q[state_now.dealer_first, state_now.player_total, action])

    meanReturn = meanReturn + 1 / (episode + 1) * (G - meanReturn)
    if r == 1:
        wins += 1

    if episode % 100 == 0:
        print("Episode %i, Mean-Return %.3f, Wins %.2f" % (episode, meanReturn, wins / (episode + 1)))
print(wins)