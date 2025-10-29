import tkinter as tk
from tkinter import messagebox, simpledialog
from dotenv import load_dotenv
import os, requests, threading, time
import fileFlaskTest
from datetime import datetime
import json

cities = []
dates = []


def start_gui():
    # Window
    window = tk.Tk()
    window.title("GET Request App")
    window.geometry("480x420")

    # Title label
    title = tk.Label(window, text="Click to send GET request", font=("Arial", 12))
    title.pack(pady=8)

    # Buttons row (GET + adders)
    btns_frame = tk.Frame(window)
    btns_frame.pack(pady=6)

    get_button = tk.Button(
        btns_frame, text="Send GET Request",
        command=handle_get_request, bg="blue", fg="black"
    )
    get_button.grid(row=0, column=0, padx=6)

    add_city_btn = tk.Button(
        btns_frame, text="Add City",
        command=lambda: add_city(city_listbox, city_count_lbl)
    )
    add_city_btn.grid(row=0, column=1, padx=6)

    add_date_btn = tk.Button(
        btns_frame, text="Add Date",
        command=lambda: add_date(date_listbox, date_count_lbl)
    )
    add_date_btn.grid(row=0, column=2, padx=6)

    # Lists section
    lists_frame = tk.Frame(window)
    lists_frame.pack(fill="x", padx=10, pady=10)

    # Cities panel
    city_panel = tk.LabelFrame(lists_frame, text="Cities")
    city_panel.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

    city_listbox = tk.Listbox(city_panel, height=10, width=24)
    city_listbox.pack(padx=8, pady=8)

    city_count_lbl = tk.Label(city_panel, text="0 cities")
    city_count_lbl.pack(padx=8, pady=(0,8))

    # Dates panel
    date_panel = tk.LabelFrame(lists_frame, text="Dates")
    date_panel.grid(row=0, column=1, sticky="nsew", padx=(8, 0))

    date_listbox = tk.Listbox(date_panel, height=10, width=24)
    date_listbox.pack(padx=8, pady=8)

    date_count_lbl = tk.Label(date_panel, text="0 dates")
    date_count_lbl.pack(padx=8, pady=(0,8))

    # Make columns expand nicely
    lists_frame.grid_columnconfigure(0, weight=1)
    lists_frame.grid_columnconfigure(1, weight=1)

    # Price section
    price_frame = tk.LabelFrame(window, text="Ride Price")
    price_frame.pack(fill="x", padx=10, pady=10)

    tk.Label(price_frame, text="Enter price (e.g., 20.50):").grid(row=0, column=0, padx=8, pady=8, sticky="w")

    price_var = tk.StringVar()
    price_entry = tk.Entry(price_frame, textvariable=price_var, width=12)
    price_entry.grid(row=0, column=1, padx=4, pady=8, sticky="w")

    price_display = tk.Label(price_frame, text="Current price: —")
    price_display.grid(row=0, column=3, padx=8, pady=8, sticky="w")

    def set_price():
        txt = price_var.get().strip()
        if not txt:
            messagebox.showwarning("Price", "Please enter a price.")
            return
        try:
            # Basic numeric validation
            value = float(txt)
            if value < 0:
                raise ValueError
            price_display.config(text=f"Current price: ${value:.2f}")
        except ValueError:
            messagebox.showerror("Price", "Invalid price. Use a positive number like 12 or 12.99.")

    set_price_btn = tk.Button(price_frame, text="Set Price", command=set_price)
    set_price_btn.grid(row=0, column=2, padx=6, pady=8)

    window.mainloop()

def add_city(listbox: tk.Listbox, count_label: tk.Label):
    """Prompt for a city and add it to the list/array/UI."""
    city = simpledialog.askstring("Add City", "Enter city name:")
    if city:
        city = city.strip()
        if not city:
            return
        cities.append(city)
        listbox.insert(tk.END, city)
        count_label.config(text=f"{len(cities)} {'city' if len(cities)==1 else 'cities'}")

def add_date(listbox: tk.Listbox, count_label: tk.Label):
    """Prompt for a date, validate, then add. Accepts YYYY-MM-DD or MM/DD/YYYY."""
    date_str = simpledialog.askstring("Add Date", "Enter date (YYYY-MM-DD or MM/DD/YYYY):")
    if not date_str:
        return

    date_str = date_str.strip()
    if not date_str:
        return

    parsed = None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y"):
        try:
            parsed = datetime.strptime(date_str, fmt)
            break
        except ValueError:
            continue

    if parsed is None:
        messagebox.showerror("Invalid Date", "Please use YYYY-MM-DD or MM/DD/YYYY.")
        return

    # Store normalized as YYYY-MM-DD for consistency
    normalized = parsed.strftime("%Y-%m-%d")
    dates.append(normalized)
    listbox.insert(tk.END, normalized)
    print("DATE: ", dates)
    count_label.config(text=f"{len(dates)} {'date' if len(dates)==1 else 'dates'}")

def handle_get_request():
    response = fileFlaskTest.send_get_request()
    try:
        data = json.loads(response)
    except TypeError:
        # If it's already a Python object (list), no need to load
        data = response
    # Filter and extract results
    results = []
    # print("DATA: ", data)
    for trip in data:  # assuming you have a list of trip dicts
        pu_city = trip.get("puCity", "").upper()
        do_city = trip.get("doCity", "").upper()
        due_date = trip.get("dueDate", "")
        pay_amount = float(trip.get("payAmount", 0))

        #  check if either city matches one in cities[]
        city_match = any(city in [pu_city, do_city] for city in cities)

        #  check if due_date contains any date substring in dates[]
        date_match = any(date_str in due_date for date_str in dates)

        #  final combined check
        if city_match and date_match and pay_amount >= 20:
            results.append((trip["boltTripId"], due_date))

        print("RESULTS:", results)
    return results

def poll_forever():
    while True:
        try:
            results = handle_get_request()
            for trip_id, due_date in results:
                payload = {
                    "boltTripIds": trip_id,
                    "driverId": "47065",
                    "eventType": "confirm",
                    "time": due_date
                }
                fileFlaskTest.send_post_request(payload)

            # Wait before next poll
            time.sleep(3)

        except Exception as e:
            print("error during polling:", e)



start_gui()