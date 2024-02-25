import pyfirmata2
import os
import time
# /tmp/servo_control is a FIFO that is read to listen to what's being output for the servo to move to that angle

control_path = '/tmp/servo_control'

PORT = pyfirmata2.Arduino.AUTODETECT

board = pyfirmata2.Arduino(PORT)
servo_5 = board.get_pin('d:5:s')
firing_6 = board.get_pin('d:6:o')
i=0
def fire_pin_6(duration=0.1): # running tests the subject has rapidly aclimated to a line where if crossed he will be under fire
    """Activates pin 6 for a specified duration."""
    firing_6.write(duration)  
    time.sleep(duration)  
    firing_6.write(0) 

while True:
    with open(control_path, 'r') as file:
        for line in file:
            print('restarting try loop')
            x = 45 # offset the x = 45 to match lidar
            try:
                angle = int(float(line)*57.2-x)
                print(angle)
                if 0 <= angle <= 180:
                    print(f"Yes Captain! Moving to {angle+x} Degrees!")
                    servo_5.write(str(angle))
                    if i == 0:
                        fire_pin_6(1)
                        i = 1
                time.sleep(0.1)
            except ValueError:
                print("Invalid Degrees Captain!")
                time.sleep(0.5)
            except KeyboardInterrupt:
                print("Aborting Captain. Exiting Program!.")
                board.exit()

        
