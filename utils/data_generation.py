import cv2
import os
import tempfile

import os
from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel

from llama_index.multi_modal_llms import GeminiMultiModal
from llama_index.program import MultiModalLLMCompletionProgram
from llama_index.output_parsers import PydanticOutputParser

from llama_index import SimpleDirectoryReader
from llama_index.llms import Gemini
import streamlit as st



results = []

prompt = "Here are some key frames of a video. " \
    "The key frams are sampled sequentially and uniformly from the video. " \
    "Please describe the content of the video."

def capture_featured_frames(video_path, num_frames=5):
    # Open the video file
    print(video_path)
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get the total number of frames and the FPS (Frames Per Second) in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Calculate the interval between each featured frame
    interval = total_frames // num_frames
    
    # Loop through the specified number of frames
    parsed_results = []
    for i in range(num_frames):
        # Calculate the frame number to capture
        frame_number = int(i * interval)
        
        # Set the current frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        # Read the frame
        ret, frame = cap.read()
        
        if not ret:
            print(f"Error: Could not read frame at position {frame_number}.")
            continue
        
        # Save the frame to a file

        with tempfile.TemporaryDirectory() as temp_dir:
            file = os.path.join(temp_dir, "frame.jpg")
            cv2.imwrite(file, frame)
            print(f"Featured frame {i+1} saved to {file}")
            results = loading_fetching(output_folder=temp_dir)
            parsed_results.append(results)
    
    # Release the video capture object
    cap.release()
    return parsed_results

GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]

class TickTokVids(BaseModel):
    title: str
    overlay: str
    clothing: str
    summary: str

def pydantic_gemini(
    model_name, output_class, image_documents, prompt
):
    gemini_llm = GeminiMultiModal(
        api_key= GOOGLE_API_KEY, model_name=model_name
    )

    llm_program = MultiModalLLMCompletionProgram.from_defaults(
        output_parser=PydanticOutputParser(output_class),
        image_documents=image_documents,
        prompt_template_str=prompt,
        multi_modal_llm=gemini_llm,
        verbose=True,
    )


    response = llm_program()
    print(response)
    return response

def loading_fetching(output_folder):

    results = []
    google_image_documents = SimpleDirectoryReader(
        output_folder
    ).load_data()

    for img_doc in google_image_documents:
        try:
            pydantic_response = pydantic_gemini(
                "models/gemini-pro-vision",
                TickTokVids,
                [img_doc],
                prompt,
            )
            for r in pydantic_response:
                print(r)
            results.append(pydantic_response)
        except Exception as e:
            print(f"Error: {e}")
            results.append("Error: Unable to process the image.")
        
    return results

def summarize(parsed_results):
    results_str = ', '.join(str(obj) for obj in parsed_results)
    resp = Gemini().complete(results_str+"Above are the contents of a video broken down into equal time frames. I want the story of the video.")
    st.write()    
    results.clear()
    return resp.text

