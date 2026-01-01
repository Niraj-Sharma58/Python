from gpiozero import LED
from time import sleep

# -------- Road 1 --------
R1 = LED(13)
Y1 = LED(12)
G1 = LED(11)

# -------- Road 2 --------
R2 = LED(10)
Y2 = LED(9)
G2 = LED(8)

# -------- Road 3 --------
R3 = LED(7)
Y3 = LED(6)
G3 = LED(5)

# -------- Road 4 --------
R4 = LED(4)
Y4 = LED(3)
G4 = LED(2)

# -------- Loop (Equivalent to Arduino loop()) --------
while True:

    # ---- Phase 1 ----
    # Road 1 & 3 GREEN
    G1.on()
    G3.on()
    R2.on()
    R4.on()
    sleep(15)

    # Yellow transition
    G1.off()
    G3.off()
    Y1.on()
    Y3.on()
    sleep(15)

    Y1.off()
    Y3.off()
    R1.on()
    R3.on()
    R2.off()
    R4.off()

    # ---- Phase 2 ----
    # Road 2 & 4 GREEN
    G2.on()
    G4.on()
    sleep(15)

    # Yellow transition
    G2.off()
    G4.off()
    Y2.on()
    Y4.on()
    sleep(15)

    Y2.off()
    Y4.off()
    # R2.on()
    # R4.on()
    R1.off()
    R3.off()
