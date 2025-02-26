from .knowledge_extractor import *
import json
import os

def Knowledge_Extraction_Pipeline():
    # 1. Load the chunks from output_chunks.json
    with open('pipelines/Semantic_Context_Transcription_Pipeline/result/output_audio_1_chunks.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    chunks = data.get("chunks", [])
    print(f"Total chunks loaded: {len(chunks)}")

    # 2. Extract Knowledge from Each Chunk
    knowledge_extractor = KnowledgeExtractor()

    for i, chunk in enumerate(chunks, start=1):
        text = chunk.get("text", "")
        start_time = chunk.get("start")
        end_time = chunk.get("end")

        print(f"\nProcessing chunk {i} (Start: {start_time}, End: {end_time})")

        # Extract valuable knowledge from the chunk text
        extracted_knowledge = knowledge_extractor.extract_valuable_knowledge(text)

        if extracted_knowledge:
            # Attach the chunk's start/end to each extracted item
            for triplet in extracted_knowledge:
                triplet['start'] = start_time
                triplet['end'] = end_time

            # Save the extracted knowledge
            knowledge_extractor.save_knowledge(extracted_knowledge)

    print("\nKnowledge extraction complete.")
    print("Please check 'knowledge.json' for the extracted valuable knowledge.")
