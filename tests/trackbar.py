import cv2
import numpy as np

def nothing():
    pass

cam = cv2.VideoCapture(0)

cv2.namedWindow('Trackbar')

cv2.createTrackbar('minh', 'Trackbar', 0, 179, nothing)
cv2.createTrackbar('mins', 'Trackbar', 0, 255, nothing)
cv2.createTrackbar('minv', 'Trackbar', 0, 255, nothing)
cv2.createTrackbar('maxh', 'Trackbar', 0, 179, nothing)
cv2.createTrackbar('maxs', 'Trackbar', 0, 255, nothing)
cv2.createTrackbar('maxv', 'Trackbar', 0, 255, nothing)

cv2.imshow('Trackbar', np.full((300, 500, 3), 255, dtype=np.uint8))

key = 0
while key != 27:
    ret, frame = cam.read()
    print(frame.shape)
    cv2.imshow('h', frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    minh = cv2.getTrackbarPos('minh', 'Trackbar')
    mins = cv2.getTrackbarPos('mins', 'Trackbar')
    minv = cv2.getTrackbarPos('minv', 'Trackbar')
    maxh = cv2.getTrackbarPos('maxh', 'Trackbar')
    maxs = cv2.getTrackbarPos('maxs', 'Trackbar')
    maxv = cv2.getTrackbarPos('maxv', 'Trackbar')
    bin_ = cv2.inRange(frame, (minh, mins, minv), (maxh, maxs, maxv))
    cv2.imshow('binary', bin_)
    bin = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
    bin = cv2.inRange(bin, (minh, mins, minv), (maxh, maxs, maxv))
    bin = cv2.resize(bin, (frame.shape[1], frame.shape[0]))
    cv2.imshow('b', bin)
    key = cv2.waitKey(10)

cv2.destroyAllWindows()
