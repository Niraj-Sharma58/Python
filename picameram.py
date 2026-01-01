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
def capture_cameras(angle_label, num_photos=2, interval=5):
    for i in range(num_photos):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        cam0_file = f"{SAVE_DIR}/camera0_{angle_label}_{i+1}_{ts}.jpg"
        cam1_file = f"{SAVE_DIR}/camera1_{angle_label}_{i+1}_{ts}.jpg"
        cam0.capture_file(cam0_file)
        cam1.capture_file(cam1_file)
        print(f"Captured images at {angle_label}° ({i+1}/{num_photos}): {cam0_file}, {cam1_file}")
        if i < num_photos - 1:
            sleep(interval)  # wait between multiple photos

# Function to move servo slowly
def move_servo(start_val, end_val, steps=20, delay=0.5):
    step_size = (end_val - start_val) / steps
    for i in range(steps + 1):
        myServo.value = start_val + step_size * i
        sleep(delay)

try:
    while True:
        print("Waiting 5 seconds before first capture...")
        sleep(5)

        # Move to 0° and capture 2 photos
        move_servo(myServo.value or 0, -1, steps=10, delay=0.5)  # smooth move to 0°
        capture_cameras("0", num_photos=2, interval=5)

        # Rotate to 120° slowly
        move_servo(-1, 0.333, steps=20, delay=0.5)  # 120° = 0.333 in servo value
        capture_cameras("120", num_photos=2, interval=5)

        # Move back to 0° slowly
        move_servo(0.333, -1, steps=20, delay=0.5)

        # Pause 50 seconds before next cycle
        print("Cycle complete. Pausing for 50 seconds...")
        sleep(50)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    cam0.stop()
    cam1.stop()
