import tkinter as tk

def create_window(title="Window", size="400x500"):
    window = tk.Toplevel()
    window.title(title)
    window.geometry(size)
    return window

def add_labeled_entry(frame, label_text):
    label = tk.Label(frame, text=label_text)
    label.pack(pady=5)
    entry = tk.Entry(frame)
    entry.pack(pady=5)
    return entry

def add_flat_button(frame, text, command):
    btn = tk.Button(frame, text=text, command=command, bg="#4CAF50", fg="white", padx=10, pady=5, relief=tk.FLAT)
    btn.pack(pady=5, fill='x', padx=20)
    return btn
