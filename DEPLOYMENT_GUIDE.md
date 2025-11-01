# 🚀 Deployment Guide

This guide will help you deploy the News Sentiment Analysis project to Streamlit Cloud.

## 📋 Prerequisites

- GitHub account
- Streamlit Cloud account (free)
- Project pushed to GitHub

## 🌐 Deploy to Streamlit Cloud

### Step 1: Push to GitHub

If you haven't already, push your project:

```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)

2. **Sign in**: Click "Sign in" and authenticate with your GitHub account

3. **Create New App**:
   - Click "New app"
   - Select your repository: `PallaviRanamale/news-sentiment-analysis-BERT`
   - Select branch: `main`
   - Main file path: `dashboard_local.py`
   - App URL: Choose a custom subdomain (optional)

4. **Configure App Settings**:
   - Python version: 3.8 or higher
   - Streamlit version: 1.47.0

5. **Add Secrets** (Optional, for API features):
   - Click on your app → Settings → Secrets
   - Add secrets in TOML format:
     ```toml
     API_KEY = "your_gnews_api_key"
     OPENAI_API_KEY = "your_openai_api_key"
     ```

6. **Deploy**: Click "Deploy" and wait for the build to complete

### Step 3: Access Your Live App

Once deployed, your app will be available at:
```
https://your-app-name.streamlit.app
```

## 🔧 Troubleshooting

### Build Failures

- **Missing dependencies**: Check `requirements.txt` is complete
- **Python version**: Ensure Python 3.8+ is selected
- **Import errors**: Check all imports are in requirements.txt

### Runtime Errors

- **Missing files**: Ensure CSV files are committed or app handles missing files gracefully
- **API errors**: Check secrets are configured correctly
- **Memory issues**: Streamlit Cloud has memory limits, consider optimizing

### Common Issues

**Issue**: "ModuleNotFoundError"  
**Solution**: Add missing package to `requirements.txt`

**Issue**: "FileNotFoundError: CSV files"  
**Solution**: The `dashboard_local.py` handles this gracefully, or commit sample CSV files

**Issue**: "API Key errors"  
**Solution**: Add secrets in Streamlit Cloud settings

## 🔄 Updating Your App

Every time you push to the `main` branch, Streamlit Cloud will automatically:
1. Detect the change
2. Rebuild your app
3. Deploy the new version

Manual redeploy:
1. Go to your app on Streamlit Cloud
2. Click "⋮" menu
3. Select "Reboot app"

## 📊 Using the Deployed App

### Features Available:
- ✅ View news articles from CSV files
- ✅ Search and filter articles
- ✅ View sentiment distribution charts
- ✅ Statistics and metrics

### Limitations:
- ⚠️ CSV files need to be committed or uploaded
- ⚠️ Real-time news fetching requires API keys (add as secrets)
- ⚠️ BigQuery connection requires GCP credentials (add as secrets)

## 🎯 Best Practices

1. **Keep `.env` out of Git**: Use Streamlit Secrets instead
2. **Handle Missing Data**: Your app gracefully handles missing CSV files
3. **Optimize Loading**: Large CSV files may take time to load
4. **Monitor Usage**: Streamlit Cloud has usage limits on free tier

## 🔗 Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Deployment Best Practices](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app)

## 📝 Next Steps

After deployment:

1. **Update README.md**: Replace the demo link with your actual Streamlit Cloud URL
2. **Share Your App**: Add the link to your GitHub repository description
3. **Test Thoroughly**: Ensure all features work in the cloud environment
4. **Monitor Performance**: Check app performance and optimize if needed

---

**Your app is now live! 🎉**

