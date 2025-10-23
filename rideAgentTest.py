import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.get(url)

# Print status code and data
print(response.status_code)
print(response.json())  # Converts JSON → Python dictionary