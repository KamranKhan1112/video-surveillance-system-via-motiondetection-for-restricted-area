def is_person_present(frame, thresh=1100):
    global foog

    # Apply background subtraction
    fgmask = foog.apply(frame)

    # Get rid of the shadows
    ret, fgmask = cv2.threshold(fgmask, 250, 255, cv2.THRESH_BINARY)

    # Apply some morphological operations to make sure you have a good mask
    fgmask = cv2.dilate(fgmask, kernel, iterations=4)

    # Detect contours in the frame
    contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if there was a contour and the area is somewhat higher than some threshold so we know its a person and not noise
    if contours and cv2.contourArea(max(contours, key=cv2.contourArea)) > thresh:

        # Get the max contour
        cnt = max(contours, key=cv2.contourArea)

        # Draw a bounding box around the person and label it as person detected
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, 'Person Detected', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1, cv2.LINE_AA)

        return True, frame


    # Otherwise report there was no one present
    else:
        return False, frame