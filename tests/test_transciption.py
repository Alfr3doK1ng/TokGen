import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import backend_api as api
from utils.audio import transcribe_audio
import unittest


class TestAudioTranscription(unittest.TestCase):

    def setUp(self):
        self.video = api.VideoStorage(
            path='../video.mp4', 
            url='https://v16m.tiktokcdn-eu.com/2414f5353034880596302769008b6503/65bf173f/video/tos/useast2a/tos-useast2a-pve-0068/07a431ea7ff64fa9a7e7743fc5425a60/?a=1233&ch=0&cr=13&dr=0&lr=all&cd=0%7C0%7C0%7C&cv=1&br=1200&bt=600&bti=NTY6QGo0QHM6OjZANDQuYCMucCMxNDNg&cs=0&ds=6&ft=XsF-iqR0mK3PD124C1MR3wUpegtAMeF~O5&mime_type=video_mp4&qs=0&rc=ODk1Zjk4ZTNlZWQ8aWY6aEBpM3Zyb215bmU1MzMzaTczM0BfYmMwLTU1NV4xNC4zYC9jYSMtZmkzZjVham5gLS1jMTZzcw%3D%3D&l=20240203224842385650555AAC040FDB7D&btag=e00088000', 
            view=48891127, 
            digg_count=1524431, 
            collect_count=38828, 
            comment_count=32106, 
            download_count=98288, 
            forward_count=0, 
            lose_comment_count=0, 
            lose_count=0, 
            play_count=48891127, 
            share_count=104030, 
            whatsapp_share_count=73440)

    def test_transcribe(self):
        r = api.parse_video_transcription(self.video)
        print(r)

    def test_speaking_transcibe(self):
        clean_audio_file = '../audio.mp3'
        r = transcribe_audio(clean_audio_file)
        print(r)

if __name__ == '__main__':
    unittest.main()