import os
import psycopg2
from tkinter import *
from tkinter import ttk, messagebox

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://saeed:bkIR0mjTFoLaQCGIEw5K1A@safe-opossum-7820.8nk.cockroachlabs.cloud:26257/Expense_record?sslmode=verify-full")

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS expenses (id SERIAL PRIMARY KEY, description TEXT, price REAL, purchase_date DATE)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS added_money (id SERIAL PRIMARY KEY, description TEXT, amount REAL, transaction_date DATE)")
        self.conn.commit()
        
    def insert_expense(self, description, price, purchase_date):
        self.cur.execute("INSERT INTO expenses (description, price, purchase_date) VALUES (%s, %s, %s)", (description, price, purchase_date))
        self.conn.commit()
    def fetch_expenses(self):
        self.cur.execute("SELECT * FROM expenses")
        return self.cur.fetchall()
    
    def clear_expenses(self):
        self.cur.execute("DELETE FROM expenses")
        self.conn.commit()

    def update_expense(self, id, description, price, purchase_date):
        self.cur.execute("UPDATE expenses SET description=%s, price=%s, purchase_date=%s WHERE id=%s", (description, price, purchase_date, id))
        self.conn.commit()

    def delete_expense(self, id):
        self.cur.execute("DELETE FROM expenses WHERE id=%s", (id,))
        self.conn.commit()

    def insert_money(self, description, amount, transaction_date):
        self.cur.execute("INSERT INTO added_money (description, amount, transaction_date) VALUES (%s, %s, %s)", (description, amount, transaction_date))
        self.conn.commit()

    def fetch_money(self):
        self.cur.execute("SELECT * FROM added_money")
        return self.cur.fetchall()

    def clear_money(self):
        self.cur.execute("DELETE FROM added_money")
        self.conn.commit()

    def update_money(self, id, description, amount, transaction_date):
        self.cur.execute("UPDATE added_money SET description=%s, amount=%s, transaction_date=%s WHERE id=%s", (description, amount, transaction_date, id))
        self.conn.commit()

    def delete_money(self, id):
        self.cur.execute("DELETE FROM added_money WHERE id=%s", (id,))
        self.conn.commit()

    def get_total_expenses(self):
        self.cur.execute("SELECT SUM(price) FROM expenses")
        total = self.cur.fetchone()[0]
        return total if total else 0.0

    def get_total_money(self):
        self.cur.execute("SELECT SUM(amount) FROM added_money")
        total = self.cur.fetchone()[0]
        return total if total else 0.0

    def close(self):
        self.conn.close()

def calculate_main_balance():
    total_expenses = data.get_total_expenses()
    total_money = data.get_total_money()
    main_balance_var.set(f"Main Balance: {total_money - total_expenses:.2f}")

def insert_expense():
    description = desc_entry.get()
    price = price_entry.get()
    purchase_date = date_entry.get()
    if description and price and purchase_date:
        data.insert_expense(description, price, purchase_date)
        refresh_data()
        clear_entries()
        calculate_main_balance()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")
def insert_money():
    description = money_desc_entry.get()
    amount = money_amount_entry.get()
    transaction_date = money_date_entry.get()
    if description and amount and transaction_date:
        data.insert_money(description, amount, transaction_date)
        refresh_data()
        clear_entries()
        calculate_main_balance()
    else:
        messagebox.showerror("Error", "Please fill in all fields.")

def update_selected_item():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_id = expenses_tree.item(selected_item, 'values')[0]
        description = desc_entry.get()
        price = price_entry.get()
        purchase_date = date_entry.get()
        if description and price and purchase_date:
            data.update_expense(item_id, description, price, purchase_date)
            refresh_data()
            clear_entries()
            calculate_main_balance()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    else:
        messagebox.showerror("Error", "Please select an item to update.")

