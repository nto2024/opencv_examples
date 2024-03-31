import cv2
import numpy as np

#служебная часть

#вспомогательные листы с цветами
colors = ['Оранжевый', 'Желтый', 'Зеленый', 'Бирюзовый', 'Синий', 
          'Фиолетовый', 'Фуксия', 'Красный'] #лист с названиями цветов
colors_lh = [[5, 20], [20, 40], [40, 90], [90, 100], [100, 120], 
             [120, 150], [150, 174], [175, 180], [0, 5]] #лист с границами цветов по hue, красный добавлен в конце 2 раза тк он есть с обоих концов шкалы hue
colors_bgr = [(0, 165, 255), (0, 255, 255) ,(0, 255, 0), (255, 255, 0), 
              (255, 0, 0), (255, 0, 255), (165, 0, 255), (0, 0, 255)] #лист с цветами в палитре bgr

#считываем камеру
vid = cv2.VideoCapture(0)
key = 0
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
_, frame_ = vid.read()

#константные значения
font = cv2.FONT_HERSHEY_COMPLEX
y_size, x_size = frame_.shape[:-1]

def warning_(): #создаем инструкцию, если нет кругов
    not_detect_img = np.full((y_size, x_size, 3), 0, np.uint8)
    cv2.rectangle(not_detect_img, (40, 40), (x_size - 40, y_size - 40), (255, 255, 255), 4)
    text = ['Круги не обнаружены! :(', 'Поместите в поле', 'видимости камеры круги', 'любых из следующих', 
            'цветов: красный,', 'оранжевый, желтый, зеленый,', 'бирюзовый, синий,', 'фиолетовый или фуксия.', 'Тогда, программа посчитает', 
            'круги и определит их цвета!'] #1 элемент - одна строка
    y = 0
    for t in text: #цикл для переноса строк
        y += 35
        cv2.putText(not_detect_img, t, (50, 50 + y), font, 1, (255, 255, 255), 2)
    return not_detect_img

not_detect_img = warning_()

def instruction(frame): #доп инструкция
    cv2.putText(frame, f"esc - выход", (5, 350), font, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, f"made by тетраэдр", (0, y_size - 10), font, 0.5, (255, 255, 255), 1)

def detect_shape(contour): #проверка, является ли обнаруженная фигура контуром
    eps = 0.029 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, eps, True) #длина approx - количество найденных вершин у "упрощенной" фигуры
    x, y, w, h = cv2.boundingRect(contour)
    if w/h <= 1.2 and w/h >= 0.8 and len(approx) >= 6 and len(approx) <= 12: return True #если соотношение ~1/1 и вершин больше 6, то это круг
    return False

def find_objects(frame): #ищем фигуры
    clrs = [0] * 8 #сколько фигур каждого цвета
    count_ = 0 #счетчик объектов
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    is_cnt = False #есть ли вообще фигуры
    for i in range(8): #проходимся по всем цветам
        bin = cv2.inRange(img, (colors_lh[i][0], 100, 0), (colors_lh[i][1], 255, 255)) #границы hue берем из ранее заданного листа
        if (i == 7):
            bin += cv2.inRange(img, (colors_lh[8][0], 100, 0), (colors_lh[8][1], 255, 255)) #обработка красного цвета
        contrs, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #ищем контуры
        for cnt in contrs:
            if cv2.contourArea(cnt) > 900 and detect_shape(cnt): #не берет во внимание мелкие объекты и не-круги
                is_cnt = True
                count_ += 1
                clrs[i] += 1
                (x, y), r = cv2.minEnclosingCircle(cnt)
                x, y, r = int(x), int(y), int(r)
                cv2.circle(frame, (x, y), r, colors_bgr[i], 5) #рисуем контур круга
                cv2.putText(frame, f"{colors[i]} круг", (x - r, y - r), font, 1, colors_bgr[i], 2) #подписываем круг
    return clrs, count_, is_cnt

def put_text(frame, count_, clrs): #размещение текста о количестве фигур на видео
    y = 30
    cv2.putText(frame, f"Количество кругов: {count_}", (5, y), font, 1, (255, 255, 255), 2)
    for i in range(8):
        y += 35
        cv2.putText(frame, f"{colors[i]}: {clrs[i]}", (5, y), font, 1, colors_bgr[i], 2)

def main(key, vid): #основной цикл отображения видео
    while key != 27: #пока пользователь не нажал esc 
        ret, frame = vid.read()
        if not ret: return 0 #если камера недоступна - выходим
        clrs, count_, is_cnt = find_objects(frame)
        if not is_cnt: #вывод инструкции если не найдено фигур
            frame = cv2.bitwise_or(frame, not_detect_img)
        else:
            put_text(frame, count_, clrs)
        instruction(frame)
        cv2.imshow('task_1', frame) #отображаем готовый кадр
        key = cv2.waitKey(1)

main(key, vid)
vid.release()
cv2.destroyAllWindows()
