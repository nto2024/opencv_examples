import cv2
import numpy as np

def nothing():
    pass

cam = cv2.VideoCapture(0)

cv2.namedWindow('Trackbar')

cv2.createTrackbar('minh', 'Trackbar', 0, 360, nothing)
cv2.createTrackbar('mins', 'Trackbar', 0, 360, nothing)
cv2.createTrackbar('minv', 'Trackbar', 0, 360, nothing)
cv2.createTrackbar('maxh', 'Trackbar', 0, 360, nothing)
cv2.createTrackbar('maxs', 'Trackbar', 0, 360, nothing)
cv2.createTrackbar('maxv', 'Trackbar', 0, 360, nothing)

cv2.imshow('Trackbar', np.full((300, 500, 3), 255, dtype=np.uint8))

key = 0
while key != 27:
    ret, frame = cam.read()
    cv2.imshow('h', frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    minb = cv2.getTrackbarPos('minh', 'Trackbar')
    ming = cv2.getTrackbarPos('mins', 'Trackbar')
    minr = cv2.getTrackbarPos('minv', 'Trackbar')
    maxb = cv2.getTrackbarPos('maxh', 'Trackbar')
    maxg = cv2.getTrackbarPos('maxs', 'Trackbar')
    maxr = cv2.getTrackbarPos('maxv', 'Trackbar')
    bin_ = cv2.inRange(frame, (minb, ming, minr), (maxb, maxg, maxr))
    cv2.imshow('binary', bin_)
    key = cv2.waitKey(10)

cv2.destroyAllWindows()
