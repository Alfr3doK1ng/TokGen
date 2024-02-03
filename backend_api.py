from dataclasses import dataclass
from typing import List
import time
from dotenv import load_dotenv
import os
from apify_client import ApifyClient

load_dotenv()
api_key = os.getenv('API_KEY')

@dataclass
class VideoStorage:
    # attributes such as path, title, description, views, etc. Should
    # be easily obtained from the tiktok API results
    path: str
    url: str
    view: int
    digg_count: int
    collect_count: int
    comment_count: int
    digg_count: int
    download_count: int
    forward_count: int
    lose_comment_count: int
    lose_count: int
    play_count: int
    share_count: int
    whatsapp_share_count: int


@dataclass
class VideoPresentation:
    # simple attributes
    path: str
    # attributes from the parse, such as captions, transciptions, storyline summary, etc
    caption: str

@dataclass
class QueryResponse:
    response: str
    related_videos: List[str]


def search_tiktok_trending_videos(q: str) -> List[VideoStorage]:
    """Use tiktok API to search for trending videos related to the query."""
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
    vo = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        item = item['aweme_info']
        path = ""  # Assuming you have a specific logic to define the path
        url = item["video"]["play_addr"]["url_list"][0]
        view_count = item["statistics"]["play_count"]
        digg_count = item["statistics"]["digg_count"]
        collect_count = item["statistics"]["collect_count"]
        comment_count = item["statistics"]["comment_count"]
        download_count = item["statistics"]["download_count"]
        forward_count = item["statistics"]["forward_count"]
        lose_comment_count = item["statistics"].get("lose_comment_count", 0)  # Using get() to avoid KeyError
        lose_count = item["statistics"].get("lose_count", 0)  # Assuming default 0 if not present
        play_count = item["statistics"]["play_count"]
        share_count = item["statistics"]["share_count"]
        whatsapp_share_count = item["statistics"].get("whatsapp_share_count", 0)  # Assuming default 0 if not present

        # Creating a VideoStorage object with extracted values
        vo.append(VideoStorage(path, url, view_count, digg_count, collect_count, comment_count, download_count, forward_count, lose_comment_count, lose_count, play_count, share_count, whatsapp_share_count))
    return vo

def store_video_representation(video: VideoStorage) -> None:
    """Parse video representation and store it in the database."""
    pass

def retrieve_videos_by_similarity(q: str) -> List[VideoPresentation]:
    """Retrieve videos from the database that are similar to the user's query."""
    return []

def generate_response_for_retrieval(q: str, videos: List[VideoPresentation]) -> str:
    """Generate a response to the user's query based on the retrieved videos."""
    time.sleep(10)
    return "Here are the trends."

def query(q: str) -> QueryResponse:
    """Retrieve related trending videos and generate a response to the user's query."""
    # search for the hottest videos related to the query on tiktok
    videos = search_tiktok_trending_videos(q)
    # parse and store the videos as objects in the database
    for video in videos:
        store_video_representation(video)
    # retrieve more fine-grained results on the trending videos
    retrived_videos = retrieve_videos_by_similarity(q)
    # generate a response to the user's query
    response = generate_response_for_retrieval(q, retrived_videos)
    return QueryResponse(response, [v.path for v in retrived_videos])