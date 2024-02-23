mkfifo /tmp/servo_control
sudo chmod 777 /dev/ttyUSB0
sudo chmod 777 /dev/ttyACM0
python3 servo_control.py
python3 target_aquisition.py
