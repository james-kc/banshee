import pandas as pd
from matplotlib import pyplot as plt

import banshee_tools as bt

DATA_DIR = 'post_flight/data/accelerometer.csv'

def accel_plot(df: pd.DataFrame, trim: str = 'flight'):
    bt.multi_line_plotter(df, 'timestamp', ['accel_x', 'accel_y', 'accel_z'], trim)

def gyro_plot(df: pd.DataFrame, trim: str = 'flight'):
    bt.multi_line_plotter(df, 'timestamp', ['gyro_x', 'gyro_y', 'gyro_z'], trim)

def gyro_plot_integrated(df: pd.DataFrame, trim: str = 'ascent'):

    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d/%m/%Y %H:%M:%S.%f')

    filtered_df = bt.data_trimmer(df, 'timestamp', trim)
    
    # Calculate the time difference between each row
    filtered_df['dt'] = filtered_df['timestamp'].diff().dt.total_seconds()

    filtered_df['angle_change_x_deg'] = filtered_df['gyro_x'] * filtered_df['dt']
    filtered_df['angle_change_y_deg'] = filtered_df['gyro_y'] * filtered_df['dt']
    filtered_df['angle_change_z_deg'] = filtered_df['gyro_z'] * filtered_df['dt']
    filtered_df['angle_change_x_deg'] = filtered_df['angle_change_x_deg'].fillna(0)
    filtered_df['angle_change_y_deg'] = filtered_df['angle_change_y_deg'].fillna(0)
    filtered_df['angle_change_z_deg'] = filtered_df['angle_change_z_deg'].fillna(0)

    filtered_df['angle_x_deg'] = filtered_df['angle_change_x_deg'].cumsum()
    filtered_df['angle_y_deg'] = filtered_df['angle_change_y_deg'].cumsum()
    filtered_df['angle_z_deg'] = filtered_df['angle_change_z_deg'].cumsum()

    bt.multi_line_plotter(filtered_df, 'timestamp', ['angle_x_deg', 'angle_y_deg', 'angle_z_deg'], trim)

def main():
    df = pd.read_csv(DATA_DIR)
    accel_plot(df, 'ascent')
    # gyro_plot(df, 'flight')
    # gyro_plot_integrated(df, 'ascent')
    plt.show()

if __name__ == '__main__':
    main()