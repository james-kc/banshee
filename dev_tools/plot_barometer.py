import pandas as pd
import matplotlib.pyplot as plt

# Load and parse CSV
df = pd.read_csv("post_flight/data/barometer.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y %H:%M:%S.%f')

# Calculate sampling intervals
deltas = df['timestamp'].diff().dropna().dt.total_seconds()
avg_interval = deltas.mean()
sample_rate = 1 / avg_interval

# Print results
print(f"Average sampling interval: {avg_interval:.6f} seconds")
print(f"Estimated sample rate: {sample_rate:.2f} Hz")

# --- Plot 1: Relative Altitude vs Time ---
plt.figure(figsize=(12, 5))
plt.plot(df['timestamp'], df['relative_altitude'], label='Relative Altitude')
plt.title('Relative Altitude Over Time')
plt.xlabel('Time')
plt.ylabel('Altitude (m)')
plt.grid(True)
plt.tight_layout()
plt.legend()
plt.show()
