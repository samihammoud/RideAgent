import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import os, requests, threading, time

load_dotenv()
get_url = os.getenv("GET_URL") 
post_url = os.getenv("POST_URL") # or "https://jsonplaceholder.typicode.com/posts/1"
token = os.getenv("AUTH_TOKEN")

def send_post_request(trip_id, due_date):
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        payload = {
            "boltTripIds": trip_id,
            "driverId": "47065",
            "eventType": "confirm",
            "time": due_date
        }

        response = requests.post(post_url, headers=headers, json=payload)
        print("Response status:", response.status_code)
        print("Response body:", response.text[:200])  # print first 200 chars
    except Exception as e:
        print("Request failed:", e)



# Function to send GET request
def send_get_request():
    time.sleep(0.2)
    print(f"Sending GET request to: {get_url}")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.get(get_url, headers=headers)
        messagebox.showinfo("Success", f"Status: {response.status_code}")
    except Exception as e:
        print("Request failed:", e)
        messagebox.showerror("Error", str(e))
    return response.text

