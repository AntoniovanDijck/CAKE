import os
import json

def convert_to_full_text():
    # Input directory containing JSON files
    json_folder = 'pipelines/Semantic_Context_Transcription_Pipeline/data/transcription_data'
    output_dir = 'pipelines/Semantic_Context_Transcription_Pipeline/data/transcription_data'

    # Maak output directory aan als deze niet bestaat
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output directory '{output_dir}' is ready.")

    # Process each JSON file individually
    for json_file in os.listdir(json_folder):
        if json_file.endswith('.json'):
            json_path = os.path.join(json_folder, json_file)
            print(f"Processing file: {json_file}")

            # Controleer of het JSON-bestand geldig is
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError) as e:
                print(f"Error: Failed to process '{json_file}'. Details: {e}")
                continue

            segments = data.get('segments', [])
            if not segments:
                print(f"Warning: No segments found in '{json_file}'.")
                continue

            # Create output text file for the individual transcript
            individual_output_path = os.path.join(output_dir, json_file.replace('.json', '.txt'))

            with open(individual_output_path, 'w', encoding='utf-8') as individual_file:
                for i, segment in enumerate(segments, start=1):
                    text = segment.get('text', '').strip()
                    if not text:
                        print(f"Warning: Segment {i} in '{json_file}' is empty.")
                        continue
                    individual_file.write(f"{text} ")

            print(f"Transcript saved to '{individual_output_path}'.")
