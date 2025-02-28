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

    # Start processing all chunks for eval 
    all_generated_questions = []  # Store all questions

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
            triplet_text = str([f"{t['subject']} {t['predicate']} {t['object']}" for t in extracted_knowledge])
            generated_questions  = knowledge_extractor.create_questions_from_chunk(triplet_text)

            # Append questions to the list
            if generated_questions:
                all_generated_questions.extend(generated_questions)
                print(f"Generated {len(generated_questions)} questions from chunk {i}.")

            else:

                print(f"No questions generated for chunk {i}.")

    knowledge_extractor.save_questions_to_file(all_generated_questions)

    print("\nKnowledge extraction complete.")
    print("Please check 'knowledge.json' for the extracted valuable knowledge.")
