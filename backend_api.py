from dataclasses import dataclass
from typing import List
import time

@dataclass
class VideoStorage:
    # attributes such as path, title, description, views, etc. Should
    # be easily obtained from the tiktok API results
    path: str

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
    return []

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