import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables for local development
load_dotenv()

# ✅ Helper function to get secrets (works both locally and on Streamlit Cloud)
def get_secret(key):
    """Get secret from Streamlit secrets or environment variable."""
    try:
        if hasattr(st, 'secrets') and key in st.secrets:
            return st.secrets[key]
    except:
        pass
    return os.getenv(key)

# ✅ Set up Streamlit layout
st.set_page_config(page_title="News Sentiment Dashboard", layout="wide")
st.title("📰 News Sentiment Analysis Dashboard")

# Check secrets status
has_gnews_api = bool(get_secret("API_KEY"))
has_openai_api = bool(get_secret("OPENAI_API_KEY"))

# Show secrets status in sidebar
st.sidebar.markdown("### 🔐 API Configuration")
st.sidebar.markdown(f"**GNews API:** {'✅ Configured' if has_gnews_api else '❌ Not configured'}")
st.sidebar.markdown(f"**OpenAI API:** {'✅ Configured' if has_openai_api else '❌ Not configured'}")

if not has_gnews_api:
    st.sidebar.info("💡 Add API_KEY in Streamlit secrets to enable news fetching")
if not has_openai_api:
    st.sidebar.info("💡 Add OPENAI_API_KEY in Streamlit secrets to enable GPT-3.5 analysis")

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

# Main tabs
tab1, tab2, tab3 = st.tabs(["📊 View Data", "📰 Fetch News", "🤖 Analyze with GPT"])

# ==================== TAB 1: View Data ====================
with tab1:
    st.markdown("### View Existing Data")
    
    # File selection
    data_source = st.selectbox(
        "Choose CSV file:",
        ["news_with_sentiment.csv", "news_with_bert_sentiment.csv", "gnews_output.csv", "news_with_gpt_sentiment.csv"]
    )
    
    try:
        # Load data from CSV
        df = pd.read_csv(data_source)
    
        if df.empty:
            st.warning("No data found in the selected file.")
        else:
            st.success(f"✅ Loaded {len(df)} articles from {data_source}")
            
            # Convert publishedAt to datetime if it exists
            if 'publishedAt' in df.columns:
                df['publishedAt'] = pd.to_datetime(df['publishedAt'], errors='coerce')
                df = df.sort_values('publishedAt', ascending=False)
            
            # Search filter
            keyword = st.text_input("🔍 Search by keyword (in title or description):")
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
                    
                    st.markdown("### 📊 Sentiment Distribution")
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
                st.info("No sentiment columns found. Use the 'Analyze with GPT' tab to add sentiment analysis.")
            
            # Show raw data stats
            with st.expander("📈 Data Statistics"):
                st.write(f"**Columns:** {', '.join(df.columns)}")
                st.write(f"**Total rows:** {len(df)}")
                if 'publishedAt' in df.columns:
                    st.write(f"**Date range:** {df['publishedAt'].min()} to {df['publishedAt'].max()}")

    except FileNotFoundError:
        st.error(f"❌ File {data_source} not found. Use other tabs to fetch or analyze data.")
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.exception(e)

# ==================== TAB 2: Fetch News ====================
with tab2:
    st.markdown("### 📰 Fetch Fresh News from GNews API")
    
    if not has_gnews_api:
        st.warning("⚠️ GNews API key not configured. Please add API_KEY in Streamlit Cloud secrets to use this feature.")
        st.info("""
        **How to add API key:**
        1. Go to your Streamlit app → Settings → Secrets
        2. Add: `API_KEY = "your_gnews_api_key"`
        3. Save and wait for app to restart
        """)
    else:
        st.success("✅ GNews API is configured!")
        
        col1, col2 = st.columns(2)
        with col1:
            query = st.text_input("🔍 Search Query:", value="India", help="What to search for")
            country = st.selectbox("🌍 Country:", ["in", "us", "uk", "au", "ca", "de", "fr", "jp"], index=0)
        with col2:
            lang = st.selectbox("🗣️ Language:", ["en", "hi", "es", "fr", "de", "ja"], index=0)
            max_articles = st.slider("📊 Number of Articles:", 10, 100, 50)
        
        if st.button("🚀 Fetch News", type="primary"):
            api_key = get_secret("API_KEY")
            
            with st.spinner("⏳ Fetching news articles from GNews..."):
                try:
                    BASE_URL = 'https://gnews.io/api/v4/search'
                    params = {
                        'token': api_key,
                        'q': query,
                        'lang': lang,
                        'country': country,
                        'max': max_articles,
                    }
                    
                    response = requests.get(BASE_URL, params=params)
                    response.raise_for_status()
                    data = response.json()
                    
                    articles = []
                    for item in data.get("articles", []):
                        articles.append({
                            "title": item.get("title"),
                            "description": item.get("description"),
                            "publishedAt": item.get("publishedAt"),
                            "source": item.get("source", {}).get("name"),
                            "url": item.get("url")
                        })
                    
                    df_new = pd.DataFrame(articles)
                    
                    if df_new.empty:
                        st.warning("⚠️ No articles found. Try different search terms.")
                    else:
                        df_new["publishedAt"] = pd.to_datetime(df_new["publishedAt"])
                        st.success(f"✅ Successfully fetched {len(df_new)} articles!")
                        
                        # Display articles
                        st.markdown("### 📄 Fetched News Articles")
                        st.dataframe(df_new, use_container_width=True)
                        
                        # Download option
                        csv = df_new.to_csv(index=False)
                        st.download_button(
                            label="📥 Download as CSV",
                            data=csv,
                            file_name=f"gnews_{query}_{country}_{lang}.csv",
                            mime="text/csv"
                        )
                        
                        # Store in session state for GPT analysis
                        st.session_state['fetched_news'] = df_new
                        st.info("💡 Tip: You can now use the 'Analyze with GPT' tab to analyze these articles!")
                        
                except Exception as e:
                    st.error(f"❌ Error fetching news: {str(e)}")
                    st.info("💡 Check your API key and try again. Make sure you haven't exceeded your API quota.")

