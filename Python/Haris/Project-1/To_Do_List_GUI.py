import sqlite3, pygame, os, threading, time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from To_Do_List_Notify import notification_Show

InMode = 0

# Other Thread For Music Loop
def play_BGM():
    BGM_Playing = BGM_Sound.play()
    print("Sound Start")
    def cek_BGM():
        while BGM_Playing.get_busy():
            time.sleep(1.0)

        play_BGM()
        
    threading.Thread(target=cek_BGM, daemon=True).start()
    
# TK Init
window = tk.Tk()
window.geometry("1280x720")
window.title("TO-DO LIST")
pygame.mixer.init()

# Path File
base_path = os.path.dirname(os.path.abspath(__file__))
SFX_path = os.path.join(base_path, "SFX")

Click_Sound = pygame.mixer.Sound(os.path.join(SFX_path, "Click.mp3"))
Notif_Sound = pygame.mixer.Sound(os.path.join(SFX_path, "Notifikasi.wav"))
Start_Sound = pygame.mixer.Sound(os.path.join(SFX_path, "Start2.mp3"))
BGM_Sound = pygame.mixer.Sound(os.path.join(SFX_path, "BGM.mp3"))
Bg_Img = Image.open(os.path.join(base_path, "Asset/city.jpg"))

# Volume Variable
volume_var = tk.DoubleVar(value=0.0)
volume_timer = None

# Path SQL/db File
root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
Task_file = "Tasks.db"
Task_Done_file = "Tasks_Done.db"
Task_path = os.path.join(base_path, Task_file)
Task_Done_path = os.path.join(base_path, Task_Done_file)
conn = sqlite3.connect(Task_path)
conn1 = sqlite3.connect(Task_Done_path)
cursor = conn.cursor()
cursor1 = conn1.cursor()

