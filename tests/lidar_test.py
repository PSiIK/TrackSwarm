# Libraries
from adafruit_rplidar import RPLidar

# Constants
PORT_NAME = "/dev/ttyACM1"

# Start lidar
lidar = RPLidar(None, PORT_NAME, timeout=5, baudrate=921600)

# Get information 
print(lidar.info)
print(lidar.health)

# Start motor and clear buffer
lidar.clear_input()
lidar.start_motor()
scan_gen = lidar.iter_scans()

# Run application loop
try:
    while True:
        # Get measurements
        measurements = next(scan_gen)

        for _, angle, distance in measurements:
            print(angle, distance)
finally:
    # Stop lidar
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
