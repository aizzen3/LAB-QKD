import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

# QBER measurements (replace with your actual measurements)
qber_measurements = [9.09,13.04,10.71,12.28,11.50,13.04,12.28,9.909,9.909,11.05] #Change qber values according to the calculation
Effective_Length_of_Optical_Fiber = [] #Change the values and naming according to requirement

# Number of measurements
n = len(qber_measurements)

# Calculate mean QBER
mean_qber = np.mean(qber_measurements)

# Calculate standard deviation of QBER
std_qber = np.std(qber_measurements, ddof=1)

# Calculate t-value for 90% confidence level and n-1 degrees of freedom
t_value = stats.t.ppf(1-0.05, df=n-1)

# Calculate margin of error
margin_of_error = t_value * (std_qber / np.sqrt(n))

# Calculate 90% confidence interval
confidence_interval = (mean_qber - margin_of_error, mean_qber + margin_of_error)

print("Mean QBER:", mean_qber)
print("90% Confidence Interval:", confidence_interval)
plt.figure(figsize=(8,6))
plt.plot(range(1,n+1),qber_measurements,'o', label="QBER Values")
plt.axhline(mean_qber, color='r', linestyle='--', label='Mean QBER')
plt.fill_between(Effective_Length_of_Optical_Fiber, confidence_interval[0], confidence_interval[1], color='b', alpha=0.2, label='90% Confidence Interval')
plt.xlabel('Effective Length of Optical Fiber (in km)')
plt.ylabel('QBER Values (in %)')
plt.ylim(-20,45)
plt.title('QBER Measurements vs Length of the Fiber (with 90% Confidence Interval)')
plt.legend()
plt.show()