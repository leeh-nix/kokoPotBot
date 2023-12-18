import requests
import dotenv
import os
import pathlib
import textwrap

import google.generativeai as genai


dotenv.load_dotenv()
API_KEY = os.getenv("API")


# curl -H 'Content-Type: application/json' -d '{ "prompt": { "text": "Write a story about a magic backpack"} }' \
# "https://generativelanguage.googleapis.com/v1beta3/models/text-bison-001:generateText?key=YOUR_API_KEY"


genai.configure(api_key=API_KEY)

# for m in genai.list_models():
#     if "generateContent" in m.supported_generation_methods:
#         print(m.name)


model_pro = genai.GenerativeModel(
    model_name="gemini-pro",
    safety_settings=None,
)
# model_pro_vision = genai.GenerativeModel("gemini-pro-vision")


def sendResponse(text):
    # response = model_pro.generate_content("What is the meaning of life?")
    response = model_pro.generate_content(text)
    return response.text


# print(sendResponse("Write a story about a magic backpack"))
