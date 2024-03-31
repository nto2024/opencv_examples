import cv2
import numpy as np

def nothing():
    pass

cam = cv2.VideoCapture(0)

cv2.namedWindow('Trackbar')

cv2.createTrackbar('minb', 'Trackbar', 0, 360, nothing)
cv2.createTrackbar('ming', 'Trackbar', 0, 360, nothing)
cv2.createTrackbar('minr', 'Trackbar', 0, 360, nothing)
cv2.createTrackbar('maxb', 'Trackbar', 0, 360, nothing)
cv2.createTrackbar('maxg', 'Trackbar', 0, 360, nothing)
cv2.createTrackbar('maxr', 'Trackbar', 0, 360, nothing)

cv2.imshow('Trackbar', np.full((300, 500, 3), 255, dtype=np.uint8))

key = 0
while key != 27:
    ret, frame = cam.read()
    cv2.imshow('h', frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    minb = cv2.getTrackbarPos('minb', 'Trackbar')
    ming = cv2.getTrackbarPos('ming', 'Trackbar')
    minr = cv2.getTrackbarPos('minr', 'Trackbar')
    maxb = cv2.getTrackbarPos('maxb', 'Trackbar')
    maxg = cv2.getTrackbarPos('maxg', 'Trackbar')
    maxr = cv2.getTrackbarPos('maxr', 'Trackbar')
    bin_ = cv2.inRange(frame, (minb, ming, minr), (maxb, maxg, maxr))
    cv2.imshow('binary', bin_)
    key = cv2.waitKey(10)

cv2.destroyAllWindows()
