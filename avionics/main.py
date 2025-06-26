import threading
from datetime import datetime
import time
import os
import csv
import RPi.GPIO as GPIO
from instruments import gps, barometer, accelerometer

# --- Constants ---
DATA_PATH = 'data'

GPS_DATA_RATE = 1  # Hz
GPS_DATA_PERIOD = 1 / GPS_DATA_RATE  # seconds

# This setting of 2000 is resulting in 11 Hz sample rate in recorded data
BAROMETER_DATA_RATE = 2000  # Hz
BAROMETER_DATA_PERIOD = 1 / BAROMETER_DATA_RATE  # seconds

# This setting of 2000 is resulting in 250 Hz sample rate in recorded data
ACCEL_DATA_RATE = 2000 # Hz
ACCEL_DATA_PERIOD = 1 / ACCEL_DATA_RATE  # seconds

BUZZER_PIN = 4

# --- Setup session folder in /data ---
current_datetime = datetime.now().strftime('%Y%m%dT%H%M%S')
SESSION_DATA_PATH = f"{DATA_PATH}/{current_datetime}"
os.makedirs(SESSION_DATA_PATH, exist_ok=True)

# --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# --- Sensor status flags ---
sensor_ready = {
    'gps': False,
    'barometer': False,
    'accelerometer': False,
}

def check_and_buzz():
    if all(sensor_ready.values()):
        print("All sensors initialized. Buzzing!")
        GPIO.output(BUZZER_PIN, GPIO.HIGH)

def barometer_thread(start_event, stop_event):
    barometer_obj = None
    with open(f"{SESSION_DATA_PATH}/barometer.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'relative_altitude'])

        while not stop_event.is_set():
            if start_event.is_set():
                if not barometer_obj:
                    barometer_obj, baseline = barometer.initialise_bme280()
                    sensor_ready['barometer'] = True
                    check_and_buzz()
                relative_altitude = barometer.get_relative_altitude(barometer_obj, baseline)
                writer.writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"), relative_altitude])
                file.flush()
                time.sleep(BAROMETER_DATA_PERIOD)

def accel_thread(start_event, stop_event):
    accel_obj = None
    with open(f"{SESSION_DATA_PATH}/accelerometer.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z'])

        while not stop_event.is_set():
            if start_event.is_set():
                if not accel_obj:
                    accel_obj = accelerometer.initialise_accelerometer()
                    sensor_ready['accelerometer'] = True
                    check_and_buzz()
                accel_data = accelerometer.get_acceleration(accel_obj)
                gyro_data = accelerometer.get_gyro(accel_obj)
                writer.writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"), *accel_data, *gyro_data])
                file.flush()
                time.sleep(ACCEL_DATA_PERIOD)

def gps_thread(start_event, stop_event):
    gps_obj = None
    with open(f"{SESSION_DATA_PATH}/gps.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            'thread_datetime',
            'datetime',
            'fix',
            'latitude',
            'longitude',
            'latitude_degrees',
            'latitude_minutes',
            'longitude_degrees',
            'longitude_minutes',
            'satellites',
            'altitude_m',
            'speed_knots',
            'track_angle_deg',
            'horizontal_dilution',
            'height_geoid',
        ])

        gps_fix = True

        while not stop_event.is_set():
            if start_event.is_set():
                if not gps_obj:
                    gps_obj = gps.initialise_gps()
                    sensor_ready['gps'] = True
                    check_and_buzz()

                prev_gps_fix = gps_fix
                position, gps_fix = gps.get_position(gps_obj)

                # print GPS fix status message
                if gps_fix != prev_gps_fix:
                    if gps_fix:
                        print("GPS fix acquired.")
                    else:
                        print("Waiting on GPS Fix")

                if gps_fix:
                    writer.writerow([
                        datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f"),
                        position['datetime'],
                        position['fix'],
                        position['latitude'],
                        position['longitude'],
                        position['latitude_degrees'],
                        position['latitude_minutes'],
                        position['longitude_degrees'],
                        position['longitude_minutes'],
                        position['satellites'],
                        position['altitude_m'],
                        position['speed_knots'],
                        position['track_angle_deg'],
                        position['horizontal_dilution'],
                        position['height_geoid'],
                    ])
                    file.flush()

                time.sleep(GPS_DATA_PERIOD)

def main():

    # Buzz the buzzer twice to indicate successful startup
    for i in range(2):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(BUZZER_PIN, GPIO.LOW)    
        time.sleep(0.5)

    # Events to control the threads
    start_event = threading.Event()
    stop_event = threading.Event()
    thread_args = (start_event, stop_event)

    # Create and start threads for image capture and sensor reading
    threads = [
        threading.Thread(target=barometer_thread, args=thread_args),
        threading.Thread(target=accel_thread, args=thread_args),
        threading.Thread(target=gps_thread, args=thread_args),
    ]

    for thread in threads:
        thread.start()

    try:
        while True:
            # Simulate starting and stopping the threads
            command = input("Enter 'start' to start capturing, 'stop' to stop capturing, 'exit' to exit: ").strip().lower()
            if command == 'start':
                start_event.set()
                print("Capture started.")
            elif command == 'stop':
                start_event.clear()
                print("Capture stopped.")
            elif command == 'exit':
                stop_event.set()
                break
    finally:
        for thread in threads:
            thread.join()
        GPIO.cleanup()

if __name__ == '__main__':
    main()
