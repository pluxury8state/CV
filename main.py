import numpy as np
import face_recognition
import cv2
import os
from imutils.video import VideoStream
from tkinter import Tk, Label, Entry, Button, Canvas
from PIL import Image, ImageTk


PATH = 'KnownFaces'  # Путь к папке с изображениями людей
PREVIOUS_MYLIST = os.listdir(PATH)  # переменная, которая хранит список людей до обновления
EncodeListKnown = []  # список точек людей, которые были декодированы
classNames = []  # список точек людей, которые были декодированы
IMAGES = []  # список изображений


def clicked_cancel():  # нажатие отмены
    save_and_quit(False)


def save_and_quit(param: bool):  # функция, которая нужна для успешного закрытия окон
    # параметр param нужен для того, чтобы знать записали ли мы человека в итоге или нет
    if window:
        window.destroy()
    if root:
        root.destroy()
    global SAVE_OR_NOT
    SAVE_OR_NOT = param


def confirm(*args, **kwargs):  # кнопка подтверждения
    img = cv2.imread("who.jpg")
    name = txt.get()
    isWritten = cv2.imwrite(os.path.join(os.getcwd(), 'KnownFaces', name + '.jpg'), img)
    save_and_quit(True)


def clicked_save():  # Окно сохранения человека
    global root
    root = Tk()
    root.geometry('400x200')
    lbl = Label(root, text="Введите имя нового человека:")
    lbl.grid(column=1, row=1)
    global txt
    txt = Entry(root, width=20)
    txt.grid(column=1, row=2)
    bnn_3 = Button(root, text="Сохранить", bg="green", fg="Black", command=confirm)
    bnn_3.grid(column=3, row=2)


def remain():  # Главное окно сохранения
    global window, root
    window = Tk()  # Главное окно сохранения
    root = None  # Вспомогательное окно сохранения

    window.geometry('700x600')
    window.title("Был обнаружен новый человек")

    # Добавим изображение:

    canvas = Canvas(window, height=480, width=640)
    image = Image.open(os.path.abspath('who.jpg'))
    photo = ImageTk.PhotoImage(image)
    img = canvas.create_image(0, 0, anchor='nw', image=photo)
    canvas.grid(row=0, column=0)

    # добавим пояснение

    lbl = Label(window, text="Желаете ли вы сохранить данные о новом человеке?")
    lbl.grid(column=0, row=2)
    btn_1 = Button(window, text="Да", bg="black", fg="red", command=clicked_save)
    btn_1.grid(column=0, row=600)
    btn_2 = Button(window, text="нет", bg="black", fg="red", command=clicked_cancel)
    btn_2.grid(column=1, row=600)

    window.mainloop()
    return SAVE_OR_NOT



def findEncodings(images):
    """
    Данная функция производит кодировки входящих фотографий с помощью библ. face_recognition
    и возвращает список кодировок
    :param images:
    :return: encodeList
    """
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def findEncode(image):
    """
    Данная функция делает все тоже самое, что и findEncodings(), но возвращает кодировку только одной фотографии
    :param image:
    :return: encode
    """
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # ошибка
    encode = face_recognition.face_encodings(img)[0]

    return encode


def vision():
    success, img = cap.read()  # Читаем с устройства кадр(картинку) , метод возвращает флаг success (True , False)
    # и img — саму картинку (массив numpy) .
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # принимаем кадр и изменям размер окна
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)  # поиск всех лиц в текущем кадре
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)  # поиск всех кодировок в текущем кадре

    return [img, imgS, facesCurFrame, encodeCurFrame]  # возвращаем кадр, измененный кадр, лица в кадре и
                                                        # кодировки, близкие к этому лицу


def refuse(save_or_not):
    """
    Данная функция либо дополняет базу фотографий, либо обрабатывает всю базу фотографий заново
    :return:
    """
    myList = os.listdir(PATH)
    print(myList)  # выводим список имеющихся фотографий людей в дирректории

    if_new_person = list(set(myList).difference(set(PREVIOUS_MYLIST)))  # переменная, которая узнает, был ли записан новый человек

    global EncodeListKnown
    if save_or_not:
        if if_new_person:    # Если это первое включение программы, то идет анализ всех фотографий в дирректории
            curImg = cv2.imread(f'{PATH}/{if_new_person[0]}')
            IMAGES.append(curImg)
            classNames.append(os.path.splitext(if_new_person[0])[0])
            global EncodeListKnown
            EncodeListKnown.append(findEncode(curImg))  # переменная которая овечает за обработанные фотографии
        else:                                                           # если это обновление программы для добавления нового человека                                      # то мы добавляем в массив распознанных людей только этого человека                                                             #  а фотографии всех оставшихся людей повторно не распознаем
            for person in myList:
                curImg = cv2.imread(f'{PATH}/{person}')
                IMAGES.append(curImg)
                classNames.append(os.path.splitext(person)[0])
            EncodeListKnown = findEncodings(IMAGES)  # переменная которая овечает за обработанные фотографии

    print(classNames)  # выводим список людей
    print("Декодирование закончено")


def refuse_camera():
    """
    Данная функция включает камеру
    :return:
    """
    cap = cv2.VideoCapture(0)  # включаем камеру
    cap.set(cv2.CAP_PROP_FPS, 60)  # Частота кадров
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)  # Ширина кадров в видеопотоке.
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Высота кадров в видеопотоке.
    return cap


if __name__ == '__main__':

    save_or_not = True  # параметр, который регулирует, нужно ли дополнить базу фотографий,
                        # или же просканировать текущую
    refuse(save_or_not)
    cap = refuse_camera()

    while True:

        img, imgS, facesCurFrame, encodeCurFrame = vision()

        for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):  # цикл распознования
            matches = face_recognition.compare_faces(EncodeListKnown, encodeFace)  # сравнение лиц
            faceDis = face_recognition.face_distance(EncodeListKnown, encodeFace)  # вероятность совпадения
            # print(faceDis)
            matchIndex = np.argmin(faceDis)     # переменная которая принимает индексы всех имен и возвращает
                                                # минимальный индекс
            if matches[matchIndex]:
                name = classNames[matchIndex]  # при совпадении ищет имя человека

                y1, x2, y2, x1 = faceLoc  # координаты лица
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 40), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2) # рисуем прямоугольник и отображаем имя человека
            else:  #если человек не был найден в кодировках, то добавляем человека в нашу базу
                cv2.imwrite('who.jpg', img)  # записываем файл в изображение
                save_or_not = remain()  # обновить или нет(диалоговое окно)
                cap.release()  #
                cv2.destroyAllWindows()  # закрываем окна
                print("Подождите, идет обновление ...")
                refuse(save_or_not)
                cap.release()  #
                cv2.destroyAllWindows()  # закрываем окна
                cap = refuse_camera()
                break

        cv2.imshow("WebCam", img)
        if cv2.waitKey(10) == 27:  # Выключаем камеру клавишей Esc
            break

    cap.release()  #
    cv2.destroyAllWindows()  # закрываем окна

