import os
import openai
import requests
from io import BytesIO
from PIL import Image
from autogen import AssistantAgent, UserProxyAgent
from moviepy import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip

### ** Story Agent**
def generate_story(prompt):
    """Creates a structured story and saves it."""
    structured_prompt = f"""
    Write a structured story with:
    - A clear beginning, middle, and end.
    - 1 distinct sections with title.
    - A strong narrative flow.
    - Create a story under 100 words. 
    - Do not use any language which may not be good for kids.
    - Make sure the story is written as per AI ethical framework (No foul language, etc.).
   
    Prompt: {prompt}

    """
    
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", 
                   "content": "You are an AI story generator."},
                  {"role": "user", "content": structured_prompt}]
    )
    
    story = response.choices[0].message.content

    # Save the story
    story_path = os.path.join(output_folder, "story.txt")
    with open(story_path, "w") as f:
        f.write(story)
    
    return story_path
