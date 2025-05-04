#task 4 - lab 08

import numpy as np

#define weather states and transition probabilities
states = ["Sunny", "Cloudy", "Rainy"]
transition_matrix = np.array([
    [0.7, 0.2, 0.1],  # P(next | Sunny)
    [0.3, 0.4, 0.3],  # P(next | Cloudy)
    [0.2, 0.3, 0.5]   # P(next | Rainy)
])

def simulate_weather(initial_state, days):
    current = initial_state
    sequence = [current]
    for _ in range(days):
        idx = states.index(current)
        current = np.random.choice(states, p=transition_matrix[idx])
        sequence.append(current)
    return sequence

def estimate_prob_at_least_rainy(initial_state, days, threshold, simulations=10000):
    rainy_counts = []
    for _ in range(simulations):
        seq = simulate_weather(initial_state, days)
        rainy_counts.append(seq.count("Rainy"))
    return np.mean([count >= threshold for count in rainy_counts])

#parameters
initial_state = "Sunny"
num_days = 10
rainy_threshold = 3
num_simulations = 10000

#run one sequence
seq = simulate_weather(initial_state, num_days)
print(f"weather over {num_days} days starting from {initial_state}:")
print(" -> ".join(seq))

#estimate probability
prob = estimate_prob_at_least_rainy(initial_state, num_days, rainy_threshold, num_simulations)
print(f"\nprobability of at least {rainy_threshold} rainy days: {prob:.4f}")
