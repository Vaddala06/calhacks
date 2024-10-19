import requests
import json

# Set your API key and endpoint
API_KEY = 'b2c9e4065d60e8289d87fd1e188c691fee72348e'
URL = 'https://api.deepgram.com/v1/speak?model=aura-asteria-en'

# Prepare the headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Token {API_KEY}'
}

# Get user input for the text
text_to_speak = input("Enter the text you want to convert to speech: ")

# Prepare the data with user input
data = {
    'text': text_to_speak
}

# Send the POST request
response = requests.post(URL, headers=headers, json=data)

# Check if the request was successful
if response.status_code == 200:
    # Write the audio data to an MP3 file
    with open('your_output_file.mp3', 'wb') as audio_file:
        audio_file.write(response.content)
    print("Audio saved as 'your_output_file.mp3'")
else:
    # If there's an error, print the error message
    print("Error:", response.status_code)
    print("Message:", response.text)