# Setup Tabel 
def setup_gui():
    global cursor, cursor1, conn, conn1
    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Task TEXT,
                Inprogress BOOLEAN
    )
    """)
    cursor1.execute("""
    CREATE TABLE IF NOT EXISTS tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Task TEXT,
                Done BOOLEAN
    )                  
    """)
    conn.commit()
    conn1.commit()

# Menu Button Place
def Menu_default():
    global InMode
    InMode = 100
    Invisible_Menu()
    Label_title.place(relx=0.5, y=40, anchor="center")
    Label_title.config(text="MENU TUGAS")
    entry.place(relx=0.5, y=2000, anchor="center")
    button_add.place(relx=0.25, y=150, anchor="center")
    button_del.place(relx=0.75, y=150, anchor="center")
    button_progress.place(relx=0.25, y=300, anchor="center")
    button_done.place(relx=0.75, y=300, anchor="center")
    button_view.place(relx=0.25, y=450, anchor="center")
    button_view_done.place(relx=0.75, y=450, anchor="center")
    button_close.place(relx=0.75, y=600, anchor="center")
    button_edit.place(relx=0.25, y=600, anchor="center")
    listbox.place(relx=0.5, y=2000,  anchor="center")
    button_cancel.place(relx=0.5, y=2000, anchor="center")
    button_enter.place(relx=0.5, y=2000, anchor="center")
    button_volume.place(relx=0.1, y=630, anchor="center")
    Sound_volume.place(relx=0.1, y=2000, anchor="center")

# All Button Invisible
def Invisible_Menu():
    entry.place_forget()
    button_add.place_forget()
    button_view.place_forget()
    button_progress.place_forget()
    button_done.place_forget()
    button_view_done.place_forget()
    button_del.place_forget()
    button_close.place_forget()
    listbox.place_forget() 
    button_cancel.place_forget()
    button_enter.place_forget()
    Sound_volume.place_forget()
    button_edit.place_forget()

# Add Task System
def button_add():
    global InMode
    Invisible_Menu()
    entry.place(relx=0.5, rely=0.2, anchor="center")
    Label_title.config(text="ISI NAMA TUGAS BARU")
    button_cancel.place(relx=0.5, y=450, anchor="center")
    button_enter.place(relx=0.5, y=300, anchor="center")
    InMode = 1

# View Task System
def view_task_gui():
    global InMode
    Invisible_Menu()
    Label_title.config(text="LIST TUGAS")
    button_cancel.place(relx=0.5, y=600, anchor="center")
    listbox.place(relx=0.5, y=300,  anchor="center")
    InMode = 0

    listbox.delete(0, tk.END)
    cursor.execute("SELECT task, Inprogress FROM tasks")
    for i, row in enumerate(cursor.fetchall(), start=1):
        Task, Inprogress = row
        status = "Dalam Pengerjaan" if Inprogress else "Belum Dikerjakan"
        listbox.insert(tk.END, f"{i}. {Task} ({status})")

# Delete Taks System
def del_task():
    global InMode
    Invisible_Menu()
    Label_title.config(text="HAPUS TUGAS")
    button_cancel.place(relx=0.35, y=600, anchor="center")
    button_enter.place(relx=0.65, y=600, anchor="center")
    listbox.place(relx=0.5, y=300,  anchor="center")
    InMode = 2
    
    listbox.delete(0, tk.END)
    cursor.execute("SELECT Task, Inprogress FROM tasks")
    for i, row in enumerate(cursor.fetchall(), start=1):
        listbox.insert(tk.END, row[0])

# Cancel Button System
def Cancel():
    Invisible_Menu()
    Menu_default()

# Enter Button System
def enter(event=None):
    global InMode,New_Name,select_edit
    if InMode == 1: # In Add Task System
        Task = entry.get()
        if Task:
            cursor.execute("INSERT INTO tasks (Task, Inprogress) VALUES (?, ?)", (Task, False))
            conn.commit()
            entry.delete(0, tk.END)
            Menu_default()
        else:
            messagebox.showwarning("Warning", "Input Tidak Boleh Kosong")
    elif InMode == 2: # In Delete Task System
        try:
            selected = listbox.get(listbox.curselection())
            cursor.execute("DELETE FROM tasks WHERE Task = ?", (selected,))
            conn.commit()
            del_task()
        except:
            messagebox.showinfo("Info", "Pilih Tugas Yang Mau Di Hapus Dulu")
    elif InMode == 3: # In Progress Task System
        try:
            selected = listbox.get(listbox.curselection())
            cursor.execute("UPDATE tasks SET Inprogress = ? WHERE Task = ?", (True, selected))
            conn.commit()
            prog_task()
        except:
            messagebox.showinfo("Info", "Pilih Tugas Yang Mau Di Tandai Dulu")
    elif InMode == 4: # In Done Task System
        try:
            selected = listbox.get(listbox.curselection())
            cursor.execute("SELECT Task FROM tasks WHERE Task = ?", (selected,))
            data = cursor.fetchone()
            cursor1.execute("INSERT INTO tasks (Task, Done) VALUES (?, ?)", (data[0], True))
            conn1.commit()
            cursor.execute("DELETE FROM tasks WHERE Task = ?", (selected,))
            conn.commit()
            conn1.commit()
            done_tasks()
        except:
            messagebox.showinfo("Info", "Pilih Tugas Yang Mau Di Tandai Dulu")
    elif InMode == 5: # In Edit Name Task For List System
        try:
            select_edit = listbox.get(listbox.curselection())
            Edit_Task()
        except Exception as e:
            print(e)
            messagebox.showinfo("Info", "Pilih Tugas Yang Mau Di Tandai Dulu")
    elif InMode == 6: # In Edit Name Task For Rename System
        New_Name = entry.get()
        if New_Name:
            cursor.execute("UPDATE tasks SET Task = ? WHERE Task = ?", (New_Name, select_edit))
            conn.commit()
            entry.delete(0, tk.END)
            Menu_default()
            print(New_Name)
        else:
            messagebox.showwarning("Warning", "Input Tidak Boleh Kosong")

# Mark Task In Progress System
def prog_task():
    global InMode
    InMode = 3
    Invisible_Menu()
    Label_title.config(text="Tandai Tugas\nDalam Pengerjaan")
    Label_title.place(relx=0.5, y=60)
    listbox.place(relx=0.5, y=325, anchor="center")
    button_cancel.place(relx=0.35, y=625, anchor="center")
    button_enter.place(relx=0.65, y=625, anchor="center")

    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM tasks WHERE Inprogress = ?", (False,))
    for i, row in enumerate(cursor.fetchall(), start=1):
        listbox.insert(tk.END, row[1])

# Mark Task Done System
def done_tasks():
    global InMode
    InMode = 4
    Invisible_Menu()
    Label_title.config(text="Tandai Tugas\nTelah Selesai")
    Label_title.place(relx=0.5, y=60, anchor="center")
    listbox.place(relx=0.5, y=325, anchor="center")
    button_cancel.place(relx=0.35, y=625, anchor="center")
    button_enter.place(relx=0.65, y=625, anchor="center")

    listbox.delete(0, tk.END)
    cursor.execute("SELECT Task FROM tasks WHERE Inprogress = ?", (True,))
    for i, row in enumerate(cursor.fetchall(), start= 1):
        listbox.insert(tk.END, row[0])

# View Done Task System
def view_done_task():
    global InMode
    InMode = 0
    Invisible_Menu()
    Label_title.config(text="Lihat Tugas Yang\nSudah Selesai")
    Label_title.place(relx=0.5, y=60, anchor="center")
    listbox.place(relx=0.5, y=325, anchor="center")
    button_cancel.place(relx=0.5, y=625, anchor="center")

    listbox.delete(0, tk.END)
    cursor1.execute("SELECT Task, Done FROM tasks")
    for i, row in enumerate(cursor1.fetchall(), start=1):
        Task, Done = row
        status = "Sudah Selesai" if Done else "Belum Selesai(BUG)"
        listbox.insert(tk.END, f"{i}. {Task} ({status})")

# Close Window System
def Close_window(event=None):
    if InMode == 100: # In Default Menu
        if messagebox.askyesno("Konfirmasi", "Yakin ni Mau Keluar?"):
            conn.close()
            conn1.close()
            window.destroy()
    else: # In Other Menu
        Invisible_Menu()
        Menu_default()

# Volume System
def set_vol(*args):
    v = float(volume_var.get())
    Click_Sound.set_volume(v)
    Notif_Sound.set_volume(v)
    Start_Sound.set_volume(v)
    BGM_Sound.set_volume(v)
    print(v)

# Click System
def Click(event=None):
    Click_Sound.play()

# Startup System
def startup():
    Start_Sound.play()
    play_BGM()
    show_notification(Task_path)

# Show Notification System (Logic System In File To_Do-List_Notify.py)
def show_notification(task_path):
    notification_Show(task_path)
    
# SLider Volume System
def volume_slider():
    button_volume.place(relx=0.1, y=2000)
    Sound_volume.place(relx=0.1, y=630)

# Auto Close Slider System
def deactive_vol(event=None):
    global volume_timer
    button_volume.place(relx=0.1, y=630)
    Sound_volume.place(relx=0.1, y=2000)

# Edit Name Task System For List System
def Edit_Task_list():
    global InMode
    InMode = 5
    Invisible_Menu()
    Label_title.config(text="Pilih Tugas Yang \nMau Di Ganti Nama nya")
    Label_title.place(relx=0.5, y=60)
    listbox.place(relx=0.5, y=325, anchor="center")
    button_cancel.place(relx=0.35, y=625, anchor="center")
    button_enter.place(relx=0.65, y=625, anchor="center")

    listbox.delete(0, tk.END)
    cursor.execute("SELECT * FROM tasks")
    for i, row in enumerate(cursor.fetchall(), start=1):
        listbox.insert(tk.END, row[1])

# Edit Name Task System For Entry System   
def Edit_Task():
    global InMode
    Invisible_Menu()
    entry.place(relx=0.5, rely=0.2, anchor="center")
    Label_title.config(text="Isi Nama Baru")
    button_cancel.place(relx=0.5, y=450, anchor="center")
    button_enter.place(relx=0.5, y=300, anchor="center")
    InMode = 6

# Background System (City Background)
w = window.winfo_screenwidth()
h = window.winfo_screenheight()
Bg_resize = Bg_Img.resize((w, h))
overlay = Image.new("RGBA", Bg_resize.size, (0, 0, 0, 100))
bg_witth_overlay = Image.alpha_composite(Bg_resize.convert("RGBA"), overlay)
bg_tk = ImageTk.PhotoImage(bg_witth_overlay)

# I Forgot This But This For Make Other Frame 
frame = tk.Frame(window)
frame.place(x=0, y=0, relwidth=1, relheight=1)

# Display The Background
bg_label = tk.Label(frame, image=bg_tk).place(x=0, y=0, relwidth=1, relheight=1)

# Timer For Start Startup System 
window.after(100, startup)
set_vol()

# All Button System
Label_title = tk.Label(frame, text="Menu Tugas", font=("Arial", 25),bg="gray")
entry = tk.Entry(frame, width=60, font=("Arial", 20), bg="gray")
button_add = tk.Button(frame, text="Tambah Tugas", bg="gray", command=button_add, font=("Arial", 20), width=20, height=3)
button_view = tk.Button(frame, text="Lihat Tugas", bg="gray", command=view_task_gui, font=("Arial", 20), width=20, height=3)
button_del = tk.Button(frame, text="Hapus Tugas", bg="gray", command=del_task, font=("Arial", 20), width=20, height=3)
button_cancel = tk.Button(frame, text="Kembali", bg="gray", command=Cancel, font=("Arial", 20), width=20, height=3)
button_enter = tk.Button(frame, text="Enter", bg="gray", command=enter, font=("Arial", 20), width=20, height=3)
listbox = tk.Listbox(window, width=60, height=15, bg="gray", font=("Arial", 18))
button_progress = tk.Button(frame, text="Tandai Dalam\nPengerjaan", command=prog_task, bg="gray", font=("Arial", 20), width=20, height=3)
button_done = tk.Button(frame, width=20, height=3, font=("Arial", 20), text="Tandai Sudah\nSelesai", command=done_tasks, bg="gray")
button_view_done = tk.Button(frame, width=20, height=3, font=("Arial", 20), text="Lihat Tugas Yang\nSudah Selesai", command=view_done_task, bg="gray")
button_close = tk.Button(frame, width=20, height=3, font=("Arial", 20), command= Close_window, bg="gray", text="Keluar")
Sound_volume = tk.Scale(frame, from_=0.0, to=1.0 , orient="horizontal", variable=volume_var, command=set_vol, length=200, resolution=0.01, bg="gray")
button_volume = tk.Button(frame, text="\U0001F50A", command=volume_slider, bg="gray", font=("Arial", 15))
button_edit = tk.Button(frame, text="Edit Nama Tugas", width=20, height=3, font=("Arial", 20), command= Edit_Task_list, bg="gray")

# Other Config For Keyboard Or Other
window.bind("<Escape>", Close_window)
window.bind("<Return>", enter)
window.bind("<ButtonPress-1>", Click)
Sound_volume.bind("<ButtonRelease-1>", deactive_vol)

window.protocol("WM_DELETE_WINDOW", Close_window)

# First System Will Start 
setup_gui()
Menu_default()
window.mainloop()