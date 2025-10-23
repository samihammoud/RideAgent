import requests
import env

load_dotenv()
url = os.getenv("URL")
token = os.getenv("AUTH_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.get(url)

# Print status code and data
print(response.status_code)
print(response.json())  # Converts JSON → Python dictionary