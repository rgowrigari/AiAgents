### ** Background Music Creator Agent**
def generate_music():
    """Creates AI-composed background music and saves it."""
    response = openai.audio.speech.create(model="music-gen", voice="alloy", input="Generate cinematic background music for the story.")
    music_path = os.path.join(output_folder, "background_music.mp3")

    with open(music_path, "wb") as f:
        f.write(response.read())
    
    return music_path
