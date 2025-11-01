# 📖 How to Use the Enhanced Dashboard

## 🎯 Overview

Your dashboard now has **3 main tabs** with powerful features:

1. **📊 View Data** - Browse existing CSV files
2. **📰 Fetch News** - Get fresh news from GNews API
3. **🤖 Analyze with GPT** - Run GPT-3.5 sentiment analysis

---

## 📰 Tab 2: Fetch Fresh News

### How to Use:

1. **Make sure GNews API key is configured**
   - Check sidebar: Should show "✅ Configured"
   - If not, add `API_KEY` in Streamlit secrets (see instructions in sidebar)

2. **Go to "Fetch News" tab**

3. **Configure your search:**
   - **Search Query**: What to search for (e.g., "India", "Technology", "Sports")
   - **Country**: Select country code (in=India, us=USA, etc.)
   - **Language**: Select language (en=English, hi=Hindi, etc.)
   - **Number of Articles**: Slider to choose how many articles (10-100)

4. **Click "🚀 Fetch News" button**

5. **View Results:**
   - Articles will appear in a table
   - Download as CSV if needed
   - Articles are automatically saved for GPT analysis!

### Example:
```
Search Query: "Artificial Intelligence"
Country: "us" (United States)
Language: "en" (English)
Number of Articles: 50

Result: 50 fresh articles about AI!
```

---

## 🤖 Tab 3: Analyze with GPT-3.5

### How to Use:

1. **Make sure OpenAI API key is configured**
   - Check sidebar: Should show "✅ Configured"
   - If not, add `OPENAI_API_KEY` in Streamlit secrets

2. **Go to "Analyze with GPT" tab**

3. **Choose data source:**
   - **Option A**: Use recently fetched news (check the checkbox)
   - **Option B**: Select a CSV file from dropdown

4. **Set analysis limits:**
   - Use slider to choose how many articles to analyze (5-100)
   - This helps control costs!

5. **Click "🚀 Run GPT-3.5 Analysis" button**

6. **Watch the progress:**
   - Progress bar shows analysis progress
   - Status text shows which article is being analyzed
   - Typically takes 1-2 seconds per article

7. **View Results:**
   - Results table with sentiment labels
   - Sentiment distribution chart
   - Statistics (Total, Positive, Negative, Neutral)
   - Download results as CSV

### Complete Workflow Example:

```
Step 1: Fetch News
  → Go to "Fetch News" tab
  → Search: "Technology"
  → Fetch 20 articles
  → ✅ Success!

Step 2: Analyze with GPT
  → Go to "Analyze with GPT" tab
  → Check "Use recently fetched news"
  → Set max to 20 articles
  → Click "Run GPT-3.5 Analysis"
  → ✅ Analysis complete!

Step 3: View Results
  → Go to "View Data" tab
  → Select "news_with_gpt_sentiment.csv" (if saved)
  → See sentiment distribution chart
```

---

## 💡 Tips & Tricks

### For Fetching News:

- ✅ **Use specific queries** for better results (e.g., "AI technology" instead of just "AI")
- ✅ **Start with fewer articles** (10-20) to test
- ✅ **Different countries** give different perspectives
- ✅ **Try different languages** for international news

### For GPT Analysis:

- ✅ **Start small** (5-10 articles) to test
- ✅ **Cost control**: Each article costs ~$0.001-0.005
- ✅ **Use fetched news** for real-time analysis workflow
- ✅ **Download results** to save for later viewing

### Cost Estimates:

- **10 articles**: ~$0.01
- **50 articles**: ~$0.05
- **100 articles**: ~$0.10

---

## 🔄 Complete Workflow

### Scenario: Real-Time News Analysis

1. **Fetch Latest News**
   ```
   Tab: Fetch News
   Query: "India technology"
   Country: in
   Articles: 30
   → Fetch
   ```

2. **Analyze with GPT**
   ```
   Tab: Analyze with GPT
   ✓ Use recently fetched news
   Max articles: 30
   → Run Analysis
   ```

3. **View & Compare**
   ```
   Tab: View Data
   Select: news_with_gpt_sentiment.csv
   → See charts and statistics
   ```

---

## ❓ Common Questions

### Q: Why can't I fetch news?
**A:** Make sure:
- API_KEY is added in Streamlit secrets
- Sidebar shows "✅ Configured"
- You have API quota remaining

### Q: Why is GPT analysis slow?
**A:** 
- Each article takes 1-2 seconds
- For 50 articles, expect 1-2 minutes
- This is normal for API calls

### Q: Can I analyze existing CSV files?
**A:** Yes! In "Analyze with GPT" tab:
- Don't check "Use recently fetched news"
- Select a CSV file from dropdown
- Click "Run Analysis"

### Q: Where are results saved?
**A:**
- Results appear in the dashboard
- Download as CSV to save locally
- Can be viewed in "View Data" tab

### Q: Can I use both features together?
**A:** Absolutely! That's the best workflow:
1. Fetch fresh news
2. Immediately analyze with GPT
3. View results

---

## 🎯 Quick Start Checklist

- [ ] GNews API key added in Streamlit secrets
- [ ] OpenAI API key added in Streamlit secrets
- [ ] Dashboard shows "✅ Configured" for both APIs
- [ ] Tested fetching 10 articles
- [ ] Tested GPT analysis on 5 articles
- [ ] Downloaded results

---

## 🚀 Next Steps

1. **Try fetching news** on different topics
2. **Run GPT analysis** on fetched articles
3. **Compare results** with VADER and BERT
4. **Download and save** your favorite analyses
5. **Share your insights!**

---

**You're all set! Start fetching and analyzing! 🎉**

