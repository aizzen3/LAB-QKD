import numpy as np
import matplotlib.pyplot as plt

# Constants
beta = 0.05  # photon loss in fiber (km^-1)
eta = 0.1  # quantum efficiency of detectors
fd = 10  # dark event frequency (Hz)
n0_values = [2e7, 2e10]  # photon emission rates (photons/s)
max_distance = 100  # maximum distance (km)
distances = np.linspace(0, max_distance, 500)  # distances to calculate (km)


# Binary entropy function
def binary_entropy(delta):
    return -delta * np.log2(delta) - (1 - delta) * np.log2(1 - delta)


# Calculate photon transfer rate, QBER, and secret bit rate for each n0
results = {}
for n0 in n0_values:
    pt = n0 * eta * 10 ** (-beta * distances)  # Photon transfer rate
    delta = fd / (pt + fd)  # QBER
    h2 = np.where(delta > 0, binary_entropy(delta), 0)  # Avoid log(0) warnings
    secret_rate = np.maximum(1 - 2 * h2, 0)  # Secret bit rate

    results[n0] = {"pt": pt, "delta": delta, "secret_rate": secret_rate}
# Plotting
plt.figure(figsize=(6, 4))
for n0, data in results.items():
    plt.plot(distances, data["pt"], label=f"n0 = {n0:.1e} photons/s")
plt.title("Photon Transfer Rate vs Distance")
plt.xlabel("Distance (km)")
plt.ylabel("Photon Transfer Rate (km/s)")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()
