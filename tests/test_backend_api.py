import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import backend_api as api

class TestBackendAPI(unittest.TestCase):

    def testQueryAPI(self):
        q = "trends in llamaindex and education and funs"
        resp = api.query(q)
        self.assertTrue(len(resp.related_videos) > 0)
        self.assertTrue(len(resp.response))
        print(resp.response)

    def testSecondQuery(self):
        q = "trends for basketball videos"
        resp = api.query(q)
        self.assertTrue(len(resp.related_videos) > 0)
        self.assertTrue(len(resp.response))
        # second query
        q = "write a script for basketball videos"
        resp = api.query(q, resp.parsed_videos)
        self.assertTrue(len(resp.related_videos) > 0)
        self.assertTrue(len(resp.response))
        print("second", resp.response)


if __name__ == '__main__':
    unittest.main()