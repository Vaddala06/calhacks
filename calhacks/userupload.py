import os
import time
import google.generativeai as genai
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from tkinter import messagebox, filedialog, scrolledtext

# Gemini API Key
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

def process_file(path):
    """Processes the file after being selected or dropped."""
    try:
        # Upload the file to Gemini
        print(f"Processing file: {path}")
        mime_type = "video/mp4"  # Assuming mp4 for now, adjust if needed
        files = [upload_to_gemini(path, mime_type)]
        wait_for_files_active(files)
        return files
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process the file: {str(e)}")
        return None

# GUI for Drag and Drop and Click to Upload
class DragDropApp(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        self.title("Video Interaction with Gemini Model")
        self.geometry("600x400")

        # Variables to store the file and chat session
        self.files = None
        self.chat_session = None

        # Create a label for instructions
        self.label = tk.Label(self, text="Drag and drop your video file here\n or click to upload", width=40, height=5, bg="lightgray")
        self.label.pack(padx=10, pady=10)

        # Text box to ask questions
        self.input_box = tk.Entry(self, width=60)
        self.input_box.pack(pady=5)

        # Button to submit question
        self.submit_button = tk.Button(self, text="Ask Question", command=self.ask_question)
        self.submit_button.pack(pady=5)

        # Text area to display responses
        self.response_area = scrolledtext.ScrolledText(self, width=70, height=15, wrap=tk.WORD)
        self.response_area.pack(pady=10)

        # Bind the drop event to the window
        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.handle_drop)

        # Bind click event to open file dialog
        self.label.bind("<Button-1>", self.handle_click)

    def handle_drop(self, event):
        """Handles drag-and-drop file."""
        file_path = event.data.strip('{}')
        if file_path and file_path.endswith('.mp4'):  # Check for MP4 files only
            print(f"File dropped: {file_path}")
            self.files = process_file(file_path)  # Process and upload the file
            if self.files:
                self.start_chat_with_gemini()  # Start the chat interaction
        else:
            messagebox.showwarning("Invalid File", "Please drop a valid MP4 video file.")

    def handle_click(self, event):
        """Handles file selection through click."""
        file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            print(f"File selected: {file_path}")
            self.files = process_file(file_path)  # Process and upload the file
            if self.files:
                self.start_chat_with_gemini()  # Start the chat interaction

    def start_chat_with_gemini(self):
        """Starts a chat session with the uploaded video as context."""
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-002",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "application/json",
            },
        )

        self.chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        self.files[0],  # Video file as the context
                    ],
                },
            ]
        )

    def ask_question(self):
        """Handles user input, sends question to the model, and displays the response."""
        if not self.files:
            messagebox.showwarning("No File", "Please upload or drop a video file first.")
            return

        user_input = self.input_box.get()
        if user_input.strip():
            prompt = f"{user_input}. Provide a detailed and descriptive explanation in natural language."

            # Send the prompt to the model
            response = self.chat_session.send_message(prompt)

            # Clear the input box
            self.input_box.delete(0, tk.END)

            # Display the response in the text area
            self.response_area.insert(tk.END, f"User: {user_input}\n")
            self.response_area.insert(tk.END, f"Model: {response.text}\n\n")
            self.response_area.yview(tk.END)  # Scroll to the end

if __name__ == "__main__":
    app = DragDropApp()
    app.mainloop()
