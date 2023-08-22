import requests
import os
import dotenv

dotenv.load_dotenv()
URL_ENDPOINT = os.getenv("URL_ENDPOINT")
# print(URL_ENDPOINT)


def imageTransform(message, height, width, aspect_ratio):
    if height and aspect_ratio:
        url = f"{URL_ENDPOINT}/tr:h-{height},ar-{aspect_ratio}/{message}"
    elif width and aspect_ratio:
        url = f"{URL_ENDPOINT}/tr:w-{width},ar-{aspect_ratio}/{message}"
    else:
        url = f"{URL_ENDPOINT}/tr:h-{height},w-{width},ar-{aspect_ratio}/{message}"

    response = requests.get(url)

    with open("image.png", "wb") as file:
        file.write(response.content)
    return response.content
