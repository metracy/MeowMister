import tkinter as tk
import math
import pyfirmata2
import os
import time
import select
import sys

servo_control = '/tmp/servo_control'
rad = 0.0174533  # rad in one degree
servo_now = math.pi/2  # Initial servo position in radians.

UNO_R4 = pyfirmata2.Arduino('/dev/ttyACM1')
XIAO = pyfirmata2.Arduino('/dev/ttyACM0')

board = pyfirmata2.Arduino(XIAO)
board2 = pyfirmata2.Arduino(UNO_R4)
firing_2 = board2.get_pin('d:2:o')
servo_6 = board.get_pin('d:6:s')
servo_5 = board.get_pin('d:5:s')

def on_key_press(event):
    global servo_now  # Access global variable.
    # detect key being pressed
    if event.keysym == 'Left':
        move_servo('left')
    elif event.keysym == 'Right':
        move_servo('right')
    elif event.keysym == 'f':
        fire_pin_2()

def write_to_fifo(angle):
    # Write angle data to FIFO.
    try:
        with open(servo_control, 'w') as fifo:
            fifo.write(f'{angle}\n')
            fifo.flush()
    except Exception as e:
        print(f"Error writing to FIFO: {e}")

def fire_pin_2(duration=0.1): # running tests the subject has rapidly aclimated to a line where if crossed he will be under fire
    """Activates pin 2 for a specified duration."""
    firing_2.write(duration)  
    time.sleep(duration)  
    firing_2.write(0) 
def on_key_press(event):
    global servo_now  # Access global variable.
    # detect key being pressed
    if event.keysym == 'Left':
        move_servo('left')
    elif event.keysym == 'Right':
        move_servo('right')
    elif event.keysym == 'f':
        fire_pin_2(0.1)
def move_servo(direction):
    global servo_now  # use the global variable.
    # reassign servo position based on direction from keyboard.
    if direction == 'left':
        servo_now += rad
    else:
        servo_now -= rad
    print(f"moving to {servo_now*57.2+45} degrees")
    write_to_fifo(servo_now)  # Communicate updated position.
    

    
root = tk.Tk()
root.title("Servo Control Instructions")

# Bind key events.
root.bind('<Left>', on_key_press)
root.bind('<Right>', on_key_press)
root.bind('<f>', on_key_press)

# Create a label with instructions.
label_text = "Press Left, Right, Up or Down to Move | Press F to Fire"
instructions = tk.Label(root, text=label_text, font=('Helvetica', 12))
instructions.pack(pady=20)

# Begin main event loop.
root.mainloop()
