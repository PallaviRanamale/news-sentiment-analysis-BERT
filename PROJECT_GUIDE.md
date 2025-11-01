# 📚 Complete Project Guide: GNews Sentiment Analysis

## 🎯 Project Overview

This project is a **News Sentiment Analysis Pipeline** that:
1. Fetches news articles from GNews API (Google News)
2. Performs sentiment analysis using **three different methods**:
   - **VADER** (rule-based, fast)
   - **BERT** (Deep learning, more accurate)
   - **GPT-3.5** (LLM-based, context-aware)
3. Stores results in CSV files
4. Uploads data to **Google BigQuery** for analytics
5. Visualizes results in a **Streamlit dashboard**

---

## 🏗️ Architecture & Data Flow

```
┌─────────────────┐
│  GNews API      │ (News Source)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ fetch_news_gnews│ (Data Collection)
│      .py        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  CSV Files      │ (news_data.csv, gnews_output.csv)
└────────┬────────┘
         │
         ├─────────────────┬─────────────────┐
         ▼                 ▼                 ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ VADER Analysis │ │ BERT Analysis  │ │ GPT-3.5        │
│ news_sentiment │ │ news_sentiment │ │ news_sentiment │
│   _vader.py    │ │   _BERT.py     │ │   _LLM.py      │
└────────┬───────┘ └────────┬───────┘ └────────┬───────┘
         │                  │                  │
         └──────────────────┴──────────────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  CSV Outputs    │
                  │ (with sentiment) │
                  └────────┬─────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ upload_to_      │
                  │ bigquery.py     │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Google BigQuery │
                  │   (Data Lake)   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  dashboard.py   │
                  │  (Streamlit UI) │
                  └─────────────────┘
```

---

## 📁 File-by-File Breakdown

### 1. **fetch_news_gnews.py** - News Data Fetcher
**Purpose**: Fetches news articles from GNews API

**Key Features**:
- Uses GNews API v4 to fetch news
- Searches for news about "India" (configurable)
- Filters by language (English) and country (India)
- Fetches up to 100 articles
- Extracts: title, description, published date, source, URL
- Saves to `gnews_output.csv`

**Technologies**:
- `requests` - HTTP library for API calls
- `pandas` - Data manipulation
- `python-dotenv` - Environment variable management
- `datetime` - Date/time handling

**API Details**:
- Base URL: `https://gnews.io/api/v4/search`
- Requires API key stored in `.env` file
- Parameters: `token`, `q` (query), `lang`, `country`, `max`

**Key Code Logic**:
```python
# Fetches news with error handling
response = requests.get(BASE_URL, params=params)
data = response.json()
# Extracts articles into structured format
# Saves to CSV with datetime conversion
```

---

### 2. **news_sentiment_vader.py** - VADER Sentiment Analysis
**Purpose**: Performs rule-based sentiment analysis using VADER

**Key Features**:
- Uses NLTK's VADER (Valence Aware Dictionary and sEntiment Reasoner)
- Analyzes both title and description separately
- Returns: Positive, Negative, or Neutral
- Threshold: ±0.05 for sentiment classification

**How VADER Works**:
- Lexicon-based approach (pre-built dictionary of words with sentiment scores)
- Considers punctuation, capitalization, word-shape
- Fast and doesn't require training

**Threshold Logic**:
- `compound >= 0.05` → Positive
- `compound <= -0.05` → Negative
- Otherwise → Neutral

**Output**: `news_with_sentiment.csv` with `sentiment_title` and `sentiment_description` columns

**Advantages**:
- ✅ Fast (no ML model loading)
- ✅ Good for social media text
- ✅ Handles negations, exclamations well

**Limitations**:
- ❌ Less accurate for complex sentences
- ❌ Doesn't understand context deeply

---

### 3. **news_sentiment_BERT.py** - BERT-Based Sentiment Analysis
**Purpose**: Performs deep learning-based sentiment analysis using BERT

**Key Features**:
- Uses **DistilBERT** model: `distilbert-base-uncased-finetuned-sst-2-english`
- Hugging Face Transformers pipeline
- PyTorch framework
- Shows progress bar using `tqdm`

**Model Details**:
- **DistilBERT**: Lightweight version of BERT (faster, smaller)
- Fine-tuned on SST-2 (Stanford Sentiment Treebank v2)
- Binary classification: POSITIVE/NEGATIVE
- Converts to Positive/Negative/Neutral format

**How BERT Works**:
- Transformer-based architecture
- Bidirectional context understanding
- Pre-trained on large corpus, then fine-tuned
- Embeddings capture semantic meaning

**Output**: `news_with_bert_sentiment.csv` with `bert_sentiment` column

