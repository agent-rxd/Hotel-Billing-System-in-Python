import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime

# ------------------------ Database Setup ------------------------
conn = sqlite3.connect('hotel.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS menu_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS menu_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (category_id) REFERENCES menu_categories(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone TEXT UNIQUE NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS delivery_addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    address TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    table_number TEXT,
    is_home_delivery INTEGER NOT NULL,
    special_additions TEXT,
    total_bill REAL NOT NULL,
    order_time TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    menu_item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
)
''')

conn.commit()

# ------------------------ Insert Categories and Menu Items ------------------------
categories = ["Breakfast", "Non-Veg", "Egg", "Rice & Main", "Sweets", "Drinks"]
for cat in categories:
    cursor.execute("INSERT OR IGNORE INTO menu_categories (name) VALUES (?)", (cat,))
conn.commit()

cursor.execute("SELECT id, name FROM menu_categories")
category_map = {name: cid for cid, name in cursor.fetchall()}

menu = {
    "Breakfast": {
        "Idli": 30, "Sambar Idli": 35, "Rava Idli": 40, "Mini Idli": 25, "Kanchipuram Idli": 40,
        "Puttu": 35, "Dosa": 40, "Masala Dosa": 50, "Paper Dosa": 45, "Set Dosa": 50,
        "Rava Dosa": 45, "Onion Dosa": 45, "Butter Dosa": 55, "Neer Dosa": 40,
        "Ragi Dosa": 35, "Mysore Masala Dosa": 60, "Cheese Dosa": 65, "Onion Uttapam": 55,
        "Tomato Uttapam": 55, "Mixed Vegetable Uttapam": 60, "Paniyaram": 30,
        "Medu Vada": 25, "Parotta": 20, "Muttaiparotta": 35, "Coin Parotta": 15,
        "Chapati": 30, "Poori": 45, "Pongal": 50, "Sweet Pongal": 50, "Kalkandu Pongal": 55,
        "Puli Pongal": 50, "Thinai Pongal": 55, "Upma": 40, "Semiya Upma": 45,
        "Rava Kesari": 30, "Kesari Bath": 30, "Jigarthanda": 50, "Filter Coffee": 20,
        "Tea": 15, "Rose Milk": 25, "Buttermilk": 20, "Lassi": 30, "Fresh Lime Juice": 25,
        "Watermelon Juice": 30, "Pineapple Juice": 30, "Mango Juice": 40, "Apple Juice": 35,
        "Orange Juice": 35, "Carrot Juice": 30, "Beetroot Juice": 30, "Milkshake": 50
    },
    "Non-Veg": {
        "Chicken 65": 110, "Chicken Chettinad": 130, "Chicken Liver Fry": 120,
        "Chicken Ghee Roast": 130, "Chicken Pepper Dry": 120, "Chicken Chukka": 125,
        "Chicken Sukka": 120, "Chicken Varuval": 110, "Chicken Kurma": 130,
        "Chicken Stew": 120, "Mutton Sukka": 160, "Mutton Pepper Fry": 170,
        "Mutton Korma": 165, "Mutton Stew": 160, "Mutton Varuval": 165,
        "Mutton Chops": 180, "Mutton Fry": 170, "Mutton Soup": 150,
        "Crab Masala": 180, "Crab Fry": 175, "Crab Soup": 160,
        "Prawn Fry": 150, "Prawn Masala": 155, "Prawn Pepper Fry": 150,
        "Prawn Kurma": 160, "Fish Fry": 140, "Fish Curry": 145,
        "Fish Moilee": 150, "Fish Pulusu": 140, "Nattu Kozhi Kuzhambu": 130,
        "Kozhi Milagu Varuval": 125, "Kozhi Vellai Kurma": 130,
        "Chicken 65 Dry": 110, "Chicken 65 Gravy": 115,
        "Nattu Kozhi Varuval": 130, "Nattu Kozhi Roast": 135,
        "Chicken Liver Roast": 120, "Chicken Heart Fry": 115,
        "Mutton Liver Fry": 150, "Mutton Brain Fry": 160,
        "Chicken Brain Fry": 140, "Chicken Feet Fry": 130,
        "Mutton Bone Soup": 145, "Fish Head Curry": 160,
        "Crab Soup": 160, "Prawn Soup": 150, "Chicken Soup": 130,
        "Mutton Soup": 150, "Fish Soup": 140, "Prawn Soup": 150,
        "Chicken Roast": 130, "Mutton Roast": 160, "Fish Roast": 140,
        "Prawn Roast": 150, "Crab Roast": 170
    },
    "Egg": {
        "Egg Curry": 60, "Egg Roast": 65, "Egg Pepper Fry": 65,
        "Egg Chukka": 65, "Egg Kurma": 70, "Egg Stew": 65,
        "Egg Kothu Parotta": 80, "Egg Biryani": 90, "Egg Masala": 65,
        "Muttai Thokku": 65, "Muttai Paniyaram": 60, "Egg Bhurji": 70
    },
    "Rice & Main": {
        "Plain Rice": 30, "Sambar Sadham": 50, "Rasam Sadham": 45,
        "Thakkali Choru": 40, "Thengai Choru": 45, "Milagu Choru": 40,
        "Paruppu Choru": 45, "Karuvepillai Choru": 40, "Thayir Choru": 35,
        "Nei Choru": 50, "Urulai Choru": 40, "Muttaikos Choru": 45,
        "Kudaimilagai Choru": 40, "Kootanchoru": 50,
        "Kothamalli Pudina Choru": 50, "Manga Choru": 45,
        "Thatta Payaru Arisi Paruppu Choru": 50, "Vetrilai Poondu Choru": 50,
        "Varutta Arisi": 50, "Brinji Choru": 60, "Vegetable Biryani": 70,
        "Chicken Biryani": 120, "Mutton Biryani": 150, "Egg Biryani": 90,
        "Plain Biryani": 50, "Kuzhambu Varieties": 60, "Mor Kuzhambu": 55,
        "Kara Kuzhambu": 60, "Paruppu Kuzhambu": 55, "Meen Kuzhambu": 140,
        "Kootu Varieties": 50, "Avial": 60, "Thoran": 50,
        "Puli Inji": 40, "Pachadi": 40, "Oothappam": 60,
        "Pesarattu": 55, "Ragi Mudde": 40, "Kambu Koozh": 40,
        "Kuthiraivali Pongal": 50, "Thinai Pongal": 50,
        "Samai Sadam": 45, "Kutharai Vali Dosai": 50
    },
    "Sweets": {
        "Payasam": 35, "Mysore Pak": 30, "Kaju Katli": 35,
        "Rava Kesari": 30, "Kesari Bath": 30, "Jigarthanda": 50,
        "Gulab Jamun": 30, "Rasgulla": 30, "Badam Milk": 35,
        "Milk Halwa": 30, "Dry Fruit Halwa": 40, "Coconut Burfi": 30,
        "Ellu Urundai": 25, "Dry Fruit Laddu": 40, "Ariselu": 35,
        "Palkova": 40, "Kheer": 35, "Paruppu Urundai Payasam": 35,
        "Semiya Payasam": 35, "Sweet Pongal": 50, "Thengai Paal": 30,
        "Elaneer Payasam": 35, "Paal Kozhukattai": 30,
        "Manapparai Murukku": 30, "Chikki": 25
    },
    "Drinks": {
        "Filter Coffee": 20, "Masala Tea": 20, "Ginger Tea": 18,
        "Elaichi Tea": 18, "Lemon Tea": 18, "Rose Milk": 25,
        "Buttermilk": 20, "Lassi": 30, "Fresh Lime Soda": 25,
        "Tender Coconut Water": 30, "Milkshake Vanilla": 50,
        "Milkshake Chocolate": 60, "Milkshake Strawberry": 55
    }
}

# Insert menu items into DB if not already present
for cat, items in menu.items():
    cat_id = category_map[cat]
    for item_name, price in items.items():
        cursor.execute('''
            INSERT OR IGNORE INTO menu_items (name, price, category_id)
            VALUES (?, ?, ?)
        ''', (item_name, price, cat_id))
conn.commit()

# ------------------------ Functions ------------------------

current_order_items = []  # (menu_item_id, item_name, qty, price)
item_map = {}

def load_categories():
    cursor.execute("SELECT name FROM menu_categories ORDER BY name")
    cats = [row[0] for row in cursor.fetchall()]
    category_combo['values'] = cats

def update_items(event=None):
    category = category_combo.get()
    if not category:
        item_combo['values'] = []
        item_combo.set('')
        return
    cursor.execute('''
        SELECT id, name, price FROM menu_items
        WHERE category_id = (SELECT id FROM menu_categories WHERE name = ?)
        ORDER BY name
    ''', (category,))
    items = cursor.fetchall()
    item_map.clear()
    item_names = []
    for mid, name, price in items:
        item_map[name] = (mid, price)
        item_names.append(name)
    item_combo['values'] = item_names
    item_combo.set('')

def add_item_to_order():
    item_name = item_combo.get()
    qty_str = qty_entry.get().strip()

    if item_name == "":
        messagebox.showerror("Error", "Select a menu item")
        return
    if not qty_str.isdigit() or int(qty_str) <= 0:
        messagebox.showerror("Error", "Enter a valid quantity")
        return

    qty = int(qty_str)
    mid, price = item_map[item_name]
    current_order_items.append((mid, item_name, qty, price))
    update_order_list()
    update_total_label()
    qty_entry.delete(0, tk.END)

def update_order_list():
    order_listbox.delete(0, tk.END)
    for _, name, qty, _ in current_order_items:
        order_listbox.insert(tk.END, f"{name} x{qty}")

def clear_order_list():
    current_order_items.clear()
    update_order_list()
    update_total_label()

def update_total_label():
    total = sum(qty * price for _, _, qty, price in current_order_items)
    total_var.set(f"Total: ₹{total}")

def add_order():
    name = name_entry.get().strip()
    phone = phone_entry.get().strip()
    table_number = table_entry.get().strip()
    additions = additions_text.get("1.0", tk.END).strip()
    is_delivery = delivery_var.get() == 1
    address = address_text.get("1.0", tk.END).strip() if is_delivery else None

    if not name:
        messagebox.showerror("Error", "Please enter customer name")
        return

    if not phone or not phone.isdigit() or len(phone) != 10:
        messagebox.showerror("Error", "Enter a valid 10-digit phone number")
        return

    if not is_delivery and not table_number:
        messagebox.showerror("Error", "Please enter table number or select home delivery")
        return

    if is_delivery and not address:
        messagebox.showerror("Error", "Please enter delivery address")
        return

    if not current_order_items:
        messagebox.showerror("Error", "Add at least one menu item to the order")
        return

    # Insert or get user
    cursor.execute("SELECT id FROM users WHERE phone=?", (phone,))
    user_row = cursor.fetchone()
    if user_row:
        user_id = user_row[0]
        # Update name in case changed
        cursor.execute("UPDATE users SET name=? WHERE id=?", (name, user_id))
    else:
        cursor.execute("INSERT INTO users (name, phone) VALUES (?, ?)", (name, phone))
        user_id = cursor.lastrowid

    # Insert or update delivery address if delivery
    if is_delivery:
        cursor.execute("SELECT id FROM delivery_addresses WHERE user_id=?", (user_id,))
        addr_row = cursor.fetchone()
        if addr_row:
            cursor.execute("UPDATE delivery_addresses SET address=? WHERE id=?", (address, addr_row[0]))
        else:
            cursor.execute("INSERT INTO delivery_addresses (user_id, address) VALUES (?, ?)", (user_id, address))

    total_bill = sum(qty * price for _, _, qty, price in current_order_items)
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert order
    cursor.execute('''
        INSERT INTO orders (user_id, table_number, is_home_delivery, special_additions, total_bill, order_time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, table_number if not is_delivery else None, int(is_delivery), additions, total_bill, time_now))
    order_id = cursor.lastrowid

    # Insert order items
    for mid, _, qty, price in current_order_items:
        cursor.execute('''
            INSERT INTO order_items (order_id, menu_item_id, quantity, price)
            VALUES (?, ?, ?, ?)
        ''', (order_id, mid, qty, price))

    conn.commit()
    messagebox.showinfo("Success", f"Order Placed! Total Bill: ₹{total_bill}")
    load_orders()
    clear_fields()

