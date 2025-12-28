from gpiozero import Servo
from time import sleep

# Equivalent of: Servo myServo;
myServo = Servo(
    18,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025
)

# Equivalent of: void setup()
sleep(1)

# Equivalent of: void loop()
while True:

    # for (int angle = 0; angle <= 120; angle++)
    for angle in range(0, 121):
        # myServo.write(angle);
        myServo.value = (angle / 90) - 1
        sleep(0.015 )   # delay(15)

    sleep(1)   # delay(1000)

    # for (int angle = 120; angle >= 0; angle--)
    for angle in range(120, -1, -1):
        myServo.value = (angle / 90) - 1
        sleep(0.015)

    sleep(1)
