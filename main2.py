import serial
from CalcLidarData import CalcLidarData
import matplotlib.pyplot as plt
import math
import threading

servo_control = '/tmp/servo_control'
file = open(servo_control, 'w')

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='polar')
ax.set_title('MEOWMISTER LIDAR DETECTION', fontsize=22)

plt.connect('key_press_event', lambda event: exit(1) if event.key == 'e' else None)

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=230400, timeout=5.0, bytesize=8, parity='N', stopbits=1)

tmpString = ""
angles = list()
distances = list()

i = 0
angle_rotation = 0
ax.set_thetamin(90)
ax.set_thetamax(180)
ax.set_ylim(0, 20) # shrink range of lidar scanner to show relevant portion

min_distance = 3  # Min distance for the 
max_distance = 10  # max distance for things
angle = 120 # default value
angle_to_display = 90
angle_in_radians = math.radians(angle_to_display)
radius_for_text = 3.5
global angle2
angle2 = angle
# Function to write to FIFO in a separate thread
def write_to_fifo(angle):
    try:
        with open(servo_control, 'w') as fifo:
            fifo.write(f'{angle}\n')
            fifo.flush()
    except Exception as e:
        print(f"Error writing to FIFO: {e}")

# Lidar Distance Calculator
def radius_calc(angle):
    '''  Since lidar radius is tested in a rectangular hallway, radius from center of lidar is a function of the degrees
    to calculate y, using top distance of 14.3,   R distance is R(for 90 to 128 degrees) = 4.3/sin(angle)
    R(128+ to 180) = 11/cos(angle)
    '''
    if 90 <= angle_degrees <= 128:
        angle_radians = angle
        R = 14.3 / math.cos(angle)
        return R
    else:
        angle_radians = math.radians(angle_degrees)
        R = 11 / math.sin(angle)
        return R



        
while True:
    loopFlag = True
    flag2c = False

    if i % 40 == 39: # every 39th iteration engage
        # plot has to be rotated based on the location of the room, each data point no longer needs to be rotated
        rotated_angles = [(angle_rotation - angle) % (2 * math.pi) for angle in angles]

        
        ax.clear() # wipe all the dots off of lidar plot
        ax.set_thetamin(90) # restrict plot to 2nd quadrant
        ax.set_thetamax(180) # restrict plot to 2nd quadrant
        ax.set_ylim(0, 20) # radius of hallway where lidar is planted.
        ax.set_title('MEOWMISTER LIDAR - E to Quit', fontsize=30)
        # Plot all new points
        ax.scatter(rotated_angles, distances, c="red", s=3)

        # Highlight points based on conditions
        for angle, distance in zip(rotated_angles, distances):
            # Highlight points between 92 and 100 degrees
            if 92 * math.pi / 180 <= angle <= 100 * math.pi / 180 and distance <= 14.5:
                ax.scatter(angle, distance, s=50, facecolors='none', edgecolors='blue', marker='s')
                angle2 = angle
            # Different max distances for degrees that range between
            elif 100 * math.pi / 180 < angle <= 110 * math.pi / 180 and min_distance <= distance <= 15:
                ax.scatter(angle, distance, s=50, facecolors='none', edgecolors='blue', marker='s')
                angle2 = angle
            elif 110 * math.pi / 180 < angle <= 115 * math.pi / 180 and min_distance <= distance <= 15.5:
                ax.scatter(angle, distance, s=50, facecolors='none', edgecolors='blue', marker='s')
                angle2 = angle
            elif 115 * math.pi / 180 < angle <= 120 * math.pi / 180 and min_distance <= distance <= 16:
                ax.scatter(angle, distance, s=50, facecolors='none', edgecolors='blue', marker='s')
                angle2 = angle
            elif 120 * math.pi / 180 < angle <= 125 * math.pi / 180 and min_distance <= distance <= 16.7:
                ax.scatter(angle, distance, s=50, facecolors='none', edgecolors='blue', marker='s')
                angle2 = angle
            elif 125 * math.pi / 180 < angle <= 130 * math.pi / 180 and min_distance <= distance <= 17.9:
                ax.scatter(angle, distance, s=50, facecolors='none', edgecolors='blue', marker='s')
                angle2 = angle
            elif 130 * math.pi / 180 < angle <= 135 * math.pi / 180 and min_distance <= distance <= 16.7:
                ax.scatter(angle, distance, s=50, facecolors='none', edgecolors='blue', marker='s')
                angle2 = angle
            elif 135 * math.pi / 180 < angle <= 180 * math.pi / 180 and min_distance <= distance <= max_distance:
                ax.scatter(angle, distance, s=50, facecolors='none', edgecolors='blue', marker='s')
                angle2 = angle
        angle_to_display = angle2*57.2        
        ax.text(3/4*math.pi, radius_for_text, f'{angle_to_display:.1f}°', 
        horizontalalignment='center', verticalalignment='center', fontsize=12, color='blue')
        write_thread = threading.Thread(target=write_to_fifo, args=(angle2,))
        write_thread.start()
        plt.pause(0.2)
        angles.clear()
        distances.clear()
        i = 0

    while loopFlag:
        b = ser.read()
        tmpInt = int.from_bytes(b, 'big')

        if tmpInt == 0x54:
            tmpString += b.hex() + " "
            flag2c = True
            continue

        elif tmpInt == 0x2c and flag2c:
            tmpString += b.hex()

            if not len(tmpString[0:-5].replace(' ', '')) == 90:
                tmpString = ""
                loopFlag = False
                flag2c = False
                continue

            lidarData = CalcLidarData(tmpString[0:-5])
            angles.extend(lidarData.Angle_i)
            distances.extend(lidarData.Distance_i)

            tmpString = ""
            loopFlag = False
        else:
            tmpString += b.hex() + " "

        flag2c = False

    i += 1

ser.close()
