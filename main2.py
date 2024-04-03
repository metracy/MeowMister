import serial
from CalcLidarData import CalcLidarData
import matplotlib.pyplot as plt
import math
import threading

servo_control = '/tmp/servo_control'
#file = open(servo_control, 'w')

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='polar')
ax.set_title('MEOWMISTER LIDAR DETECTION', fontsize=22)

plt.connect('key_press_event', lambda event: exit(1) if event.key == 'e' else None)

# Open up Serial connection to Lidar USB Lidar Device
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=230400, timeout=5.0, bytesize=8, parity='N', stopbits=1)

tmpString = ""
angles = list()
distances = list()

i = 0
angle_rotation = 0  # relic
ax.set_thetamin(90) # specified in degrees
ax.set_thetamax(180) # specified in degrees
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
            fifo.flush() #
    except Exception as e:
        print(f"Error writing to FIFO: {e}")

# Lidar Distance Calculator
def radius_calc(angle):
    '''  Since lidar radius is tested in a rectangular hallway, radius from center of lidar to the defined box is a function of the degrees
    to calculate y, using top distance of 14.3,   R distance is R(for 90 to 128 degrees) = 14.3/sin(angle)
    R(128+ to 180) = 10.3/cos(angle)
    '''
    if 92 <= math.degrees(angle) <= 128:
        R = 14.3 / math.sin(angle)
        return R
    elif 128 < math.degrees(angle) <= 177:
        R = -10.3 / math.cos(angle) # flip negative sign 
        return R
    else:
        R = 3
        return R

def coord_calc(angle2, distance):
    Y = distance * math.sin(angle2)
    X = -distance * math.cos(angle2)
    return X, Y

        
while True:
    loopFlag = True
    flag2c = False

    if i % 40 == 39: # every 40th iteration engage and plot all the data points collected
    #UPDATE: each data point no longer needs to be rotated just mirrored by making
                                                # error check for values > 3.14 radian.
        rotated_angles = [(angle_rotation - angle) % (2 * math.pi) for angle in angles]
        
        ax.clear() # wipe all previously plotted points off of the polar plot
        ax.set_thetamin(90) # restrict plot to 2nd quadrant
        ax.set_thetamax(180) # restrict plot to 2nd quadrant
        ax.set_ylim(0, 20) # radius of hallway where lidar is planted.
        ax.set_title('MEOWMISTER LIDAR - E to Quit', fontsize=30)
        # Plot all new points
        ax.scatter(rotated_angles, distances, c="red", s=3)

        # Highlight points based on conditions
        for angle, distance in zip(rotated_angles, distances): # Pair angle, distance lists
            # Highlight points between 92 and 100 degrees
            if 92 <= math.degrees(angle) <= 178 and distance >= min_distance and distance <= radius_calc(angle):
                ax.scatter(angle, distance, s=50, facecolors='none', edgecolors='blue', marker='s')
                angle2 = angle
                X, Y = coord_calc(angle2, distance)
        try:
            #Plot the Coordinates of the last detected point that fit the constraints and give the X and Y coordinate in Units
            ax.text(6/5*math.pi, radius_for_text-1, f'Coordinates:({X:.1f},{Y:.1f})', 
                horizontalalignment='right', verticalalignment='center', fontsize=12, color='blue')
        except:
            pass
        angle_to_display = math.degrees(angle2) # Convert the last detected point that Fit Constraints to Degrees and display on the polar plot.
        ax.text(3/4*math.pi, radius_for_text, f'{angle_to_display:.1f}°', 
        horizontalalignment='center', verticalalignment='center', fontsize=12, color='blue')
        # Non-blocking way of writing to the angle to FIFO. Executes function in separate thread
        write_thread = threading.Thread(target=write_to_fifo, args=(angle2,))
        write_thread.start() # launch Thread
        plt.pause(0.2)
        angles.clear() #clear the angles list
        distances.clear() # clear the distances list
        i = 0 #reset i back to 

######################################################################################
### henjin0's Demon Magic - READ HEX DATA FROM LIDAR AND PARSE BYTES to int angles ###
######################################################################################
    while loopFlag: 
        b = ser.read() # Read data byte by byte
        tmpInt = int.from_bytes(b, 'big')

        if tmpInt == 0x54: # Find start of data packet from lidar
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

    i += 1 # add 1 to counter and restart loop

ser.close()
