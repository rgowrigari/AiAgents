import os
import openai
import requests
from io import BytesIO
from PIL import Image
from autogen import AssistantAgent, UserProxyAgent
from moviepy import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip

### ** Text-to-Speech Agent**
def generate_tts_narration(story_path):
    """Generates speech narration from a saved story."""
    with open(story_path, "r") as f:
        story_text = f.read()
    
    response = openai.audio.speech.create(model="tts-1", voice="alloy", input=story_text)
    narration_path = os.path.join(output_folder, "narration.mp3")

    with open(narration_path, "wb") as f:
        f.write(response.read())
    
    return narration_path

