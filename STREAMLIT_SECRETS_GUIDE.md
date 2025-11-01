# 🔐 Streamlit Cloud Secrets Guide

## 📋 What Are Streamlit Secrets?

Streamlit Secrets allow you to securely store API keys and credentials in your Streamlit Cloud deployment without exposing them in your code. They're similar to environment variables but managed through Streamlit Cloud's interface.

---

## 🚀 How to Add API Secrets in Streamlit Cloud

### Step-by-Step Instructions

#### Step 1: Access Your App Settings

1. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)
2. **Sign in** with your GitHub account
3. **Click on your deployed app** (the News Sentiment Analysis dashboard)
4. **Click the "⋮" (three dots) menu** in the top right
5. **Select "Settings"** from the dropdown menu

#### Step 2: Navigate to Secrets

1. In the Settings page, look for the **"Secrets"** section in the left sidebar
2. Click on **"Secrets"**

#### Step 3: Add Your API Keys

You'll see a text editor where you can add secrets in TOML (Tom's Obvious, Minimal Language) format.

**Add both API keys like this:**

```toml
API_KEY = "your_gnews_api_key_here"
OPENAI_API_KEY = "your_openai_api_key_here"
```

**Example with actual format:**

```toml
API_KEY = "9d56ceaf8083ebfd0a9b90848596fe3b"
OPENAI_API_KEY = "sk-proj-abc123xyz789..."
```

#### Step 4: Save the Secrets

1. Click **"Save"** at the bottom of the editor
2. Your app will automatically restart with the new secrets

#### Step 5: Verify Secrets Are Loaded

After saving, check that your app reloads successfully. The secrets are now available in your code!

---

## 🔍 What Happens When You Add Secrets?

