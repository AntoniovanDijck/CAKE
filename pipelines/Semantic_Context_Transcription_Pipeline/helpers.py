"""
Antonio van Dijck
studentnumber: 12717673
Email: antonio.van.dijck@student.uva.nl

Helper functions to download audio and video data from YouTube links.
"""

import os
from pydub import AudioSegment
import subprocess

def download_and_convert_to_wav(youtube_url, output_wav_path):

    print(f"Downloading audio from {youtube_url}...")
    audio_file = "temp_audio.mp4"  # Temporary file
    os.system(f'yt-dlp -f "worstaudio" -o "{audio_file}" "{youtube_url}"')

    print("Converting to WAV format...")
    audio = AudioSegment.from_file(audio_file)
    audio.export(output_wav_path, format="wav")

    os.remove(audio_file)
    print(f"Conversion complete! WAV file saved to: {output_wav_path}")

def download_video(youtube_url, output_video_path):

    try:
        print(f"Downloading video from {youtube_url} (high quality video only)...")
        output_template = "temp_video.mp4"

        command = [
            "yt-dlp", "-f", "worstvideo[ext=mp4]", "-o", output_template, youtube_url
        ]

        subprocess.run(command, check=True)

        if os.path.exists(output_template):
            os.rename(output_template, output_video_path)
            print(f"Video saved as '{output_video_path}'.")
        else:
            raise FileNotFoundError("Failed to download video as MP4.")

    except subprocess.CalledProcessError as e:
        print(f"Error downloading video: {e}")

def process_links_from_file(input_link):

    os.makedirs("pipelines/Semantic_Context_Transcription_Pipeline/data/audio_data", exist_ok=True)
    os.makedirs("pipelines/Semantic_Context_Transcription_Pipeline/data/video_data", exist_ok=True)

    
    link = input_link
    if link:
        output_wav_path = os.path.join("pipelines/Semantic_Context_Transcription_Pipeline/data/audio_data", f"output_audio_1.wav")
        output_video_path = os.path.join("pipelines/Semantic_Context_Transcription_Pipeline/data/video_data", f"input_video_1.mp4")
        download_and_convert_to_wav(link, output_wav_path)
        download_video(link, output_video_path)

# input_file = "pipelines/Semantic_Context_Transcription_Pipeline/data/youtube_links.txt"

# # Download and convert to wav and download video
# process_links_from_file(input_file)
# print("All audio and video files downloaded and converted!")