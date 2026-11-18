import random

import numpy as np

# A reproducible tabular Q-Learning example.
NUM_STATES = 5
NUM_ACTIONS = 2
GOAL_STATE = NUM_STATES - 1
LEARNING_RATE = 0.8
DISCOUNT_FACTOR = 0.95
EPISODES = 500
EPSILON_START = 1.0
EPSILON_END = 0.05

random.seed(42)
np.random.seed(42)
Q = np.zeros((NUM_STATES, NUM_ACTIONS), dtype=float)


for episode in range(EPISODES):
    state = 0
    epsilon = EPSILON_END + (EPSILON_START - EPSILON_END) * (1 - episode / EPISODES)

    while state != GOAL_STATE:
        if random.random() < epsilon:
            action = random.randrange(NUM_ACTIONS)
        else:
            action = int(np.argmax(Q[state]))

        if action == 0:
            next_state = max(0, state - 1)
        else:
            next_state = min(GOAL_STATE, state + 1)

        reward = 10.0 if next_state == GOAL_STATE else -0.1
        Q[state, action] += LEARNING_RATE * (
            reward
            + DISCOUNT_FACTOR * np.max(Q[next_state])
            - Q[state, action]
        )
        state = next_state

print("Trained Q-Table (State x Action):")
print(np.round(Q, 3))

print("Optimal learned policy:")
for state in range(NUM_STATES):
    action = int(np.argmax(Q[state]))
    print(f"State {state}: {'left' if action == 0 else 'right'}")
