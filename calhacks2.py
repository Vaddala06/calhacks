"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config

import cv2
import time
import os
from .gemini import *
import chromadb
from .db_test import *


#Create a reflex page
# Create a Reflex component for the video stream
def video_stream_component():
    return rx.box(
        rx.heading("OpenCV Video Stream", size="lg"),
        # Use an img tag to display the video stream from the Flask server
        rx.image(src="http://0.0.0.0.8000/video_feed", width="640px", height="480px"),
        padding="10px",
    )

def start_stream():
    # Start the video stream
    # Initialize the video capture from the default camera (or use video file path)
    cap = cv2.VideoCapture(0)  # Use '0' for default webcam, or a file path

    # Read the first frame and preprocess it
    ret, frame1 = cap.read()
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)      # Blur to reduce noise

    SENSITIVITY = 20000  # Adjust this value as needed
    THRESHOLD_VALUE = 50  # Adjust this value as needed


    # Get the default frame rate of the video (FPS)
    fps = int(cap.get(cv2.CAP_PROP_FPS))  # Frames per second of the camera
    if fps == 0:  # Handle cases where FPS is not detected correctly
        fps = 30  # Default to 30 FPS if unable to fetch


    start_time = time.time()

    time_block = 0


    while cap.isOpened():

        # Read the next frame
        ret, frame2 = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale and blur
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

        # Compute the absolute difference between the current frame and the previous one
        diff = cv2.absdiff(gray1, gray2)

        # Threshold the difference to make motion areas more distinct
        thresh = cv2.threshold(diff, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)  # Fill in gaps in the detected motion

        # Find contours (i.e., the outlines of the moving objects)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False

        for contour in contours:
            # Filter out small movements (contours with small area)
            if cv2.contourArea(contour) < SENSITIVITY:  # Adjust this threshold as needed
                continue

            # Get the bounding box for the contour
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw the rectangle

            motion_detected = True

        # Display the result
        cv2.imshow("Motion Detection", frame2)

        #print("Time value", time.time() - start_time)
        if motion_detected and time.time() > time_block:
            print("Motion detected! Recording a 5-second video...")

            video_filename = os.path.join('./assets/output_folder', f"motion_clip_{int(time.time())}.mp4")

            # Define the codec and create VideoWriter object for MP4
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 files
            out = cv2.VideoWriter(video_filename, fourcc, fps, (frame2.shape[1], frame2.shape[0]))

            # Record for 5 seconds (5 * fps frames)
            start_time = time.time()
            while time.time() - start_time < 5:
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)  # Write the frame to the video file
                cv2.imshow("Recording", frame)  # Display the recording process (optional)

                # Break the loop if 'q' is pressed during recording
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Release the VideoWriter object after recording is complete
            out.release()
            print(f"Recording finished and saved as {video_filename}.")


            message = generate_alert_message(video_filename)
            print("message =", message)

            add_motion_video(message, video_filename, int(time.time()))


            #time.sleep(1)

            time_block = time.time() + 5


        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Update the previous frame to the current frame
        gray1 = gray2

    # Release the video capture and close windows
    cap.release()
    cv2.destroyAllWindows()

# State to manage alerts and video actions
class IterState(rx.State):
    alerts = []
    all_documents = []
    all_metadatas = []
    all_ids = []

    # Function to fetch alerts from ChromaDB and update the state
    def fetch_alerts(self):
        alerts_data = get_all_alerts()  # Assuming this function interacts with ChromaDB
        self.alerts = alerts_data['documents']  # Update the state with documents from ChromaDB
        self.all_metadatas = alerts_data['metadatas']
        self.all_ids = alerts_data['ids']


class State(rx.State):

    def start_stream(self):
        start_stream()

# Create the Reflex app
def index():
    return rx.center(
        rx.text("Video Stream!", font_size="20px", color="blue"),
        video_stream_component(),
        rx.button("Start!", on_click=State.start_stream()),
        rx.foreach(IterState.alerts, lambda alert: rx.text(alert)),
        height="100vh",
    )

    

app = rx.App()

# Add the route to the Reflex app
app.add_page(index)

