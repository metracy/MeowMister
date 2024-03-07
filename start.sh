mkfifo /tmp/servo_control
sudo chmod 007 /dev/ttyUSB0
sudo chmod 007 /dev/ttyACM0
python3 servo_control.py
python3 main2.py
