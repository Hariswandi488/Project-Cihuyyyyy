import tkinter as tk
import os
from PIL import Image, ImageTk

window = tk.Tk()
window.geometry("480x720")
window.title("Tebak Angka Random")

frame = tk.Frame(window)
frame.place(x=0, y=0, relheight=1, relwidth=1)

base_path = os.path.dirname(os.path.abspath(__file__))
asset_path = os.path.join(base_path, "Asset")
bg_img = Image.open(os.path.join(asset_path, "bg.jpg"))

w = window.winfo_screenwidth()
h = window.winfo_screenheight()
bg_resize = bg_img.resize((w, h))
bg_overlay = Image.new("RGBA", bg_resize.size, (0, 0, 0, 50))
bg_color_set = Image.alpha_composite(bg_resize.convert("RGBA"), bg_overlay)
bg_tk = ImageTk.PhotoImage(bg_color_set)
bg_label = tk.Label(frame, image=bg_tk).place(x=0, y=0, relwidth=1, relheight=1)

def setup_button():
    entry.place(relx=0.5, rely=0.2, anchor="center")
    button_1.place(relx=0.25, rely=0.4, anchor="center")
    button_2.place(relx=0.5, rely=0.4, anchor="center")
    button_3.place(relx=0.75, rely=0.4, anchor="center")
    button_4.place(relx=0.25, rely=0.55, anchor="center")
    button_5.place(relx=0.5, rely=0.55, anchor="center")
    button_6.place(relx=0.75, rely=0.55, anchor="center")
    button_7.place(relx=0.25, rely=0.7, anchor="center")
    button_8.place(relx=0.5, rely=0.7, anchor="center")
    button_9.place(relx=0.75, rely=0.7, anchor="center")
    button_guess.place(relx=0.5, rely=0.85, anchor="center")
    text.place(relx=0.5, rely=0.1, anchor="center")    

entry = tk.Entry(frame, font=("Arial", 20), width=25)
button_1 = tk.Button(
    frame,
    font=("Arial", 20),
    text="1",
    width=6,
    height=2
)
button_2 = tk.Button(
    frame,
    font=("Arial", 20),
    text="2",
    width=6,
    height=2
)
button_3 = tk.Button(
    frame,
    font=("Arial", 20),
    text="3",
    width=6,
    height=2
)
button_4 = tk.Button(
    frame,
    font=("Arial", 20),
    text="4",
    width=6,
    height=2
)
button_5 = tk.Button(
    frame,
    font=("Arial", 20),
    text="5",
    width=6,
    height=2
)
button_6 = tk.Button(
    frame,
    font=("Arial", 20),
    text="6",
    width=6,
    height=2
)
button_7 = tk.Button(
    frame,
    font=("Arial", 20),
    text="7",
    width=6,
    height=2
)
button_8 = tk.Button(
    frame,
    font=("Arial", 20),
    text="8",
    width=6,
    height=2
)
button_9 = tk.Button(
    frame,
    font=("Arial", 20),
    text="9",
    width=6,
    height=2
)
button_guess = tk.Button(
    frame,
    font=("Arial", 20),
    text="Tebak",
    width=21,
    height=1
)
text= tk.Label(frame, font=("Arial",15), text="Tebak Angka Random")


setup_button()
window.mainloop()