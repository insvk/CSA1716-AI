import numpy as np

# Basic Markov Chain for weather prediction
states = ["Sunny", "Rainy"]

# Transition Matrix
# Sunny -> Sunny (0.8), Sunny -> Rainy (0.2)
# Rainy -> Sunny (0.4), Rainy -> Rainy (0.6)
transition_matrix = np.array([
    [0.8, 0.2], 
    [0.4, 0.6]
])

current_state = 0 # Start with Sunny
num_days = 10

print(f"Markov Chain Sequence Prediction for {num_days} events:")
for day in range(num_days):
    print(f"Event {day + 1}: {states[current_state]}")
    # Predict next state based on current state's transition probabilities
    current_state = np.random.choice([0, 1], p=transition_matrix[current_state])
