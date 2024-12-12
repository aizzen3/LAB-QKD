import numpy as np
import matplotlib.pyplot as plt

# Constants
beta = 0.05  # photon loss in fiber (km^-1)
eta = 0.1  # quantum efficiency of detectors
fd = 10  # dark event frequency (Hz)
Tp = 0.5  # Polarizer transmission efficiency
n0_values = [2e7, 2e10]  # photon emission rates (photons/s)
max_distance = 100  # maximum distance (km)
distances = np.linspace(0, max_distance, 500)  # distances to calculate (km)

# Binary entropy function
def binary_entropy(delta):
    delta = np.clip(delta, 1e-12, 1 - 1e-12)  # Avoid log(0) warnings
    return -delta * np.log2(delta) - (1 - delta) * np.log2(1 - delta)

# Function to find the maximum secure distance
def find_max_secure_distance(delta_values, distances, threshold=0.11):
    secure_indices = np.where(delta_values <= threshold)[0]  # Indices where QBER is below the threshold
    if len(secure_indices) > 0:
        return distances[secure_indices[-1]]  # Maximum distance with secure QBER
    else:
        return 0  # No secure distance

# Calculate photon transfer rate, QBER, and secret bit rate for PBS and Polarizer setups
results_pbs = {}
results_polarizer = {}
for n0 in n0_values:
    # PBS setup
    pt_pbs = n0 * eta * 10 ** (-beta * distances)  # Photon transfer rate
    delta_pbs = fd / (pt_pbs + fd)  # QBER
    h2_pbs = binary_entropy(delta_pbs)  # Binary entropy
    secret_rate_pbs = np.maximum(1 - 2 * h2_pbs, 0)  # Secret bit rate
    results_pbs[n0] = {"pt": pt_pbs, "delta": delta_pbs, "secret_rate": secret_rate_pbs}

    # Polarizer setup
    pt_polarizer = n0 * eta * Tp * 10 ** (-beta * distances)  # Adjusted photon transfer rate with polarizer
    delta_polarizer = fd / (pt_polarizer + fd)  # QBER
    h2_polarizer = binary_entropy(delta_polarizer)  # Binary entropy
    secret_rate_polarizer = np.maximum(1 - 2 * h2_polarizer, 0)  # Secret bit rate
    results_polarizer[n0] = {"pt": pt_polarizer, "delta": delta_polarizer, "secret_rate": secret_rate_polarizer}

# Find maximum secure distances for each setup and n0 value
max_distances = {"PBS": {}, "Polarizer": {}}
for n0 in n0_values:
    max_distances["PBS"][n0] = find_max_secure_distance(results_pbs[n0]["delta"], distances)
    max_distances["Polarizer"][n0] = find_max_secure_distance(results_polarizer[n0]["delta"], distances)

# Print maximum secure distances
print("Maximum Secure Communication Distances:")
for setup, distances in max_distances.items():
    print(f"\nSetup: {setup}")
    for n0, distance in distances.items():
        print(f"n0 = {n0:.1e} photons/s: {distance:.2f} km")