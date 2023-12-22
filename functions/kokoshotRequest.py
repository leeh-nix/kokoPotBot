import dotenv
import os
from io import BytesIO
import requests

dotenv.load_dotenv()

CUSTOMER_KEY = os.getenv("CUSTOMER_KEY")
secret_phrase = ""  # leave secret phrase empty, if not needed


def kokoshotRequest(url, cachelimit, delay, zoom, dimension, device):
    # to save screenshot as an image check the api guide for more details
    url = f"""https://api.screenshotlayer.com/api/capture?
    key={CUSTOMER_KEY}&
    url={url}&
    cacheLimit={cachelimit}&
    delay={delay}&
    zoom={zoom}&
    dimension={dimension}&
    device={device}"""

    response = requests.get(url)

    if response.status_code == 200:
        # Convert the image data to BytesIO
        image_data = BytesIO(response.content)

        # Return the BytesIO object
        return image_data
    else:
        print("Failed to capture screenshot. Status code:", response.status_code)
    return None


# print(
#     kokoshotRequest(
#         "https://pricehistoryapp.com/product/rk-royal-kludge-rk84-80-rgb-triple-mode-bt5-0-2-4g-wired-hot-swappable-mechanical-keyboard-84-keys-wireless-bluetooth-gaming-keyboard-tactile-brown",
#         3,
#         200,
#         100,
#         "1366x768",
#         "desktop",
#     )
# )