**Advantages**:
- ✅ More accurate than VADER
- ✅ Understands context and nuance
- ✅ Better for complex sentences

**Limitations**:
- ❌ Slower (requires model loading)
- ❌ More memory intensive
- ❌ Requires GPU for optimal performance

---

### 4. **news_sentiment_LLM.py** - GPT-3.5 Sentiment Analysis
**Purpose**: Uses OpenAI's GPT-3.5 for sentiment analysis

**Key Features**:
- Uses OpenAI API (GPT-3.5-turbo)
- Chat completions endpoint
- System prompt for sentiment analysis
- Temperature=0.3 (low randomness for consistency)
- Max tokens=10 (efficient)

**API Call Structure**:
```python
System: "You are a sentiment analysis assistant."
User: "What is the sentiment of the following news text? 
       Respond with Positive, Negative, or Neutral only."
```

**Advantages**:
- ✅ Most context-aware
- ✅ Can handle ambiguous text better
- ✅ Understands implicit sentiment

**Limitations**:
- ❌ Cost per API call
- ❌ Requires internet connection
- ❌ Slower (API latency)
- ❌ Rate limits apply

**Output**: `news_with_gpt_sentiment.csv` with `gpt_sentiment` column

---

### 5. **upload_to_bigquery.py** - Data Pipeline to Cloud
**Purpose**: Uploads CSV data to Google BigQuery

**Key Features**:
- Uses Google Cloud service account authentication
- Creates dataset if it doesn't exist
- Uploads DataFrame directly to BigQuery table
- Location: `asia-south1` (Mumbai region)

**Configuration**:
- Dataset: `news_dataset_asia`
- Table: `news_with_sentiment`
- Authentication: JSON service account key file

**Key Steps**:
1. Load credentials from JSON file
2. Initialize BigQuery client
3. Check/create dataset
4. Load DataFrame to table
5. Wait for job completion

**Why BigQuery?**:
- Scalable data warehouse
- SQL querying capabilities
- Integration with other GCP services
- Cost-effective for large datasets
- Real-time analytics

---

### 6. **dashboard.py** - Streamlit Visualization
**Purpose**: Interactive web dashboard for viewing news and sentiment analysis

**Key Features**:
- Streamlit web app
- Connects to BigQuery for real-time data
- Search/filter functionality
- Sentiment distribution visualization (Plotly)
- Displays latest 100 articles

**Dashboard Components**:
1. **Connection Status**: Shows BigQuery connection
2. **Search Bar**: Filter by keyword in title/description
3. **Data Table**: Displays filtered news articles
4. **Sentiment Chart**: Bar chart showing sentiment distribution
5. **Footer**: Attribution

**Technologies**:
- Streamlit: Web framework for Python
- Plotly: Interactive charts
- Google Cloud BigQuery: Data source
- Pandas: Data manipulation

**SQL Query**:
```sql
SELECT * 
FROM `{project_id}.news_dataset_asia.news_with_sentiment`
ORDER BY publishedAt DESC
LIMIT 100
```

**How to Run**:
```bash
streamlit run dashboard.py
```

---

## 🔧 Technologies & Libraries

### Core Technologies
1. **Python 3.x** - Programming language
2. **Pandas** - Data manipulation and analysis
3. **Requests** - HTTP library for API calls

### NLP & ML
1. **NLTK** - Natural Language Toolkit (VADER)
2. **Transformers** - Hugging Face library (BERT)
3. **PyTorch** - Deep learning framework
4. **OpenAI API** - GPT-3.5 access

### Cloud & Data
1. **Google Cloud BigQuery** - Data warehouse
2. **google-cloud-bigquery** - Python client
3. **google-auth** - Authentication

### Visualization & UI
1. **Streamlit** - Web dashboard framework
2. **Plotly** - Interactive charts

### Utilities
1. **python-dotenv** - Environment variable management
2. **tqdm** - Progress bars

---

## 🔄 Complete Workflow

