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
sleep(2)  # warm-up

# Initialize servo
myServo = Servo(18, min_pulse_width=0.0005, max_pulse_width=0.0025)
sleep(1)  # initial delay

# Function to capture one photo per camera
def capture_cameras(angle_label):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    cam0_file = f"{SAVE_DIR}/camera0_{angle_label}_{ts}.jpg"
    cam1_file = f"{SAVE_DIR}/camera1_{angle_label}_{ts}.jpg"
    cam0.capture_file(cam0_file)
    cam1.capture_file(cam1_file)
    print(f"Captured at {angle_label}°: {cam0_file}, {cam1_file}")

# Smooth servo movement
def move_servo_to(target_value, steps=20, delay=0.05):
    """Smoothly move servo from current position to target_value"""
    start_val = myServo.value if myServo.value is not None else 0
    step_size = (target_value - start_val) / steps
    for i in range(steps + 1):
        myServo.value = start_val + step_size * i
        sleep(delay)

# Main loop
try:
    while True:
        # Step 1: Move motor to 0° if not already
        if myServo.value != -1:
            print("Moving motor to 0°...")
            move_servo_to(-1, steps=20, delay=0.05)

        # Step 2: Wait 5 seconds
        print("Waiting 5 seconds before capture at 0°...")
        sleep(5)

        # Step 3: Capture images at 0°
        capture_cameras("0")

        # Step 4: Rest 3 seconds
        sleep(3)

        # Step 5: Move motor to 120° (0.333 in servo.value)
        print("Moving motor to 120°...")
        move_servo_to(0.333, steps=20, delay=0.05)

        # Step 6: Wait 5 seconds
        print("Waiting 5 seconds before capture at 120°...")
        sleep(5)

        # Step 7: Capture images at 120°
        capture_cameras("120")

        # Step 8: Rest 50 seconds before next cycle
        print("Cycle complete. Waiting 50 seconds before next cycle...")
        sleep(50)

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    cam0.stop()
    cam1.stop()
