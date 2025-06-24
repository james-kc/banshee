# Functions relating to the use of the accelerometer/gyroscope module LGA-14L
# Library found here https://github.com/adafruit/Adafruit_CircuitPython_LSM6DS/tree/main
#
# Datasheet:
# https://www.mouser.co.uk/datasheet/2/744/en_DM00133076-2488588.pdf

import time
import board
from adafruit_lsm6ds.lsm6ds3 import LSM6DS3
from adafruit_lsm6ds import Rate, AccelRange, GyroRange

## Sensor settings
# Gyro range options:
# "RANGE_125_DPS"
# "RANGE_250_DPS"
# "RANGE_500_DPS"
# "RANGE_1000_DPS"
# "RANGE_2000_DPS"

# Accelerometer range options:
# "RANGE_2G"
# "RANGE_16G"
# "RANGE_4G"
# "RANGE_8G"

# Data rate options:
# "RATE_SHUTDOWN"
# "RATE_1_6_HZ"
# "RATE_12_5_HZ"
# "RATE_26_HZ"
# "RATE_52_HZ"
# "RATE_104_HZ"
# "RATE_208_HZ"
# "RATE_416_HZ"
# "RATE_833_HZ"
# "RATE_1_66K_HZ"
# "RATE_3_33K_HZ"
# "RATE_6_66K_HZ"

def initialise_accelerometer():
    """Function used to initialise the accelerometer module."""

    i2c = board.I2C()
    sensor = LSM6DS3(i2c)

    sensor.accelerometer_range = AccelRange.RANGE_16G
    print(f"Accelerometer range set to: {AccelRange.string[sensor.accelerometer_range]} G")

    sensor.gyro_range = GyroRange.RANGE_2000_DPS
    print(f"Gyro range set to: {GyroRange.string[sensor.gyro_range]} DPS")

    # sensor.accelerometer_data_rate = Rate.RATE_1_66K_HZ
    sensor.accelerometer_data_rate = Rate.RATE_3_33K_HZ
    print(f"Accelerometer rate set to: {Rate.string[sensor.accelerometer_data_rate]} HZ")

    # sensor.gyro_data_rate = Rate.RATE_1_66K_HZ
    sensor.gyro_data_rate = Rate.RATE_3_33K_HZ
    print(f"Gyro rate set to: {Rate.string[sensor.gyro_data_rate]} HZ")

    return sensor

def get_acceleration(sensor):
    return sensor.acceleration

def get_gyro(sensor):
    return sensor.gyro


def main():
    sensor = initialise_accelerometer()

    while True:
        # print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
        # print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (sensor.gyro))
        print(get_acceleration(sensor))
        print(get_gyro(sensor))
        print("")
        time.sleep(0.5)

if __name__ == '__main__':
    main()