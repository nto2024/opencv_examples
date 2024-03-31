import cv2
import numpy as np

colors = ['Оранжевый', 'Желтый', 'Зеленый', 'Бирюзовый', 'Синий', 
          'Фиолетовый', 'Фуксия', 'Красный'] #лист с названиями цветов
colors_lh = [[5, 20], [20, 40], [40, 90], [90, 100], [100, 120], 
             [120, 150], [150, 174], [175, 180], [0, 5]] #лист с границами цветов по hue, красный добавлен в конце 2 раза тк он есть с обоих концов шкалы hue
colors_bgr = [(0, 165, 255), (0, 255, 255) ,(0, 255, 0), (255, 255, 0), 
              (255, 0, 0), (255, 0, 255), (165, 0, 255), (0, 0, 255)] #лист с цветами в палитре bgr

def print_coord(img, coords):
    for c in coords:
        x, y, w, h = c
        img = cv2.putText(img, f'x: {x + w//2} y: {y + h//2}', (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 1, (175, 175, 175))

def print_colors(img, coords, clrs):
    for i in range (len(coords)):
        x, y, w, h = coords[i]
        img = cv2.putText(img, clrs[i][0], (x, y + h), cv2.FONT_HERSHEY_PLAIN, 1.5, colors_bgr[clrs[i][1]], 2)
        cv2.rectangle(img, (x, y), (x+w, y+h), colors_bgr[clrs[i][1]], 2)

def detect_form(img, contours, coords):
    for i in range(len(contours)):
        eps = 0.029 * cv2.arcLength(contours[i], True) #кооф перед arclength это кошмар можно еще поиграться с ним но вроде норм (отвечает за кол-во углов которое найдет у фигуры)
        approx = cv2.approxPolyDP(contours[i], eps, True)
        x, y = coords[i][0] + 4, coords[i][1] + coords[i][3] // 2
        match len(approx):
            case 2:
                fig = 'line'
            case 3:
                fig = 'triangle'
            case 4:
                fig = 'rectangle'
            case 5:
                fig = 'pentagon'
            case 6:
                fig = 'hexagon'
            case _:
                fig = 'circle'
        img = cv2.putText(img, f"it's {fig}", (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)


def find_objects(img): #в range_ указываем какие цвета хотим найти
    objects = []
    coords = []
    clrs = []
    count_ = 0 #счетчик объектов
    for i in range(8):
        bin = cv2.inRange(img, (colors_lh[i][0], 100, 0), (colors_lh[i][1], 255, 255)) #нижние границы при лучшем освещении желательно брать другие, повыше
        if (i == 7):
            bin += cv2.inRange(img, (colors_lh[8][0], 100, 0), (colors_lh[8][1], 255, 255)) #обработка красного цвета
        contrs, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contrs:
            if cv2.contourArea(cnt) > 900: #не берет во внимание мелкие объекты
                count_ += 1
                objects.append(cnt)
                x, y, w, h = cv2.boundingRect(cnt)
                coords.append([x, y, w, h])
                clrs.append([colors[i], i])
    return objects, coords, clrs, count_

def main():
    vid = cv2.VideoCapture(0)
    key = 0

    while key != 27:
        ret, frame = vid.read()
        bin = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        contours, coords, clrs, count_ = find_objects(bin)
        print_colors(frame, coords, clrs)
        detect_form(frame, contours, coords)
        print_coord(frame, coords)
        frame = cv2.putText(frame, f'count: {count_}', (0, 460), cv2.FONT_HERSHEY_PLAIN, 2, (175, 175, 175), 2)
        cv2.imshow('orig', frame)
        key = cv2.waitKey(1)

    vid.release()
    cv2.destroyAllWindows()

main()