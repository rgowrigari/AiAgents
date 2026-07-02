import os
import openai
import requests
from io import BytesIO
from PIL import Image
from autogen import AssistantAgent, UserProxyAgent
from moviepy import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip
from .generate_story_agent import generate_story
from .generate_image_agent import generate_image
from .generate_music_agent import generate_music
from .generate_tts_agent import generate_tts_narration
from .generate_video_agent import create_video

# --- MASTER WORKFLOW ---
def master_agent_workflow(prompt):
    
    # --- MASTER AGENT SETUP (LOCAL EXECUTION, NO DOCKER) ---
    
    # Configure AI Agents (TO RUN LOCALLY)
    story_agent = AssistantAgent("StoryAgent", llm_config={"model": "gpt-4o-mini"}, code_execution_config=code_execution_config)
    image_agent = AssistantAgent("ImageAgent", llm_config={"model": "gpt-4o-mini"}, code_execution_config=code_execution_config)
    tts_agent = AssistantAgent("TTSAgent", llm_config={"model": "gpt-4o-mini"}, code_execution_config=code_execution_config)
    music_agent = AssistantAgent("MusicAgent", llm_config={"model": "gpt-4o-mini"}, code_execution_config=code_execution_config)
    video_agent = AssistantAgent("VideoAgent", llm_config={"model": "gpt-4o-mini"}, code_execution_config=code_execution_config)
    
    
    # For local execution when you dont have docker images
    code_execution_config = {"use_docker": False}  
    master_agent = UserProxyAgent("MasterAgent", code_execution_config=code_execution_config)

    
    """Master agent orchestrates all other agents (running locally, NO Docker)."""
    print("Master Agent: Generating story...")
    story_path = generate_story(prompt)
    print("Master Agent: Story Generated...")

    print("Generating images...")
    with open(story_path, "r") as f:
        story_text = f.read()

    story_parts = story_text.split('. ')
    image_paths = [generate_image(scene) for scene in story_parts]
    print("Images Generated...")

    print("Generating text to speech narration...")
    narration_path = generate_tts_narration(story_path)
    print("TTS completed...")

    print("Generating background music...")
    music_path = generate_music()
    print("Background music generated...")

    print("Creating Final video...")
    video_path = create_video(image_paths, story_parts, narration_path, music_path)

    print(f"Video generated successfully! File saved at: {video_path}")

