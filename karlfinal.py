# import the necessary packages
from collections import deque
import numpy as np
import imutils
import cv2

# lower and upper boundaries of the "green" in HSV

#  dark values
# greenLower = (29, 86, 6)
# greenUpper = (64, 255, 255)

# light values
greenLower = (15, 65, 165)
greenUpper = (50, 185, 254)

# White line values
whiteLower = (0, 0, 230)
whiteUpper = (47, 10, 255)

# Red Value
redLower = (177, 155, 160)
redUpper = (185, 172, 188)

# Green Ground Value
courtLower = (29, 86, 6)
courtUpper = (64, 255, 255)

buffer_size = 20
pts = deque(maxlen=buffer_size)
pts2 = deque(maxlen=buffer_size)

# camera = cv2.VideoCapture(0)
camera = cv2.VideoCapture("tennis2.MOV")

hsv = []


def mouse_drawing(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(hsv[y][x])


# infinite loop
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    if frame is not None:
        # resize the frame, blur it, and convert it to the HSV color space
        frame = imutils.resize(frame, width=600)
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, greenLower, greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        # print(pts)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            if radius > 40:
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # update the points queue
        pts.appendleft(center)

        gx = 0
        for i in range(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue
            bx = (pts[i2 - 1])
            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(buffer_size / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
            try:
                gx = bx[0]+30
            except:
                gx = -1000

        # show the frame to our screen
        cv2.imshow("Frame", frame)

        # cv2.imshow("Frame", mask)
        key = cv2.waitKey(1) & 0xFF

        cv2.setMouseCallback("Frame", mouse_drawing)

    # white mask
    mask = cv2.inRange(hsv, whiteLower, whiteUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cntsw = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                             cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    # only proceed if at least one contour was found
    if len(cntsw) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        cx = max(cntsw, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(cx)
        M = cv2.moments(cx)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

    # update the points queue
    pts2.appendleft(center)

    wx = 0
    # loop over the set of tracked points
    for i2 in range(1, len(pts2)):
        # if either of the tracked points are None, ignore
        # them
        if pts2[i2 - 1] is None or pts2[i2] is None:
            continue
        lx = pts2[i2 - 1]
        thickness = int(np.sqrt(buffer_size / float(i2 + 1)) * 2.5)
        cv2.line(frame, pts2[i2 - 1], pts2[i2], (250, 0, 2), 5)
        wx = lx[0]

    text=2
    for i in range(gx):
        try:
            if wx <= gx:
                #print("in")
                text=1
        except:
            text=2

    for i in range(gx):
        try:
            if wx > gx:
                #print("out")
                text=0


        except:
            text=2


    if text==1:
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, 'in', (10, 100), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
    else:
        if text==0:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, 'out', (10, 100), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
        else:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, 'Undetermined', (10, 100), font, 2, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()