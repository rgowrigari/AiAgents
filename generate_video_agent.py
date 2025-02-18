import os
import openai
import requests
from io import BytesIO
from PIL import Image
from autogen import AssistantAgent, UserProxyAgent
from moviepy import ImageClip, concatenate_videoclips, TextClip, CompositeVideoClip, AudioFileClip


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