### Step 1: Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (.env file)
API_KEY=<gnews_api_key>
OPENAI_API_KEY=<openai_key>
GOOGLE_APPLICATION_CREDENTIALS=<path_to_gcp_key.json>
GCP_PROJECT_ID=<project_id>
```

### Step 2: Fetch News
```bash
python fetch_news_gnews.py
```
- Fetches news from GNews API
- Saves to `gnews_output.csv`

### Step 3: Sentiment Analysis (Choose one or all)

**Option A: VADER (Fast)**
```bash
python news_sentiment_vader.py
```
- Output: `news_with_sentiment.csv`

**Option B: BERT (Accurate)**
```bash
python news_sentiment_BERT.py
```
- Output: `news_with_bert_sentiment.csv`

**Option C: GPT-3.5 (Most Context-Aware)**
```bash
python news_sentiment_LLM.py
```
- Output: `news_with_gpt_sentiment.csv`

### Step 4: Upload to BigQuery
```bash
python upload_to_bigquery.py
```
- Creates dataset if needed
- Uploads CSV to BigQuery table

### Step 5: Visualize
```bash
streamlit run dashboard.py
```
- Opens web dashboard
- View news and sentiment analysis

---

## 🎓 Key Concepts to Understand

### 1. **Sentiment Analysis Methods**

#### VADER (Rule-Based)
- **Type**: Lexicon-based
- **Speed**: Fastest
- **Accuracy**: Good for simple text
- **Use Case**: Real-time, high-volume processing

#### BERT (Deep Learning)
- **Type**: Transformer-based neural network
- **Speed**: Medium (requires model loading)
- **Accuracy**: High
- **Use Case**: When accuracy is more important than speed

#### GPT-3.5 (LLM-Based)
- **Type**: Large Language Model
- **Speed**: Slowest (API calls)
- **Accuracy**: Highest (context-aware)
- **Use Case**: Complex, ambiguous text

### 2. **API Integration**
- **GNews API**: RESTful API, requires authentication token
- **OpenAI API**: Chat completions endpoint, rate-limited
- **Error Handling**: Try-except blocks for robust code

### 3. **Data Pipeline**
- **ETL Process**: Extract (API) → Transform (Sentiment) → Load (BigQuery)
- **Data Formats**: CSV for intermediate storage, BigQuery for analytics
- **Data Transformation**: Pandas DataFrames for manipulation

### 4. **Cloud Architecture**
- **Google Cloud Platform**: BigQuery data warehouse
- **Service Account**: Secure authentication method
- **Region**: asia-south1 (Mumbai) for low latency

### 5. **Visualization**
- **Streamlit**: Python-first, no HTML/CSS needed
- **Plotly**: Interactive, publication-ready charts
- **Real-time**: Queries BigQuery on each page load

---

## 💼 Interview Questions & Answers

### Q1: What is this project about?
**Answer**: This project is an end-to-end news sentiment analysis pipeline that fetches news articles from GNews API, performs sentiment analysis using three different methods (VADER, BERT, and GPT-3.5), stores the results in BigQuery, and visualizes them in an interactive Streamlit dashboard.

---

### Q2: Why did you use three different sentiment analysis methods?
**Answer**: Each method has different strengths:
- **VADER**: Fast, rule-based, good for quick processing of large volumes
- **BERT**: More accurate, understands context better, uses deep learning
- **GPT-3.5**: Most context-aware, handles ambiguous text, but slower and costs money

This comparison allows evaluating trade-offs between speed, accuracy, and cost.

---

### Q3: Explain how BERT sentiment analysis works.
**Answer**: BERT (Bidirectional Encoder Representations from Transformers) is a transformer-based model that:
1. Uses attention mechanisms to understand context in both directions
2. Was pre-trained on large text corpora
3. Was fine-tuned on SST-2 dataset for sentiment classification
4. Processes text through tokenization, embedding layers, and transformer layers
5. Outputs probabilities for POSITIVE/NEGATIVE classes

In this project, I use DistilBERT (a smaller, faster version) which maintains most of BERT's accuracy with better efficiency.

---

### Q4: What is the difference between rule-based and ML-based sentiment analysis?
**Answer**: 
- **Rule-based (VADER)**: Uses predefined dictionaries of words with sentiment scores. Fast, deterministic, but limited by vocabulary and rules.
- **ML-based (BERT/GPT)**: Learns patterns from data. More accurate, understands context, but requires training data and computational resources.

---

### Q5: Why did you choose Google BigQuery?
**Answer**: 
- **Scalability**: Handles large datasets efficiently
- **SQL Interface**: Easy querying with familiar SQL syntax
- **Integration**: Works seamlessly with other GCP services
- **Cost-effective**: Pay per query, not for storage infrastructure
- **Real-time Analytics**: Fast queries even on large datasets
- **Managed Service**: No infrastructure management needed

---

### Q6: How does the Streamlit dashboard work?
**Answer**: The dashboard:
1. Connects to BigQuery using service account credentials
2. Executes a SQL query to fetch the latest 100 articles
3. Displays data in an interactive table
4. Allows keyword filtering in real-time
5. Visualizes sentiment distribution using Plotly bar charts
6. Updates dynamically on each page interaction

---

### Q7: How do you handle errors in API calls?
**Answer**: I use try-except blocks:
- `response.raise_for_status()` checks HTTP status codes
- Exception handling catches network errors, API errors, and parsing errors
- Graceful degradation (returns empty data structure if API fails)
- Debug prints help identify issues

---

### Q8: What are the challenges you faced?
**Answer**: 
1. **API Rate Limits**: GNews and OpenAI have rate limits, requiring careful request management
2. **Model Loading Time**: BERT model takes time to load, affecting first-run performance
3. **Cost Management**: GPT-3.5 API calls can be expensive for large datasets
4. **Data Consistency**: Different sentiment methods may produce different results
5. **BigQuery Authentication**: Setting up service account credentials correctly

---

### Q9: How would you improve this project?
**Answer**:
1. **Caching**: Cache BERT model in memory, cache API responses
2. **Batch Processing**: Process multiple articles in batches for efficiency
3. **Scheduling**: Use Airflow/Prefect for automated daily runs
4. **Data Validation**: Add data quality checks before uploading
5. **Monitoring**: Add logging and error tracking (e.g., Sentry)
6. **Testing**: Unit tests for each component
7. **Containerization**: Dockerize for easy deployment
8. **CI/CD**: Automated testing and deployment pipeline
9. **Real-time Updates**: Use webhooks or scheduled jobs for fresh data
10. **Advanced Analytics**: Time-series analysis, trend detection

---

### Q10: What is the data flow from API to dashboard?
**Answer**:
1. **Extract**: `fetch_news_gnews.py` → GNews API → `gnews_output.csv`
2. **Transform**: Sentiment analysis scripts → Add sentiment columns → Updated CSV
3. **Load**: `upload_to_bigquery.py` → BigQuery table
4. **Visualize**: `dashboard.py` → Query BigQuery → Streamlit UI

This follows the ETL (Extract, Transform, Load) pattern.

---

### Q11: Explain VADER's compound score.
**Answer**: VADER's compound score ranges from -1 (most negative) to +1 (most positive). It's a normalized, weighted composite of the positive, negative, and neutral scores. In this project, I use thresholds:
- ≥ 0.05 → Positive
- ≤ -0.05 → Negative  
- Between → Neutral

This threshold helps reduce noise and classify clear sentiments.

---

### Q12: What is the difference between DistilBERT and full BERT?
**Answer**: 
- **DistilBERT**: 60% smaller, 60% faster, ~97% of BERT's performance
- **Full BERT**: More parameters, slower, slightly more accurate
- **Trade-off**: Speed vs. accuracy - DistilBERT is often better for production

---

### Q13: How would you deploy this project?
**Answer**:
1. **Containerization**: Docker container with all dependencies
2. **Cloud Run/App Engine**: Serverless deployment for dashboard
3. **Cloud Functions**: Serverless functions for sentiment analysis
4. **Cloud Scheduler**: Automated daily news fetching
5. **Environment Variables**: Secure credential management
6. **CI/CD Pipeline**: GitHub Actions for automated deployment

---

### Q14: What is the cost consideration for each sentiment method?
**Answer**:
- **VADER**: Free, runs locally
- **BERT**: Free, but requires computational resources (CPU/GPU)
- **GPT-3.5**: Pay per API call (~$0.002 per 1K tokens), can be expensive at scale

For 100 articles, GPT-3.5 might cost a few cents, while VADER/BERT are essentially free.

---

### Q15: How do you ensure data quality?
**Answer**:
- Validate API responses before processing
- Handle missing/null values (using `pd.isna()`)
- Check data types and formats
- Validate sentiment outputs (ensure they're Positive/Negative/Neutral)
- BigQuery schema validation on upload

---

## 📊 Project Statistics

- **Languages**: Python
- **APIs Used**: 2 (GNews, OpenAI)
- **Sentiment Methods**: 3 (VADER, BERT, GPT-3.5)
- **Storage**: CSV (local) + BigQuery (cloud)
- **Visualization**: Streamlit + Plotly
- **Cloud Provider**: Google Cloud Platform

---

## 🚀 Running the Project

### Prerequisites
1. Python 3.8+
2. GNews API key
3. OpenAI API key (for LLM analysis)
4. Google Cloud Project with BigQuery enabled
5. Service account JSON key file

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('vader_lexicon')"

# Create .env file with:
# API_KEY=your_gnews_key
# OPENAI_API_KEY=your_openai_key
# GOOGLE_APPLICATION_CREDENTIALS=path/to/key.json
# GCP_PROJECT_ID=your_project_id
```

### Execution Order
1. Fetch news → 2. Analyze sentiment → 3. Upload to BigQuery → 4. View dashboard

---

## 📝 Notes

- The project demonstrates both traditional NLP and modern ML approaches
- Shows understanding of API integration, cloud services, and data visualization
- Demonstrates end-to-end data pipeline architecture
- Handles real-world challenges like error handling and scalability

---

**Good luck with your interview! You've got this! 🎯**

