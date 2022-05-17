import tkinter
import tkinter.filedialog as fl
import os
import matplotlib.pyplot as plt
#
#
# def clicked():
#     lbl.configure(text="Был, да сплыл...")
#
#
# window = Tk()
# window.geometry('400x250')
# window.title("Добро пожаловать в приложение PythonRu")
# lbl = Label(window, text="Был найден новый человек")
# lbl.grid(column=1, row=1)
# btn_1 = Button(window, text="Сохранить", bg="black", fg="red", command=clicked)
# btn_1.grid(column=0, row=0)
# btn_2 = Button(window, text="Отмена", bg="black", fg="red")
# btn_2.grid(column=1000, row=1000)
#
# window.mainloop()

# fl.asksaveasfilename() # Выберите имя файла для сохранения и верните имя файла
fl.askopenfilename() # Выберите файл для открытия и верните имя файла


root = tkinter.Tk() # Создать экземпляр Tkinter.Tk ()
root.withdraw() # скрыть экземпляр Tkinter.Tk ()
default_dir = os.path.abspath("")
file_path = tkinter.filedialog.askopenfilename(title = u'выбрать файл', initialdir=(os.path.expanduser(default_dir)))
image = tkinter.Image.open(file_path)
plt.imshow(image)
plt.show()
root = tkinter.Tk () # Создать экземпляр Tkinter.Tk ()
root.withdraw () # скрыть экземпляр Tkinter.Tk ()

fname = tkinter.filedialog.asksaveasfilename(title = u'save file ', filetypes = [("PNG", ".png")])
image.save(str(fname) + '.png', 'PNG')
