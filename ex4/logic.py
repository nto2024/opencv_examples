import cv2
import numpy as np
import random

vid = cv2.VideoCapture(0)
key = 0
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
_, frame_ = vid.read()

font = cv2.FONT_HERSHEY_COMPLEX
y_size, x_size = frame_.shape[:-1]
radius = 15
radius_apple = 20

def find_snake(frame):
    global snake_len
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    img = cv2.inRange(img, (40, 110, 10), (100, 255, 255))
    contrs, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contrs:
        if cv2.contourArea(cnt) > 800:
            (x, y), r = cv2.minEnclosingCircle(cnt)
            x, y, r = map(int, (x, y, r))
            snake_len = [(x, y)] + snake_len[:-1]

def draw_snake(frame): #это ткинтер
    for coord in snake_len:
        cv2.circle(frame, coord, radius, (0, 255, 0), -1, -1)

def draw_apple(frame, coords): #и это ткинтер
    cv2.circle(frame, coords, radius_apple, (0, 0, 255), -1, -1)

def is_game_over():
    h = snake_len[0]
    if h[0] < radius or h[0] > x_size - radius or h[1] < radius or h[1] > y_size - radius:
        return True
    for b in range(1, len(snake_len)):
        d = int(((h[0] - snake_len[b][0]) ** 2 + (h[1] - snake_len[b][1]) ** 2) ** 0.5)
        if d < 2 * radius:
            return True
    return False

def generate_apple():
    x = random.randint(radius_apple + radius, x_size - radius_apple - radius)
    y = random.randint(radius_apple + radius, y_size - radius_apple - radius)
    return (x, y)

def is_apple_eaten():
    global apple_coord
    global snake_len
    d = int(((snake_len[0][0] - apple_coord[0]) ** 2 + (snake_len[0][1] - apple_coord[1]) ** 2) ** 0.5)
    if d < radius + radius_apple:
        snake_len = snake_len + [(snake_len[-1][0], snake_len[-1][1])]
        apple_coord = generate_apple()

def main(frame, count_):
    if count_ == 0:
        find_snake(frame)
        if is_game_over():
            print('game over')
        else:
            print('okay')
            is_apple_eaten()
    draw_snake(frame)
    draw_apple(frame, apple_coord)

snake_len = [(0, 0)]
apple_coord = generate_apple()

def showing(key, vid): #вот тут ткинтер
    count_ = -1
    while key != 27: #пока пользователь не нажал esc 
        ret, frame = vid.read()
        if not ret: return 0 #если камера недоступна - выходим
        count_ = (count_ + 1)%3
        main(frame, count_)
        cv2.imshow('task_1', frame) #отображаем готовый кадр
        key = cv2.waitKey(1)

showing(key, vid)
vid.release()
cv2.destroyAllWindows()
