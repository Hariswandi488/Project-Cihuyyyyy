import tkinter as tk

window = tk.Tk()
window.geometry("640x800")
window.title("Tebak Angka Random")

frame = tk.Frame(window)
frame.place(x=0, y=0, relheight=1, relwidth=1)

window.mainloop()