# ==================== TAB 3: GPT Analysis ====================
with tab3:
    st.markdown("### 🤖 Analyze Sentiment with GPT-3.5")
    
    if not has_openai_api:
        st.warning("⚠️ OpenAI API key not configured. Please add OPENAI_API_KEY in Streamlit Cloud secrets to use this feature.")
        st.info("""
        **How to add API key:**
        1. Go to your Streamlit app → Settings → Secrets
        2. Add: `OPENAI_API_KEY = "your_openai_api_key"`
        3. Save and wait for app to restart
        
        **Get OpenAI API Key:**
        - Sign up at https://platform.openai.com/
        - Go to API Keys section
        - Create a new secret key
        """)
    else:
        st.success("✅ OpenAI API is configured!")
        
        # Option to use fetched news or load from file
        use_fetched = st.checkbox("Use recently fetched news (from Fetch News tab)", value=False)
        
        if use_fetched and 'fetched_news' in st.session_state:
            df_analyze = st.session_state['fetched_news']
            st.info(f"📊 Analyzing {len(df_analyze)} articles from fetched news")
        else:
            # Load data for analysis
            analysis_file = st.selectbox(
                "📁 Select data to analyze:",
                ["gnews_output.csv", "news_data.csv", "pune_news_data.csv"]
            )
            
            try:
                df_analyze = pd.read_csv(analysis_file)
                st.info(f"📊 Ready to analyze {len(df_analyze)} articles from {analysis_file}")
            except FileNotFoundError:
                st.error(f"❌ File {analysis_file} not found.")
                st.stop()
            except Exception as e:
                st.error(f"❌ Error loading file: {str(e)}")
                st.stop()
        
        # Limit articles for analysis (to control costs)
        max_analyze = st.slider("📊 Max articles to analyze:", 5, min(100, len(df_analyze)), min(20, len(df_analyze)))
        df_analyze = df_analyze.head(max_analyze)
        
        if st.button("🚀 Run GPT-3.5 Analysis", type="primary"):
            # Initialize OpenAI client
            openai_key = get_secret("OPENAI_API_KEY")
            client = OpenAI(api_key=openai_key)
            
            def classify_sentiment_gpt(text):
                """Classify sentiment using GPT-3.5"""
                if pd.isna(text) or not str(text).strip():
                    return "Neutral"
                
                # Use description if available, otherwise title
                text_to_analyze = str(text)[:500]  # Limit length to control costs
                
                prompt = f"What is the sentiment of the following news text? Respond with only one word: Positive, Negative, or Neutral.\n\nText: {text_to_analyze}"
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a sentiment analysis assistant. Always respond with only one word: Positive, Negative, or Neutral."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.3,
                        max_tokens=10
                    )
                    sentiment = response.choices[0].message.content.strip()
                    # Normalize response
                    if "Positive" in sentiment or "positive" in sentiment:
                        return "Positive"
                    elif "Negative" in sentiment or "negative" in sentiment:
                        return "Negative"
                    else:
                        return "Neutral"
                except Exception as e:
                    st.error(f"Error analyzing: {str(e)}")
                    return "Unknown"
            
            # Analyze with progress bar
            progress_bar = st.progress(0)
            status_text = st.empty()
            results = []
            
            for idx, row in df_analyze.iterrows():
                status_text.text(f"⏳ Analyzing article {idx + 1}/{len(df_analyze)}...")
                
                # Use description if available, otherwise title
                text_to_analyze = row.get('description', row.get('title', ''))
                sentiment = classify_sentiment_gpt(text_to_analyze)
                results.append(sentiment)
                
                progress_bar.progress((idx + 1) / len(df_analyze))
            
            # Add results to dataframe
            df_analyze['gpt_sentiment'] = results
            
            progress_bar.empty()
            status_text.empty()
            st.success(f"✅ Analysis complete! Analyzed {len(df_analyze)} articles.")
            
            # Show results
            st.markdown("### 📊 Analysis Results")
            st.dataframe(df_analyze[['title', 'description', 'gpt_sentiment']].head(20))
            
            # Sentiment distribution
            sentiment_counts = pd.Series(results).value_counts()
            fig = px.bar(
                x=sentiment_counts.index,
                y=sentiment_counts.values,
                color=sentiment_counts.index,
                title="GPT-3.5 Sentiment Distribution",
                labels={'x': 'Sentiment', 'y': 'Count'},
                color_discrete_map={'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray', 'Unknown': 'orange'}
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Analyzed", len(df_analyze))
            with col2:
                positive_count = results.count('Positive')
                st.metric("Positive", positive_count)
            with col3:
                negative_count = results.count('Negative')
                st.metric("Negative", negative_count)
            with col4:
                neutral_count = results.count('Neutral')
                st.metric("Neutral", neutral_count)
            
            # Download results
            csv = df_analyze.to_csv(index=False)
            st.download_button(
                label="📥 Download Results as CSV",
                data=csv,
                file_name="news_with_gpt_sentiment.csv",
                mime="text/csv"
            )
            
            st.info("💡 The analyzed data has been saved. You can now view it in the 'View Data' tab!")

# Footer
st.markdown("---")
st.write("© 2025 Pallavi Ranamale | Powered by Streamlit")

