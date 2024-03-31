from tkinter import *
import cv2
from PIL import Image, ImageTk
import numpy as np
import numpy.typing as npt
import random
import time
Mat = npt.NDArray[np.uint8]

#вспомогательные листы с цветами
colors = ['Оранжевый', 'Желтый', 'Зеленый', 'Бирюзовый', 'Синий', 
          'Фиолетовый', 'Красный'] #лист с названиями цветов
colors_lh = [[5, 20], [20, 40], [40, 90], [90, 100], [100, 120], 
             [120, 150], [150, 180], [0, 5]] #лист с границами цветов по hue, красный добавлен в конце 2 раза тк он есть с обоих концов шкалы hue
colors_rgb = [(255, 165, 0), (255, 255, 0) ,(0, 255, 0), (0, 255, 255), 
              (0, 0, 255), (255, 0, 255), (255, 0, 0)] #лист с цветами в палитре rgb

# захват камеры
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()
_, frame_ = cap.read()

#константные значения
font = cv2.FONT_HERSHEY_COMPLEX
y_size, x_size = frame_.shape[:-1]
base = np.full((y_size, x_size, 3), 0, np.uint8)

# параметры окна
root = Tk()
root.geometry(f"{x_size}x{y_size + 60}")
root.resizable(False, False)

#сообщение, если нет корзины в кадре
def instr_bascket():
    bascket = base.copy()
    text=["Не нашел корзину :(", "Поместите корзину (черный", "прямоугольник) в поле", "видимости камеры.",
          "Затем, поместите в корзину круги", "любых из следующих",
          'цветов: красный,', 'оранжевый, желтый, зеленый,', 
          'бирюзовый, синий,', ' или фиолетовый.', 'Затем, нажмите "Пуск"!']
    y = 0
    for t in text:
        y += 35
        cv2.putText(bascket, t, (5, y), font, 1, (255, 255, 255), 2)
    return bascket

bascket = instr_bascket()

# функция спавна шариков
ovals = []
def launchSpheres():
    global imageUnconverted
    #ищем объекты в корзине
    colors, rads = find_objects(imageUnconverted[coords[1]:coords[1] + coords[3], coords[0]:coords[0] + coords[2]])
    for i in range(len(colors)):
        r = rads[i] #круг будет нужного размера
        pt1 = (random.uniform(0 + r, x_size - r), random.uniform(-100 - r, 0)) #рандомное положение и рандомный порядок их выпадения
        ovals.append((canvasWidget.create_oval(pt1[0]-r, pt1[1]-r, pt1[0]+r, pt1[1]+r, fill=('#%02x%02x%02x'%colors[i])), 0))

# функция выхода из программы
def quit():
    root.destroy()

def detect_bascket_shape(contour): #проверка, является ли обнаруженная корзина прямоугольником
    eps = 0.029 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, eps, True) #длина approx - количество найденных вершин у "упрощенной" фигуры
    if len(approx) == 4: return True #если вершин 4, то это прямоугольник
    return False

coords = ()
def find_bascket(frame): #ищем корзину
    global coords
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    img = cv2.inRange(img, (0, 0, 0), (0, 0, 35)) #определяем черный цвет
    contrs, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contrs = sorted(contrs, key=cv2.contourArea)
    for cnt in contrs:
        if cv2.contourArea(cnt) > 800 and detect_bascket_shape(cnt): #если контур достаточно большой и прямоугольный
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 4)
            cv2.putText(frame, "Корзина", (x, y - 5), font, 1, (255, 255, 255), 2)
            buttonLaunchWidget.config(state="active", bg="#AAFF62")
            coords = (x, y, w, h)
            return True
    buttonLaunchWidget.config(state="disabled", bg="#BBFF95") #если корзины нет, кнопка пуск не активна
    return False

def detect_circle(contour): #проверка, является ли обнаруженная фигура кругом
    eps = 0.029 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, eps, True) #длина approx - количество найденных вершин у "упрощенной" фигуры
    x, y, w, h = cv2.boundingRect(contour)
    if w/h <= 1.2 and w/h >= 0.8 and len(approx) >= 6 and len(approx) <= 12: return True #если соотношение ~1/1 и вершин больше 6, то это круг
    return False

def find_objects(frame): #ищем фигуры
    clrs, rads = [], [] #цвета и радиусы, которые будем использовать для отрисовки кругов
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    for i in range(7): #проходимся по всем цветам
        bin = cv2.inRange(img, (colors_lh[i][0], 100, 0), (colors_lh[i][1], 255, 255)) #границы hue берем из ранее заданного листа
        if (i == 6):
            bin += cv2.inRange(img, (colors_lh[7][0], 100, 0), (colors_lh[7][1], 255, 255)) #обработка красного цвета
        contrs, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) #ищем контуры
        for cnt in contrs:
            if cv2.contourArea(cnt) > 500 and detect_circle(cnt): #не берет во внимание мелкие объекты и не-круги
                clrs.append(colors_rgb[i])
                (x, y), r = cv2.minEnclosingCircle(cnt)
                x, y, r = int(x), int(y), int(r)
                rads.append(r)
    return clrs, rads

# объявление и внедрение разнообразных виджетов в окно
buttonLaunchWidget = Button(text="Пуск", bd=2, bg="#AAFF62", activebackground="#CBFFA8", command=launchSpheres)
buttonLaunchWidget.place(width=120, height=40, x=80, y=10)

buttonQuitWidget = Button(text="Выйти", bd=2, bg="#FF6262", activebackground="#FFA8A8", command=quit)
buttonQuitWidget.place(width=120, height=40, x=440, y=10)

canvasWidget = Canvas(width=640, height=480)
canvasWidget.place(width=640, height=480, y=60)
backgroundImage = canvasWidget.create_image(0, 0, anchor=NW)

while True:
    # чтение картинки с камеры
    works, imageUnconverted = cap.read()
    if not works:
        quit()
    is_bascket = find_bascket(imageUnconverted)
    if not is_bascket:
        imageUnconverted = cv2.bitwise_or(imageUnconverted, bascket)
    # обработка картинки с камеры
    cv2.putText(imageUnconverted, f"made by тетраэдр", (0, y_size - 10), font, 0.5, (255, 255, 255), 1)
    imageRGB = cv2.cvtColor(imageUnconverted, cv2.COLOR_BGR2RGB)
    imageDefault = Image.fromarray(imageRGB)
    try:
        imageTK = ImageTk.PhotoImage(image=imageDefault)
        canvasWidget.itemconfigure(backgroundImage, image=imageTK) #меняем фреймы
    except RuntimeError:
        break

    # свободное падение
    for i in range(len(ovals)):
        if canvasWidget.coords(ovals[i][0])[3] >= y_size:
            ovals[i] = (ovals[i][0], (-ovals[i][1] * 0.97 + 9.8))
        else:
            ovals[i] = (ovals[i][0], (ovals[i][1] * 0.97 + 9.8))
        canvasWidget.move(ovals[i][0], 0, (ovals[i][1] * 0.03) // 1)                  

    # обновление окна
    root.update_idletasks()
    root.update()
    time.sleep(0.01)