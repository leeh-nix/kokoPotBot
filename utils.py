import json
import requests

API_BASE_URL = "https://api.popcat.xyz"


def encoding(message):
    url = f"{API_BASE_URL}/encode?text={message}"

    response = requests.get(url)

    if response.status_code == 200:
        response = json.loads(response.text)
        return response["binary"]
    else:
        raise Exception("Unexpected response from API")


def decoding(message):
    url = f"{API_BASE_URL}/decode?binary={message}"

    response = requests.get(url)

    if response.status_code == 200:
        response = json.loads(response.text)
        return response["text"]
    else:
        raise Exception("Unexpected response from API")


def doublestruckAPI(message):
    url = f"{API_BASE_URL}/doublestruck?text={message}"

    response = requests.get(url)
    if response.status_code == 200:
        response = json.loads(response.text)
        return response["text"]
    else:
        raise Exception("Unexpected response from API")
