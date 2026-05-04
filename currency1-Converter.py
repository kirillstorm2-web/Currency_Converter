import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from datetime import datetime

API_KEY = "YOUR_API_KEY"
URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

HISTORY_FILE = "history.json"

currencies = ["USD", "EUR", "RUB", "GBP", "JPY"]

def convert_currency():
    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            raise ValueError

        from_cur = from_currency.get()
        to_cur = to_currency.get()

        response = requests.get(URL + from_cur)
        data = response.json()

        rate = data["conversion_rates"][to_cur]
        result = amount * rate

        result_label.config(text=f"Result: {result:.2f} {to_cur}")

        save_history(from_cur, to_cur, amount, result)

    except ValueError:
        messagebox.showerror("Error", "Enter a positive number")

def save_history(from_cur, to_cur, amount, result):
    record = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "from": from_cur,
        "to": to_cur,
        "amount": amount,
        "result": result
    }

    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    except:
        history = []

    history.append(record)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

    update_table(history)

def load_history():
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
            update_table(history)
    except:
        pass

def update_table(history):
    for row in tree.get_children():
        tree.delete(row)

    for item in history:
        tree.insert("", "end", values=(
            item["time"], item["from"], item["to"],
            item["amount"], round(item["result"], 2)
        ))

# GUI
root = tk.Tk()
root.title("Currency Converter")

from_currency = ttk.Combobox(root, values=currencies)
from_currency.set("USD")
from_currency.pack()

to_currency = ttk.Combobox(root, values=currencies)
to_currency.set("EUR")
to_currency.pack()

amount_entry = tk.Entry(root)
amount_entry.pack()

convert_btn = tk.Button(root, text="Convert", command=convert_currency)
convert_btn.pack()

result_label = tk.Label(root, text="Result:")
result_label.pack()

tree = ttk.Treeview(root, columns=("Time", "From", "To", "Amount", "Result"), show="headings")
for col in ("Time", "From", "To", "Amount", "Result"):
    tree.heading(col, text=col)
tree.pack()

load_history()

root.mainloop()
