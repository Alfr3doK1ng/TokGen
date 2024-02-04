from dataclasses import dataclass
from typing import List

@dataclass
class VideoStorage:
    # attributes such as path, title, description, views, etc. Should
    # be easily obtained from the tiktok API results
    title: str
    path: str
    url: str
    view: int
    # digg_count: int
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
    transcript: str
    summary: str

@dataclass
class QueryResponse:
    response: str
    related_videos: List[str]