from dataclasses import dataclass
from typing import List
import time
from dotenv import load_dotenv
import os
from apify_client import ApifyClient

load_dotenv()
api_key = os.getenv('API_KEY')

@dataclass
class QueryResponse:
    response: str
    related_videos: List[str]

def query(q: str) -> QueryResponse:
    return get_video(q)

def get_video(q: str):
    # Access the API key
    client = ApifyClient(api_key)
    run_input = {
        "type": "SEARCH",
        "keyword": q,
        "sortType": 0,
        "publishTime": "ALL_TIME",
        "limit": 20,
        "proxyConfiguration": {
            "useApifyProxy": False
        }
    }
    # Run the Actor and wait for it to finish
    run = client.actor("nCNiU9QG1e0nMwgWj").call(run_input=run_input)
    # Fetch and print Actor results from the run's dataset (if there are any)
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        print(item)
        return item

# # example usage
# query('viral')