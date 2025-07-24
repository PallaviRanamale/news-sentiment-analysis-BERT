import streamlit as st
from google.cloud import bigquery
import pandas as pd
import plotly.express as px
import os

# ✅ Step 1: Set Google credentials (hardcoded path)
gcp_key_path = r"<PATH_TO_GCP_KEY>.json"  # Make sure this is the correct .json key
project_id = "<YOUR_PROJECT_ID>"

if not os.path.exists(gcp_key_path):
    st.error(f"❌ GCP key file not found at: {gcp_key_path}")
    st.stop()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gcp_key_path

# ✅ Step 2: Set up Streamlit layout
st.set_page_config(page_title="News Dashboard", layout="wide")
st.title("📰 Real-time News Sentiment Dashboard")

try:
    st.write("🔌 Connecting to BigQuery...")

    # ✅ Step 3: Initialize BigQuery client
    client = bigquery.Client()

    # ✅ Step 4: Define dataset and table
    dataset = "news_dataset_asia"
    table = "news_with_sentiment"

    # ✅ Step 5: Run SQL query
    query = f"""
    SELECT * 
    FROM `{project_id}.{dataset}.{table}`
    ORDER BY publishedAt DESC
    LIMIT 100
    """

    st.code(query)
    st.write("📥 Running query...")

    df = client.query(query).to_dataframe()
    st.success("✅ Data fetched successfully!")

    # ✅ Step 6: Search filter
    keyword = st.text_input("🔍 Search by keyword (in title or description):")
    if keyword:
        df = df[df['title'].str.contains(keyword, case=False, na=False) |
                df['description'].str.contains(keyword, case=False, na=False)]

    # ✅ Step 7: Show filtered results
    st.markdown("### 📄 News Results")
    st.dataframe(df)

    # ✅ Step 8: Sentiment Distribution
    if 'sentiment' in df.columns:
        sentiment_counts = df['sentiment'].value_counts().reset_index()
        sentiment_counts.columns = ['sentiment', 'count']

        st.markdown("### 📊 Sentiment Distribution")
        fig = px.bar(sentiment_counts, x='sentiment', y='count',
                     color='sentiment', title="News Sentiment Distribution")
        st.plotly_chart(fig)

except Exception as e:
    st.error("❌ An error occurred while fetching data from BigQuery:")
    st.exception(e)

# ✅ Step 9: Footer
st.markdown("---")
st.write("© 2025 Pallavi Ranamale | Powered by Streamlit & Google BigQuery")
