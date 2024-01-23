import cv2, os, time

'''
Use OpenCV and the haarcascade face model to draw a target where object is detected
and relay those coordinates to the adjustment function before passing it to the lidar
detection function for adjusting coordinates.
'''

def servo_control(x_coordinate, frame_width, flipped=1):
    # Flip the x_coordinate so I can used it the depends if camera is mirroring
    # by default flipped
    x_flipped = frame_width - x
    if flipped == 0:
        return int((x_coordinate / frame_width) * 180)
    else:
        return int((x_flipped / frame_width) * 180)

'''
Using haarcascade model
stand in for a later better model and also mix with lidar

I believe I'll only use this portion for identifying if a cat is in the area and have the lidar do the actual
angle where the cat is

on mint linux is /usr/local/share/opencv4/haarcascades/haarcascade_frontalface_default.xml
Use print(cv2.data.haarcascades) to get the directory and reconfigure
'''

stock_model = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(stock_model)

# capture frames from webcam /dev/video0
webcam = cv2.VideoCapture(0)

# Get the width of the video frame
frame_width = int(webcam.get(3))

fifo_path = '/tmp/servo_control'

while True:
    # Grab the frame from webcam and if it doesn't pull the frame then break out of loop
    valid, frame = webcam.read()
    if not valid:
        break

    # make grayscale using cv2.cvtColor
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    '''
    Guide: https://www.analyticsvidhya.com/blog/2022/10/face-detection-using-haar-cascade-using-python/
    
    face_cascade.detectMultiScale is the method used to detect faces in the image.
    The face_cascade object is a pre-trained Haar Cascade classifier loaded earlier in the script.
    gray: The grayscale image in which to detect faces.

    scaleFactor: This parameter specifies how much the image size is reducd at each image scale. A value of 1.1 means reducing the size by 10% at each scale. It is used to detect faces at different distances from the camera.

    minNeighbors=5: This parameter specifies how many neighbors (or detections) each candidate rectangle should have to retain it. A higher number results in fewer detections but with higher quality.

    minSize=(35, 35): Minimum possible object size. Objects smaller than this are ignored. This helps to avoid false detections of small objects that aren't faces.
    '''
    
    faces = face_cascade.detectMultiScale(gray, minNeighbors=10, minSize=(35, 35))

    if len(faces) == 0:
        print('No Target')
    time.sleep(0.02)
    for (x, y, w, h) in faces:
        # calculate halfway point of 
        center_x = int(x + (w / 2))
        center_y = int(y + (h / 2))

        print("X Position:",center_x," Y Position:",center_y)
        # put if function here to set a 30 second activation for a fifo write to firing 
        # if cat
        #   write a 1 to fifo cat_detected
        #   time.sleep(5000)
        #   write a 0 to fifo cat_detected
        
        # Temporary until lidar comes in, use function from above for whether vid is flipped or not
        servo_angle = servo_control(center_x, frame_width, 1)

        # Write the servo angle to the FIFO file
        with open(fifo_path, 'w') as fifo:
            fifo.write(str(servo_angle))

        # Draw a red crosshair at the center of the face
        crosshair = 30 # crosshair in pixel length

        '''
        https://www.geeksforgeeks.org/python-opencv-cv2-line-method/

        cv2.line(image, start_point, end_point, color, thickness) 
        Parameters: image: It is the image on which line is to be drawn. 

        start_point: It is the starting coordinates of the line. The coordinates are represented as tuples of two values i.e. (X coordinate value, Y coordinate value). 
        end_point: It is the ending coordinates of the line. The coordinates are represented as tuples of two values i.e. (X coordinate value, Y coordinate value). 
        color: It is the color of the line to be drawn. For RGB, we pass a tuple. eg: (255, 0, 0) for blue color.
        thickness: It is the thickness of the line in px. 
        Return Value: It returns an image.
        '''
        cv2.line(frame, (center_x - crosshair, center_y), (center_x + crosshair, center_y), (0, 0, 255), 2) # draw line 4 pixels that is red 20 pixels long on x axis
        cv2.line(frame, (center_x, center_y - crosshair), (center_x, center_y + crosshair), (0, 0, 255), 2) # draw line 4 pixels that is red 20 pixels long on y axis

    # Display the captured frame with face detections
    cv2.imshow('Target Acquisition', frame)

    # exit if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

#cleanup
webcam.release()
cv2.destroyAllWindows()
