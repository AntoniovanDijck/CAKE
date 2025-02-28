import json
import os
import pickle
from datetime import datetime
from llama_cpp import Llama
import threading
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from json import JSONDecodeError

class LlamaSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, model_path="pipelines/Knowledge_Extraction_Pipeline/data/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf", chat_format="chatml"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LlamaSingleton, cls).__new__(cls)
                cls._instance.llm = Llama(model_path=model_path, chat_format=chat_format, n_ctx=2048)
            return cls._instance

class Chatbot:
    def __init__(self, 
                 messages_file='pipelines/Knowledge_Extraction_Pipeline/data/messages.json', 
                 knowledge_file='pipelines/Knowledge_Extraction_Pipeline/result/knowledge.json', 
                 faiss_index_file='pipelines/Knowledge_Extraction_Pipeline/result/faiss_index.pkl',
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
                        "You are a knowledge extractor. Try to Extract any knowledge from the user.\n"
                        "Return ONLY JSON with the following schema:\n"
                        "{\n"
                        "  \"valuable_knowledge\": [\n"
                        "    {\n"
                        "      \"subject\": \"...\",\n"
                        "      \"predicate\": \"...\",\n"
                        "      \"object\": \"...\",\n"
                        "      \"timestamp\": \"...\"  # ISO8601\n"
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
                                    "object": {"type": "string"},
                                    "timestamp": {"type": "string", "format": "date-time"}
                                },
                                "required": ["subject", "predicate", "object", "timestamp"]
                            }
                        }
                    },
                    "required": ["valuable_knowledge"],
                },
            },
            temperature=0.5,
        )
        try:
            knowledge_data = json.loads(response['choices'][0]['message']['content'])
            print(knowledge_data)
            if "valuable_knowledge" not in knowledge_data:
                knowledge_data["valuable_knowledge"] = []
            return knowledge_data["valuable_knowledge"]
        except (JSONDecodeError, KeyError):
            return []

    def save_message(self, role, content):
        messages = self.load_json_data(self.messages_file)
        message = {"role": role, "content": content, "timestamp": datetime.utcnow().isoformat()}
        messages.append(message)
        self.save_json_data(self.messages_file, messages)

    def save_knowledge(self, triplets):
        if not triplets:
            return
        knowledge = self.load_json_data(self.knowledge_file)
        existing_set = {(t['subject'], t['predicate'], t['object']) for t in knowledge}
        new_triplets = []
        for triplet in triplets:
            triplet['timestamp'] = datetime.utcnow().isoformat()
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

    def search_knowledge(self, query, top_k=5):
        if self.index is None or len(self.knowledge_data) == 0:
            return []
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_embedding, dtype=np.float32), top_k)
        results = []
        for idx in indices[0]:
            if idx == -1:
                continue
            results.append(self.knowledge_data[idx])
        return results

    def generate_response(self, conversation_history, user_message):
        knowledge_matches = self.search_knowledge(user_message, top_k=5)
        current_time = datetime.utcnow().isoformat()
        system_message = f"Current date and time: {current_time}\n"
        if knowledge_matches:
            system_message += "Answer based on retrieved knowledge:\n"
            for t in knowledge_matches:
                system_message += f"- {t['subject']} {t['predicate']} {t['object']} (Videotimestamps: start: {t['start']}, end: {t['end']})\n"
            
        else:
            system_message += "No direct related knowledge found. Proceeding with general reasoning.\n"
        enriched_history = [{"role": "system", "content": f"You are a helpful assistent; {system_message}"}] #+ conversation_history
        enriched_history.append({"role": "user", "content": user_message})
        print(enriched_history)
        response = self.llm.create_chat_completion(
            messages=enriched_history,
            temperature=0.7,
        )['choices'][0]['message']['content']
        return response

    def chat(self):
        print("Chatbot is ready! Type 'exit' to end the conversation.")
        while True:
            user_message = input("You: ")
            if user_message.lower().strip() in ['exit', 'quit']:
                print("Chatbot: Goodbye!")
                break
            self.save_message(role='user', content=user_message)
            conversation = self.load_json_data(self.messages_file)[-3:]
            assistant_response = self.generate_response(conversation, user_message)
            print(f"Assistant: {assistant_response}")
            #generate_speech(assistant_response)
            self.save_message(role='assistant', content=assistant_response)
            #user_knowledge_response = self.extract_valuable_knowledge(user_message)
            #print(user_knowledge_response)  
            #if user_knowledge_response:
                #self.save_knowledge(user_knowledge_response)

# if __name__ == "__main__":
#     chatbot = Chatbot()
#     chatbot.chat()