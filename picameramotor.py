from picamera2 import Picamera2
from gpiozero import Servo
from time import sleep
from datetime import datetime
import os

# Folder to save images
SAVE_DIR = "/home/pi/Pictures/pi_dual_camera"
os.makedirs(SAVE_DIR, exist_ok=True)

# Initialize cameras
cam0 = Picamera2(camera_num=0)
cam1 = Picamera2(camera_num=1)
cam0.configure(cam0.create_still_configuration())
cam1.configure(cam1.create_still_configuration())
cam0.start()
cam1.start()
sleep(2)  # warm-up time

# Initialize servo on GPIO 18
myServo = Servo(18, min_pulse_width=0.0005, max_pulse_width=0.0025)
sleep(1)  # initial delay

# Function to capture both cameras
def capture_cameras(angle_label):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    cam0_file = f"{SAVE_DIR}/camera0_{angle_label}_{ts}.jpg"
    cam1_file = f"{SAVE_DIR}/camera1_{angle_label}_{ts}.jpg"
    cam0.capture_file(cam0_file)
    cam1.capture_file(cam1_file)
    print(f"Captured images at {angle_label}°: {cam0_file}, {cam1_file}")

try:
    while True:
        # Move servo to 0° and capture
        myServo.value = -1  # 0° position
        sleep(1)  # give servo time to move
        capture_cameras("0")

        # Move servo to 120° and capture
        myServo.value = (120 / 90) - 1  # convert 120° to gpiozero value
        sleep(1)  # give servo time to move
        capture_cameras("120")

        # Move servo back to 0° for next cycle
        myServo.value = -1
        sleep(1)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    cam0.stop()
    cam1.stop()
