from dataclasses import dataclass
from typing import List
import time
from dotenv import load_dotenv
import os
from apify_client import ApifyClient
import tempfile
from utils.audio import extract_audio_from_video, transcribe_audio
import requests
from pathlib import Path
from utils.data_generation import capture_featured_frames, summarize
from utils.retrieval_storage import LlamaIndexQdrantStorage
from typedefs import VideoStorage, VideoPresentation, QueryResponse
import openai

load_dotenv()
api_key = os.getenv('API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')


def download_video(url, title, save_path):
    """Download a video from a URL using the video's caption as the filename."""
    # Sanitize the title to use as a filename
    filename = title.replace(" ", "_").replace('&', '_') + ".mp4"
    full_path = Path(save_path) / filename

    # Ensure the save_path directory exists
    full_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(full_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
        print(f"Video downloaded successfully and saved to {full_path}")
    else:
        print(f"Failed to download video. Status code: {response.status_code}")
    return full_path

def search_tiktok_trending_videos(q: str) -> List[VideoStorage]:
    """Use tiktok API to search for trending videos related to the query."""
        # Access the API key
    client = ApifyClient(api_key)
    run_input = {
        "type": "SEARCH",
        "keyword": q,
        "sortType": 0,
        "publishTime": "ALL_TIME",
        "limit": 2,
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
        title = item["desc"]
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
        try:
            path = str(download_video(url, title, "./videos"))
            print(path)
            vo.append(VideoStorage(title, path, url, view_count, digg_count, collect_count, comment_count, download_count, forward_count, lose_comment_count, lose_count, play_count, share_count, whatsapp_share_count))
        except:
            continue    
    return vo

def parse_video_transcription(video: VideoStorage) -> str:
    """Parse the video's transcription using an audio model."""
    with tempfile.TemporaryDirectory() as temp_dir:
        audio_file = os.path.join(temp_dir, "audio.mp3")
        # convert to audio file
        extract_audio_from_video(video.path, audio_file)
        # transcribe the audio
        transcription = transcribe_audio(audio_file)
    return transcription

def parse_video_summary(video: VideoStorage, transcription: str) -> VideoPresentation:
    """Parse the video's keyframes and other attributes to generate a summary.
    
    This function will set the transcription attribute as well.
    """
    print(video.path)
    capture_featured_frames(video.path, num_frames=5)
    summary = summarize()

    return VideoPresentation(summary=summary, transcript=transcription, path=video.path)

def parse_video_representation(video: VideoStorage) -> None:
    """Parse video representation."""
    transcription = parse_video_transcription(video)
    video_presentation = parse_video_summary(video, transcription)
    return video_presentation

def retrieve_videos_by_similarity(q: str, videos: List[VideoPresentation], top_k: int) -> List[VideoPresentation]:
    """Retrieve videos from the database that are similar to the user's query."""
    store = LlamaIndexQdrantStorage("data_store", videos)
    retrieved_videos = store.retrieve(q, top_k=top_k)
    return retrieved_videos

def generate_response_for_retrieval(q: str, videos: List[VideoPresentation]) -> str:
    """Generate a response to the user's query based on the retrieved videos."""
    # Join the summaries of all videos to form the input text for the API
    input_text = f"Imagine you are a consultant, you are giving the tiktok \
        content creaters ideas about their next videos. Here are some current trending\
        video summaries. The content creator is interested in {q}.\
        Based on these summary and the need from content creator, generate a new idea for the content\
        creater. be specific about what to do in each frame; what to wear; provide a\
        transcript for them. Be as specific as possible."
        
    input_text += "\n".join([f"- {video.summary}" for video in videos])
    
    openai.api_key = openai_api_key
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=input_text,
            temperature=0.7,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        generated_text = response.choices[0].text.strip()
        return generated_text
    except Exception as e:
        print(f"An error occurred while calling the OpenAI API: {e}")
        return "We encountered an error while generating a response to your query."

# Example usage (Remember to replace 'your_openai_api_key' with your actual OpenAI API key)
# videos = [VideoPresentation(path="video1.mp4", transcript="Transcript 1", summary="Summary 1"), VideoPresentation(path="video2.mp4", transcript="Transcript 2", summary="Summary 2")]
# response = generate_response_for_retrieval("Query about videos", videos, "your_openai_api_key")
# print(response)

def query(q: str) -> QueryResponse:
    """Retrieve related trending videos and generate a response to the user's query."""
    # search for the hottest videos related to the query on tiktok
    videos = search_tiktok_trending_videos(q)
    # parse and store the videos as objects in the database
    video_reprs = [parse_video_representation(video) for video in videos]
    # retrieve more fine-grained results on the trending videos
    retrived_videos = retrieve_videos_by_similarity(q, video_reprs)
    # generate a response to the user's query
    response = generate_response_for_retrieval(q, retrived_videos)
    return QueryResponse(response, [v.path for v in retrived_videos])