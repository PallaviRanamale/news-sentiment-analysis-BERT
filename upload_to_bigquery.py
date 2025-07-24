from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
# from dotenv import load_dotenv
import os


# 🔐 Load environment variables
# load_dotenv()

# ✅ Get project ID securely
# project_id = os.getenv("GCP_PROJECT_ID")  # Update your .env to use this key
project_id = "<YOUR_PROJECT_ID>"
# 🔐 Load credentials from JSON file path stored in .env
# credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
credentials_path = "<YOUR_CREDENTIALS_PATH>"
if not credentials_path or not os.path.exists(credentials_path):
    raise FileNotFoundError("Google service account key not found. Please set GOOGLE_APPLICATION_CREDENTIALS in your .env file.")

# 🔑 Load GCP service account credentials
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# ✅ Dataset and Table names
dataset_id = 'news_dataset_asia'
table_id = 'news_with_sentiment'

# 📄 Load CSV file
df = pd.read_csv("news_with_bert_sentiment.csv")
print(f"📄 Total rows in CSV: {len(df)}")

# 🚀 Initialize BigQuery client
client = bigquery.Client(credentials=credentials, project=project_id)

# 🔗 Dataset reference
dataset_ref = bigquery.DatasetReference(project_id, dataset_id)

# 📁 Create dataset if not exists
try:
    client.get_dataset(dataset_ref)
    print("✅ Dataset exists.")
except Exception as e:
    print("⚠️ Dataset not found. Creating new dataset...")
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "asia-south1"
    client.create_dataset(dataset)
    print("✅ Dataset created successfully.")

# ⬆️ Upload DataFrame to BigQuery table
table_ref = dataset_ref.table(table_id)
job = client.load_table_from_dataframe(df, table_ref, location="asia-south1")
job.result()  # Wait for the job to complete

print("✅ Data uploaded successfully to BigQuery!")
