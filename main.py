import tkinter as tk
import analyse
from tkinter import *
win = tk.Tk()
win.geometry(f"800x500+100+200")
win.title('Морфологический анализатор')

def add_let() :
    pos = len(ent1.get())
    ent1.insert(pos, 'æ')

def fill_text():
    lang = 'oss'
    if r_var.get() == True:
        lang = 'dig'
    tokens = analyse.get_tags(ent1.get(), lang)
    output_text=""
    err_msg="Нет результатов анализа по данному слову"
    for analysed_word in tokens:
        output_text+=analysed_word+"\n\n"
        err_msg=""
    text.delete(1.0, END)
    text.insert(1.0, output_text+err_msg)


label_1 = tk.Label(win, text="Впишите слово, словарную форму которого нужно найти",
                   font = ('Arial', 20),
                   pady=20)
btn1 = tk.Button(win, text="æ", font=('Arial', 15), command=add_let)
ent1 = tk.Entry(win, font=('Arial', 15))
btn2 = tk.Button(win, text='Найти', font=('Arial', 15), command=fill_text)
text = Text(width=40, height=15, font=('Arial', 14))
scroll = Scrollbar(command=text.yview)

r_var = BooleanVar()
r_var.set(False)
r1 = Radiobutton(text='Осетинский корпус', variable=r_var, value=False, font=('Arial', 15))
r2 = Radiobutton(text='Дигорский корпус', variable=r_var, value=True, font=('Arial', 15))


label_1.grid(row=0, columnspan=3)
r1.grid(row = 1, column = 0, stick ='w')
r2.grid(row = 2, column = 0, stick ='w')
btn1.grid(row = 3, column=0, stick ='e')
ent1.grid(row=3, column=1, stick ='we', ipady = 5)
btn2.grid(row=3, column=2, stick ='w')
text.grid(row = 5, column = 0, pady = 20, columnspan = 2, stick='we')
scroll.grid(row = 5, column = 2, stick='nsw', pady=20)
text.config(yscrollcommand=scroll.set)
win.mainloop()
