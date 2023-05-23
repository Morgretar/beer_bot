import tkinter
from tkinter import ttk
from tkinter import *
from db import DataBase

db = DataBase('localhost', 'root', 'Morgretar2023', 'beer')
def alert():
    def close_form():
        top_window.destroy()
    top_window = tkinter.Toplevel(window)
    top_window.overrideredirect(True)
    window.eval(f'tk::PlaceWindow {str(top_window)} center')
    lbl = Label(top_window, text="Ошибка добавления записи!")
    lbl.place(x=25, y=10)
    top_window.title("Ошибка")
    top_window.geometry("250x70")
    alert_button = Button(top_window, text="Окай :-(", command=close_form)
    alert_button.place(x=85, y=40)

def ok():
    def close_form():
        top_window.destroy()
    top_window = tkinter.Toplevel(window)
    top_window.overrideredirect(True)
    window.eval(f'tk::PlaceWindow {str(top_window)} center')
    lbl = Label(top_window, text="Запись успешно добавлена!")
    lbl.place(x=25, y=10)
    top_window.title("Добавлено")
    top_window.geometry("250x70")
    alert_button = Button(top_window, text="Ок", command=close_form)
    alert_button.place(x=15, y=50)

def get_values_drink(name, counts):
    drink_name = name.get()
    count_drink = counts.get()
    try:
        db.insert_drink(drink_name, count_drink)
        ok()
    except:
        alert()



window = Tk()
window.geometry("300x150")
window.title("Добавление остатков")
window.eval('tk::PlaceWindow . center')
drinks_name = Label(window, text="Напиток")
drinks_name.place(x=35, y=25)
list_drinks = ttk.Combobox(window, values=db.get_all_drink(), width=25)
list_drinks.place(x=105, y=25)
drinks_name = Label(window, text="Количество")
drinks_name.place(x=35, y=75)
count_drinks = Entry(window, width=5)
count_drinks.place(x=105, y=75)
btn_add = Button(window, text="Добавить", command=lambda: get_values_drink(list_drinks, count_drinks))
btn_add.place(x=115, y=115)

window.mainloop()
