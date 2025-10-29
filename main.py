import tkinter as tk
from tkinter import messagebox, simpledialog
from dotenv import load_dotenv
import os, requests, threading, time
import fileFlaskTest
from datetime import datetime
import json

puCities = []
doCities = []
dates = []
dateTimes = []
pays = []

parent = None

def start_gui():
    # Window
    window = tk.Tk()
    window.title("GET Request App")
    window.geometry("480x420")
    parent = window

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


def open_trips_popup(parent, puCities, doCities, dateTime, pays):
    """
    Open a popup window titled 'Trips' and display each trip as text.
    To: puCities[i], From: doCities[i], Date/Time: dateTime[i], Pay: pays[i]
    """
    n = min(len(puCities), len(doCities), len(dateTime), len(pays))
    if n == 0:
        messagebox.showinfo("Trips", "No trips to display.")
        return

    # Create popup window
    win = tk.Toplevel(parent)
    win.title("Trips")
    win.geometry("420x360")

    # Text widget to show trips
    text_box = tk.Text(win, wrap="word", font=("Arial", 11))
    text_box.pack(fill="both", expand=True, padx=10, pady=10)

    # Populate trips
    for i in range(n):
        trip_text = (
            f"Trip {i+1}:\n"
            f"  To:   {puCities[i]}\n"
            f"  From: {doCities[i]}\n"
            f"  Date/Time: {dateTime[i]}\n"
            f"  Pay: ${pays[i]:.2f}\n"
            "--------------------------\n"
        )
        text_box.insert(tk.END, trip_text)

    text_box.config(state="disabled")  # make it read-only

    # Buttons frame
    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=8)

    # Reserve button (does nothing yet)
    reserve_btn = tk.Button(btn_frame, text="Reserve Trips", bg="green", fg="white")
    reserve_btn.grid(row=0, column=0, padx=6)

    # Close button
    close_btn = tk.Button(btn_frame, text="Close", command=win.destroy)
    close_btn.grid(row=0, column=1, padx=6)

def add_city(listbox: tk.Listbox, count_label: tk.Label):
    """Prompt for a city and add it to the list/array/UI."""
    city = simpledialog.askstring("Add City", "Enter city name:")
    if city:
        city = city.strip()
        if not city:
            return
        puCities.append(city)
        listbox.insert(tk.END, city)
        count_label.config(text=f"{len(puCities)} {'city' if len(puCities)==1 else 'cities'}")

def add_date(listbox: tk.Listbox, count_label: tk.Label):
    """Prompt for a date, validate, then add. Accepts YYYY-MM-DD or MM/DD/YYYY."""
    date_str = simpledialog.askstring("Add Date", "Enter date MM/DD):")
    if not date_str:
        return

    date_str = date_str.strip()
    if not date_str:
        return



    # Store normalized as YYYY-MM-DD for consistency
    dates.append(date_str)
    listbox.insert(tk.END, date_str)
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
        print("PU CITY:", pu_city)
        do_city = trip.get("doCity", "").upper()
        print("DO CITY:", do_city)
        due_date = trip.get("dueTime", "")
        print("DUE DATE:", due_date)
        pay_amount = float(trip.get("payAmount", 0))
        print("PAY AMOUNT:", pay_amount)

        #  check if either city matches one in puCities[]
        # TODO: add dropoff checking 
        city_match = any(city in [pu_city] for city in puCities)


        #  check if due_date contains any date substring in dates[]
        date_match = any(date_str in due_date for date_str in dates)

        #  final combined check
        if city_match and date_match and pay_amount >= 20:
            results.append((trip["boltTripId"], due_date))
            dateTimes.append(due_date)
            doCities.append(do_city)
            pays.append(pay_amount)

        
        print("RESULTS:", results)
    open_trips_popup(parent, puCities, doCities, dateTimes, pays)
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