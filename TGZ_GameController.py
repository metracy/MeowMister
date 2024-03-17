import tkinter as tk
import math
import threading
import time
from xbox360controller import Xbox360Controller
import pyfirmata2
import os # relict to when fifo was used for lidar
import time


UNO_R4 = '/dev/ttyACM0'
XIAO = '/dev/ttyACM1'

board_XIAO = pyfirmata2.Arduino(XIAO)
board_UNO_R4 = pyfirmata2.Arduino(UNO_R4)
servo_Z_pin_6 = board_XIAO.get_pin('d:6:s')
servo_X_pin_5 = board_XIAO.get_pin('d:5:s')


servo_control = '/tmp/servo_control' # this line not used, it's for fifo lidar
rad = 0.0174533  # radian in one degree
servo_Z = 0  # Initial servo_Z position in radians.
servo_X = math.pi / 2 # Initial servo_X position in radians.
def fire_pin_2(duration=0.25): # will be under fire
    """Activates pin 2 for a specified duration."""
    def fire_sequence():
        print(f"Firing Water Cannon for {duration} seconds.")
        board_UNO_R4.digital[8].write(1) #turns on HIGH 5V to Pin 8 on arduino uno
        time.sleep(duration)  # turn on or only default 0.25 sec
        board_UNO_R4.digital[8].write(0)
    threading.Thread(target=fire_sequence).start() # launch thread in separate process to avoid blocking

def move_servo_Z(direction):
    global servo_Z
    if direction == 'down':
        servo_Z += rad*2
    elif direction == 'up':
        servo_Z -= rad*2
    print(f"Moving to {servo_Z * 57.2958} degrees")
    servo_Z_pin_6.write(int(max(0, min(180, math.degrees(servo_Z))))) #writing to arduino needs str degrees

def move_servo_X(direction):
    global servo_X
    if direction == 'left':
        servo_X += rad*4
    elif direction == 'right':
        servo_X -= rad*4
    print(f"Moving to {math.degrees(servo_X)} degrees")
    servo_X_pin_5.write(int(max(0, min(180, math.degrees(servo_X))))) # Firmata express supports writing 0 to 180 for integer value of servo degree
    

def handle_controller_input():
    try:
        with Xbox360Controller(0, axis_threshold=0.2) as controller:
            while True:
                if controller.button_a.is_pressed:
                    fire_pin_2()

                # Use the left joystick's X-axis to control the servo left/right.
                if controller.axis_l.x < 0:
                    move_servo_X('left')
                elif controller.axis_l.x > 0:
                    move_servo_X('right')

                # Use TGZ right joystick (currently down on my end from wiring issues)
                if controller.axis_r.y < 0:
                    move_servo_Z('up')
                elif controller.axis_r.y > 0:
                    move_servo_Z('down') 
                time.sleep(0.05)
    except KeyboardInterrupt: #
        print("Controller thread interrupted and ending.")

def start_controller_thread():
    controller_thread = threading.Thread(target=handle_controller_input)
    controller_thread.daemon = True
    controller_thread.start()

root = tk.Tk()
root.title("Servo Control Instructions")
label_text = "TGZ Gamepad Left Axis to move, Press A to Pay Respects"
instructions = tk.Label(root, text=label_text, font=('Helvetica', 12))
instructions.pack(pady=20)

# Spin up controller thread
start_controller_thread()

# Default main event loop for the tkinter GUI. Makes
root.mainloop()
