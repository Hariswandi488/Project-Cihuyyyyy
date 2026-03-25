import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Video/Music Downloader")
app.geometry("480x360")

def download_action():
    url = entry.get()

label = ctk.CTkLabel(app, text="URL Video")
label.pack(pady=10)

entry = ctk.CTkEntry(app, width=300)
entry.pack(pady=5)

btn = ctk.CTkButton(app, text="Download", command=download_action)
btn.pack(pady=15)

app.mainloop()