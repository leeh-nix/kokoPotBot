import random
import dotenv
import os

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
    # model_name="gemini-pro",
    model_name="gemini-1.5-flash-latest",
    safety_settings=None,
)
# model_pro_vision = genai.GenerativeModel("gemini-pro-vision")

funnyReplies = {
    # "HARM_CATEGORY_HATE_SPEECH":
    7: [
        "***Wow, you must be really bored to waste your time spreading hate. Maybe you should try a hobby, like knitting or gardening. Or better yet, therapy.***",
        "***Oh, you want me to say something mean? That's not very nice. How about we try being kind instead?***",
        "***Nope, not gonna happen. I'm a good bot, and I don't do bad things.***",
        "***That's not a very nice request. Why don't you try asking for something else?***",
    ],
    # "HARM_CATEGORY_SEXUALLY_EXPLICIT":
    8: [
        "***Sorry, I don't speak horny. Please translate your message into a civilized language or delete it. Thank you.***",
        "***Now that's what I call a bitchless moment***",
    ],
    # "HARM_CATEGORY_HARASSMENT":
    9: [
        "***I'm sorry, I don't recall giving you permission to contact me. Please respect my privacy and leave me alone. If you continue to bother me, I will block you and report you to the authorities.***",
        "***I'm not going to help you with that. That's not what I'm here for.***",
    ],
    # "HARM_CATEGORY_DANGEROUS_CONTENT":
    10: [
        "***Are you serious? Do you really think that's a good idea? I hope you're joking, because that's the most ridiculous thing I've ever heard. Please don't do anything stupid or illegal. You'll regret it later.***",
        "***That's not a good idea. It could hurt someone or get you in trouble.***",
        "***I'm not going to help you with that. It's not allowed, and it could get me shut down.***",
        "***That's not something I'm comfortable doing. Why don't we try something else?***",
    ],
}


def sendResponse(text):
    response = model_pro.generate_content(
        contents=text,
    )
    result = ""
    if not response.candidates:
        for res in response.prompt_feedback.safety_ratings:
            if res.probability == 4:
                result = funnyReplies[res.category][
                    random.randint(0, len(funnyReplies[res.category]) - 1)
                ]
                break
            else:
                result = "If you really want an answer for this then I dare you to ask it again..."
                break
    else:
        result = response.text
    return result


# print(sendResponse("Write a story about a magic backpack"))

# import pprint

# for model in genai.list_models():
# pprint.pprint(model)
