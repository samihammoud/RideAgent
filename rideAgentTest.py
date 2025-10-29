# from flask import Flask, jsonify
# from dotenv import load_dotenv
# import os, threading, time, requests

# load_dotenv()
# url = os.getenv("URL") 

# app = Flask(__name__)
# token = os.getenv("AUTH_TOKEN")

# @app.route('/')
# def home():
#     return jsonify({"message": "Server is running"})

# # Function to send GET request after startup
# def send_get_request():
#     time.sleep(1)  # wait a moment for Flask to start
#     print(f"Sending GET request to: {url}")
#     try:
#         headers = {
#             "Authorization": f"Bearer {token}",
#             "Accept": "application/json"
#         }
#         response = requests.get(url, headers=headers)
#         print("Response status:", response.status_code)
#         print("Response body:", response.text[:200])  # print first 200 chars
#     except Exception as e:
#         print("Request failed:", e)
    
# if __name__ == '__main__':
#     # Run GET request in a separate thread so Flask can start normally
#     threading.Thread(target=send_get_request).start()
#     app.run(host='0.0.0.0', port=3000, debug=True)