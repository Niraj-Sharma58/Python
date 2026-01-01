from picamera2 import Picamera2
import time
from datetime import datetime
import os

# Folder to save images
SAVE_DIR = "/home/pi/Pictures/pi_dual_camera"
os.makedirs(SAVE_DIR, exist_ok=True)

try:
    # Initialize cameras
    cam0 = Picamera2(camera_num=0)
    cam1 = Picamera2(camera_num=1)

    # Configure for still capture
    cam0.configure(cam0.create_still_configuration())
    cam1.configure(cam1.create_still_configuration())

    # Start cameras
    cam0.start()
    cam1.start()

    # Give cameras time to warm up
    time.sleep(2)

    # Timestamp for filenames
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Capture images
    cam0.capture_file(f"{SAVE_DIR}/camera0_{ts}.jpg")
    cam1.capture_file(f"{SAVE_DIR}/camera1_{ts}.jpg")

    print(f"Images saved successfully in {SAVE_DIR}")

finally:
    # Ensure cameras are stopped
    cam0.stop()
    cam1.stop()
