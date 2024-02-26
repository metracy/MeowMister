# MeowMister
 
MeowMister is a program to control a turret to focus on an object if it meets the criteria for distance from source of lidar. It utilizes pyfirmata2, a FirmataExpress sketch ( and opencv to control a servo to rotate the turret).  I am using the FirmataExpress module that includes the boards.h that adds support for the Seeed XAIO m0 board. Now using a small lidar device (LD19) for controlling direction of turret. Will only fire once while I continue to prototype it.

Lidar Plot running main2.py
![animated](https://github.com/metracy/MeowMister/assets/12073647/aa362e29-e5b7-47d3-bacd-be8ba3df3c56)


Circuit arrangement.
![circuit_diagram](https://github.com/metracy/MeowMister/assets/12073647/4ced766c-6f89-4e9b-967f-524543f69b9a)



Seeeduino XAIO pinout
![Seeeduino-XIAO-pinout-1](https://github.com/metracy/MeowMister/assets/12073647/bf2b7dc1-ec3a-4821-946b-a08e1268069b)



1/2" Nozzle and 1/4" tubing line feeds through printed Boxhole.stl
![3dPrint](https://github.com/metracy/MeowMister/assets/12073647/ad61f396-daed-49fa-8947-06ce98be9814)



My cat is not pleased with this device.
![unhappy_cat](https://github.com/metracy/MeowMister/assets/12073647/886b0888-1341-46b1-84da-2097e17319d2)


02/26/2024
Cleaned up the readme file. Added XAIO pinout and wiring arrangement.

02/25/2024
Line from bottom of lidar now blocks the cats access to door - No longer meows because the cat knows it will get shot with water if he crosses into lidar range.

02/22/2024
Added old open cv tracking servo, not using it currently. Am using LD19 module with https://github.com/henjin0/LIDAR_LD06_python_loder/blob/main/README_en.md lidar calculator for python. Adapted it to support displaying lidar set in the bottom right
corner of a hallway and using matplotlib to draw the details of the incoming data from a LD19 to serial-USB converter.

01-23-2024
Added shell script to start the processes and launch servo_control.py and target_acquisition.py
