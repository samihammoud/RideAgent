from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os  

# Load .env variables
load_dotenv()

url = os.getenv("URL")
token = os.getenv("AUTH_TOKEN")

# Create Flask app instance
app = Flask(__name__)

# Example route that uses your env vars
@app.route('/{url}')
def show_env():
    return jsonify({
        "url": url,
        "token": token
    })

# Run the server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
