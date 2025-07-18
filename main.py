import tkinter as tk
from auth import register_screen, login_screen

root = tk.Tk()
root.title("Share Watchlist")
root.geometry("300x350")

tk.Label(root, text="📈 Share Watchlist", font=("Helvetica", 18)).pack(pady=30)
tk.Button(root, text="Register", command=register_screen, width=20, height=2).pack(pady=10)
tk.Button(root, text="Login", command=login_screen, width=20, height=2).pack(pady=10)

root.mainloop()
#navigation.py