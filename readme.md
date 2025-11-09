# Hotel Mess Ordering System

A desktop application built with Python, Tkinter, and SQLite for managing a hotel or restaurant's ordering process. It supports both dine-in and home delivery, saves customer information, and generates bills.


*(**Note:** Take a screenshot of your running application and add it here.)*

## 🌟 Features

* **Full Menu System:** A pre-populated, multi-category menu (Breakfast, Non-Veg, etc.).
* **Customer Management:** Saves customer names and phone numbers for easy recall.
* **Dual Order Modes:**
    * **Dine-In:** Assign orders to a specific table number.
    * **Home Delivery:** Automatically prompts for and saves a delivery address.
* **Order Cart:** Dynamically add items, specify quantity, and see a running total.
* **Persistent Storage:** Uses **SQLite** to save all menu items, customers, and order history.
* **Order History:** A sortable table displays all past orders with complete details.
* **Bill Generation:** Instantly save a formatted bill for any selected order as a `.txt` file.

## 🚀 Installation & Usage

This project is very easy to run because it uses only Python's built-in libraries.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/agent-rxd/Hotel-Billing-System-in-Python.git
    cd hotel-ordering-system
    ```

2.  **Run the application:**
    Since there are **no external dependencies**, you don't need to `pip install` anything. Just run the script with Python.
    ```bash
    python3 main.py
    ```

3.  **Database Setup:**
    The first time you run the script, it will automatically create a `hotel.db` file in the same directory. This file will be fully populated with all the menu items, and it will store all your future orders.
