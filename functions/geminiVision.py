import random
import dotenv
import io
import os
import PIL.Image
import google.generativeai as genai

dotenv.load_dotenv()
API_KEY = os.getenv("API")

genai.configure(api_key=API_KEY)

# for m in genai.list_models():
#     if "generateContent" in m.supported_generation_methods:
#         print(m.name)

model_pro_vision = genai.GenerativeModel("gemini-pro-vision", safety_settings=None)


def geminiVision(prompt, img):
    print(type(img))
    img = io.BytesIO(img)
    img = PIL.Image.open(img)
    buffer = []
    try:
        response = model_pro_vision.generate_content([prompt, img], stream=True)
        print(response)
        for chunk in response:
            for part in chunk.parts:
                buffer.append(part.text)
        print(buffer)
    except Exception as e:
        print(e)
    return "".join(buffer)
