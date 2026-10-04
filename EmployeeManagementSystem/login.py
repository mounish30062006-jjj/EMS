from customtkinter import *
from PIL import Image, ImageOps
from tkinter import messagebox
import tkinter as tk
import os
import sys


def resource_path(filename):
    """Find a file next to this script, whether run normally or bundled by PyInstaller."""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)


def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'All Fields Are Required')
    elif usernameEntry.get() == 'mounish' and passwordEntry.get() == '30062006':
        messagebox.showinfo('Success', 'Login Is Successful')
        root.destroy()
        import ems
    else:
        messagebox.showerror('Error', 'Wrong Credentials')


root = CTk()


def _suppress_harmless_tcl_errors(exc, val, tb):
    if issubclass(exc, tk.TclError) and "invalid command name" in str(val):
        return  # harmless timing quirk between customtkinter and Tcl on window close
    import traceback
    traceback.print_exception(exc, val, tb)


root.report_callback_exception = _suppress_harmless_tcl_errors

root.geometry('1280x720')
root.minsize(900, 560)
root.resizable(True, True)
root.title('LOGIN PAGE')

try:
    root.state('zoomed')  # start maximized
except Exception:
    pass

# ---- Fullscreen background that rescales with the window ----
bg_label = CTkLabel(root, text='')
bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

_bg_source = None
try:
    _bg_source = Image.open(resource_path('cover_pic.jpeg'))
except FileNotFoundError:
    pass

_last_bg_size = [0, 0]


def _resize_background(event=None):
    if _bg_source is None:
        return
    w, h = root.winfo_width(), root.winfo_height()
    if w < 2 or h < 2:
        return
    if [w, h] == _last_bg_size:
        return
    _last_bg_size[0], _last_bg_size[1] = w, h
    fitted = ImageOps.fit(_bg_source, (w, h), Image.LANCZOS)
    ctk_img = CTkImage(fitted, size=(w, h))
    bg_label.configure(image=ctk_img)
    bg_label.image = ctk_img


root.bind('<Configure>', lambda e: _resize_background() if e.widget == root else None)
root.after(50, _resize_background)

# ---- Centered login card, stays centered at any window size ----
card = CTkFrame(root, width=420, height=380, corner_radius=20, fg_color=('gray90', '#121829'))
card.place(relx=0.5, rely=0.5, anchor='center')
card.pack_propagate(False)

headinglabel = CTkLabel(card, text='Employee Management\nSystem', font=('Segoe UI', 22, 'bold'),
                         text_color=('#10294d', '#8fd9d0'), justify='center')
headinglabel.pack(pady=(36, 28))

usernameEntry = CTkEntry(card, placeholder_text='Username', width=280, height=42, font=('Segoe UI', 14))
usernameEntry.pack(pady=10)

passwordEntry = CTkEntry(card, placeholder_text='Password', width=280, height=42, font=('Segoe UI', 14), show='*')
passwordEntry.pack(pady=10)
passwordEntry.bind('<Return>', lambda e: login())

loginButton = CTkButton(card, text='Login', cursor='hand2', command=login, width=280, height=42,
                         font=('Segoe UI', 14, 'bold'), corner_radius=10)
loginButton.pack(pady=(26, 10))

root.mainloop()