def delete_selected_item():
    selected_item = expenses_tree.selection()
    if selected_item:
        item_id = expenses_tree.item(selected_item, 'values')[0]
        data.delete_expense(item_id)
        refresh_data()
        clear_entries()
        calculate_main_balance()
    else:
        messagebox.showerror("Error", "Please select an item to delete.")

def update_selected_money_item():
    selected_item = money_tree.selection()
    if selected_item:
        item_id = money_tree.item(selected_item, 'values')[0]
        description = money_desc_entry.get()
        amount = money_amount_entry.get()
        transaction_date = money_date_entry.get()
        if description and amount and transaction_date:
            data.update_money(item_id, description, amount, transaction_date)
            refresh_data()
            clear_entries()
            calculate_main_balance()
        else:
            messagebox.showerror("Error", "Please fill in all fields.")
    else:
        messagebox.showerror("Error", "Please select a money item to update.")

def delete_selected_money_item():
    selected_item = money_tree.selection()
    if selected_item:
        item_id = money_tree.item(selected_item, 'values')[0]
        data.delete_money(item_id)
        refresh_data()
        clear_entries()
        calculate_main_balance()
    else:
        messagebox.showerror("Error", "Please select a money item to delete.")

def clear_all_entries(entries, data, treeview):
    for entry in entries:
        entry.delete(0, 'end')
    if treeview == expenses_tree:
        data.clear_expenses()
    elif treeview == money_tree:
        data.clear_money()
    refresh_data()
    calculate_main_balance()

def clear_entries():
    desc_entry.delete(0, 'end')
    price_entry.delete(0, 'end')
    date_entry.delete(0, 'end')
    money_desc_entry.delete(0, 'end')
    money_amount_entry.delete(0, 'end')
    money_date_entry.delete(0, 'end')

def refresh_data():
    expenses_tree.delete(*expenses_tree.get_children())
    money_tree.delete(*money_tree.get_children())

    for item in data.fetch_expenses():
        expenses_tree.insert('', 'end', values=item)

    for item in data.fetch_money():
        money_tree.insert('', 'end', values=item)

def exit_app():
    data.close()
    root.destroy()

def display_selected_item(event, entry1, entry2, entry3):
    selected_item = event.widget.selection()
    if selected_item:
        values = event.widget.item(selected_item, 'values')
        entry1.delete(0, 'end')
        entry2.delete(0, 'end')
        entry3.delete(0, 'end')
        entry1.insert(0, values[1])
        entry2.insert(0, values[2])
        entry3.insert(0, values[3])
root = Tk()
root.title('Expense Tracker')

data = Database()

notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, fill='both', expand=True)

expenses_tab = ttk.Frame(notebook)
notebook.add(expenses_tab, text='Expenses')

desc_label = Label(expenses_tab, text='Description:')
desc_label.grid(row=0, column=0, padx=10, pady=5)
desc_entry = Entry(expenses_tab)
desc_entry.grid(row=0, column=1, padx=10, pady=5)

price_label = Label(expenses_tab, text='Price:')
price_label.grid(row=1, column=0, padx=10, pady=5)
price_entry = Entry(expenses_tab)
price_entry.grid(row=1, column=1, padx=10, pady=5)

date_label =Label(expenses_tab, text='Purchase Date:')
date_label.grid(row=2, column=0, padx=10, pady=5)
date_entry = Entry(expenses_tab)
date_entry.grid(row=2, column=1, padx=10, pady=5)

add_expense_button =Button(expenses_tab, text='Add Expense', command=insert_expense, bg='green')
add_expense_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

update_expense_button = Button(expenses_tab, text='Update Expense', command=update_selected_item, bg='grey')
update_expense_button.grid(row=4, column=0, padx=10, pady=10)

delete_expense_button = Button(expenses_tab, text='Delete Expense', command=delete_selected_item, bg='yellow')
delete_expense_button.grid(row=4, column=1, padx=10, pady=10)

