import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import os, requests, threading, time
import fileFlaskTest
from datetime import date






def start_gui():
    #window 
    window = tk.Tk()
    window.title("GET Request App")
    window.geometry("300x150")

    label = tk.Label(window, text="Click to send GET request", font=("Arial", 12))
    label.pack(pady=20)


    #buttons
    button = tk.Button(window, text="Send Request", command=fileFlaskTest.send_get_request, bg="blue", fg="white")
    button.pack(pady=10)



    window.mainloop()



start_gui()