### Before Adding Secrets:
- ❌ **GNews API**: Cannot fetch fresh news articles
- ❌ **OpenAI API**: Cannot perform GPT-3.5 sentiment analysis
- ✅ **Dashboard**: Still works with existing CSV files
- ✅ **VADER & BERT**: Work fine (don't need API keys)

### After Adding Secrets:

#### 1. **GNews API Key (API_KEY)**

**What becomes possible:**
- ✅ **Fetch fresh news** directly from GNews API
- ✅ **Real-time updates** - get latest news articles on demand
- ✅ **Custom queries** - search for specific topics, countries, languages
- ✅ **No CSV files needed** - can fetch directly in the dashboard

**How it works:**
```python
# Your code can now access:
api_key = st.secrets["API_KEY"]  # or os.getenv("API_KEY") with load_dotenv()
# Then use it to fetch news from GNews API
```

**What users can do:**
- Click "Fetch Fresh News" button in dashboard
- Enter search query (e.g., "technology", "sports")
- Select country and language
- Get instant results without pre-loaded CSV files

---

#### 2. **OpenAI API Key (OPENAI_API_KEY)**

**What becomes possible:**
- ✅ **GPT-3.5 sentiment analysis** - most accurate, context-aware analysis
- ✅ **Run GPT analysis on demand** - analyze articles directly in dashboard
- ✅ **Compare all 3 methods** - VADER vs BERT vs GPT-3.5
- ✅ **Better accuracy** - especially for complex, ambiguous text

**How it works:**
```python
# Your code can now access:
openai_key = st.secrets["OPENAI_API_KEY"]
# Initialize OpenAI client and analyze sentiment
```

**What users can do:**
- Select "GPT-3.5 Analysis" option in dashboard
- Analyze individual articles or batches
- Get more nuanced sentiment results
- Compare results across all three methods

---

## 💡 Enhanced Features Available

### New Dashboard Features:

1. **"Fetch News" Button**
   - Appears when `API_KEY` is available
   - Allows real-time news fetching
   - Customizable search queries

2. **"Run GPT Analysis" Button**
   - Appears when `OPENAI_API_KEY` is available
   - Analyzes selected articles with GPT-3.5
   - Shows progress bar during analysis

3. **Side-by-Side Comparison**
   - Compare VADER, BERT, and GPT-3.5 results
   - See accuracy differences
   - Make informed decisions

---

## 📝 Code Changes Needed

To use secrets in your Streamlit app, update your code like this:

### Old Way (Local .env file):
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
```

### New Way (Streamlit Secrets - Works Both Locally and Cloud):
```python
import streamlit as st
import os

# Try Streamlit secrets first, then fall back to environment variable
if 'API_KEY' in st.secrets:
    api_key = st.secrets["API_KEY"]
else:
    api_key = os.getenv("API_KEY")
```

### Best Practice (Works Everywhere):
```python
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()  # For local development

# Priority: Streamlit secrets > Environment variable
def get_secret(key):
    if hasattr(st, 'secrets') and key in st.secrets:
        return st.secrets[key]
    return os.getenv(key)

api_key = get_secret("API_KEY")
openai_key = get_secret("OPENAI_API_KEY")
```

---

## 🔒 Security Notes

### ✅ What Streamlit Secrets Provide:

1. **Encrypted Storage**: Secrets are encrypted at rest
2. **Not in Git**: Secrets are never committed to your repository
3. **Per-App**: Each Streamlit app has its own secrets
4. **Access Control**: Only you (app owner) can view/edit secrets
5. **Audit Log**: Changes to secrets are logged

### ⚠️ Important Security Tips:

1. **Never commit secrets** to GitHub (use `.gitignore` for `.env` files)
2. **Don't print secrets** in your code (remove debug print statements)
3. **Use different keys** for development and production if possible
4. **Rotate keys** periodically for security
5. **Don't share secrets** via email or chat

---

## 🧪 Testing Your Secrets

### Test 1: Check if Secrets Load

Add this to your dashboard temporarily:

```python
import streamlit as st

# Test secrets (remove after testing!)
if 'API_KEY' in st.secrets:
    st.success("✅ GNews API Key loaded!")
else:
    st.warning("⚠️ GNews API Key not found")

if 'OPENAI_API_KEY' in st.secrets:
    st.success("✅ OpenAI API Key loaded!")
else:
    st.warning("⚠️ OpenAI API Key not found")
```

### Test 2: Test GNews API

Try fetching news:
```python
if 'API_KEY' in st.secrets:
    # Test API call
    response = requests.get("https://gnews.io/api/v4/search", 
                          params={"token": st.secrets["API_KEY"], 
                                  "q": "test", "max": 1})
    if response.status_code == 200:
        st.success("✅ GNews API working!")
```

### Test 3: Test OpenAI API

Try a simple GPT call:
```python
if 'OPENAI_API_KEY' in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    # Test with minimal call
    st.success("✅ OpenAI client initialized!")
```

---

## 📊 Before vs After Comparison

| Feature | Without Secrets | With Secrets |
|---------|----------------|--------------|
| **View CSV Data** | ✅ Works | ✅ Works |
| **VADER Analysis** | ✅ Works | ✅ Works |
| **BERT Analysis** | ✅ Works | ✅ Works |
| **Fetch Fresh News** | ❌ No | ✅ Yes |
| **GPT-3.5 Analysis** | ❌ No | ✅ Yes |
| **Real-time Updates** | ❌ No | ✅ Yes |
| **Custom Queries** | ❌ No | ✅ Yes |
| **Compare All Methods** | ⚠️ Partial | ✅ Full |

---

## 🎯 Recommended Workflow

1. **Start Simple**: Deploy dashboard without secrets first
2. **Verify It Works**: Make sure basic features function
3. **Add GNews Key**: Enable news fetching functionality
4. **Test Fetching**: Verify you can get fresh news
5. **Add OpenAI Key**: Enable GPT-3.5 analysis
6. **Test GPT**: Run a few analyses
7. **Monitor Usage**: Check API usage/costs

---

## 💰 Cost Considerations

### GNews API:
- **Free Tier**: Limited requests per day
- **Paid Tier**: More requests available
- **Cost**: Usually free for low-volume use

### OpenAI API:
- **GPT-3.5-turbo**: ~$0.002 per 1K tokens
- **Example**: 100 articles ≈ $0.10-0.50 (depends on text length)
- **Tip**: Use max_tokens=10 to minimize costs

---

## ❓ Troubleshooting

### Problem: "Secret not found"

**Solution:**
- Check secret name matches exactly (case-sensitive)
- Ensure you clicked "Save" in Streamlit Cloud
- Wait for app to restart (usually automatic)

### Problem: "API call failed"

**Solutions:**
- Verify API key is correct (no extra spaces)
- Check API key hasn't expired
- Verify you have API credits/quota remaining
- Check network connectivity

### Problem: "Secrets work locally but not in cloud"

**Solution:**
- Local uses `.env` file
- Cloud uses Streamlit Secrets
- Make sure both are configured

---

## ✅ Summary

**Adding secrets enables:**
1. Real-time news fetching from GNews
2. GPT-3.5 sentiment analysis
3. Full comparison of all three methods
4. Interactive, on-demand analysis
5. More dynamic and powerful dashboard

**Your dashboard becomes:**
- More interactive
- More accurate (with GPT-3.5)
- More real-time (fresh data)
- More comprehensive (all methods)

---

**Ready to enhance your app! Add those secrets and unlock the full potential! 🚀**

