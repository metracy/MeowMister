import tkinter as tk
import math
import threading
import time
from xbox360controller import Xbox360Controller
import pyfirmata2
import time

#Linux Device Location
UNO_R3 = '/dev/ttyACM0'

#initialize uno R3 microcontroller
board_UNO_R3 = pyfirmata2.Arduino(UNO_R3)

def fire_pin_8(duration=0.25): # will be under fire
    """Activates pin 8 for a specified duration."""
    print(f"Firing Water Cannon for {duration} seconds.")
    board_UNO_R3.digital[8].write(1) #turns on HIGH 5V to Pin 8 on arduino uno
    time.sleep(duration)  # turn on or only default 0.25 sec
    board_UNO_R3.digital[8].write(0)
    #threading.Thread(target=fire_sequence).start() # launch thread in separate process to avoid blocking

def handle_controller_input():
    try:
        with Xbox360Controller(0, axis_threshold=0.2) as controller:
            while True:
                if controller.button_a.is_pressed:
                    fire_pin_8()

    except KeyboardInterrupt: #
        print("Controller thread interrupted and ending.")

def start_controller_thread():
    controller_thread = threading.Thread(target=handle_controller_input)
    controller_thread.daemon = True
    controller_thread.start()

root = tk.Tk() #Make main window
root.title("Servo Control Instructions") #Window title
label_text = "TGZ Gamepad Left Axis to move, Press A to Pay Respects" #
instructions = tk.Label(root, text=label_text, font=('Helvetica', 12))
instructions.pack(pady=20)

# Spin up controller thread
start_controller_thread()

# Default main event loop for the tkinter GUI. Makes
root.mainloop()
