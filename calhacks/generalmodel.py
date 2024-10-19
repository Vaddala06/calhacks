import os
import time
import google.generativeai as genai

GEMINI_API_KEY = 'AIzaSyBjWprVJ6UMCQXHE4GnO7OapYn1r_0ejak' 
genai.configure(api_key=GEMINI_API_KEY)

def upload_to_gemini(path, mime_type=None):
    """Uploads the given file to Gemini."""
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file

def wait_for_files_active(files):
    """Waits for the given files to be active."""
    print("Waiting for file processing...")
    for name in (file.name for file in files):
        file = genai.get_file(name)
        while file.state.name == "PROCESSING":
            print(".", end="", flush=True)
            time.sleep(10)
            file = genai.get_file(name)
        if file.state.name != "ACTIVE":
            raise Exception(f"File {file.name} failed to process")
    print("...all files ready")
    print()

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-002",
    generation_config=generation_config,
)

# Upload your video file
files = [
    upload_to_gemini(r"C:\Users\vadda\OneDrive\Desktop\calhacks\calhacks.mp4", mime_type="video/mp4"),
]

# Wait for the files to be processed
wait_for_files_active(files)

# Start a chat session with the uploaded video file as context
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                files[0],
            ],
        },
    ]
)

# Now you can ask questions interactively
while True:
    user_input = input("Ask a question about the video (or type 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break
    
    # Modify the input to encourage more conversational responses
    prompt = f"{user_input}. Provide a detailed and descriptive explanation in natural language."

    
    # Send the modified prompt to the model
    response = chat_session.send_message(prompt)
    
    # Output the model's response in text form
    print(response.text)
