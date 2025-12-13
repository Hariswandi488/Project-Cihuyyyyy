import tkinter as tk

window = tk.Tk()
window.geometry("480x720")
window.title("Kalkulator Sederhana")

frame = tk.Frame(window, bg="#2f2f2f")
frame.place(x=0, y=0, relwidth=1, relheight=1)

op_check = 1

def setup_button():
    entry.place(relx=0.5, rely=0.1, anchor="center")
    but_float.place(relx=0.1, rely=0.9, anchor="center")
    but_0.place(relx=0.365, rely=0.9, anchor="center")
    but_1.place(relx=0.1, rely=0.75, anchor="center")
    but_2.place(relx=0.365, rely=0.75, anchor="center")
    but_3.place(relx=0.635, rely=0.75, anchor="center")
    but_4.place(relx=0.1, rely=0.6, anchor="center")
    but_5.place(relx=0.365, rely=0.6, anchor="center")
    but_6.place(relx=0.635, rely=0.6, anchor="center")
    but_7.place(relx=0.1, rely=0.45, anchor="center")
    but_8.place(relx=0.365, rely=0.45, anchor="center")
    but_9.place(relx=0.635, rely=0.45, anchor="center")
    but_add.place(relx=0.9, rely=0.6, anchor="center")
    but_subtract.place(relx=0.9, rely=0.45, anchor="center")
    but_divide.place(relx=0.9, rely=0.3, anchor="center")
    but_multiple.place(relx=0.635, rely=0.3, anchor="center")
    but_clear.place(relx=0.365, rely=0.3, anchor="center")
    but_backspace.place(relx=0.1, rely=0.3, anchor="center")
    but_empty.place(relx=0.635, rely=0.9, anchor="center")
    but_equal.place(relx=0.9, rely=0.825, anchor="center")

def input_angka(angka):
    global op_check
    last_entry = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, last_entry + str(angka))
    op_check = 0
    

def input_operator(ope):
    global op_check
    if op_check == 0:
        last_entry = entry.get()
        entry.delete(0, tk.END)
        entry.insert(0, last_entry + str(ope))
        op_check = 1


def clear_entry():
    global op_check
    entry.delete(0, tk.END)
    op_check = 1

def backspace():
    global op_check
    last_entry = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, last_entry[:-1])
    op_check = 0
    backspace_op_check()

def backspace_op_check():
    global op_check
    current = entry.get()
    if not current:
        op_check = 1

def result():
    current = entry.get()
    res = eval(current)
    entry.delete(0, tk.END)
    entry.insert(0, res)

entry = tk.Entry(frame, width=15, font=("Arial", 35), bg="#b1b1b1")
but_equal = tk.Button(frame, text="=", width=8, height=7, bg="#b1b1b1", font=("Arial",18), command=result)
but_add = tk.Button(frame, text="+", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=lambda: input_operator("+"))
but_subtract = tk.Button(frame, text="-", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=lambda: input_operator("-"))
but_divide = tk.Button(frame, text="/", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=lambda: input_operator("/"))
but_multiple = tk.Button(frame, text="x", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=lambda: input_operator("*"))
but_float = tk.Button(frame, text="00,0", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=lambda: input_operator("."))
but_clear = tk.Button(frame, text="C", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=clear_entry)
but_backspace = tk.Button(frame, text="<--", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=backspace)
but_empty = tk.Button(frame, text=" ", width=8, height=3, bg="#b1b1b1", font=("Arial",18))
but_0 = tk.Button(frame, text="0", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=lambda: input_angka(0))
but_1 = tk.Button(frame, text="1", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=lambda: input_angka(1))
but_2 = tk.Button(frame, text="2", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=lambda: input_angka(2))
but_3 = tk.Button(frame, text="3", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=lambda: input_angka(3))
but_4 = tk.Button(frame, text="4", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=lambda: input_angka(4))
but_5 = tk.Button(frame, text="5", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=lambda: input_angka(5))
but_6 = tk.Button(frame, text="6", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=lambda: input_angka(6))
but_7 = tk.Button(frame, text="7", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=lambda: input_angka(7))
but_8 = tk.Button(frame, text="8", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=lambda: input_angka(8))
but_9 = tk.Button(frame, text="9", width=8, height=3, bg="#b1b1b1", font=("Arial",18), command=lambda: input_angka(9))

setup_button()
window.mainloop()