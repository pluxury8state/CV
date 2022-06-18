import numpy as np
import face_recognition
import cv2
import os
from imutils.video import VideoStream
from datetime import datetime
from test import remain


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name):
    with open("Attendance.csv", "r+") as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")
            f.writelines(f'\n{name}, {dtString}')


def vision():
    success, img = cap.read()  # Читаем с устройства кадр(картинку) , метод возвращает флаг success (True , False)
    # и img — саму картинку (массив numpy) .
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)  # принимаем кадр и изменям размер окна # ошибка возможно
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)  # поиск всех лиц в текущем кадре
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)  # поиск всех кодировок в текущем кадре

    return [img, imgS, facesCurFrame, encodeCurFrame]


def findEncode(image):

    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)[0]

    return encode


def refuse():
    path = 'KnownFaces'
    images = []
    classNames = []
    myList = os.listdir(path)
    print(myList)  # выводим список имеющихся фотографий людей в дирректории

    for cls in myList:
        curImg = cv2.imread(f'{path}/{cls}')
        images.append(curImg)
        classNames.append(os.path.splitext(cls)[0])

    print(classNames)  # выводим список людей

    encodeListKnown = findEncodings(images)  # переменная которая овечает за обработанные фотографии
    print("Декодирование закончено")
    return [encodeListKnown, classNames]



def refuse_camera():
    cap = cv2.VideoCapture(0)  # включаем камеру
    cap.set(cv2.CAP_PROP_FPS, 60)  # Частота кадров
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)  # Ширина кадров в видеопотоке.
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Высота кадров в видеопотоке.
    return cap


if __name__ == '__main__':


    encodeListKnown, classNames = refuse()
    cap = refuse_camera()

    while True:

        img, imgS, facesCurFrame, encodeCurFrame = vision()

        for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):  # цикл распознования
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)  # сравнение лиц
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)  # вероятность совпадения
            # print(faceDis)
            matchIndex = np.argmin(faceDis)     # переменная которая принимает индексы всех имен и возвращает
                                                # минимальный индекс
            if matches[matchIndex]:
                name = classNames[matchIndex]  # при совпадении ищет имя человека

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 40), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2) # рисуем прямоугольник и отображаем имя человека
                markAttendance(name)  # записываем данные о человеке
            else:
                cv2.imwrite('who.png', img)
                remain()
                cap.release()  #
                cv2.destroyAllWindows()  # закрываем окна
                print("Подождите, идет обновление ...")
                encodeListKnown, classNames = refuse()
                cap.release()  #
                cv2.destroyAllWindows()  # закрываем окна
                cap = refuse_camera()
                break

        cv2.imshow("WebCam", img)
        if cv2.waitKey(10) == 27:  # Выключаем камеру клавишей Esc
            break

    cap.release()  #
    cv2.destroyAllWindows()  # закрываем окна