expenses_tree = ttk.Treeview(expenses_tab, columns=('ID', 'Description', 'Price', 'Purchase Date'), show='headings')
expenses_tree.heading('ID', text='ID')
expenses_tree.heading('Description', text='Description')
expenses_tree.heading('Price', text='Price')
expenses_tree.heading('Purchase Date', text='Purchase Date')
expenses_tree.column('ID', width=50)
expenses_tree.column('Description', width=200)
expenses_tree.column('Price', width=100)
expenses_tree.column('Purchase Date', width=150)
expenses_tree.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

expenses_tree.bind('<<TreeviewSelect>>', lambda event: display_selected_item(event, desc_entry, price_entry, date_entry))

money_tab = ttk.Frame(notebook)
notebook.add(money_tab, text='Money')

money_desc_label = Label(money_tab, text='Description:')
money_desc_label.grid(row=0, column=0, padx=10, pady=5)
money_desc_entry = Entry(money_tab)
money_desc_entry.grid(row=0, column=1, padx=10, pady=5)

money_amount_label = Label(money_tab, text='Amount:')
money_amount_label.grid(row=1, column=0, padx=10, pady=5)
money_amount_entry = Entry(money_tab)
money_amount_entry.grid(row=1, column=1, padx=10, pady=5)

money_date_label = Label(money_tab, text='Transaction Date:')
money_date_label.grid(row=2, column=0, padx=10, pady=5)
money_date_entry = Entry(money_tab)
money_date_entry.grid(row=2, column=1, padx=10, pady=5)

add_money_button = Button(money_tab, text='Add Money', command=insert_money, bg='green')
add_money_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

update_money_button =Button(money_tab, text='Update Money', command=update_selected_money_item, bg='grey')
update_money_button.grid(row=4, column=0, padx=10, pady=10)

delete_money_button = Button(money_tab, text='Delete Money', command=delete_selected_money_item, bg='orange')
delete_money_button.grid(row=4, column=1, padx=10, pady=10)

money_tree = ttk.Treeview(money_tab, columns=('ID', 'Description', 'Amount', 'Transaction Date'), show='headings')
money_tree.heading('ID', text='ID')
money_tree.heading('Description', text='Description')
money_tree.heading('Amount', text='Amount')
money_tree.heading('Transaction Date', text='Transaction Date')
money_tree.column('ID', width=50)
money_tree.column('Description', width=200)
money_tree.column('Amount', width=100)
money_tree.column('Transaction Date', width=150)
money_tree.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

money_tree.bind('<<TreeviewSelect>>', lambda event: display_selected_item(event, money_desc_entry, money_amount_entry, money_date_entry))

selection_tab = ttk.Frame(notebook)
notebook.add(selection_tab, text='Selection and Clear')

selected_tab = ttk.Notebook(selection_tab)
selected_tab.grid(row=0, column=0, padx=10, pady=10)

selection_expenses_tab = ttk.Frame(selected_tab)
selected_tab.add(selection_expenses_tab, text='Expenses')

clear_expenses_button = Button(selection_expenses_tab, text='Clear Expenses Inputs', command=lambda: clear_all_entries((desc_entry, price_entry, date_entry), data, expenses_tree), bg='grey')
clear_expenses_button.pack(pady=20)

selection_money_tab = ttk.Frame(selected_tab)
selected_tab.add(selection_money_tab, text='Money')

clear_money_button = Button(selection_money_tab, text='Clear Money Inputs', command=lambda: clear_all_entries((money_desc_entry, money_amount_entry, money_date_entry), data, money_tree), bg='teal')
clear_money_button.pack(pady=20)

refresh_button = Button(selection_tab, text='Refresh Data', command=refresh_data, bg='tan')
refresh_button.grid(row=1, column=0, padx=10, pady=10)

exit_button = Button(root, text='Exit', command=exit_app,bg='tan')
exit_button.pack(pady=10)

main_balance_var = StringVar()
main_balance_label = Label(root, textvariable=main_balance_var, font=("Helvetica", 14, "bold"))
main_balance_label.pack(pady=10)

refresh_data()
calculate_main_balance()

root.after(100,root.mainloop())
