import numpy as np
import cv2
import dropbox
import os
from glob import iglob

access_token = 'paste your access token here'  # paste your access token in-between ''
client = dropbox.client.DropboxClient(access_token)
print
'linked account: ', client.account_info()
PATH = ''

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('C:\python27\output1.avi', fourcc, 20.0, (640, 480))

# here output1.avi is the filename in which your video which is captured from webcam is stored. and it resides in C:\python27 as per the path is given.

while (cap.isOpened()):
    ret, frame = cap.read()
if ret == True:
# frame = cv2.flip(frame,0) #if u want to flip your video

# write the (unflipped or flipped) frame

    out.write(frame)

cv2.imshow('frame', frame)
if cv2.waitKey(1) & 0xFF == ord('q'):
    break
else:
    break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()

for filename in iglob(os.path.join(PATH, 'C:/Python27/output1.avi')):
    print
    filename
try:
    f = open(filename, 'rb')
response = client.put_file('/livevideo1.avi', f)
print
"uploaded:", response
f.close()


