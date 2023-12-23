import dotenv
import os
from io import BytesIO
import requests

dotenv.load_dotenv()

CUSTOMER_KEY = os.getenv("CUSTOMER_KEY")
secret_phrase = ""  # leave secret phrase empty, if not needed


def kokoshotRequest(url, cachelimit, delay, zoom, dimension, device):
    # to save screenshot as an image check the api guide for more details
    url = f"""https://api.screenshotmachine.com/?key={CUSTOMER_KEY}&url={url}&cacheLimit={cachelimit}&delay={delay}&zoom={zoom}&device={device}&dimension={dimension}"""
    # &click=flex--item6%20s-btn%20s-btn__filled%20js-accept-cookies%20js-consent-banner-hide
    # &cookies=SOCS=CAESEwgDEgk0ODE3Nzk3MjQaAmVuIAEaBgiA_LyaBg
    response = requests.get(url)

    image_data = BytesIO(response.content)
    # image = image_data.read()
    # Return the BytesIO object
    return image_data


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
