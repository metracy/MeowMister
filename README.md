# MeowMister
 
MeowMister is a program to control a turret to focus on an object if it meets the criteria for distance from source of lidar. It utilizes pyfirmata2, a FirmataExpress sketch ( and opencv to control a servo to rotate the turret).  I am using FirmataExpress module that includes the boards.h that adds support for the Seeed XAIO m0 board. Now using small lidar device for controlling direction of turret.
![animated](https://github.com/metracy/MeowMister/assets/12073647/369f0b9b-114d-45e2-a6dd-8e855cca93e6)

02/22/2024
Added old open cv tracking servo, not using it currently. Am using LD19 module with https://github.com/henjin0/LIDAR_LD06_python_loder/blob/main/README_en.md lidar calculator for python. Adapted it to support displaying lidar set in the bottom right
corner of a hallway and using matplotlib to draw the details of the incoming data from a LD19 to serial-USB converter.
01-23-2024
Added shell script to start the processes and launch servo_control.py and target_acquisition.py
