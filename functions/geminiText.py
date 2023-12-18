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


# api_endpoint = f"https://generativelanguage.googleapis.com/v1beta3/models/text-bison-001:generateText?key={API_KEY}"


# def sendRequest(text):
#     data = {"prompt": {"text": f"{text}"}}

#     response = requests.post(
#         url=api_endpoint,
#         data=data,
#         headers={
#             "Content-Type": "application/json",
#         },
#     )

#     try:
#         if response.status_code == 200:
#             data = response.json()
#             result = data["candidates"][0]["output"]
#         else:
#             print(response.status_code)
#             result = f"oof an error occured `Error: {response.status_code}`"
#             print("Error sending data  lmaoded")
#     except Exception as e:
#         print(e)
#         result = e
#     finally:
#         return result


# Test:
# print(sendRequest("how to be a good programmer"))

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.

genai.configure(api_key=API_KEY)

# for m in genai.list_models():
#     if "generateContent" in m.supported_generation_methods:
#         print(m.name)


model_pro = genai.GenerativeModel("gemini-pro")
model_pro_vision = genai.GenerativeModel("gemini-pro-vision")


def sendResponse(text):
    # response = model_pro.generate_content("What is the meaning of life?")
    response = model_pro.generate_content(text)
    return response.text


# print(response)
# print(send_response("What is the meaning of life?"))
