import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk

# 🔁 Load previous CSV
df = pd.read_csv("news_data.csv")

# 📥 Download VADER Lexicon (if not already downloaded)
nltk.download('vader_lexicon')

# 🧠 Initialize VADER
vader = SentimentIntensityAnalyzer()

# 🧪 Apply sentiment analysis to each row
def get_sentiment(text):
    if pd.isna(text):
        return "Neutral"
    score = vader.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# 🧾 Apply to title and description (you can choose one or both)
df["sentiment_title"] = df["title"].apply(get_sentiment)
df["sentiment_description"] = df["description"].apply(get_sentiment)

# 💾 Save updated data
df.to_csv("news_with_sentiment.csv", index=False)

# ✅ Preview result
print("Sentiment analysis complete!")
print(df[["title", "sentiment_title", "description", "sentiment_description"]].head())
