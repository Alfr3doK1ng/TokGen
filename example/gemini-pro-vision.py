import os
from dotenv import load_dotenv
load_dotenv()

from pydantic import BaseModel
from PIL import Image
import matplotlib.pyplot as plt

import google.generativeai as genai

from llama_index.multi_modal_llms import GeminiMultiModal
from llama_index.program import MultiModalLLMCompletionProgram
from llama_index.output_parsers import PydanticOutputParser

from llama_index import SimpleDirectoryReader


GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
print(GOOGLE_API_KEY)


# Not really needed
genai.configure(
    api_key=GOOGLE_API_KEY,
    client_options={"api_endpoint": "generativelanguage.googleapis.com"},
)

for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)


class TickTokVids(BaseModel):

    """Data model for a Ticktok image"""
    title: str
    overlay: str
    clothing: str
    summary: str

# google_image_url = "./storage/ticktok4.jpg"
# print(google_image_url)
# image = Image.open(google_image_url).convert("RGB")
#
# plt.figure(figsize=(16, 5))
# plt.imshow(image)
# plt.show()

# prompt_template_str = """\
#     can you summarize what is in the image\
#     and return the answer with json format \
# """

prompt = "Here are some key frames of a video. " \
    "The key frams are sampled sequentially and uniformly from the video. " \
    "Please describe the content of the video."

promt2 = "Take in all this data and put it together as one"

def pydantic_gemini(
    model_name, output_class, image_documents, prompt
):
    gemini_llm = GeminiMultiModal(
        api_key=GOOGLE_API_KEY, model_name=model_name
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


google_image_documents = SimpleDirectoryReader(
    "./storage/ugc"
).load_data()

results = []

# Loading in the entire folder - which would the entire video
#pydantic_gemini("models/gemini-pro-vision", GoogleRestaurant, google_image_documents, prompt)

for img_doc in google_image_documents:
    pydantic_response = pydantic_gemini(
        "models/gemini-pro-vision",
        TickTokVids,
        [img_doc],
        prompt,
    )
    for r in pydantic_response:
        print(r)
    results.append(pydantic_response)

results_str = ', '.join(str(obj) for obj in results)

print(results_str)


# Combining part
from llama_index.llms import Gemini
#
resp = Gemini().complete(results_str+"Above are the contents of a video broken down into equal time frames. I want the story of the video.")
print(resp)

