import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import os, requests, threading, time

# Load environment variables
load_dotenv()
url = os.getenv("URL") or "https://jsonplaceholder.typicode.com/posts/1"
token = os.getenv("AUTH_TOKEN")

# Function to send GET request
def send_get_request():
    time.sleep(0.2)
    print(f"Sending GET request to: {url}")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers)
        messagebox.showinfo("Success", f"Status: {response.status_code}")
    except Exception as e:
        print("Request failed:", e)
        messagebox.showerror("Error", str(e))
    return response.text

