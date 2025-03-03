"""
Antonio van Dijck
studentnumber: 12717673
Email: antonio.van.dijck@student.uva.nl

The knowledge extractor is a component of the CAKE pipeline that extracts valuable
"""

from llama_cpp import Llama
import json
import os
import pickle
import threading
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from json import JSONDecodeError

# LLama model loaded in from hugginface and downloaded in models folder
llm = Llama.from_pretrained(
    repo_id="bartowski/Qwen2.5-7B-Instruct-GGUF",
    filename="*Q4_K_M.gguf",
    verbose=False,
    local_dir="pipelines/Knowledge_Extraction_Pipeline/data/models",
)

# Class llama singleton to let the gpu chill
class LlamaSingleton:
    _instance = None
    _lock = threading.Lock()

    # Llama gguf model loading from the folder (so no cache needed)
    def __new__(cls, model_path="pipelines/Knowledge_Extraction_Pipeline/data/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf", chat_format="chatml"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LlamaSingleton, cls).__new__(cls)
                cls._instance.llm = Llama(model_path=model_path, chat_format=chat_format, n_ctx=2048) #context lengte kan aangepast worden
            return cls._instance

# the main class for knowledge extraction
class KnowledgeExtractor:
    def __init__(self, 
                 messages_file='pipelines/Knowledge_Extraction_Pipeline/data/messages.json', #wordt niet gebruikt nu
                 knowledge_file='pipelines/Knowledge_Extraction_Pipeline/result/knowledge.json', #result file
                 faiss_index_file='pipelines/Knowledge_Extraction_Pipeline/result/faiss_index.pkl', #result file vectordatabase
                 model_name='all-MiniLM-L6-v2'):
        self.messages_file = messages_file
        self.knowledge_file = knowledge_file
        self.faiss_index_file = faiss_index_file
        self.llm = LlamaSingleton().llm
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.knowledge_data = []
        self.initialize_files()
        self.load_faiss_index()

    def initialize_files(self):
        for file in [self.messages_file, self.knowledge_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    json.dump([], f)

    def load_json_data(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)

    def save_json_data(self, file_path, data):
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def extract_valuable_knowledge(self, message):
        response = self.llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a knowledge extractor. Try to extract any knowledge.\n"
                        "Return ONLY JSON with the following schema:\n"
                        "{\n"
                        "  \"valuable_knowledge\": [\n"
                        "    {\n"
                        "      \"subject\": \"...\",\n"
                        "      \"predicate\": \"...\",\n"
                        "      \"object\": \"...\"\n"
                        "    }\n"
                        "  ]\n"
                        "}\n"
                        "If no knowledge can be extracted, return:\n"
                        "{\"valuable_knowledge\": []}"
                    )
                },
                {"role": "user", "content": message},
            ],
            response_format={
                "type": "json",
                "schema": {
                    "type": "object",
                    "properties": {
                        "valuable_knowledge": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "subject": {"type": "string"},
                                    "predicate": {"type": "string"},
                                    "object": {"type": "string"}
                                },
                                "required": ["subject", "predicate", "object"]
                            }
                        }
                    },
                    "required": ["valuable_knowledge"],
                },
            },
            temperature=0.7,
        )
        try:
            knowledge_data = json.loads(response['choices'][0]['message']['content'])
            print("Extracted knowledge from a chunk:", knowledge_data)
            if "valuable_knowledge" not in knowledge_data:
                knowledge_data["valuable_knowledge"] = []
            return knowledge_data["valuable_knowledge"]
        except (JSONDecodeError, KeyError):
            return []

    def save_knowledge(self, triplets):
        if not triplets:
            return
        knowledge = self.load_json_data(self.knowledge_file)
        existing_set = {(t['subject'], t['predicate'], t['object']) for t in knowledge}
        new_triplets = []
        for triplet in triplets:
            key = (triplet['subject'], triplet['predicate'], triplet['object'])
            if key not in existing_set:
                knowledge.append(triplet)
                new_triplets.append(triplet)
                existing_set.add(key)
        self.save_json_data(self.knowledge_file, knowledge)
        if new_triplets:
            self.update_faiss_index(new_triplets)

    def update_faiss_index(self, triplets):
        texts = [f"{t['subject']} {t['predicate']} {t['object']}" for t in triplets]
        embeddings = self.model.encode(texts)
        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings, dtype=np.float32))
        self.knowledge_data.extend(triplets)
        self.save_faiss_index()

    def save_faiss_index(self):
        with open(self.faiss_index_file, 'wb') as f:
            pickle.dump((self.index, self.knowledge_data), f)

    def load_faiss_index(self):
        if os.path.exists(self.faiss_index_file):
            with open(self.faiss_index_file, 'rb') as f:
                self.index, self.knowledge_data = pickle.load(f)
        else:
            self.index = None
            self.knowledge_data = []

    #again response format is used to get the questions in the right format
    def create_questions_from_chunk(self, chunk_text):
        response = llm.create_chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a knowledge question creator. Given an input text, generate a list of two exam multiple-choice questions.\n"
                        "in the following JSON format:\n\n"
                        "[\n"
                        "    {\n"
                        "      \"question\": \"Question text\",\n"
                        "      \"options\": [\n"
                        "        \"Option 1\",\n"
                        "        \"Option 2\",\n"
                        "        \"Option 3\",\n"
                        "        \"Option 4\"\n"
                        "      ],\n"
                        "      \"correct_answer\": \"Correct answer\"\n"
                        "    }\n"
                        "    // ... more questions\n"
                        "]\n\n"
                        "Return ONLY valid JSON.\n"
                        "If no questions can be generated, return an empty list: []."
                    )
                },
                {"role": "user", "content": chunk_text},
            ],
            response_format={
                "type": "json",
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "question": {"type": "string"},
                            "options": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 4,
                                "maxItems": 4
                            },
                            "correct_answer": {"type": "string"}
                        },
                        "required": ["question", "options", "correct_answer"]
                    }
                }
            },
            temperature=0.7,
        )
        try:
            questions_data = json.loads(response['choices'][0]['message']['content'])
            if isinstance(questions_data, list):

                # Add the required eval fields manually after AI generation
                for question in questions_data:
                    question["llm_answer_with_kb"] = ""
                    question["llm_answer_without_kb"] = ""
                return questions_data
            return []
        except (JSONDecodeError, KeyError):
            return []
        
    def save_questions_to_file(self, questions, file_path="pipelines/Knowledge_Extraction_Pipeline/data/questions.json"):
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save new questions to file (overwrite existing file)
        with open(file_path, "w") as f:
            json.dump(questions, f, indent=4)