import os
import time
import random

# angle file where angle is written
servo_control = '/tmp/servo_control'

try:
    with open(servo_control, 'w') as file:
        while True:
            # Making up an ANGLE as Captain!
            angle = random.randint(0, 180)
            print(f"Writing angle: {angle}")
            file.write(f"{angle}\n")
            file.flush()
            print(f"Your orders are to go to {angle} Degree! Make it so!")
            time.sleep(1)
except KeyboardInterrupt:
    print("Aborting fifo test! Abandon Ship!")