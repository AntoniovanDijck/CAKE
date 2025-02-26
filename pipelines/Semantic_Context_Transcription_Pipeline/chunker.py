import os
import json
from chonkie import SDPMChunker

def load_document(file_path: str) -> str:
    """
    Load the content of the document from the given file path.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def load_json(file_path: str) -> dict:
    """
    Load and parse a JSON file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The JSON file '{file_path}' does not exist.")
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error: Failed to decode JSON file. Details: {e}")

def create_chunker(embedding_model="minishlab/potion-base-8M", chunk_size=512, min_sentences=1):
    """
    Create and return an instance of SDPMChunker with specified parameters.
    """
    return SDPMChunker(
        embedding_model=embedding_model,
        chunk_size=chunk_size,
        min_sentences=min_sentences
    )

def process_text_and_json(text_folder: str, json_folder: str, output_folder: str):
    """
    Process text and JSON files to create timestamped chunked outputs.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for text_file in os.listdir(text_folder):
        if text_file.endswith(".txt"):
            base_name = os.path.splitext(text_file)[0]
            text_path = os.path.join(text_folder, text_file)
            json_path = os.path.join(json_folder, base_name + ".json")

            if not os.path.exists(json_path):
                print(f"Warning: No matching JSON file for {text_file}")
                continue

            text_content = load_document(text_path)
            json_data = load_json(json_path)
            segments = json_data.get('word_segments', [])

            if not segments:
                raise ValueError(f"Error: No segments found in the JSON file {json_path}.")

            word_list = [[seg.get('word', '').strip(), seg.get('start', ''), seg.get('end', '')] for seg in segments if seg.get('word', '').strip()]
            chunker = create_chunker()
            chunks = chunker.chunk(text_content)

            final_chunks = []
            current_word_index = 0
            for chunk in chunks:
                chunk_text = chunk.text
                chunk_words = chunk_text.split()
                chunk_word_data = []
                chunk_start = None
                chunk_end = None

                for chunk_word in chunk_words:
                    if current_word_index < len(word_list):
                        word_info = word_list[current_word_index]
                        if chunk_word == word_info[0]:
                            chunk_word_data.append({
                                "word": word_info[0],
                                "start": word_info[1],
                                "end": word_info[2]
                            })
                            if chunk_start is None:
                                chunk_start = word_info[1]
                            chunk_end = word_info[2]
                            current_word_index += 1
                        else:
                            raise ValueError(f"Word mismatch at chunk '{chunk_text}': Expected '{word_info[0]}', found '{chunk_word}'.")
                    else:
                        raise IndexError("Ran out of words in word_data to match with chunks.")

                final_chunks.append({
                    "text": chunk_text,
                    "start": chunk_start,
                    "end": chunk_end,
                    "words": chunk_word_data
                })

            output_json_path = os.path.join(output_folder, base_name + "_chunks.json")
            with open(output_json_path, 'w', encoding='utf-8') as f:
                json.dump({"chunks": final_chunks}, f, ensure_ascii=False, indent=4)
                print(f"Processed {text_file} and saved to {output_json_path}")