import bcrypt
from tkinter import messagebox
from db import get_db_connection
from ui_helpers import create_window, add_labeled_entry, add_flat_button
from dashboard import show_dashboard

def register_screen():
    win = create_window("Register")

    username_entry = add_labeled_entry(win, "Username:")
    password_entry = add_labeled_entry(win, "Password:")

    def register():
        conn = get_db_connection()
        cursor = conn.cursor()
        username = username_entry.get()
        password = password_entry.get()
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_pw))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful")
            win.destroy()
        except:
            messagebox.showerror("Error", "Username already taken")
        conn.close()

    add_flat_button(win, "Register", register)

def login_screen():
    win = create_window("Login")

    username_entry = add_labeled_entry(win, "Username:")
    password_entry = add_labeled_entry(win, "Password:")

    def login():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        username = username_entry.get()
        password = password_entry.get()

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
            win.destroy()
            show_dashboard(user)
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")
        conn.close()

    add_flat_button(win, "Login", login)
