import json
import requests
import aiohttp

API_BASE_URL = "https://api.popcat.xyz"

async def make_http_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.read()
                return data
            else:
                raise Exception("Unexpected response from API")

def encoding(message):
    url = f"{API_BASE_URL}/encode?text={message}"
    
    response = requests.get(url)
    
    if response.status_code == 200: 
        response = json.loads(response.text)
        return response["binary"]
    else: raise Exception('Unexpected response from API')

def decoding(message):
    url = f"{API_BASE_URL}/decode?binary={message}"    
    response = requests.get(url)
    
    if response.status_code == 200: 
        response = json.loads(response.text)
        return response["text"]
    else: raise Exception('Unexpected response from API')

def doublestruckAPI(message):
    url = f"{API_BASE_URL}/doublestruck?text={message}"
    response = requests.get(url)
    if response.status_code == 200: 
            response = json.loads(response.text)
            return response["text"]    
    else: raise Exception('Unexpected response from API')
    
async def clownApiRequest(image_url):
    url = f"{API_BASE_URL}/clown?image={image_url}"
    return await make_http_request(url)

async def adApiRequest(message):
    url = f"{API_BASE_URL}/ad?image={message}"
    return await make_http_request(url)

async def uncoverApiRequest(message):
    url = f"{API_BASE_URL}/uncover?image={message}"
    return await make_http_request(url)

async def jailApiRequest(message):
    url = f"{API_BASE_URL}/jail?image={message}"
    
    return await make_http_request(url)