def load_orders():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute('''
        SELECT o.id, u.name, u.phone, o.table_number,
               CASE WHEN o.is_home_delivery=1 THEN 'Home Delivery' ELSE 'Dine In' END,
               COALESCE(d.address, ''),
               GROUP_CONCAT(mi.name || " x" || oi.quantity, ", "),
               o.special_additions, o.total_bill, o.order_time
        FROM orders o
        JOIN users u ON o.user_id = u.id
        LEFT JOIN delivery_addresses d ON u.id = d.user_id
        JOIN order_items oi ON o.id = oi.order_id
        JOIN menu_items mi ON oi.menu_item_id = mi.id
        GROUP BY o.id
        ORDER BY o.order_time DESC
    ''')
    for row in cursor.fetchall():
        # Show: OrderID, Name, Phone, Table/Delivery, Address, Items, Special, Total, Time
        tree.insert('', 'end', values=row)

def clear_fields():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    table_entry.delete(0, tk.END)
    additions_text.delete("1.0", tk.END)
    address_text.delete("1.0", tk.END)
    delivery_var.set(0)
    toggle_address_fields()
    clear_order_list()
    category_combo.set('')
    item_combo.set('')
    qty_entry.delete(0, tk.END)

def delete_order():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select an order to delete")
        return
    order_id = tree.item(selected[0])['values'][0]
    cursor.execute("DELETE FROM order_items WHERE order_id=?", (order_id,))
    cursor.execute("DELETE FROM orders WHERE id=?", (order_id,))
    conn.commit()
    load_orders()
    messagebox.showinfo("Deleted", "Order deleted successfully")

