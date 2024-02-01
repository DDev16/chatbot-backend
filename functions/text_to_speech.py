import requests
from decouple import config

ELEVEN_LABS_API_KEY = config('ELEVEN_LABS_API_KEY')

# Eleven Labs - Text to Speech
# Converts text to speech
def convert_text_to_speech(message):
    # Define Data 
    body = {
        "text": message,
        "voice_settings": {
        "stability": 0,
        "similarity_boost": 0,  # Corrected typo here
        }
    }
    
    # Define voice
    voice_rachel = "21m00Tcm4TlvDq8ikWAM"

    # Constructing Headers and endpoint
    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json",
        "accept": "audio/mpeg"
    }
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

    # Send the request
    try:
        response = requests.post(endpoint, json=body, headers=headers)
    except Exception as e:
        print("Error during API request:", e)
        return

    # Inspect and Log Response
    
    print("API Response Code:", response.status_code)
    if response.status_code != 200:
        print("API Response Content:", response.text)

    # Handle Response
    if response.status_code == 200:
        return response.content
    else:
        return
    