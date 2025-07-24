import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_sentiment(text):
    prompt = f"What is the sentiment of the following news text? Respond with Positive, Negative, or Neutral only.\n\nText: {text}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a sentiment analysis assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=10
        )
        sentiment = response.choices[0].message.content.strip()
        return sentiment
    except Exception as e:
        print("Error:", e)
        return "Unknown"

# Load news data
df = pd.read_csv("pune_news_data.csv")

# Apply sentiment analysis
df['gpt_sentiment'] = df['description'].apply(lambda x: classify_sentiment(str(x)))

# Save to new file
df.to_csv("news_with_gpt_sentiment.csv", index=False)

# ✅ Only show columns that exist
print(df[['title', 'description', 'gpt_sentiment']].head())
