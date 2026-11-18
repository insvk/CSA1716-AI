import numpy as np

rng = np.random.default_rng(42)
states = ["Sunny", "Rainy"]
transition_matrix = np.array([
    [0.8, 0.2],
    [0.4, 0.6],
])

current_state = 0
num_events = 10
print(f"Markov Chain Sequence Prediction for {num_events} events:")

sequence = []
for event in range(1, num_events + 1):
    sequence.append(states[current_state])
    print(f"Event {event}: {states[current_state]}")
    current_state = int(rng.choice([0, 1], p=transition_matrix[current_state]))

print("Predicted sequence:", " -> ".join(sequence))
