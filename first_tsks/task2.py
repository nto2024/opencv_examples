import cv2
import numpy as np
import os

def test(ansn):
    a = open('ans.txt', 'r')
    ans = a.read().split(':')
    for i in range(len(ansn)):
        if ans[i] != str(ansn[i]):
            print(f'{i}; orig: {ans[i]}; new: {ansn[i]}')
     
def change(frame):
    frame = frame[59:59 + 370, 144:144 + 370]
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame = cv2.resize(frame, (64, 64), interpolation=cv2.INTER_LINEAR)
    frame = cv2.inRange(frame, (0, 0, 200), (30, 360, 360))
    return frame

def sol(path='./movie2.mp4'):
    vid = cv2.VideoCapture(path)
    ret, frame = vid.read()
    frame = change(frame)
    contr, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contr[0])
    ans = []
    while True:
        ret, frame = vid.read()
        if not ret: break
        frame = change(frame)
        contr, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        x1, y1, w, h = cv2.boundingRect(contr[0])
        ans.append((y1 - y, x1 - x))
        x, y = x1, y1
    # test(ans)
    with open ('ans.txt', 'w') as a:
        for i in ans:
            a.write(f'({i[0]}, {i[1]}), ')
    return ans
   

