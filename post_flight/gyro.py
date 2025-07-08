from vpython import box, vector, rate, scene
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv("post_flight/data/accelerometer.csv")
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y %H:%M:%S.%f')

dt = df['timestamp'].diff().dt.total_seconds().fillna(0).values
acc = df[['accel_x', 'accel_y', 'accel_z']].values
gyro = df[['gyro_x', 'gyro_y', 'gyro_z']].values

# Complementary filter parameters
alpha = 0.98
pitch = 0.0
roll = 0.0

pitch_list = []
roll_list = []

# Precompute pitch and roll estimates
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

# Create a 3D box
b = box(length=2, height=1, width=1, color=vector(0.2,0.6,0.8), opacity=0.8)

# VPython scene setup
scene.title = "3D Orientation Visualizer"
scene.width = 800
scene.height = 600
scene.autoscale = False
scene.range = 3

# Rotation helper function
def get_rotation_matrix(pitch, roll):
    cp, sp = np.cos(pitch), np.sin(pitch)
    cr, sr = np.cos(roll), np.sin(roll)

    Rx = np.array([[1, 0, 0],
                   [0, cp, -sp],
                   [0, sp, cp]])

    Ry = np.array([[cr, 0, sr],
                   [0, 1, 0],
                   [-sr, 0, cr]])

    return Ry @ Rx

# Playback loop
for i in range(len(df)):
    rate(250)  # limit to 250 loops per second

    R = get_rotation_matrix(pitch_list[i], roll_list[i])

    # VPython’s box axis and up vectors:
    # axis = direction box’s length points (default (1,0,0))
    # up = direction box’s height points (default (0,1,0))

    # Rotate the default axis (1,0,0) and up (0,1,0)
    axis_vec = vector(*R @ np.array([1,0,0]))
    up_vec = vector(*R @ np.array([0,1,0]))

    b.axis = axis_vec
    b.up = up_vec

    # Optional: show time in the window title
    elapsed = (df['timestamp'].iloc[i] - df['timestamp'].iloc[0]).total_seconds()
    scene.title = f"3D Orientation Visualizer — Time: {elapsed:.3f} s"
