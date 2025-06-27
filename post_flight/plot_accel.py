import pandas as pd
import matplotlib.pyplot as plt

# Cargar CSV
df = pd.read_csv("post_flight/data/accelerometer.csv")

# Convertir el timestamp a datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y %H:%M:%S.%f')

# Compute time differences between samples
deltas = df['timestamp'].diff().dropna().dt.total_seconds()

# Average interval and sample rate
avg_interval = deltas.mean()
sample_rate = 1 / avg_interval

print(f"Average sampling interval: {avg_interval:.6f} seconds")
print(f"Estimated sample rate: {sample_rate:.2f} Hz")

# Crear figura con subplots
fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

# Plot acelerómetro
axs[0].plot(df['timestamp'], df['accel_x'], label='Accel X')
axs[0].plot(df['timestamp'], df['accel_y'], label='Accel Y')
axs[0].plot(df['timestamp'], df['accel_z'], label='Accel Z')
axs[0].set_ylabel('Acceleration (m/s²)')
axs[0].set_title('Accelerometer')
axs[0].legend()

# Plot giroscopio
axs[1].plot(df['timestamp'], df['gyro_x'], label='Gyro X')
axs[1].plot(df['timestamp'], df['gyro_y'], label='Gyro Y')
axs[1].plot(df['timestamp'], df['gyro_z'], label='Gyro Z')
axs[1].set_ylabel('Angular Velocity (rad/s)')
axs[1].set_title('Gyroscope')
axs[1].legend()

# Ajustes de formato
axs[1].set_xlabel('Time')
fig.autofmt_xdate()
plt.tight_layout()
plt.show()