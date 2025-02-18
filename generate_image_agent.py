import os
import openai
import requests
from io import BytesIO
from PIL import Image
from autogen import AssistantAgent, UserProxyAgent
from moviepy import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip

### ** Image Generation Agent**
def generate_image(description):
    """Generates an AI-created image using OpenAI's DALL-E."""
    
    response = openai.images.generate(model= 'dall-e-2', 
                                      prompt=description, 
                                      size='256x256', 
                                      quality= 'standard', 
                                      style='natural', 
                                      n=1)
    image_url = response.data[0].url
    img_response = requests.get(image_url)
    img = Image.open(BytesIO(img_response.content))

    img_path = os.path.join(output_folder, f"scene_{description.replace(' ', '_')}.png")
    img.save(img_path)
    return img_path
