from gpiozero import LED
from time import sleep

# Road 1 LEDs
R1 = LED(13)   # Red
Y1 = LED(12)   # Yellow
G1 = LED(11)   # Green

print("Starting Road 1 LED test...")

while True:
    # Red ON
    print("RED ON")
    R1.on()
    Y1.off()
    G1.off()
    sleep(2)

    # Yellow ON
    print("YELLOW ON")
    R1.off()
    Y1.on()
    G1.off()
    sleep(2)

    # Green ON
    print("GREEN ON")
    R1.off()
    Y1.off()
    G1.on()
    sleep(2)