def print_bill():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Warning", "Select an order to print")
        return
    order = tree.item(selected[0])['values']
    try:
        filename = f"bill_{order[0]}_{order[-1].replace(' ', '_').replace(':', '-')}.txt"
        with open(filename, "w") as file:
            file.write(f"Hotel Mess Bill\n\n")
            file.write(f"Date/Time: {order[-1]}\n")
            file.write(f"Order ID: {order[0]}\n")
            file.write(f"Name: {order[1]}\n")
            file.write(f"Phone: {order[2]}\n")
            if order[3]:
                file.write(f"Table Number: {order[3]}\n")
            if order[4] == 'Home Delivery':
                file.write(f"Delivery Address: {order[5]}\n")
            file.write(f"Items: {order[6]}\n")
            file.write(f"Special Requests: {order[7]}\n")
            file.write(f"Total Bill: ₹{order[8]}\n")
        messagebox.showinfo("Saved", f"Bill saved as '{filename}' in current directory")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save bill: {e}")

def toggle_address_fields():
    if delivery_var.get() == 1:
        table_entry.config(state='disabled')
        address_text.config(state='normal')
    else:
        table_entry.config(state='normal')
        address_text.config(state='disabled')

# ------------------------ UI Setup ------------------------

root = tk.Tk()
root.title("Hotel Mess Ordering System with Home Delivery")
root.geometry("1050x800")
root.configure(bg='#f0f4f8')

