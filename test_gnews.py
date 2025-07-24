import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY ="9d56ceaf8083ebfd0a9b90848596fe3b"

BASE_URL = 'https://gnews.io/api/v4/search'
params = {
    'token': API_KEY,
    'q': 'Modi'  # more general
    # 'lang': 'en',
    # 'country': 'in',
    # 'max': 10
}

response = requests.get(BASE_URL, params=params)
print("Status Code:", response.status_code)
print("URL:", response.url)

try:
    data = response.json()
    print("Total Articles:", data.get("totalArticles"))
    for article in data.get("articles", []):
        print("-", article["title"])
except Exception as e:
    print("Error parsing JSON:", e)

print(data)