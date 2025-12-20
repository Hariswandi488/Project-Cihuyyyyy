import tkinter as tk
import os, random
from PIL import Image, ImageTk

kesempatan = 0
angka_akhir = 0
secret_num = 0

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

def setup_button_diff():
    text.config(text="Pilih Mode Kesulitan")
    text.place(relx=0.5, rely=0.1, anchor="center")
    button_easy.place(relx=0.5, rely=0.3, anchor="center")
    button_normal.place(relx=0.5, rely=0.45, anchor="center")
    button_hard.place(relx=0.5, rely=0.6, anchor="center")
    button_insane.place(relx=0.5, rely=0.75, anchor="center")
    button_imposible.place(relx=0.5, rely=0.9, anchor="center")

def invisible_button_diff():
    button_easy.place_forget()
    button_normal.place_forget()
    button_hard.place_forget()
    button_insane.place_forget()
    button_imposible.place_forget()

def settings_diff(diff):
    global kesempatan, angka_akhir, secret_num
    invisible_button_diff()
    if diff == "easy":
        kesempatan = 5
        angka_akhir = 10
    elif diff == "normal":
        kesempatan = 10
        angka_akhir = 25
    elif diff == "hard":
        kesempatan = 15
        angka_akhir = 50
    elif diff == "insane":
        kesempatan = 25
        angka_akhir = 100
    elif diff == "imposible":
        kesempatan = 50
        angka_akhir = 1000


    teks = f"!!INFORMASI GAME!!\n\nkamu akan di suruh menebak angka Random\n\nkamu memilih diff {diff}\njadi angka akan di acak dari 1 - {angka_akhir}\nkamu juga di beri \nkesempatan menebak sebanyak {kesempatan}\n\ntekan tombol Lanjutkan\nuntuk memulai game tebak angka nya"

    button_next.place(relx=0.5, rely=0.85, anchor="center")
    text.place(relx=0.5, rely=0.5, anchor="center")
    text.config(text=teks)
    secret_num = random.randint(1, angka_akhir)


def setup_button_game():
    button_next.place_forget()
    text.config(text="Tebak Angka Random")
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
    button_guess.place(relx=0.625, rely=0.85, anchor="center")
    button_clear.place(relx=0.25, rely=0.85, anchor="center")
    text.place(relx=0.5, rely=0.1, anchor="center")

def entry_number(num):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + str(num))

def entry_clear():
    entry.delete(0, tk.END)

def guess():
    current = entry.get()
    if current == secret_num:
        pass
    elif current <= secret_num:
        pass
    elif current >= secret_num:
        pass




entry = tk.Entry(frame, font=("Arial", 20), width=25)
button_easy = tk.Button(frame, font=("Arial", 20), text="Easy", width=15, height=2,command=lambda:settings_diff("easy"))
button_normal = tk.Button(frame, font=("Arial", 20), text="Normal", width=15, height=2,command=lambda:settings_diff("normal"))
button_hard = tk.Button(frame, font=("Arial", 20), text="Hard", width=15, height=2,command=lambda:settings_diff("hard"))
button_insane = tk.Button(frame, font=("Arial", 20), text="Insane", width=15, height=2,command=lambda:settings_diff("insane"))
button_imposible = tk.Button(frame, font=("Arial", 20), text="Imposible", width=15, height=2,command=lambda:settings_diff("imposible"))
button_next = tk.Button(frame, font=("Arial", 20), text="Lanjutkan", width=15, height=2, command=setup_button_game)
button_1 = tk.Button(
    frame,
    font=("Arial", 20),
    text="1",
    width=6,
    height=2,
    command=lambda:entry_number(1)
)
button_2 = tk.Button(
    frame,
    font=("Arial", 20),
    text="2",
    width=6,
    height=2,
    command=lambda:entry_number(2)
)
button_3 = tk.Button(
    frame,
    font=("Arial", 20),
    text="3",
    width=6,
    height=2,
    command=lambda:entry_number(3)
)
button_4 = tk.Button(
    frame,
    font=("Arial", 20),
    text="4",
    width=6,
    height=2,
    command=lambda:entry_number(4)
)
button_5 = tk.Button(
    frame,
    font=("Arial", 20),
    text="5",
    width=6,
    height=2,
    command=lambda:entry_number(5)
)
button_6 = tk.Button(
    frame,
    font=("Arial", 20),
    text="6",
    width=6,
    height=2,
    command=lambda:entry_number(6)
)
button_7 = tk.Button(
    frame,
    font=("Arial", 20),
    text="7",
    width=6,
    height=2,
    command=lambda:entry_number(7)
)
button_8 = tk.Button(
    frame,
    font=("Arial", 20),
    text="8",
    width=6,
    height=2,
    command=lambda:entry_number(8)
)
button_9 = tk.Button(
    frame,
    font=("Arial", 20),
    text="9",
    width=6,
    height=2,
    command=lambda:entry_number(9)
)
button_guess = tk.Button(
    frame,
    font=("Arial", 20),
    text="Tebak",
    width=13,
    height=2,
    command=entry_number("guess")
)
button_clear = tk.Button(
    frame,
    font=("Arial", 20),
    text="C",
    width=6,
    height=2,
    command=entry_clear
)
text= tk.Label(frame, font=("Arial",15), text="Tebak Angka Random")


setup_button_diff()
window.mainloop()