import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend_api import *

videos = search_tiktok_trending_videos("viral")
print(videos)