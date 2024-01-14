import pyfirmata2
import os
import time
# /tmp/servo_control is a FIFO that is read to listen to what's being output for the servo to move to that angle


control_path = '/tmp/servo_control'

PORT = pyfirmata2.Arduino.AUTODETECT

board = pyfirmata2.Arduino(PORT)
servo_5 = board.get_pin('d:5:s')



try:
    while True:
        with open(control_path, 'r') as file:
            for line in file:
                try: 
                    angle = int(line)
                    print(f"Yes Captain! Moving to {angle} Degrees!")
                    servo_5.write(angle)
                    time.sleep(0.001)
                except ValueError:
                    print("Invalid Degrees Captain!")
                    time.sleep(0.001)
except KeyboardInterrupt:
    print("Aborting Captain. Exiting Program!.")
    board.exit()