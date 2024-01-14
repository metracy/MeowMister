import pyfirmata2
import os
import time
#mkfifo /tmp/servo_control listen to what's being output here
# setup
control_path = '/tmp/servo_control'

PORT = pyfirmata2.Arduino.AUTODETECT

board = pyfirmata2.Arduino(PORT)
servo_5 = board.get_pin('d:5:s')



while True:
    with open(control_path, 'r') as file:
        for line in file:
            try: 
                angle = int(line.strip())
                print(f"Yes Captain! Moving to {angle} Degrees!")
                servo_5.write(v)
                time.sleep(0.001)
            except:
                print("Invalid Degrees Captain!")
                time.sleep(0.001)

board.exit()
