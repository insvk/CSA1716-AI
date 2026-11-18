import numpy as np
import random

# Simple 1D Environment: States 0 to 4. Goal is state 4.
# Actions: 0 (move left), 1 (move right)
NUM_STATES = 5
NUM_ACTIONS = 2
Q = np.zeros((NUM_STATES, NUM_ACTIONS))

learning_rate = 0.8
discount_factor = 0.95
epochs = 200

# Training the RL Agent using Q-Learning
for _ in range(epochs):
    state = 0 # Start state
    while state != 4: # While goal not reached
        # Epsilon-greedy action selection
        if random.uniform(0, 1) < 0.1:
            action = random.choice([0, 1])
        else:
            action = np.argmax(Q[state])
        
        # Environment transition
        next_state = max(0, state - 1) if action == 0 else min(NUM_STATES - 1, state + 1)
        reward = 1 if next_state == 4 else 0
        
        # Q-value update
        Q[state, action] = Q[state, action] + learning_rate * (
            reward + discount_factor * np.max(Q[next_state]) - Q[state, action]
        )
        state = next_state

print("Trained Q-Table (State x Action):\n", np.round(Q, 3))
print("Optimal policy prefers moving right (action 1) to reach state 4.")