style = ttk.Style(root)
style.theme_use('clam')
style.configure('TButton', font=('Segoe UI', 11), padding=6, background='#4a90e2', foreground='white')
style.map('TButton', background=[('active', '#357ABD')])
style.configure('TLabel', font=('Segoe UI', 11), background='#f0f4f8')
style.configure('TEntry', font=('Segoe UI', 11))
style.configure('TCombobox', font=('Segoe UI', 11))

input_frame = ttk.Frame(root, padding=15)
input_frame.pack(fill=tk.X, padx=20, pady=10)

cust_frame = ttk.LabelFrame(input_frame, text="Customer Details", padding=15)
cust_frame.grid(row=0, column=0, sticky='nw', padx=10, pady=5)

ttk.Label(cust_frame, text="Name:").grid(row=0, column=0, sticky='e', pady=5, padx=5)
name_entry = ttk.Entry(cust_frame, width=30)
name_entry.grid(row=0, column=1, pady=5, padx=5)

ttk.Label(cust_frame, text="Phone:").grid(row=1, column=0, sticky='e', pady=5, padx=5)
phone_entry = ttk.Entry(cust_frame, width=30)
phone_entry.grid(row=1, column=1, pady=5, padx=5)

# Delivery option
delivery_var = tk.IntVar(value=0)
delivery_frame = ttk.Frame(cust_frame)
delivery_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky='w')

