import tkinter as tk
import os, sqlite3, random

window = tk.Tk()
window.geometry("480x720")
window.title("Random Nickname Generator")

frame = tk.Frame(window, bg="#2f2f2f")
frame.place(x=0, y=0, relheight=1, relwidth=1)

base_path = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(base_path, "Nick_List.db")
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

list_name = [
    "Budi",
    "Bambang",
    "Agus",
    "Rizki",
    "Ikbal",
    "Raffi"
]

def tabel_db():
    cursor.execute("""CREATE TABLE IF NOT EXISTS list_name(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT
    )
    """)

def invisible():
    gen_button.place_forget()
    view_button.place_forget()
    label_text.place_forget()
    back_button.place_forget()
    list_box.place_forget()

def setup_button():
    invisible()
    gen_button.place(relx=0.5, rely=0.6, anchor="center")
    label_text.place(relx=0.5, rely=0.2, anchor="center")
    view_button.place(relx=0.5, rely= 0.7, anchor="center")

def random_name():
    Name = random.choice(list_name) + str(random.randint(1, 100))
    cursor.execute("SELECT name FROM list_name")
    used_name = cursor.fetchall()

    if Name not in used_name:
        cursor.execute("INSERT INTO list_name (name) VALUES (?)", (Name,))
        conn.commit()
        label_text.config(text=f"{Name}")
    else:
        random_name()


def view_name():
    invisible()
    list_box.place(relx=0.5, rely=0.5, anchor="center")
    label_text.place(relx=0.5, rely=0.1, anchor="center")
    back_button.place(relx=0.5, rely=0.9, anchor="center")
    label_text.config(text="List-List NickName\nYang Sudah Ada")

    cursor.execute("SELECT * FROM list_name")
    rows = cursor.fetchall()
    list_box.delete(0, tk.END)
    for i, row in enumerate(rows, start=1):
        id, name = row
        list_box.insert(tk.END, f"{i}. {name}")

back_button = tk.Button(frame, font=("Arial", 20), text="Kembali", command=setup_button)
list_box = tk.Listbox(frame, font=("Arial", 15), width=30, height=18)
view_button = tk.Button(frame, text="View all List Name", font=("Arial", 20), command=view_name)
gen_button = tk.Button(frame, text="GENERATE", font=("Arial", 20), command=random_name)
label_text = tk.Label(frame, text="Tekan Tombol Untuk\nGenerate Random Nickname", font=("Arial", 20))

tabel_db()
setup_button()
window.mainloop()