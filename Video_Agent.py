import os
import openai
import requests
from io import BytesIO
from PIL import Image
from autogen import AssistantAgent, UserProxyAgent
from moviepy import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip

os.environ['OPENAI_API_KEY'] = "your-api-key"
os.environ["PYDEVD_WARN_SLOW_RESOLVE_TIMEOUT"] = "5"
os.environ["PYDEVD_WARN_EVALUATION_TIMEOUT"] = "10"

# Create a folder to store generated content
output_folder = "AI_Agent_Content"
os.makedirs(output_folder, exist_ok=True)


# --- AI AGENTS ---
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


### ** Background Music Creator Agent**
def generate_music():
    """Creates AI-composed background music and saves it."""
    response = openai.audio.speech.create(model="music-gen", voice="alloy", input="Generate cinematic background music for the story.")
    music_path = os.path.join(output_folder, "background_music.mp3")

    with open(music_path, "wb") as f:
        f.write(response.read())
    
    return music_path


### ** Video Agent **
# def create_video(image_paths, story_segments, narration_path, music_path): -->Music path disabled
def create_video(image_paths, story_segments, narration_path):
    """Creates a video using AI-generated images, narration, and music."""
    clips = []
    for idx, img_path in enumerate(image_paths):
        img_clip = ImageClip(img_path, duration = 5)
        """ Below code is disabled due to Mac OS error """
        # text_clip = TextClip(story_segments[idx],color='white', font = 'Arial', fontsize = 24, duration = 5)
        # text_clip = text_clip.set_position(('center', 0.85), relative=True)
        # combined = CompositeVideoClip([img_clip, text_clip])
        # clips.append(combined)
        img_clip = ImageClip(img_path, duration = 5)
        clips.append(img_clip)

    video = concatenate_videoclips(clips, method="compose")

    # Add narration
    narration = AudioFileClip(narration_path)
    
    # video = video.set_audio(narration)
    video = CompositeVideoClip([video]).with_audio(narration)

    # Add background music --> Commented as this required Meta Music Gen or 
    # if music_path:
    #     music = AudioFileClip(music_path).volumex(0.5)
    #     final_audio = music.set_duration(video.duration).audio_fadeout(2)
    #     video = video.set_audio(final_audio)

    video_path = os.path.join(output_folder, "generated_video.mp4")
    video.write_videofile(video_path, fps=24)
    
    return video_path

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

# --- MASTER WORKFLOW ---
def master_workflow(prompt):
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

# Run the workflow (LOCAL EXECUTION)
if __name__ == "__main__":
    prompt = "A futuristic AI city where robots and humans coexist in harmony."
    master_workflow(prompt)
