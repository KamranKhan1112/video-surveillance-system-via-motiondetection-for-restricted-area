import cv2
import numpy as np
# initlize video capture object
#cap = cv2.VideoCapture('sample_video.mp4')
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
#cap = cv2.VideoCapture(0)
# you can set custom kernel size if you want
kernel = None

# initilize background subtractor object
foog = cv2.createBackgroundSubtractorMOG2(detectShadows=False, varThreshold=100, history=2500)

# Noise filter threshold
thresh =2500

while (1):
    ret, frame = cap.read()
    if not ret:
        break

    # Apply background subtraction
    fgmask = foog.apply(frame)

    # Get rid of the shadows
    ret, fgmask = cv2.threshold(fgmask, 250, 255, cv2.THRESH_BINARY)

    # Apply some morphological operations to make sure you have a good mask
    fgmask = cv2.erode(fgmask,kernel,iterations = 1)
    fgmask = cv2.dilate(fgmask, kernel, iterations=4)

    # Detect contours in the frame
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:

        # Get the maximum contour
        cnt = max(contours, key=cv2.contourArea)

        # make sure the contour area is somewhat hihger than some threshold to make sure its a person and not some noise.
        if cv2.contourArea(cnt) > thresh:
            # Draw a bounding box around the intruder and label it as intruder detected
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, 'Intruder Detected', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1,
                        cv2.LINE_AA)

    # Stack both frames and show the image
    fgmask_3 = cv2.cvtColor(fgmask, cv2.COLOR_GRAY2BGR)
    stacked = np.hstack((fgmask_3, frame))
    cv2.imshow('Combined', cv2.resize(stacked, None, fx=0.65, fy=0.65))

    k = cv2.waitKey(40) & 0xff
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()