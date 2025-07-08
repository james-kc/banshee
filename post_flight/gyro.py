import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# === Load & Prepare Data ===
df = pd.read_csv("post_flight/data/accelerometer.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y %H:%M:%S.%f')

dt = df['timestamp'].diff().dt.total_seconds().fillna(0).values
acc = df[['accel_x', 'accel_y', 'accel_z']].values
gyro = df[['gyro_x', 'gyro_y', 'gyro_z']].values

# === Estimate Orientation (Pitch & Roll) ===
pitch, roll = 0.0, 0.0
alpha = 0.98
pitch_list, roll_list = [], []

for i in range(len(df)):
    ax, ay, az = acc[i]
    gx, gy, gz = gyro[i]
    dT = dt[i]

    acc_pitch = np.arctan2(ay, np.sqrt(ax**2 + az**2))
    acc_roll = np.arctan2(-ax, az)

    pitch += gy * dT
    roll += gx * dT

    pitch = alpha * pitch + (1 - alpha) * acc_pitch
    roll = alpha * roll + (1 - alpha) * acc_roll

    pitch_list.append(pitch)
    roll_list.append(roll)

# === Define Cube Model ===
cube_vertices = np.array([
    [1, 1, 1], [1, 1, -1], [1, -1, -1], [1, -1, 1],
    [-1, 1, 1], [-1, 1, -1], [-1, -1, -1], [-1, -1, 1]
])

cube_edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# === Rotation Function ===
def rotation_matrix(pitch, roll):
    cp, sp = np.cos(pitch), np.sin(pitch)
    cr, sr = np.cos(roll), np.sin(roll)

    Rx = np.array([[1, 0, 0],
                   [0, cp, -sp],
                   [0, sp, cp]])

    Ry = np.array([[cr, 0, sr],
                   [0, 1, 0],
                   [-sr, 0, cr]])

    return Ry @ Rx

# === Plot Setup ===
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Initial cube
initial_rotated = cube_vertices @ rotation_matrix(pitch_list[0], roll_list[0]).T
lines = []
for i, j in cube_edges:
    line, = ax.plot(*zip(initial_rotated[i], initial_rotated[j]), 'k')
    lines.append(line)

ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([-2, 2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# === Frame Skipping ===
source_rate = 250  # Hz
target_fps = 30    # Target visual frame rate
step = max(1, int(source_rate / target_fps))  # How many samples to skip
frame_indices = range(0, len(df), step)

# === Animation Function ===
def update(frame_idx):
    idx = frame_indices[frame_idx]
    R = rotation_matrix(pitch_list[idx], roll_list[idx])
    rotated = cube_vertices @ R.T

    for line, (i, j) in zip(lines, cube_edges):
        x, y, z = zip(rotated[i], rotated[j])
        line.set_data(x, y)
        line.set_3d_properties(z)

    ax.set_xlim([-2, 2])
    ax.set_ylim([-2, 2])
    ax.set_zlim([-2, 2])

    elapsed_sec = (df['timestamp'].iloc[idx] - df['timestamp'].iloc[0]).total_seconds()
    ax.set_title(f"Time: {elapsed_sec:.2f} s")

    return lines

# === Run Animation ===
ani = FuncAnimation(
    fig,
    update,
    frames=len(frame_indices),
    interval=1000 / target_fps,  # ms between frames
    blit=False
)

plt.tight_layout()
plt.show()
