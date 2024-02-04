import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend_api import *

output = parse_video_summary(video=VideoStorage(
    path="/Users/mckenzie/Downloads/temp/video.mp4",
    url = "placeholder",
    view = "placeholder",
    # digg_count = "placeholder",
    collect_count = "placeholder",
    comment_count = "placeholder",
    digg_count = "placeholder",
    download_count = "placeholder",
    forward_count = "placeholder",
    lose_comment_count = "placeholder",
    lose_count = "placeholder",
    play_count = "placeholder",
    share_count = "placeholder",
    whatsapp_share_count = "placeholder"
    ), transcription="random")

print(output)