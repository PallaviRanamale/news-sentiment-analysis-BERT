# 📰 Real-Time News Sentiment Analysis with GPT & BigQuery

This project performs real-time sentiment analysis on news headlines using OpenAI's GPT model, stores the results in Google BigQuery, and visualizes the output with a Streamlit dashboard.

---

## 📁 Project Structure

```
GnewsSentimentAnalysis/
├── fetch_news_gnews.py          # Fetches real-time news from GNews API
├── news_sentiment_BERT.py       # Sentiment analysis using BERT
├── news_sentiment_vader.py      # Sentiment analysis using Vader
├── news_sentiment_LLM.py        # Sentiment analysis using OpenAI LLM
├── upload_to_bigquery.py        # Uploads sentiment-labeled data to BigQuery
├── dashboard.py                 # Streamlit dashboard for visualization
├── news_sentiment_output.csv    # Output file with headlines and sentiment
├── .env                         # Stores API keys and credentials
├── requirements.txt             # Python dependencies
├── README.md                    # This file
```

---

## ✅ Features

- ✅ Fetch latest news headlines using GNews API  
- ✅ Perform sentiment analysis with multiple models:  
  - BERT-based transformer  
  - Traditional Vader  
  - OpenAI GPT (LLM)  
- ✅ Store results in Google BigQuery  
- ✅ Visualize sentiment trends in a live dashboard  
- ✅ Modular design for automation and extension  

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/PallaviRanamale/news-sentiment-analysis-BERT.git
cd news-sentiment-analysis-BERT
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root with the following:

```env
GNEWS_API_KEY=your_gnews_api_key
OPENAI_API_KEY=your_openai_api_key
GOOGLE_APPLICATION_CREDENTIALS=your_service_account_file.json
PROJECT_ID=your_gcp_project_id
```

---

## 🚀 Running the Pipeline

### 1. Fetch News

```bash
python fetch_news_gnews.py
```

### 2. Perform Sentiment Analysis

Choose any of the following:

```bash
python news_sentiment_BERT.py      # For BERT-based model
python news_sentiment_vader.py     # For traditional Vader
python news_sentiment_LLM.py       # For OpenAI LLM
```

Output will be saved in `news_sentiment_output.csv`.

### 3. Upload to BigQuery

Ensure dataset exists in your GCP BigQuery project.

```bash
python upload_to_bigquery.py
```

### 4. Run the Dashboard

```bash
streamlit run dashboard.py
```

---

## 📦 Requirements

From `requirements.txt`:

```txt
openai
gnewsclient
python-dotenv
google-cloud-bigquery
pandas
plotly
streamlit
```

Install via:

```bash
pip install -r requirements.txt
```

---

## 📊 Example Output (CSV)

| title                             | sentiment |
| --------------------------------- | --------- |
| Markets rally amid optimism       | Positive  |
| Inflation fears weigh on stocks  | Negative  |

---

## 🙋‍♀️ Author

**Pallavi Ranamale**  
📍 Pune, India  
🔗 [LinkedIn](https://www.linkedin.com/in/pallavi-ranamale)

---

## 📄 License

This project is licensed under the **MIT License**.  
You are free to use, copy, modify, merge, publish, and distribute this software.
