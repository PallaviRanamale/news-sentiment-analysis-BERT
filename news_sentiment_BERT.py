import pandas as pd
from transformers import pipeline
from tqdm import tqdm

# Load your CSV file
df = pd.read_csv("gnews_output.csv")  # Make sure this file exists

# Load sentiment-analysis pipeline from Hugging Face
sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", framework="pt")

# Function to classify sentiment using BERT
def classify_sentiment_bert(text):
    try:
        result = sentiment_pipeline(str(text))[0]
        label = result['label']
        # Convert labels like 'POSITIVE'/'NEGATIVE' to 'Positive'/'Negative'/'Neutral'
        if label == 'POSITIVE':
            return 'Positive'
        elif label == 'NEGATIVE':
            return 'Negative'
        else:
            return 'Neutral'
    except Exception as e:
        print("Error:", e)
        return 'Unknown'

# Apply BERT sentiment analysis with a progress bar
tqdm.pandas()
df['bert_sentiment'] = df['description'].progress_apply(classify_sentiment_bert)

# Save results to new CSV
df.to_csv("news_with_bert_sentiment.csv", index=False)

# Show a preview
print(df[['title', 'bert_sentiment']].head(10))

# ✅ Only show columns that exist
print(df[['title', 'description', 'bert_sentiment']].head())