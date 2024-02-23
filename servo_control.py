import pyfirmata2
import os
import time
# /tmp/servo_control is a FIFO that is read to listen to what's being output for the servo to move to that angle

control_path = '/tmp/servo_control'

PORT = pyfirmata2.Arduino.AUTODETECT

board = pyfirmata2.Arduino(PORT)
servo_5 = board.get_pin('d:5:s')


while True:
    with open(control_path, 'r') as file:
        for line in file:
            print('restarting try loop')
            x = 45 # offset the x = 45 to match lidar
            try:
                angle = int(float(line)*57.2-x)
                if 0 <= angle <= 180:
                    print(f"Yes Captain! Moving to {angle+x} Degrees!")
                    servo_5.write(str(angle))
                time.sleep(0.1)
            except ValueError:
                print("Invalid Degrees Captain!")
                time.sleep(0.5)
            except KeyboardInterrupt:
                print("Aborting Captain. Exiting Program!.")
                board.exit()
