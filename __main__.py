import os
import openai
import requests
from io import BytesIO
from PIL import Image
from autogen import AssistantAgent, UserProxyAgent
from moviepy import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
from .master_agent_wf import master_agent_workflow

# Run the workflow (LOCAL EXECUTION)
if __name__ == "__main__":
    prompt = "A futuristic AI city where robots and humans coexist in harmony."
    master_workflow(prompt)
