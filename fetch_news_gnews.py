import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import os

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")
print("🔐 Loaded API Key:", API_KEY)  # Debug print

BASE_URL = 'https://gnews.io/api/v4/search'

params = {
    'token': API_KEY,
    'q': 'India',        # Test with broader keyword
    'lang': 'en',
    'country': 'in',
    'max': 100,
}

try:
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()
except Exception as e:
    print("❌ Error fetching data:", e)
    data = {}

articles = []
for item in data.get("articles", []):
    articles.append({
        "title": item.get("title"),
        "description": item.get("description"),
        "publishedAt": item.get("publishedAt"),
        "source": item.get("source", {}).get("name"),
        "url": item.get("url")
    })

df = pd.DataFrame(articles)

if df.empty:
    print("⚠️ No articles found. Please check your query.")
else:
    df["publishedAt"] = pd.to_datetime(df["publishedAt"])
    df.to_csv("gnews_output.csv", index=False)
    print("✅ Successfully fetched news!")
    print(df.head())
