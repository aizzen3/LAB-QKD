import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set the data path
data_path = "."

# Preprocess data function
def preprocess_data(file_path):
    data = pd.read_csv(file_path, sep=';')
    data.columns = ['ROW', 'BASIS', 'BITVALUE', 'DET?']
    return data

# Calculate QBER function
def calculate_qber(alice_data, bob_data):
    alice_filtered = alice_data[alice_data['DET?'] == 'Y']
    bob_filtered = bob_data[bob_data['DET?'] == 'Y']
    alice_filtered.reset_index(drop=True, inplace=True)
    bob_filtered.reset_index(drop=True, inplace=True)
    merged_data = pd.merge(alice_filtered, bob_filtered, on="ROW", suffixes=('_alice', '_bob'))
    matching_bases = merged_data[merged_data['BASIS_alice'] == merged_data['BASIS_bob']]
    total_bits = len(matching_bases)
    error_bits = sum(matching_bases['BITVALUE_alice'] != matching_bases['BITVALUE_bob'])
    qber = (error_bits / total_bits) * 100 if total_bits > 0 else 0
    return qber, total_bits, error_bits

# Data references
# Diode currents
diode_currents = [100, 20, 40, 60, 80]  # mA
current_groups = [
    range(13, 16),  # 100 mA
    range(16, 19),  # 20 mA
    range(19, 22),  # 40 mA
    range(22, 25),  # 60 mA
    range(25, 28),  # 80 mA
]

# Pulse lengths
pulse_lengths = [2, 4, 6, 8, 10]  # μs
pulse_groups = [
    range(28, 31),  # 2 μs
    range(31, 34),  # 4 μs
    range(34, 37),  # 6 μs
    range(37, 41),  # 8 μs
    range(41, 44),  # 10 μs
]

# Helper function to calculate stats
def calculate_stats(group_qber):
    mean = np.mean(group_qber)
    std_dev = np.std(group_qber, ddof=1)  # Sample standard deviation
    ci = 1.645 * std_dev / np.sqrt(len(group_qber))  # 90% confidence interval
    return mean, ci

# Calculate QBER for diode currents
qber_diode = []
ci_diode = []
for group in current_groups:
    group_qber = []
    for i in group:
        alice_file = f"{data_path}/Alice_{i:02d}.csv"
        bob_file = f"{data_path}/Bob_{i:02d}.csv"
        alice_data = preprocess_data(alice_file)
        bob_data = preprocess_data(bob_file)
        qber, _, _ = calculate_qber(alice_data, bob_data)
        group_qber.append(qber)
    mean, ci = calculate_stats(group_qber)
    qber_diode.append(mean)
    ci_diode.append(ci)

# Calculate QBER for pulse lengths
qber_pulse = []
ci_pulse = []
for group in pulse_groups:
    group_qber = []
    for i in group:
        alice_file = f"{data_path}/Alice_{i:02d}.csv"
        bob_file = f"{data_path}/Bob_{i:02d}.csv"
        alice_data = preprocess_data(alice_file)
        bob_data = preprocess_data(bob_file)
        qber, _, _ = calculate_qber(alice_data, bob_data)
        group_qber.append(qber)
    mean, ci = calculate_stats(group_qber)
    qber_pulse.append(mean)
    ci_pulse.append(ci)

# Plot QBER vs. Diode Current with 90% CI
plt.figure(figsize=(10, 6))
plt.errorbar(diode_currents, qber_diode, yerr=ci_diode, fmt='o', capsize=5, label='QBER with 90% CI', color='blue')
plt.title('QBER vs. Diode Current')
plt.xlabel('Diode Current (mA)')
plt.ylabel('QBER (%)')
plt.grid()
plt.legend()
plt.show()

# Plot QBER vs. Pulse Length with 90% CI
plt.figure(figsize=(10, 6))
plt.errorbar(pulse_lengths, qber_pulse, yerr=ci_pulse, fmt='o', capsize=5, label='QBER with 90% CI', color='green')
plt.title('QBER vs. Pulse Length')
plt.xlabel('Pulse Length (μs)')
plt.ylabel('QBER (%)')
plt.grid()
plt.legend()
plt.show()