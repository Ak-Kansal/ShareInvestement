import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from db import get_db_connection
from ui_helpers import create_window, add_labeled_entry, add_flat_button

def show_dashboard(user):
    dash = create_window("Dashboard")

    tk.Label(dash, text=f"Welcome {user['username']}", font=('Arial', 14)).pack(pady=10)
    balance_label = tk.Label(dash, text=f"Balance: ₹{user['balance']:.2f}", font=('Arial', 12))
    balance_label.pack()

    def refresh_balance():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT balance FROM users WHERE id=?", (user['id'],))
        user['balance'] = cursor.fetchone()[0]
        conn.close()
        balance_label.config(text=f"Balance: ₹{user['balance']:.2f}")

    def open_buy_window():
        win = create_window("Buy Share")

        symbol = add_labeled_entry(win, "Symbol:")
        price = add_labeled_entry(win, "Price:")
        qty = add_labeled_entry(win, "Quantity:")

        def buy():
            sym, pr, qt = symbol.get(), float(price.get()), int(qty.get())
            cost = pr * qt
            if cost > user['balance']:
                messagebox.showerror("Error", "Insufficient balance")
                return
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, quantity, avg_price FROM shares WHERE user_id=? AND symbol=?", (user['id'], sym))
            row = cursor.fetchone()
            if row:
                sid, existing_qty, avg_price = row
                new_qty = existing_qty + qt
                new_avg = ((existing_qty * avg_price) + (qt * pr)) / new_qty
                cursor.execute("UPDATE shares SET quantity=?, avg_price=? WHERE id=?", (new_qty, new_avg, sid))
            else:
                cursor.execute("INSERT INTO shares (user_id, symbol, quantity, avg_price) VALUES (?, ?, ?, ?)",
                               (user['id'], sym, qt, pr))
            cursor.execute("INSERT INTO transactions (user_id, symbol, type, quantity, price) VALUES (?, ?, 'BUY', ?, ?)",
                           (user['id'], sym, qt, pr))
            user['balance'] -= cost
            cursor.execute("UPDATE users SET balance=? WHERE id=?", (user['balance'], user['id']))
            conn.commit()
            conn.close()
            refresh_balance()
            messagebox.showinfo("Success", f"Bought {qt} of {sym}")
            win.destroy()

        add_flat_button(win, "Confirm Buy", buy)

    def open_sell_window():
        win = create_window("Sell Share")

        symbol = add_labeled_entry(win, "Symbol:")
        price = add_labeled_entry(win, "Price:")
        qty = add_labeled_entry(win, "Quantity:")

        def sell():
            sym, pr, qt = symbol.get(), float(price.get()), int(qty.get())
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, quantity FROM shares WHERE user_id=? AND symbol=?", (user['id'], sym))
            row = cursor.fetchone()
            if not row or row[1] < qt:
                messagebox.showerror("Error", "Not enough shares")
                return
            remaining_qty = row[1] - qt
            if remaining_qty == 0:
                cursor.execute("DELETE FROM shares WHERE id=?", (row[0],))
            else:
                cursor.execute("UPDATE shares SET quantity=? WHERE id=?", (remaining_qty, row[0]))
            cursor.execute("INSERT INTO transactions (user_id, symbol, type, quantity, price) VALUES (?, ?, 'SELL', ?, ?)",
                           (user['id'], sym, qt, pr))
            user['balance'] += pr * qt
            cursor.execute("UPDATE users SET balance=? WHERE id=?", (user['balance'], user['id']))
            conn.commit()
            conn.close()
            refresh_balance()
            messagebox.showinfo("Sold", f"Sold {qt} of {sym}")
            win.destroy()

        add_flat_button(win, "Confirm Sell", sell)

    from tkinter import ttk

    def open_holdings():
        win = create_window("Your Holdings", "600x400")

        columns = ("Symbol", "Quantity", "Avg Price", "Current Price", "Total Value", "P/L")
        tree = ttk.Treeview(win, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.pack(fill="both", expand=True)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT symbol, quantity, avg_price FROM shares WHERE user_id=?", (user['id'],))
        holdings = cursor.fetchall()

        def populate_table():
            for row in holdings:
                sym, qty, avg = row
            # Ask user for current price once per share
                current_price = float(simpledialog.askstring("Current Price", f"{sym} current price:"))
                total_value = qty * current_price
                total_invest = qty * avg
                pl = total_value - total_invest
                tree.insert("", "end", values=(sym, qty, f"₹{avg:.2f}", f"₹{current_price:.2f}", f"₹{total_value:.2f}", f"₹{pl:.2f}"))

        populate_table()
        conn.close()


    def open_transactions():
        win = create_window("Transaction History", "500x400")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT symbol, type, quantity, price, date FROM transactions WHERE user_id=? ORDER BY date DESC", (user['id'],))
        for t in cursor.fetchall():
            tk.Label(win, text=f"{t[4].strftime('%Y-%m-%d')} | {t[1]} {t[2]} {t[0]} @ ₹{t[3]}").pack()
        conn.close()

    def open_profit_loss():
        win = create_window("Profit/Loss")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT symbol, quantity, avg_price FROM shares WHERE user_id=?", (user['id'],))
        total_inv = total_val = 0
        for row in cursor.fetchall():
            sym, qty, avg = row
            price_entry = add_labeled_entry(win, f"{sym} current price:")
            def calculate(sym=sym, qty=qty, avg=avg, pe=price_entry):
                cp = float(pe.get())
                invest = avg * qty
                val = cp * qty
                tk.Label(win, text=f"{sym} P/L: ₹{val - invest:.2f}").pack()
            add_flat_button(win, f"Calc {sym}", lambda sym=sym, qty=qty, avg=avg, pe=price_entry: calculate(sym, qty, avg, pe))
        conn.close()

    # Buttons
    add_flat_button(dash, "Buy Share", open_buy_window)
    add_flat_button(dash, "Sell Share", open_sell_window)
    add_flat_button(dash, "View Holdings", open_holdings)
    add_flat_button(dash, "Transaction History", open_transactions)
    add_flat_button(dash, "Profit/Loss Summary", open_profit_loss)
#dashboard page