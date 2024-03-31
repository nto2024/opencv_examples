import cv2
import numpy as np

#служебная часть

#вспомогательные листы с цветами
colors = ['Оранжевый', 'Желтый', 'Зеленый', 'Бирюзовый', 'Синий', 
          'Фиолетовый', 'Красный'] #лист с названиями цветов
colors_lh = [[5, 20], [20, 40], [40, 90], [90, 100], [100, 120], 
             [120, 150], [150, 180], [0, 5]] #лист с границами цветов по hue, красный добавлен в конце 2 раза тк он есть с обоих концов шкалы hue
colors_bgr = [(0, 165, 255), (0, 255, 255) ,(0, 255, 0), (255, 255, 0), 
              (255, 0, 0), (255, 0, 255), (0, 0, 255)] #лист с цветами в палитре bgr

#считываем камеру
vid = cv2.VideoCapture(0)
key = 0
vid.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
_, frame_ = vid.read()

#константные значения
font = cv2.FONT_HERSHEY_COMPLEX
y_size, x_size = frame_.shape[:-1]

#если несколько или нет совсем кругов в кадре
def make_warring():
    warring = np.full((y_size, x_size, 3), 0, np.uint8)
    cv2.rectangle(warring, (40, 40), (x_size - 40, y_size - 40), (255, 255, 255), 4)
    text = ['Поместите в поле', 'видимости камеры ОДИН круг', 'любой из следующих', 
        'цветов: красный,', 'оранжевый, желтый, зеленый,', 'бирюзовый, синий,', 'или фиолетовый.', 'Тогда, программа отрисует', 
        'путь круга его цветом!']
    y = 0
    for t in text: #цикл для переноса строк
        y += 35
        cv2.putText(warring, t, (50, 50 + y), font, 1, (255, 255, 255), 2)
    return warring

warring = make_warring()

#информацияЮ находящаяся постоянно на экране
def instruction(frame):
    cv2.putText(frame, f"esc - выход", (5, 70), font, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, f"e - стереть", (5, 95), font, 0.5, (255, 255, 255), 1)
    cv2.putText(frame, f"made by тетраэдр", (0, y_size - 10), font, 0.5, (255, 255, 255), 1)

def detect_shape(contour): #проверка, является ли обнаруженная фигура кругом
    eps = 0.029 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, eps, True) #длина approx - количество найденных вершин у "упрощенной" фигуры
    x, y, w, h = cv2.boundingRect(contour)
    if w/h <= 1.1 and w/h >= 0.9 and len(approx) >= 7 and len(approx) <= 12: return True #если соотношение ~1/1 и вершин больше 6, то это круг
    return False

def find_objects(frame, path, path_a): #ищем фигуры
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    is_one = False #есть ли вообще фигуры
    x, y, r = 0, 0, 0
    for i in range(7): #проходимся по всем цветам
        bin = cv2.inRange(img, (colors_lh[i][0], 100, 10), (colors_lh[i][1], 255, 255)) #границы hue берем из ранее заданного листа
        if (i == 6):
            bin += cv2.inRange(img, (colors_lh[7][0], 100, 10), (colors_lh[7][1], 255, 255)) #обработка красного цвета
        bin = cv2.morphologyEx(bin, cv2.MORPH_OPEN, np.full((5, 5), 1, np.uint8))
        contrs, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #ищем контуры
        for cnt in contrs:
            if cv2.contourArea(cnt) > 800 and detect_shape(cnt): #не берет во внимание мелкие объекты и не-круги
                if is_one: return False, 0, path, path_a #если мы нашли подходящий контур до этого, значит в кадре > 1 круга => не подходит
                is_one = True
                clr_i = i
                (x, y), r = cv2.minEnclosingCircle(cnt)
                x, y, r = int(x), int(y), int(r)
    if not is_one: return False, 0,  path, path_a
    cv2.circle(path, (x, y), r, colors_bgr[clr_i], -1) #рисуем траекторию
    cv2.circle(path_a, (x, y), r, (0, 0, 0), -1) #и ее "альфа-канал"
    return True, clr_i, path, path_a

def main():
    path = np.zeros((y_size, x_size, 3), np.uint8) #здесь отрисовывается траектория
    path_a = np.full((y_size, x_size, 3), 255, np.uint8) #"альфа-канал" траектории
    count_ = 0
    key = 0
    is_one, instr = False, False
    clr_i = 0
    while key != 27: #пока пользователь не нажмет esc
        ret, frame = vid.read()
        if not ret: return 0
        cv2.imshow('camera', frame) #вывод оригинального кадра с камеры для удобства перемещения кружка
        count_ = (count_ + 1) % 3 #искуственная задержка, создана для того, чтобы траектория отображалась именно кругами, а не сплошной линией
        if count_ == 0:
            is_one, clr_i, path, path_a = find_objects(frame, path, path_a)
        frame = cv2.bitwise_and(frame, path_a) #добавляем альфа-канал в кадр
        frame = cv2.bitwise_or(frame, path) #добавляем саму цветную траекторию
        if not is_one:
            if not instr: #если не показывали инструкцию до этого
                frame = cv2.bitwise_or(frame, warring)
        else: #пишем, какой круг сейчас в кадре
            instr = True
            (w, h), y = cv2.getTextSize(f"{colors[clr_i]} круг", font, 1, 2)
            cv2.rectangle(frame, (5, 35 + y), (5 + w, 30 - h), (255, 255, 255), -1)
            cv2.putText(frame, f"{colors[clr_i]} круг", (5, 35), font, 1, colors_bgr[clr_i], 2) #подписываем круг
        instruction(frame)
        cv2.imshow('path', frame)
        key = cv2.waitKey(1)
        if key == ord('e'):
            instr = False 
            path = np.zeros((y_size, x_size, 3), np.uint8)
            path_a = np.full((y_size, x_size, 3), 255, np.uint8)
        
main()
vid.release()
cv2.destroyAllWindows()