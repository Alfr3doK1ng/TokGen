from moviepy.editor import *
from openai import OpenAI
import json

client = OpenAI()

def extract_audio_from_video(video_path, output_audio_path):
    # Load the video file
    video = VideoFileClip(video_path)
    
    # Extract the audio from the video
    audio = video.audio
    
    # Write the audio to a file
    audio.write_audiofile(output_audio_path)
    
    # Close the video file
    video.close()
    
    print(f"Audio extracted and saved to {output_audio_path}")

def transcribe_audio(audio_path, n_repeat: int = 2):
    # Transcribe the audio using an audio model
    transcripts = []
    with open(audio_path, "rb") as audio_file:
        for _ in range(n_repeat):
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file, 
                response_format="text"
            )
            print("Raw Transcription:", transcript)
            transcripts.append(transcript)
    
    # clean the transcription
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You will help to detech audio transcriptions."},
            {"role": "user", "content": "You will see the transcription of an audio file. The audio may be a person actual speaking"
            " or some non-speaking audio, such as background music or some random noise."
            " You will need to determine if the audio is speaking or non-speaking."
            " If the audio is speaking, you will need to provide a clean transcription of the audio."
            " If the audio is non-speaking, you will need to return an empty string."
            " Return your result as JSON. For example, "
            "{'transcription': 'The quick brown fox jumps over the lazy dog.' # or ''}\n"
            f"To help you decide, we transcribe the same audio for {n_repeat} times."
            " If the transcriptions diverge significantly, the audio is non-speaking."
            " For example, if one transcript is 'Cos they want money-money-money! Money-Money-Money!'"
            " and another transcript is '... ... have a good day.', this is a non-speaking audio and you should return an empty string\n\n"
            "Here are the raw audio transcriptions: \n" + '\n'.join(transcripts)
            },
        ],
        response_format={ "type": "json_object" }
    )
    result = json.loads(response.choices[0].message.content)
    print("Cleaned Transcription:", result)

    # rules to check
    max_len = max([len(t) for t in transcripts])
    min_len = min([len(t) for t in transcripts])
    if max_len >= 2*min_len:
        result["transcription"] = ""
    return result["transcription"]
