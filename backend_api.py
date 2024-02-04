import json
from typing import List
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
from openai import OpenAI
import streamlit as st


load_dotenv()
api_key = os.getenv('API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')
print(openai_api_key)
client = OpenAI(api_key=openai_api_key)


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
        "limit": 1,
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
    st.write(f'Video downloaded and processed successfully.')    
    return vo

def parse_video_transcription(video: VideoStorage) -> str:
    """Parse the video's transcription using an audio model."""
    with tempfile.TemporaryDirectory() as temp_dir:
        audio_file = os.path.join(temp_dir, "audio.mp3")
        # convert to audio file
        extract_audio_from_video(video.path, audio_file)
        # transcribe the audio
        transcription = transcribe_audio(audio_file)
        st.write(f"**Researching on** [{video.title}]({video.url})")
    return transcription

def parse_video_summary(video: VideoStorage, transcription: str) -> VideoPresentation:
    """Parse the video's keyframes and other attributes to generate a summary.
    
    This function will set the transcription attribute as well.
    """
    print(video.path)
    parsed_results = capture_featured_frames(video.path, num_frames=5)

    try:
        summary = summarize(parsed_results)
    except RuntimeError as e:
        print(f"A RuntimeError occurred")
        summary = "Error: Unable to process the video summary due to safety concerns."

    return VideoPresentation(summary=summary, transcript=transcription, path=video.path,\
                             title = video.title, url = video.url)

def parse_video_representation(video: VideoStorage) -> None:
    """Parse video representation."""
    transcription = parse_video_transcription(video)
    video_presentation = parse_video_summary(video, transcription)
    return video_presentation

def retrieve_videos_by_similarity(q: str, videos: List[VideoPresentation], top_k: int) -> List[VideoPresentation]:
    """Retrieve videos from the database that are similar to the user's query."""
    # import pdb; pdb.set_trace()
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
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant. You will help to generate new ideas for the content creators."},
                {"role": "user", "content": input_text}
            ],
            model="gpt-3.5-turbo-0125")
        generated_text = response.choices[0].message.content.strip()
        return generated_text
    except Exception as e:
        print(f"An error occurred while calling the OpenAI API: {e}")
        return "We encountered an error while generating a response to your query."
    
def generate_qa_response_for_retrieval(q: str, videos: List[VideoPresentation]) -> str:
    """Generate a answer to the user's query based on the retrieved videos."""
    input_text = f"Imagine you are a consultant, you are giving the tiktok \
        content creaters ideas about trending tiktok videos. Here are some current trending\
        video summaries. The content creator has this question: {q}.\
        Based on these summary and the need from content creator, answer their question about trends. Details are welcomed."
        
    input_text += "\n".join([f"- {video.summary}" for video in videos])
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant. You will help to prepare new ideas for the content creators."},
                {"role": "user", "content": input_text}
            ],
            model="gpt-3.5-turbo-0125")
        generated_text = response.choices[0].message.content.strip()
        return generated_text
    except Exception as e:
        print(f"An error occurred while calling the OpenAI API: {e}")
        return "We encountered an error while generating a response to your query."

def check_query_type(q: str) -> str:
    """Check the type of query."""
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant. You will help to prepare new ideas for the content creators."},
                {"role": "user", "content": f"Please help me to analyze the user intend of the following query. The query is: {q}" \
                    "Is this an request to generate a script for a video or a question about a video? " \
                    "If it is an request to generate a script, return 'script' for intend. "
                    "Return the result in JSON format: {'intend': 'script' or 'question'}."}
            ],
            model="gpt-3.5-turbo-0125",
            response_format={ "type": "json_object" })
        data = json.loads(response.choices[0].message.content)
        return data['intend']
    except Exception as e:
        print(f"An error occurred while calling the OpenAI API: {e}")
        return "We encountered an error while generating a response to your query."

def query(q: str, parsed_videos: List[VideoPresentation] = None, progress_bar = None) -> QueryResponse:
    """Retrieve related trending videos and generate a response to the user's query."""
    # search for the hottest videos related to the query on tiktok
    videos = search_tiktok_trending_videos(q)
    if progress_bar:
        progress_bar.progress(25)
    # parse and store the videos as objects in the database
    if not parsed_videos:
        video_reprs = []
        for video in videos:
            try:
                video_reprs.append(parse_video_representation(video))
            except Exception as e:
                print(f"Failed to parse video: {video}")
                print(e)
        parsed_videos = video_reprs
    if progress_bar:
        progress_bar.progress(50)
    # retrieve more fine-grained results on the trending videos
    retrived_videos = retrieve_videos_by_similarity(q, parsed_videos, top_k=10)
    if progress_bar:
        progress_bar.progress(75)
    # generate a response to the user's query
    query_type = check_query_type(q)
    if query_type == "script":
        response = generate_response_for_retrieval(q, parsed_videos)
    else:
        response = generate_qa_response_for_retrieval(q, parsed_videos)
    if progress_bar:
        progress_bar.progress(100)
    return QueryResponse(
        response, 
        [v.path for v in retrived_videos], 
        [(v.title, v.url) for v in retrived_videos],
        parsed_videos)
