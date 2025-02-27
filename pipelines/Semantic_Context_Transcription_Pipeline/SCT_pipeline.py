from .helpers import *
from .transcribe import *
from .full_text import *
from .chunker import *

def Semantic_Context_Transcription_Pipeline(input_link = "https://www.youtube.com/watch?v=g4lHxSAyf7M"):

    #check if video_data folder is empty
    if not os.listdir("pipelines/Semantic_Context_Transcription_Pipeline/data/video_data"):
        print("No video data found. Downloading video data...")

        # Download and convert to wav and download video
        process_links_from_file(input_link)

        # Process all WAV files in the folder
        for filename in os.listdir("pipelines/Semantic_Context_Transcription_Pipeline/data/audio_data"):
            if filename.endswith(".wav"):
                audio_path = os.path.join("pipelines/Semantic_Context_Transcription_Pipeline/data/audio_data", filename)
                transcribe(audio_path)
        print("All audio and video files downloaded and converted!")
    else:
        #process_links_from_file(input_link)

        print("Video data found. Skipping download...")

        # Process all WAV files in the folder
        for filename in os.listdir("pipelines/Semantic_Context_Transcription_Pipeline/data/audio_data"):
            if filename.endswith(".wav"):
                audio_path = os.path.join("pipelines/Semantic_Context_Transcription_Pipeline/data/audio_data", filename)
                transcribe(audio_path)

    print("All audio files transcribed!")

    # Convert transcriptions to full text
    convert_to_full_text()

    text_folder = 'pipelines/Semantic_Context_Transcription_Pipeline/data/transcription_data'
    json_folder = 'pipelines/Semantic_Context_Transcription_Pipeline/data/transcription_data'
    output_folder = 'pipelines/Semantic_Context_Transcription_Pipeline/result'
    process_text_and_json(text_folder, json_folder, output_folder)

# result op: pipelines/Semantic_Context_Transcription_Pipeline/data/transcription_data/output_audio_1_chunks.json
