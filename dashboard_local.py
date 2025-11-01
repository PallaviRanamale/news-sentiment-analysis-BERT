import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

# Load environment variables for local development
load_dotenv()

# ✅ Helper function to check secrets (works both locally and on Streamlit Cloud)
def get_secret(key):
    """Check if secret exists in Streamlit secrets or environment variable."""
    try:
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except:
        pass
    return os.getenv(key)

# ✅ Set up Streamlit layout
st.set_page_config(page_title="News Dashboard", layout="wide")
st.title("News Sentiment Dashboard (Local)")

# Check secrets status
has_gnews_api = bool(get_secret("API_KEY"))
has_openai_api = bool(get_secret("OPENAI_API_KEY"))

# Show secrets status in sidebar
st.sidebar.markdown("### 🔐 API Configuration")
st.sidebar.markdown(f"**GNews API:** {'✅ Configured' if has_gnews_api else '❌ Not configured'}")
st.sidebar.markdown(f"**OpenAI API:** {'✅ Configured' if has_openai_api else '❌ Not configured'}")

if not has_gnews_api or not has_openai_api:
    with st.sidebar.expander("ℹ️ How to add API keys"):
        st.markdown("""
        1. Go to **share.streamlit.io**
        2. Click your app → **⋮ Menu** → **Settings**
        3. Click **Secrets** in sidebar
        4. Add:
        ```toml
        API_KEY = "your_key"
        OPENAI_API_KEY = "your_key"
        ```
        5. Click **Save**
        """)

# File selection
st.sidebar.markdown("### Select Data Source")
data_source = st.sidebar.selectbox(
    "Choose CSV file:",
    ["news_with_sentiment.csv", "news_with_bert_sentiment.csv", "gnews_output.csv"]
)

try:
    # Load data from CSV
    df = pd.read_csv(data_source)
    
    if df.empty:
        st.warning("No data found in the selected file.")
    else:
        st.success(f"Loaded {len(df)} articles from {data_source}")
        
        # Convert publishedAt to datetime if it exists
        if 'publishedAt' in df.columns:
            df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
            df = df.sort_values('publishedAt', ascending=False)
        
        # Search filter
        keyword = st.text_input("Search by keyword (in title or description):")
        if keyword:
            mask = (
                df['title'].astype(str).str.contains(keyword, case=False, na=False) |
                df['description'].astype(str).str.contains(keyword, case=False, na=False)
            )
            df = df[mask]
            st.info(f"Found {len(df)} articles matching '{keyword}'")
        
        # Show data
        st.markdown("### News Results")
        st.dataframe(df, use_container_width=True)
        
        # Sentiment Distribution
        sentiment_columns = [col for col in df.columns if 'sentiment' in col.lower()]
        
        if sentiment_columns:
            selected_sentiment = st.selectbox("Select sentiment column:", sentiment_columns)
            
            if selected_sentiment in df.columns:
                sentiment_counts = df[selected_sentiment].value_counts().reset_index()
                sentiment_counts.columns = ['sentiment', 'count']
                
                st.markdown("### Sentiment Distribution")
                fig = px.bar(
                    sentiment_counts, 
                    x='sentiment', 
                    y='count',
                    color='sentiment', 
                    title=f"News Sentiment Distribution ({selected_sentiment})",
                    color_discrete_map={
                        'Positive': 'green',
                        'Negative': 'red',
                        'Neutral': 'gray',
                        'POSITIVE': 'green',
                        'NEGATIVE': 'red'
                    }
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Show statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Articles", len(df))
                with col2:
                    positive_count = len(df[df[selected_sentiment].isin(['Positive', 'POSITIVE'])])
                    st.metric("Positive", positive_count)
                with col3:
                    negative_count = len(df[df[selected_sentiment].isin(['Negative', 'NEGATIVE'])])
                    st.metric("Negative", negative_count)
        else:
            st.info("No sentiment columns found. Run sentiment analysis scripts first.")
        
        # Show raw data stats
        with st.expander("Data Statistics"):
            st.write(f"Columns: {', '.join(df.columns)}")
            st.write(f"Total rows: {len(df)}")
            if 'publishedAt' in df.columns:
                st.write(f"Date range: {df['publishedAt'].min()} to {df['publishedAt'].max()}")

except FileNotFoundError:
    st.error(f"File {data_source} not found. Please run the sentiment analysis scripts first.")
except Exception as e:
    st.error(f"An error occurred: {str(e)}")
    st.exception(e)

# Footer
st.markdown("---")
st.write("© 2025 Pallavi Ranamale | Powered by Streamlit")

