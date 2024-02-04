import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import backend_api as api
from utils.audio import transcribe_audio
import unittest
import json


class TestVideoRetrieve(unittest.TestCase):

    def setUp(self):
        self.q = "trends in basketballs"
        self.top_k = 10
        # videos = api.search_tiktok_trending_videos(self.q)
        # self.videos = [api.parse_video_representation(video) for video in videos]
        # self.dump_videos(self.videos, "videos.json")
        self.videos = self.load_videos("tests/videos.json")

    def dump_videos(self, videos, filename):
        vs = []
        for video in videos:
            vs.append(video.__dict__)
        with open(filename, 'w') as f:
            json.dump(vs, f)

    def load_videos(self, filename):
        with open(filename, 'r') as f:
            videos = json.load(f)
        return [api.VideoPresentation(**video) for video in videos]

    def test_retrieve(self):
        results = api.retrieve_videos_by_similarity(self.q, self.videos, top_k=self.top_k)
        self.assertTrue(len(results) == self.top_k)
        print(results)

if __name__ == '__main__':
    unittest.main()