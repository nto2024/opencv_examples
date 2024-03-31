import cv2
import numpy as np

vid = cv2.VideoCapture(0)
key = 0

while key != 27:
    ret, frame = vid.read()
    bin = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    bin1 = cv2.inRange(bin, (0, 117, 70), (5, 255, 255))
    bin = cv2.inRange(bin, (169, 117, 70), (179, 255, 255))
    bin += bin1
    contours, _ = cv2.findContours(bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.si(cnt) > 300:
            print('красный объект обнаружен')
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))
    
    cv2.imshow('orig', frame)
    cv2.imshow('bin', bin)
    key = cv2.waitKey(1)

vid.release()
cv2.destroyAllWindows()