ttk.Label(delivery_frame, text="Order Type:").grid(row=0, column=0, padx=5)
ttk.Radiobutton(delivery_frame, text="Dine In", variable=delivery_var, value=0, command=toggle_address_fields).grid(row=0, column=1, padx=5)
ttk.Radiobutton(delivery_frame, text="Home Delivery", variable=delivery_var, value=1, command=toggle_address_fields).grid(row=0, column=2, padx=5)

ttk.Label(cust_frame, text="Table Number:").grid(row=3, column=0, sticky='e', pady=5, padx=5)
table_entry = ttk.Entry(cust_frame, width=30)
table_entry.grid(row=3, column=1, pady=5, padx=5)

ttk.Label(cust_frame, text="Delivery Address:").grid(row=4, column=0, sticky='ne', pady=5, padx=5)
address_text = tk.Text(cust_frame, width=30, height=4, state='disabled')
address_text.grid(row=4, column=1, pady=5, padx=5)

order_frame = ttk.LabelFrame(input_frame, text="Add Menu Items", padding=15)
order_frame.grid(row=0, column=1, sticky='nw', padx=10, pady=5)

ttk.Label(order_frame, text="Category:").grid(row=0, column=0, sticky='e', pady=5, padx=5)
category_combo = ttk.Combobox(order_frame, values=[], state="readonly", width=30)
category_combo.grid(row=0, column=1, pady=5, padx=5)
category_combo.bind("<<ComboboxSelected>>", update_items)

ttk.Label(order_frame, text="Select Item:").grid(row=1, column=0, sticky='e', pady=5, padx=5)
item_combo = ttk.Combobox(order_frame, values=[], state="readonly", width=30)
item_combo.grid(row=1, column=1, pady=5, padx=5)

ttk.Label(order_frame, text="Quantity:").grid(row=2, column=0, sticky='e', pady=5, padx=5)
qty_entry = ttk.Entry(order_frame, width=10)
qty_entry.grid(row=2, column=1, pady=5, padx=5, sticky='w')

add_item_btn = ttk.Button(order_frame, text="Add Item", command=add_item_to_order)
add_item_btn.grid(row=3, column=0, columnspan=2, pady=10)

ttk.Label(order_frame, text="Current Order Items:").grid(row=4, column=0, columnspan=2, pady=(10, 5))

order_listbox = tk.Listbox(order_frame, width=40, height=8, font=('Segoe UI', 10))
order_listbox.grid(row=5, column=0, columnspan=2, pady=5, padx=5)

total_var = tk.StringVar(value="Total: ₹0")
total_label = ttk.Label(order_frame, textvariable=total_var, font=('Segoe UI', 12, 'bold'), foreground='#2e7d32')
total_label.grid(row=6, column=0, columnspan=2, pady=10)

special_frame = ttk.LabelFrame(root, text="Special Additions / Requests", padding=15)
special_frame.pack(fill=tk.X, padx=20, pady=10)

additions_text = tk.Text(special_frame, height=4, font=('Segoe UI', 11))
additions_text.pack(fill=tk.X, padx=5, pady=5)

buttons_frame = ttk.Frame(root, padding=15)
buttons_frame.pack(fill=tk.X, padx=20, pady=10)

place_order_btn = ttk.Button(buttons_frame, text="Place Order", command=add_order)
place_order_btn.pack(side=tk.LEFT, padx=10)

delete_order_btn = ttk.Button(buttons_frame, text="Delete Order", command=delete_order)
delete_order_btn.pack(side=tk.LEFT, padx=10)

print_bill_btn = ttk.Button(buttons_frame, text="Print Bill", command=print_bill)
print_bill_btn.pack(side=tk.LEFT, padx=10)

orders_frame = ttk.Frame(root, padding=15)
orders_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

tree = ttk.Treeview(orders_frame, columns=("Order ID", "Name", "Phone", "Table/Delivery", "Delivery Address", "Items", "Special", "Total", "Time"), show='headings')
for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor='center')
tree.pack(fill=tk.BOTH, expand=True)

# Hover effect for buttons
def on_enter(e):
    e.widget.configure(style='Hover.TButton')

def on_leave(e):
    e.widget.configure(style='TButton')

style = ttk.Style(root)
style.configure('Hover.TButton', background='#2a5dab')

for btn in [place_order_btn, delete_order_btn, print_bill_btn, add_item_btn]:
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

load_categories()
toggle_address_fields()
root.mainloop()
