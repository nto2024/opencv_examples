import cv2
import numpy as np
import os

def find_circ(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(img, img[0, 0] + 10, 255, cv2.THRESH_BINARY)
    cont, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(cont[0])
    return w // 2 + 1, x + w // 2, y + h // 2

def test():
    for i in range(100):
        img = cv2.imread(f'./var7/img{i}.png')
        r, x, y = find_circ(img)
        ans = open(f'./files/{i}.txt', 'r')
        r1, x1, y1 = map(int, ans.read().split())
        ans.close()
        if r != r1:
            print(f"{i}; r orig: {r1}; r get: {r}")
        if x != x1:
            print(f"{i}; r orig: {x1}; r get: {x}")
        if y != y1:
            print(f"{i}; r orig: {y1}; r get: {y}")
        # cv2.waitKey(0)
    return 'done'

def sol(path='./files/'):
    ans = []
    for i in range(100):
        img = cv2.imread(f'./var7/img{i}.png')
        img = img[59:59 + 370, 144:144 + 370]
        img = cv2.resize(img, (64, 64), interpolation=cv2.INTER_LINEAR)
        r, y, x = find_circ(img)
        print(x, y, r)
        ans.append([x, y, r])
    with open ('a.txt', 'w') as a:
        for i in ans:
            a.write(f'[{i[0]}, {i[1]}, {i[2]}], ')
    
    return ans
