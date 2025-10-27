import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
import os, requests, threading, time

# Load environment variables
load_dotenv()
get_url = os.getenv("GET_URL") 
post_url = os.getenv("POST_URL")

app = Flask(__name__)
token = os.getenv("AUTH_TOKEN")

# Function to send GET request
def send_get_request():
    time.sleep(1)  # wait a moment for Flask to start
    print(f"Sending GET request to: {get_url}")
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }
        response = requests.get(get_url, headers=headers)
        return response
        print("Response status:", response.status_code)
        print("Response body:", response.text[:200])  # print first 200 chars
    except Exception as e:
        print("Request failed:", e)
        return None


def send_post_request(payload):
    time.sleep(1)
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(post_url, headers=headers, json=payload)
        print("Response status:", response.status_code)
        print("Response body:", response.text[:200])  # print first 200 chars
    except Exception as e:
        print("Request failed:", e)


# @app.route('/send_post_request', methods=['POST'])
# def send_post_request():
#     """Accept a JSON body from Postman and forward it to the remote API."""
#     try:
#         payload = request.get_json()

#         time.sleep(1)

#         headers = {
#             "Authorization": f"Bearer {token}",
#             "Accept": "application/json",
#             "Content-Type": "application/json"
#         }

#         # Send POST to external API
#         response = requests.post(post_url, headers=headers, json=payload)

#         # Print to terminal for debug
#         print("Response status:", response.status_code)
#         print("Response body:", response.text[:200])

#         # Return response summary to the client
#         return jsonify({
#             "status": "success",
#             "remote_status": response.status_code,
#             "remote_response": response.json()
#         }), 200

    # except Exception as e:
    #     print("Request failed:", e)
    #     return jsonify({"status": "failed", "error": str(e)}), 500

    


if __name__ == '__main__':
    # Run GET request in a separate thread so Flask can start normally
    threading.Thread(target=send_get_request).start()
    app.run(host='0.0.0.0', port=3000, debug=True)
