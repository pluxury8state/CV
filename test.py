
import os
from tkinter import Tk, Label, Entry, Button, Canvas

import cv2
from PIL import Image, ImageTk


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


if __name__ == "__main__":
    print(remain())
