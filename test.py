from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv
import pandas as pd
import os

# 🔐 Load environment variables from .env
load_dotenv()

# ✅ Get values from .env
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
project_id = os.getenv("GCP_PROJECT_ID")
dataset_id = os.getenv("DATASET_ID")
table_id = os.getenv("TABLE_ID")

# 🔍 Check if path is valid
print(f"🔍 Path from .env: {credentials_path}")
print(f"✅ File exists at path? {os.path.exists(credentials_path)}")

if not credentials_path or not os.path.exists(credentials_path):
    raise FileNotFoundError("Google service account key not found. Please check GOOGLE_APPLICATION_CREDENTIALS in your .env file.")

# 🔑 Load service account credentials
credentials = service_account.Credentials.from_service_account_file(credentials_path)

# 📄 Load CSV data
csv_file = "news_with_bert_sentiment.csv"
df = pd.read_csv(csv_file)
print(f"📄 Total rows in CSV: {len(df)}")

# 🚀 Initialize BigQuery client
client = bigquery.Client(credentials=credentials, project=project_id)

# 🔗 Reference dataset
dataset_ref = bigquery.DatasetReference(project_id, dataset_id)

# 📁 Create dataset if not exists
try:
    client.get_dataset(dataset_ref)
    print("✅ Dataset exists.")
except Exception:
    print("⚠️ Dataset not found. Creating it...")
    dataset = bigquery.Dataset(dataset_ref)
    dataset.location = "asia-south1"
    client.create_dataset(dataset)
    print("✅ Dataset created.")

# ⬆️ Upload DataFrame to BigQuery
table_ref = dataset_ref.table(table_id)
job = client.load_table_from_dataframe(df, table_ref, location="asia-south1")
job.result()  # Wait for upload to finish

print("✅ Data uploaded successfully to BigQuery!")
