import cv2
# load a video
cap = cv2.VideoCapture('sample_video.mp4')

# Create the background subtractor object
foog = cv2.createBackgroundSubtractorMOG2(detectShadows=True, varThreshold=50, history=2800)

while (1):

    ret, frame = cap.read()
    if not ret:
        break

    # Apply the background object on each frame
    fgmask = foog.apply(frame)

    # Get rid of the shadows
    ret, fgmask = cv2.threshold(fgmask, 250, 255, cv2.THRESH_BINARY)

    # Show the background subtraction frame.
    cv2.imshow('All three', fgmask)
    k = cv2.waitKey(10)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
