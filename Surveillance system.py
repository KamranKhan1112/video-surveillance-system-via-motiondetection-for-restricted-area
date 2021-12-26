import cv2
import time
from collections import deque
import numpy as np
import dropbox
from twilio.rest import Client
import datetime

# Note the starting time
start_time = time.time()
# sleep time
time.sleep(2)
# Initialize these variables for calculating FPS
fps = 0
frame_counter = 0
# you can set custom kernel size if you want
kernel = None
# Set Window normal so we can resize it
cv2.namedWindow('frame', cv2.WINDOW_NORMAL)

# This is a test video
# cap = cv2.VideoCapture('video.avi')

# Read the video stream from the camera
# cap = cv2.VideoCapture('http://192.168.18.4:8080/video',cv2.CAP_DSHOW)

# Read the video stream from webcam
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

# Read the video stream from mobile camera
# cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

# Get width and height of the frame
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Get Fps and the n_frame
FPS = int(cap.get(cv2.CAP_PROP_FPS))
n_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Initialize the background Subtractor
foog = cv2.createBackgroundSubtractorMOG2(detectShadows=True, varThreshold=150, history=1500)
# Noise filter threshold
thresh = 1500

# Status is True when intruder is present and False when the intruder is not present.
status = False

# After the intruder disapears from view, wait atleast 10 seconds before making the status False
Video_release_Timer = 5

# We don't consider an initial detection unless its detected 15 times, this gets rid of false positives
detection_thresh = 10

# Initial time for calculating if Video_release_Timer time is up
initial_time = None

# We are creating a deque object of length detection_thresh and will store individual detection statuses here
de = deque([False] * detection_thresh, maxlen=detection_thresh)

while True:
    ret, frame = cap.read()
    if not ret:
        break

# This function will return a boolean variable telling if someone was present or not, it will also draw boxes if it
# finds someone
    def is_intruder_present(frame, thresh=1100):
        global foog

        # Apply background subtraction
        fgmask = foog.apply(frame)

        # Get rid of the shadows
        ret, fgmask = cv2.threshold(fgmask, 250, 255, cv2.THRESH_BINARY)

        # Apply some morphological operations to make sure you have a good mask
        fgmask = cv2.erode(fgmask, kernel, iterations=1)
        fgmask = cv2.dilate(fgmask, kernel, iterations=4)

        # Detect contours in the frame
        contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Check if there was a contour and the area is somewhat higher than some threshold so we know its an intruder and not noise
        if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > thresh:

            # Get the max contour
            cnt = max(contours, key=cv2.contourArea)

            # Draw a bounding box around the intruder and label it as intruder detected
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, 'Intruder Detected', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
                        cv2.LINE_AA)

            return True, frame
# Otherwise report there was no one present
        else:
            return False, frame
    detected, annotated_image = is_intruder_present(frame)

# Register the current detection status on our deque object
    de.appendleft(detected)

# This function will simply write the video to the specified path or store on a disk
# If we have consectutively detected a intruder 15 times then we are sure that soemone is present
# We also make this is the first time that this intruder has been detected so we only initialize the videowriter once
# Also we will take 5 images of the detected frame with rectangle box when someone enter the frame and store it in the disk.
    if sum(de) == detection_thresh and not status:
        status = True
        entry_time = datetime.datetime.now().strftime("%A, %I-%M-%S %p %d %B %Y")
# storing the video on the disk with ".avi" formatte + storing the images in desk with ".jpg" fromatte
        imagepath1 = 'C:\\Users\\hidat\\Pictures\\Motion detection\\pics'
        imagepath2 = 'C:\\Users\\hidat\\Dropbox\\Detected pictures'
        count = 0
        while count < 5:
            # Resize image
            resized_image = cv2.resize(frame, (600, 600))
            # detected_frame()
            cv2.imwrite(f'{imagepath1}/{entry_time}-{count}.jpg',resized_image)
            cv2.imwrite(f'{imagepath2}/{entry_time}-{count}.jpg', resized_image)
            count += 1

        videopath1 = 'C:\\Users\\hidat\\Pictures\\Motion detection\\videos'
        # videopath2 = 'C:\\Users\\hidat\\Dropbox\\Rec videos'
        out = cv2.VideoWriter(f'{videopath1}/{entry_time}.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15.0, (width, height))
       # out = cv2.VideoWriter(f'{videopath2}/{entry_time}.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15.0, (width, height))

# If status is True but the intruder is not in the current frame
    if status and not detected:

# Restart the patience timer only if the intruder has not been detected for a few frames so we are sure it was'nt a
# False positive
        if sum(de) > (detection_thresh / 2):

            if initial_time is None:
                initial_time = time.time()

        elif initial_time is not None:

            # If the Video_release_Timer has run out and the intruder is still not detected then set the status to False
            # Also save the video by releasing the video writer and send a text message.
            if time.time() - initial_time >= Video_release_Timer:
                status = False
                exit_time = datetime.datetime.now().strftime("%A, %I:%M:%S %p %d %B %Y")
                out.release()
                initial_time = None

            # Read and store the credentials information in a dict
                '''with open('credentials.txt', 'r') as myfile:
                    data = myfile.read()

                # Convert data variable into dictionary
                info_dict = eval(data)

                # Your Account SID from twilio.com/console
                account_sid = info_dict['account_sid']

                # Your Auth Token from twilio.com/console
                auth_token = info_dict['auth_token']

                #The Entry_time for body
                entry_time = datetime.datetime.now().strftime("%A, %I-%M-%S %p %d %B %Y")
                
                # Set client and send the message
                client = Client(account_sid, auth_token)
                message = client.messages.create(to=info_dict['your_num'], from_=info_dict['trial_num'],
    body="Alert:An Intruder Detected:\n Entered the Surveillance area at {}\nGo to the links to check the footages:\nhttps://www.dropbox.com/sh/fxror8dleujjbbl/AAA3Cb5DhChrxUseHCsRzwI2a?dl=0".format(entry_time))'''


# If significant amount of detections (more than half of detection_thresh) has occured then we reset the Initial Time.
    elif status and sum(de) > (detection_thresh / 2):
        initial_time = None

    # Get the current time in the required format
    current_time = datetime.datetime.now().strftime("%A, %I:%M:%S %p %d %B %Y")

    # Display the FPS
    cv2.putText(annotated_image, 'FPS: {:.2f}'.format(fps), (540, 450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (0, 255, 255), 1)

    # Display Time
    cv2.putText(annotated_image, current_time, (280, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, (0, 0, 255), 1)

    # Display the Aera Status
    cv2.putText(annotated_image, 'Area Occupied: {}'.format(str(status)), (10, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (0, 255, 255), 1)

    # Show the Video_release_Timer Value
    if initial_time is None:
        text = 'Video_release_Timer: {}'.format(Video_release_Timer)
    else:
        text = 'Video_release_Timer: {:.2f}'.format(max(0.0, Video_release_Timer - (time.time() - initial_time)))

    cv2.putText(annotated_image, text, (10, 450), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (0, 0, 255), 1)

    # If status is true save the frame
    if status:
        out.write(annotated_image)
    # Show the Frame
    cv2.imshow('frame', frame)
    # Calculate the Average FPS
    frame_counter += 1
    fps = (frame_counter / (time.time() - start_time))

    # Exit if q is pressed.
    if cv2.waitKey(30) == ord('q'):
        break

# Release Capture and destroy windows
cap.release()
cv2.destroyAllWindows()
