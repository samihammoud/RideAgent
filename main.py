import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import os, requests, threading, time
import fileFlaskTest
from datetime import date
import json


def start_gui():
    #window 
    window = tk.Tk()
    window.title("GET Request App")
    window.geometry("300x150")

    label = tk.Label(window, text="Click to send GET request", font=("Arial", 12))
    label.pack(pady=20)


    #buttons
    # button = tk.Button(window, text="Send Get Request", command=handle_get_request, bg="blue", fg="black")
    # button.pack(pady=10)


    button = tk.Button(window, text="Send Post Request", command=handle_post_request, bg="blue", fg="black")
    button.pack(pady=10)

    window.mainloop()

def handle_get_request():
    response = fileFlaskTest.send_get_request()
    try:
        data = json.loads(response)
    except TypeError:
        # If it's already a Python object (list), no need to load
        data = response
    # Filter and extract results
    results = []
    print("DATA: ", data)
    for trip in data:
        # Normalize city names
        pu_city = trip.get("puCity", "").strip().upper()
        # print("PU CITY:", pu_city)
        do_city = trip.get("doCity", "").strip().upper()
        # print("DO CITY:", do_city)
        pay_amount = float(trip.get("payAmount", 0))
        # print("PAY AMOUNT:", pay_amount)
        due_date = trip.get("dueDateTime", "")
        # print("DUE DATE:", due_date)
        if (
            ("RIVERSIDE" in [pu_city, do_city] or "CORONA" or "RANCHO MIRAGE" in [pu_city]) and
            "29 Oct" in due_date and pay_amount>=20
        ):
            results.append((trip["boltTripId"], due_date))
        # print("RESULTS:", results)
    return results

##GETS BOLT TRIP ID, TIME; BUILD FINAL JSON STRUCTURE IN fileFlaskTest
def handle_post_request():
    results = handle_get_request()
    # print(results[0], "FIRST ONE")
    trip_id, due_date = results[0]
    response = fileFlaskTest.send_post_request(trip_id, due_date)



start_gui()