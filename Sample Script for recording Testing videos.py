import numpy as np
import cv2

cap = cv2.VideoCapture(0)
'''# This is how we define our codec
#fourcc = cv2.VideoWriter_fourcc(*'DIVX')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Save our video at 20.0 FPS with the defined dimensions, Note my default camera has these dimensions, yours might be different
out = cv2.VideoWriter(r'sampletestnew2.mp4', cv2.VideoWriter_fourcc(*'DIVX'),15, (width, height))
while True:
    ret, frame = cap.read()
    # Save this frame
    out.write(frame)

    cv2.imshow ('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video writer Object
out.release()
cap.release()
cv2.destroyAllWindows()'''

# This is how we define our codec
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
width = int(cap.get(3))
height = int(cap.get(4))

# Save our video at 20.0 FPS with the defined dimensions, Note my default camera has these dimensions, yours might be different
out = cv2.VideoWriter(r'sampletestnew.avi', fourcc, 20.0, (width, height))

while (True):
    ret, frame = cap.read()
    if not ret:
        break

    # Save this frame
    out.write(frame)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video writer Object
out.release()
cap.release()
cv2.destroyAllWindows()