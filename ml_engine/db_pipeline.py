import pandas as pd
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
MONGODB_DATABASE = os.getenv('MONGODB_DATABASE', 'phishing_Database')


def setup_database():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DATABASE]
    collection = db['dataset']

    print("Reading dataset...")
    # Get absolute path for data
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, 'data', 'phishingData.csv')
    df = pd.read_csv(data_path)
    records = df.to_dict(orient='records')

    collection.delete_many({})
    collection.insert_many(records)
    print(f"Inserted {collection.count_documents({})} records.")

    pipeline1 = [
        {"$group": {"_id": "$SSLfinal_State", "value": {"$sum": 1}}},
        {"$out": "ssl_state_counts"}
    ]
    collection.aggregate(pipeline1)
    print("Aggregation Job 1 complete: ssl_state_counts created.")

    pipeline2 = [
        {"$group": {"_id": "$Result", "value": {"$sum": "$web_traffic"}}},
        {"$out": "traffic_phishing_distribution"}
    ]
    collection.aggregate(pipeline2)
    print("Aggregation Job 2 complete: traffic_phishing_distribution created.")


if __name__ == "__main__":
    setup_database()