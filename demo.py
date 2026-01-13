from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file, make sure to set your API key there
load_dotenv()

# Create a Gemini AI client
client = genai.Client(api_key=os.getenv("GOOGLE_AI_STUDIO_API_KEY"))

# Define the video path
video_path = "demo.mp4"
print(f"Uploading video from path: {video_path}x`")

# Upload the video
video_file = client.files.upload(file=video_path)

# Wait for the upload and processing on cloud to complete
while video_file.state == "PROCESSING":
    time.sleep(2)
    video_file = client.files.get(name=video_file.name)
print(f"Video file uploaded and processed: {video_file.name}, state: {video_file.state}")

# Define the prompt for video understanding
prompt = "Describe the content of the video in detail."

# Configure generation parameters (optional)
# Different model has different capabilities and may require different configurations
# for more details check here: https://ai.google.dev/gemini-api/docs/video-understanding
# This configuration requests the response in JSON format, if you want plain text, you can delete this configuration
config=types.GenerateContentConfig(
    response_mime_type="application/json"
)

# Generate content based on the uploaded video and prompt
response = client.models.generate_content(
    model="gemini-3-pro-preview", # model can also be gemini-2.5-flash
    contents=[video_file, prompt],
    config=config
)

# Print the generated response
print("Generated Response:\n", response.text)

# Check the usage details
usage = response.usage_metadata
print("Input Tokens:", usage.prompt_token_count)
print("Output Tokens:", usage.candidates_token_count)
print("Thinking Tokens:", usage.thoughts_token_count)
print("Total Tokens:", usage.total_token_count)