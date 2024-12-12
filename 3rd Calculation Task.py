import numpy as np
import matplotlib.pyplot as plt

# Constants
beta = 0.05  # photon loss in fiber (km^-1)
eta = 0.1  # quantum efficiency of detectors
fd = 10  # dark event frequency (Hz)
Tp = 0.5  # Polarizer transmission efficiency
n0_values = [2e7, 2e10]  # photon emission rates (photons/s)
max_distance = 100  # maximum distance (km)
distances = np.linspace(0, max_distance, 50000)  # distances to calculate (km)

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

# Calculate photon transfer rate, QBER, and secret bit rate for Polarizer setup
results_polarizer = {}
for n0 in n0_values:
    pt_polarizer = n0 * eta * Tp * 10 ** (-beta * distances)  # Adjusted photon transfer rate with polarizer
    delta_polarizer = fd / (pt_polarizer + fd)  # QBER
    h2_polarizer = binary_entropy(delta_polarizer)  # Binary entropy
    secret_rate_polarizer = np.maximum(1 - 2 * h2_polarizer, 0)  # Secret bit rate
    results_polarizer[n0] = {"pt": pt_polarizer, "delta": delta_polarizer, "secret_rate": secret_rate_polarizer}

# Find maximum secure distances for Polarizer setup
max_distances_polarizer = {}
for n0 in n0_values:
    max_distances_polarizer[n0] = find_max_secure_distance(results_polarizer[n0]["delta"], distances)

# Print maximum secure distances for Polarizer setup
print("Maximum Secure Communication Distances (Polarizer setup):")
for n0, distance in max_distances_polarizer.items():
    print(f"n0 = {n0:.1e} photons/s: {distance:.2f} km")

plt.figure(figsize=(6,4))
for n0, data in results_polarizer.items():
    plt.plot(distances, data["secret_rate"], label=f"n0 = {n0:.1e}")
plt.axhline(0.11, color='Red', linestyle='solid', label="QBER Threshold (11%)")
plt.title("Secret Bit Rate vs Distance (Polarizer setup)")
plt.xlabel("Distance (km)")
plt.ylabel("Secret Bit Rate")
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
