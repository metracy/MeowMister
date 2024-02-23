mkfifo /tmp/servo_control
chmod 777 /tmp/servo_control
python3 servo_control.py
python3 main2.py

