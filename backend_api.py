from dataclasses import dataclass
from typing import List
import time

@dataclass
class QueryResponse:
    response: str
    related_videos: List[str]

def query(q: str) -> QueryResponse:
    time.sleep(20)
    return QueryResponse("this is a response", [])