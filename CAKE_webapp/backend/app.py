from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import pickle
from datetime import datetime
from openai import OpenAI
import threading
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from json import JSONDecodeError

app = Flask(__name__)
CORS(app)

class Chatbot:
    def __init__(self, 
                messages_file='messages.json', 
                knowledge_file='./public/data/user_knowledge.json', 
                faiss_index_file='faiss_index.pkl',
                model_name='all-MiniLM-L6-v2'):
        self.messages_file = messages_file
        self.knowledge_file = knowledge_file
        self.faiss_index_file = faiss_index_file
        
        self.client = OpenAI(api_key="") # Add your OpenAI API key here

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
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
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
                temperature=0.5,
            )
            knowledge_data = json.loads(response.choices[0].message.content)
            if "valuable_knowledge" not in knowledge_data:
                knowledge_data["valuable_knowledge"] = []
            return knowledge_data["valuable_knowledge"]
        except Exception as e:
            print(f"Error extracting knowledge: {e}")
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
        print(knowledge_matches)
        current_time = datetime.utcnow().isoformat()
        system_message = f"Current date and time: {current_time}\n"
        if knowledge_matches:
            system_message += "Answer based on retrieved knowledge:\n"
            for t in knowledge_matches:
                system_message += f"- {t['subject']} {t['predicate']} {t['object']} (Added on: {t['timestamp']})\n"
        else:
            system_message += "No direct related knowledge found. Proceeding with general reasoning.\n"

        enriched_history = [{"role": "system", "content": f"You are a helpful assistant; {system_message}"}] + conversation_history
        enriched_history.append({"role": "user", "content": user_message})

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=enriched_history,
                #temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble generating a response right now."

chatbot = Chatbot()

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        chatbot.save_message(role='user', content=user_message)
        conversation = chatbot.load_json_data(chatbot.messages_file)[-3:]
        assistant_response = chatbot.generate_response(conversation, user_message)
        chatbot.save_message(role='assistant', content=assistant_response)
        
        user_knowledge_response = chatbot.extract_valuable_knowledge(user_message)
        
        if user_knowledge_response:
            chatbot.save_knowledge(user_knowledge_response)

        return jsonify({
            "response": assistant_response,
            "extracted_knowledge": user_knowledge_response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
