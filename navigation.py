import tkinter as tk
from auth import register_screen, login_screen

def show_main_screen(root):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="📈 Share Watchlist", font=("Helvetica", 18)).pack(pady=30)
    tk.Button(root, text="Register", command=lambda: register_screen(root), width=20, height=2).pack(pady=10)
    tk.Button(root, text="Login", command=lambda: login_screen(root), width=20, height=2).pack(pady=10)
