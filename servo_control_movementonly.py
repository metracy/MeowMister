import pyfirmata2
import time
import math
#import select
#import sys
#import threading
# /tmp/servo_control is a FIFO that is read to listen to what's being output for the servo to move to that angle

control_path = '/tmp/servo_control'
#UNO_R4 = '/dev/ttyACM0'
XIAO = '/dev/ttyACM1'

#PORT = pyfirmata2.Arduino.AUTODETECT
#board_UNO_R4 = pyfirmata2.Arduino(UNO_R4)
board = pyfirmata2.Arduino(XIAO)
servo_5 = board.get_pin('d:5:s')
#global i
#i=5 # single shot testing protocol - WTF system

#def fire_pin_2(duration=0.1): # running tests the subject has rapidly aclimated to a line where if crossed he will be under fire
#    """Activates pin 2 for a specified duration."""
#    firing_2.write(1)  
#    time.sleep(duration)  
#    firing_2.write(0) 
#def fire_pin_2(duration=0.25): # will be under fire
#    """Activates pin 2 for a specified duration."""
#    def fire_sequence():
#        print(f"Firing Water Cannon for {duration} seconds.")
#        board_UNO_R4.digital[8].write(1) #turns on HIGH 5V to Pin 8 on arduino uno
#        time.sleep(duration)  # turn on or only default 0.25 sec
#        board_UNO_R4.digital[8].write(0)
#    threading.Thread(target=fire_sequence).start() # launch thread in separate process to avoid blocking

a = 120
while True:
    with open(control_path, 'r') as file:
        for line in file:
            
            x = 45 # offset the x = 45 to match lidar
            try:
                angle = int(math.degrees(float(line))-x) # convert ~ to degree
                if angle == a:
                    pass
                elif 0 <= angle <= 180: # catch
                    print('restarting try loop')
                    print(f"Yes Captain! Moving to {angle+x} Degrees!")
                    servo_5.write(int(angle))
                    #if i % 50 == 0:
                    #    print(f"Shooting Water at {angle+x} Degrees! i={i}")
                    #    fire_pin_2()
                    #i += 1
                time.sleep(0.1)
                a = angle
            except ValueError:
                print("Invalid Degrees Captain!")
                time.sleep(0.5)
            except KeyboardInterrupt:
                print("Aborting Captain. Exiting Program!.")
                board.exit()

        
