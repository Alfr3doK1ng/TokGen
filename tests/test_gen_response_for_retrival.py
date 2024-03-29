import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import backend_api as api
import unittest

class TestGen(unittest.TestCase):

    def setUp(self):
        self.videos = [
            api.VideoPresentation(
                path='videos/follow_my_ig_and_snap_:_diamant.blazi_i_follow_back__#diamantblazi_#seckoff_#bball_#basketball_#dunk_#shoot_#duo_#basketball_#challenge_#trend_#florida_#usa_#viral_#fyp_.mp4', transcript="It's a remix and I'm coming with that bow, bow, bow Pretty bitch, I'm trying to hit her with that bow, bow, bow Can't catch me slipping, I'mma up it when I bow, bow, bow Them bitches dance, I throw them bands and make them dance, nigga", summary="Two young men in black t-shirts and shorts, with multi-colored sneakers, spin basketballs on their fingers. They are in a gym, and they are both dribbling the ball and moving around the court. They are playing basketball, and they are both having fun. They are both good at basketball, and they are both enjoying the game. They are both sweating, and they are both tired, but they are both still having fun. They are both friends, and they are both enjoying each other's company. They are both happy, and they are both enjoying the game of basketball."), api.VideoPresentation(path='videos/follow_my_ig_and_snap_:_diamant.blazi_i_follow_back__#diamantblazi_#seckoff_#bball_#basketball_#dunk_#shoot_#duo_#basketball_#challenge_#trend_#florida_#usa_#viral_#fyp_.mp4', transcript="It's a remix and I'm coming with that bow, bow, bow Pretty bitch, I'm trying to hit her with that bow, bow, bow Can't catch me slipping, I'mma up it when I bow, bow, bow Them bitches dance, I throw them bands and make them dance, nigga", summary='Two young men in black t-shirts and shorts spin basketballs on their fingers. They are standing in a gym, and the sound of other people playing basketball can be heard in the background.\n\nThe two men start dribbling the basketballs and moving around the court. They are both skilled players, and they are able to make some impressive moves. They dribble the ball between their legs, behind their backs, and even through their legs.\n\nThe two men continue to play basketball for a while, and they are both having a lot of fun. They are laughing and joking with each other, and they are clearly enjoying the game.\n\nEventually, the two men get tired and they decide to take a break. They sit down on the bench and talk for a while. They talk about their favorite basketball players, their favorite teams, and their dreams of playing in the NBA.\n\nAfter a while, the two men get up and start playing basketball again. They play for a few more hours, and they have a great time. When they are finally finished, they are both exhausted, but they are also very happy. They have had a great day playing basketball, and they have made some new friends.'), 
            api.VideoPresentation(path='videos/follow_my_ig_and_snap_:_diamant.blazi_i_follow_back__#diamantblazi_#seckoff_#bball_#basketball_#dunk_#shoot_#duo_#basketball_#challenge_#trend_#florida_#usa_#viral_#fyp_.mp4', transcript="It's a remix and I'm coming with that bow, bow, bow Pretty bitch, I'm trying to hit her with that bow, bow, bow Can't catch me slipping, I'mma up it when I bow, bow, bow Them bitches dance, I throw them bands and make them dance, nigga", summary='Two young men in black t-shirts and shorts spin basketballs on their fingers. They are standing in a gym, and the sound of other people playing basketball can be heard in the background.\n\nThe two men start dribbling the basketballs and moving around the court. They are both skilled players, and they are able to make some impressive moves. They dribble the ball between their legs, behind their backs, and even through their legs.\n\nThe two men continue to play basketball for a while, and they are both having a lot of fun. They are laughing and joking with each other, and they are clearly enjoying the game.\n\nEventually, the two men get tired and they decide to take a break. They sit down on the bench and talk for a while. They talk about their favorite basketball players, their favorite teams, and their dreams of playing in the NBA.\n\nAfter a while, the two men get up and start playing basketball again. They play for a few more hours, and they have a great time. When they are finally finished, they are both exhausted, but they are also very happy. They have had a great day playing basketball, and they have made some new friends.')]

    def test_gen_response_for_retrieval(self):
        q = 'trend in basketball'
        intent = api.check_query_type(q)
        self.assertEqual(intent, "question")
        resp = api.generate_qa_response_for_retrieval(q, self.videos)
        print(resp)

    def test_gen_script(self):
        q = 'write a script for basketball videos'
        intent = api.check_query_type(q)
        self.assertEqual(intent, "script")
        resp = api.generate_response_for_retrieval(q, self.videos)
        print(resp)


if __name__ == '__main__':
    unittest.main()