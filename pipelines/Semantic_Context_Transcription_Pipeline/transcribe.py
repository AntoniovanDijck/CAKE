import whisperx
import gc
import torch
import json
import os

def transcribe(audio_file):
    
    # Define paths
    wav_folder = "pipelines/Semantic_Context_Transcription_Pipeline/data/audio_data"
    output_folder = "pipelines/Semantic_Context_Transcription_Pipeline/data/transcription_data"
    # unsupported_folder = "pipelines/Semantic_Context_Transcription_Pipeline/data/unsupported_language"
    model_dir = "pipelines/Semantic_Context_Transcription_Pipeline/data/whisper-models"

    # Ensure output folders exist
    os.makedirs(output_folder, exist_ok=True)
    # os.makedirs(unsupported_folder, exist_ok=True)

    # Check system for compatibility
    if torch.cuda.is_available():
        device = "cuda"
        print("CUDA wordt gebruikt")
        compute_type = "float16"  # change to "int8" if low on GPU mem (may reduce accuracy)
        batch_size = 16  # reduce if low on GPU mem
    elif torch.backends.mps.is_available():
        device = "cpu"
        print("MPS (Apple Silicon) gebruikt")
        compute_type = "int8"
        batch_size = 8
    else:
        print("CPU gebruikt")
        device = "cpu"
        compute_type = "int8"
        batch_size = 4

    if not os.path.exists(model_dir):
        model = whisperx.load_model("medium", device, compute_type=compute_type, download_root=model_dir)
    else:
        model = whisperx.load_model("pipelines/Semantic_Context_Transcription_Pipeline/data/whisper-models/models--Systran--faster-whisper-medium/snapshots/08e178d48790749d25932bbc082711ddcfdfbc4f", device, compute_type=compute_type)

    audio = whisperx.load_audio(audio_file)

    # Perform transcription with automatic language detection
    result = model.transcribe(audio, batch_size=batch_size)
    detected_language = result.get("language", "en")

    # Check if detected language is supported, otherwise move file to unsupported folder
    # if detected_language not in ["en", "fr", "de", "es"]:
    #     print(f"Language detected as {detected_language}, moving to unsupported folder.")
    #     os.rename(audio_file, os.path.join(unsupported_folder, os.path.basename(audio_file)))
    #     return

    print(f"Detected language: {detected_language}")

    # Try alignment, handle missing model error
    try:
        model_a, metadata = whisperx.load_align_model(language_code=detected_language, device=device)
        result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)
        gc.collect()
        torch.cuda.empty_cache()
        del model_a
    except ValueError as e:
        print(f"Skipping alignment due to error: {e}")

    # Save as JSON
    base_filename = os.path.splitext(os.path.basename(audio_file))[0]
    output_json_path = os.path.join(output_folder, f"{base_filename}.json")
    with open(output_json_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"Results saved to {output_json_path}")
