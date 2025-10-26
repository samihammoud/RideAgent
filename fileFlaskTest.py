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
    def run_request():
        time.sleep(0.2)
        print(f"Sending GET request to: {url}")
        try:
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            }
            response = requests.get(url, headers=headers)
            print("Response status:", response.status_code)
            print("Response body:", response.text[:200])
            messagebox.showinfo("Success", f"Status: {response.status_code}")
        except Exception as e:
            print("Request failed:", e)
            messagebox.showerror("Error", str(e))
    threading.Thread(target=run_request).start()

# ---- Tkinter GUI ----
window = tk.Tk()
window.title("GET Request App")
window.geometry("300x150")

label = tk.Label(window, text="Click to send GET request", font=("Arial", 12))
label.pack(pady=20)

button = tk.Button(window, text="Send Request", command=send_get_request, bg="blue", fg="white")
button.pack(pady=10)

window.mainloop()
