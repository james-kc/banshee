import pandas as pd
import matplotlib.pyplot as plt

# Load GPS data
df = pd.read_csv("post_flight/data/gps.csv")

# Convert timestamps
df['thread_datetime'] = pd.to_datetime(df['thread_datetime'], format='%d/%m/%Y %H:%M:%S.%f')


# Compute sampling intervals
gps_deltas = df['thread_datetime'].diff().dropna().dt.total_seconds()
gps_avg_interval = gps_deltas.mean()
gps_sample_rate = 1 / gps_avg_interval

# Print results
print(f"Average GPS sampling interval: {gps_avg_interval:.6f} seconds")
print(f"Estimated GPS sample rate: {gps_sample_rate:.2f} Hz")

# Convert timestamps
times = (df['thread_datetime'] - df['thread_datetime'].min()).dt.total_seconds()

# Normalize for colormap
norm = plt.Normalize(times.min(), times.max())
cmap = plt.colormaps['viridis']

# Plot with color gradient
plt.figure(figsize=(8, 8))
for i in range(len(df) - 1):
    plt.plot(
        df['longitude'].iloc[i:i+2], 
        df['latitude'].iloc[i:i+2], 
        color=cmap(norm(times.iloc[i]))
    )
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('GPS Track Colored by Time')
plt.axis('equal')
plt.grid(True)
plt.tight_layout()
plt.show()
