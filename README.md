# 📰 News Sentiment Analysis Project

A comprehensive end-to-end news sentiment analysis pipeline that fetches news articles, performs sentiment analysis using multiple methods (VADER, BERT, GPT-3.5), stores results, and visualizes them in an interactive dashboard.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.47.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Project Overview

This project demonstrates a complete data pipeline for news sentiment analysis:

1. **Data Collection**: Fetches news articles from GNews API
2. **Sentiment Analysis**: Implements three different approaches:
   - **VADER**: Fast rule-based sentiment analysis
   - **BERT**: Deep learning-based sentiment analysis (DistilBERT)
   - **GPT-3.5**: Large Language Model-based sentiment analysis
3. **Data Storage**: Local CSV files and Google BigQuery integration
4. **Visualization**: Interactive Streamlit dashboard with real-time filtering and charts

## 🚀 Live Demo

👉 **[View Live Dashboard on Streamlit Cloud](https://your-app-name.streamlit.app)**

*Note: Update the link above with your Streamlit Cloud deployment URL*

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Sentiment Analysis Methods](#sentiment-analysis-methods)
- [Screenshots](#screenshots)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- 🔍 **Multi-source News Fetching**: Fetch news from GNews API with customizable queries
- 🧠 **Multiple Sentiment Methods**: Compare rule-based, ML, and LLM approaches
- 📊 **Interactive Dashboard**: Real-time filtering, sentiment distribution charts
- ☁️ **Cloud Integration**: Google BigQuery for scalable data storage
- 🔄 **ETL Pipeline**: Complete Extract, Transform, Load workflow
- 📈 **Data Visualization**: Plotly charts for sentiment insights
- 🔐 **Secure Configuration**: Environment variable management for API keys

## 🏗️ Architecture

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
│  CSV Files      │ (Local Storage)
└────────┬────────┘
         │
         ├─────────────────┬─────────────────┐
         ▼                 ▼                 ▼
┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ VADER Analysis │ │ BERT Analysis  │ │ GPT-3.5 Analysis  │
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

## 💻 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/GnewsSentimentAnalysis.git
cd GnewsSentimentAnalysis
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Download NLTK Data

```bash
python -c "import nltk; nltk.download('vader_lexicon')"
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root:

```env
# GNews API Key (get from https://gnews.io/)
API_KEY=your_gnews_api_key_here

# OpenAI API Key (optional, for GPT-3.5 analysis)
OPENAI_API_KEY=your_openai_api_key_here

# Google Cloud Platform (optional, for BigQuery)
GOOGLE_APPLICATION_CREDENTIALS=path/to/gcp_key.json
GCP_PROJECT_ID=your_project_id
DATASET_ID=news_dataset_asia
TABLE_ID=news_with_sentiment
```

## 🚀 Usage

### Quick Start (Local Dashboard)

1. **Run Local Dashboard** (works without API keys):
```bash
streamlit run dashboard_local.py
```
The dashboard will open at `http://localhost:8501`

### Complete Pipeline

#### Step 1: Fetch News Articles

```bash
python fetch_news_gnews.py
```

This creates `gnews_output.csv` with fetched news articles.

#### Step 2: Perform Sentiment Analysis

Choose one or more methods:

**VADER (Fast, Rule-based):**
```bash
python news_sentiment_vader.py
```
Output: `news_with_sentiment.csv`

**BERT (Accurate, Deep Learning):**
```bash
python news_sentiment_BERT.py
```
Output: `news_with_bert_sentiment.csv`

**GPT-3.5 (Most Context-Aware):**
```bash
python news_sentiment_LLM.py
```
Output: `news_with_gpt_sentiment.csv`

#### Step 3: Upload to BigQuery (Optional)

```bash
python upload_to_bigquery.py
```

Make sure to configure:
- GCP credentials path
- Project ID
- Dataset and table names

#### Step 4: View Dashboard

**Local Version (CSV files):**
```bash
streamlit run dashboard_local.py
```

**BigQuery Version:**
```bash
streamlit run dashboard.py
```

## 📁 Project Structure

```
GnewsSentimentAnalysis/
│
├── 📄 Core Scripts
│   ├── fetch_news_gnews.py          # Fetch news from GNews API
│   ├── news_sentiment_vader.py      # VADER sentiment analysis
│   ├── news_sentiment_BERT.py       # BERT sentiment analysis
│   ├── news_sentiment_LLM.py        # GPT-3.5 sentiment analysis
│   ├── upload_to_bigquery.py        # Upload data to BigQuery
│   ├── dashboard.py                 # BigQuery dashboard
│   └── dashboard_local.py           # Local CSV dashboard
│
├── 📊 Data Files
│   ├── gnews_output.csv             # Raw news data
│   ├── news_data.csv                # Processed news data
│   ├── news_with_sentiment.csv      # VADER results
│   ├── news_with_bert_sentiment.csv # BERT results
│   └── news_with_gpt_sentiment.csv  # GPT-3.5 results
│
├── 📚 Documentation
│   ├── README.md                    # This file
│   ├── PROJECT_GUIDE.md             # Comprehensive project guide
│   ├── QUICK_REFERENCE.md           # Quick reference cheat sheet
│   ├── TECHNICAL_DETAILS.md         # Technical implementation details
│   └── RUN_SUMMARY.md               # Execution summary
│
├── ⚙️ Configuration
│   ├── requirements.txt             # Python dependencies
│   ├── .gitignore                   # Git ignore rules
│   └── .env                         # Environment variables (not in repo)
│
└── 🧪 Testing
    ├── test_gnews.py                # Test GNews API
    └── test.py                      # Test BigQuery connection
```

## 🛠️ Technologies Used

### Core Languages & Frameworks
- **Python 3.8+** - Programming language
- **Pandas** - Data manipulation and analysis
- **Streamlit** - Web dashboard framework
- **Plotly** - Interactive data visualization

### NLP & Machine Learning
- **NLTK** - Natural Language Toolkit (VADER sentiment)
- **Transformers (Hugging Face)** - BERT model integration
- **PyTorch** - Deep learning framework
- **OpenAI API** - GPT-3.5 access

### Cloud & Data Storage
- **Google Cloud BigQuery** - Data warehouse
- **google-cloud-bigquery** - Python client library

### APIs & Services
- **GNews API** - News article fetching
- **OpenAI API** - GPT-3.5 sentiment analysis

### Utilities
- **python-dotenv** - Environment variable management
- **tqdm** - Progress bars
- **requests** - HTTP library

## 🧠 Sentiment Analysis Methods

### 1. VADER (Valence Aware Dictionary and sEntiment Reasoner)

**Type:** Rule-based lexicon  
**Speed:** ⚡⚡⚡ Fastest  
**Accuracy:** ⭐⭐ Good for simple text  
**Use Case:** High-volume, real-time processing

**How it works:**
- Uses pre-built dictionary of words with sentiment scores
- Considers punctuation, capitalization, word shape
- Compound score threshold: ≥ 0.05 (Positive), ≤ -0.05 (Negative)

### 2. BERT (Bidirectional Encoder Representations from Transformers)

**Type:** Deep Learning (Transformer)  
**Speed:** ⚡⚡ Medium (requires model loading)  
**Accuracy:** ⭐⭐⭐ High  
**Use Case:** When accuracy is more important than speed

**Model Used:**
- **DistilBERT**: `distilbert-base-uncased-finetuned-sst-2-english`
- Lightweight version (60% smaller, 60% faster)
- Fine-tuned on SST-2 dataset
- ~97% of full BERT's accuracy

### 3. GPT-3.5 (Large Language Model)

**Type:** LLM-based  
**Speed:** ⚡ Slowest (API calls)  
**Accuracy:** ⭐⭐⭐⭐ Highest (context-aware)  
**Use Case:** Complex, ambiguous text requiring deep understanding

**Configuration:**
- Model: `gpt-3.5-turbo`
- Temperature: 0.3 (low randomness)
- Max tokens: 10 (cost optimization)

## 📊 Dashboard Features

The interactive dashboard provides:

- 📰 **News Article Viewing**: Browse fetched articles with details
- 🔍 **Keyword Search**: Filter articles by title or description
- 📈 **Sentiment Distribution**: Visual charts showing sentiment breakdown
- 📊 **Statistics**: Count of positive, negative, and neutral articles
- 📅 **Date Filtering**: Sort by publication date
- 📱 **Responsive Design**: Works on desktop and mobile

## 🔧 Configuration

### API Keys Setup

1. **GNews API Key**:
   - Sign up at [https://gnews.io/](https://gnews.io/)
   - Get your free API key
   - Add to `.env`: `API_KEY=your_key`

2. **OpenAI API Key** (Optional):
   - Sign up at [https://platform.openai.com/](https://platform.openai.com/)
   - Get API key from dashboard
   - Add to `.env`: `OPENAI_API_KEY=your_key`

3. **Google Cloud Setup** (Optional):
   - Create project in [Google Cloud Console](https://console.cloud.google.com/)
   - Enable BigQuery API
   - Create service account and download JSON key
   - Add to `.env`: 
     ```
     GOOGLE_APPLICATION_CREDENTIALS=path/to/key.json
     GCP_PROJECT_ID=your_project_id
     ```

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Deploy to Streamlit Cloud"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select repository and branch
   - Main file: `dashboard_local.py` (or `dashboard.py` for BigQuery)
   - Click "Deploy"

3. **Add Secrets** (for API keys):
   - Go to app settings → Secrets
   - Add secrets in TOML format:
     ```toml
     API_KEY = "your_gnews_key"
     OPENAI_API_KEY = "your_openai_key"
     ```

### Alternative Deployment Options

- **Heroku**: Use `Procfile` and `runtime.txt`
- **Docker**: Containerize the application
- **Google Cloud Run**: Serverless deployment
- **AWS EC2/ECS**: Cloud infrastructure

## 📸 Screenshots

*Add screenshots of your dashboard here*

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Pallavi Ranamale**

- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-profile)

## 🙏 Acknowledgments

- GNews API for news data
- Hugging Face for transformer models
- Streamlit for the dashboard framework
- OpenAI for GPT-3.5 access
- Google Cloud Platform for BigQuery

## 📚 Additional Resources

- [PROJECT_GUIDE.md](PROJECT_GUIDE.md) - Comprehensive project documentation
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick reference cheat sheet
- [TECHNICAL_DETAILS.md](TECHNICAL_DETAILS.md) - Technical implementation details

## ❓ FAQ

**Q: Do I need all API keys to run the project?**  
A: No! You can run the local dashboard with existing CSV files without any API keys.

**Q: Which sentiment method is best?**  
A: Depends on your needs:
- Speed → VADER
- Accuracy → BERT
- Context understanding → GPT-3.5

**Q: Can I use my own news source?**  
A: Yes! Modify `fetch_news_gnews.py` to integrate with any news API.

**Q: How much does GPT-3.5 analysis cost?**  
A: Approximately $0.002 per 1K tokens. For 100 articles, expect a few cents.

---

⭐ If you find this project helpful, please give it a star!
