# MeowMister
 
MeowMister is a program to control a turret to focus on an object if it meets the criteria for distance from source of lidar. It utilizes pyfirmata2, a FirmataExpress sketch ( and opencv to control a servo to rotate the turret).  I am using FirmataExpress module that includes the boards.h that adds support for the Seeed XAIO m0 board. Now using small lidar device for controlling direction of turret.
![animated](https://github.com/metracy/MeowMister/assets/12073647/aa362e29-e5b7-47d3-bacd-be8ba3df3c56)
![circuit_diagram](https://github.com/metracy/MeowMister/assets/12073647/4ced766c-6f89-4e9b-967f-524543f69b9a)
![Seeeduino-XIAO-pinout-1](https://github.com/metracy/MeowMister/assets/12073647/bf2b7dc1-ec3a-4821-946b-a08e1268069b)


![linedection1](https://github.com/metracy/MeowMister/assets/12073647/aa591002-b9cc-4e0b-ab52-f1eb85b4a12d)
My cat is not pleased with this device.

![linedection2](https://github.com/metracy/MeowMister/assets/12073647/f2e8e56a-d0d5-4852-9a2c-f56feb6bc52c)


02/25/2024
Line from bottom of lidar now blocks the cats access to door - No longer meows because it knows it will get shot with water if it crosses the line and meows repeatedly.
02/22/2024
Added old open cv tracking servo, not using it currently. Am using LD19 module with https://github.com/henjin0/LIDAR_LD06_python_loder/blob/main/README_en.md lidar calculator for python. Adapted it to support displaying lidar set in the bottom right
corner of a hallway and using matplotlib to draw the details of the incoming data from a LD19 to serial-USB converter.
01-23-2024
Added shell script to start the processes and launch servo_control.py and target_acquisition.py
