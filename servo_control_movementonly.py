import pyfirmata2
import time
import math

# /tmp/servo_control is a FIFO that is read to listen to what's being output for the servo to move to that angle

servo = '/tmp/servo_control'

# Seeeduino XIAO Location
XIAO = '/dev/ttyACM1'

board = pyfirmata2.Arduino(XIAO)
servo_5 = board.get_pin('d:5:s')

a = 120 # Start Value for a
while True:
    with open(control_path, 'r') as file:
        for line in file:
            
            x = 45 # offset the angle to match location of Lidar
            try:
                angle = int(math.degrees(float(line))-x) # convert ~ to degree
                if angle == a:
                    pass # Skip Iteration if read angle isn't different from last time.
                elif 0 <= angle <= 180: # catch
                    print('restarting try loop')
                    print(f"Yes Captain! Moving to {angle+x} Degrees!")
                    servo_5.write(int(angle))
                time.sleep(0.1)
                a = angle
            except ValueError:
                print("Invalid Degrees Captain!")
                time.sleep(0.5)
            except KeyboardInterrupt:
                print("Aborting Captain. Exiting Program!.")
                board.exit()

        
