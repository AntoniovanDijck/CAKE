"""
Antonio van Dijck
studentnumber: 12717673
Email: antonio.van.dijck@student.uva.nl

The evaluation script is a component of the CAKE pipeline that evaluates the performance of the LLM with and without knowledge base.
"""

import json
import os
import pickle
import threading
import sys
from datetime import datetime
from llama_cpp import Llama
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from json import JSONDecodeError

# model check
llm = Llama.from_pretrained(
    repo_id="bartowski/Qwen2.5-7B-Instruct-GGUF",
    filename="*Q4_K_M.gguf",
    verbose=False,
    local_dir="pipelines/Knowledge_Extraction_Pipeline/data/models",
)

class LlamaSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, model_path="pipelines/Knowledge_Extraction_Pipeline/data/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf", chat_format="chatml"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(LlamaSingleton, cls).__new__(cls)
                cls._instance.llm = Llama(model_path=model_path, chat_format=chat_format, n_ctx=2048)
            return cls._instance

class Evaluationes:
    def __init__(self, 
                 messages_file='pipelines/Knowledge_Extraction_Pipeline/data/messages.json', 
                 knowledge_file='pipelines/Knowledge_Extraction_Pipeline/result/knowledge.json', 
                 faiss_index_file='pipelines/Knowledge_Extraction_Pipeline/result/faiss_index.pkl',
                 model_name='all-MiniLM-L6-v2',
                 llm_model_path="pipelines/Knowledge_Extraction_Pipeline/data/models/Qwen2.5-7B-Instruct-Q4_K_M.gguf"):
        self.messages_file = messages_file
        self.knowledge_file = knowledge_file
        self.faiss_index_file = faiss_index_file
        self.llm = LlamaSingleton(model_path=llm_model_path).llm
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

    # generate response with knowledge base
    def generate_response_with_kb(self, user_message):
        knowledge_matches = self.search_knowledge(user_message, top_k=5)
        current_time = datetime.utcnow().isoformat()
        system_message = f"Current date and time: {current_time}\n"
        if knowledge_matches:
            system_message += "Choose only one answer without explanation, based on your knowledge:\n"
            for t in knowledge_matches:
                system_message += f"- {t['subject']} {t['predicate']} {t['object']} (Videotimestamps: start: {t['start']}, end: {t['end']})\n"
        else:
            system_message += "\n"
        enriched_history = [{"role": "system", "content": f"You are a helpful assistent; {system_message}"}]
        enriched_history.append({"role": "user", "content": user_message})
        print(knowledge_matches)
        response = self.llm.create_chat_completion(
            messages = enriched_history,
            temperature=0.5,
        )['choices'][0]['message']['content']
        return response

    # generate response without knowledge base for eval
    def generate_response_without_kb(self, user_message):
        current_time = datetime.utcnow().isoformat()
        system_message = f"Current date and time: {current_time}\n"
        enriched_history = [{"role": "system", "content": f"You are a helpful assistent. Choose only one answer without explanation; {system_message}"}]
        enriched_history.append({"role": "user", "content": user_message})
        response = self.llm.create_chat_completion(
            messages=enriched_history,
            temperature=0.5,
        )['choices'][0]['message']['content']
        return response

def run_evaluation(llm_model_path, questions_path):

    # Load the questions from JSON file
    with open(questions_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    # evalution llm using the provided model path
    chatbot = Evaluationes(llm_model_path=llm_model_path)

    # Loop over all questions
    for question in questions:
        # make a prompt that includes the question text and options.
        prompt = f"Question: {question['question']}\nOptions:\n"
        for idx, opt in enumerate(question['options']):
            # prompt += f"{idx+1}. {opt}\n"         # This is the original line but this has 1.2.3.4 before the options: this is not nice for the eval.
            prompt += f"{opt}\n"

        # Generate responses using the two new functions
        response_with_kb = chatbot.generate_response_with_kb(prompt)
        response_without_kb = chatbot.generate_response_without_kb(prompt)

        # Add the responses to the question JSON object
        question["llm_answer_with_kb"] = response_with_kb
        question["llm_answer_without_kb"] = response_without_kb

    # LLm name
    llm_name = os.path.splitext(os.path.basename(llm_model_path))[0]
    result_filename = f"result_eval_{llm_name}.json"

    # Save the updated questions JSON to the new file
    with open(result_filename, 'w', encoding='utf-8') as f:
        json.dump(questions, f, indent=4)

    # Calculate the accuracy of the LLM with and without KB for the questions
    scores = {"llm_with_kb": 0, "llm_without_kb": 0}
    total_questions = len(questions)

    for question in questions:
        correct_answer = question["correct_answer"].lower()

        # Check if the generated responses match the correct answer and lower
        if correct_answer in question["llm_answer_with_kb"].lower():
            scores["llm_with_kb"] += 1
        if correct_answer in question["llm_answer_without_kb"].lower():
            scores["llm_without_kb"] += 1

    accuracy_with_kb = (scores["llm_with_kb"] / total_questions) * 100
    accuracy_without_kb = (scores["llm_without_kb"] / total_questions) * 100

    improvement = accuracy_with_kb - accuracy_without_kb

    # create a resulting dictionary
    evaluation_results = {
        "llm_model": llm_name,
        "total_questions": total_questions,
        "scores": {
            "llm_with_kb": scores["llm_with_kb"],
            "llm_without_kb": scores["llm_without_kb"]
        },
        "accuracy": {
            "llm_with_kb": f"{accuracy_with_kb:.2f}%",
            "llm_without_kb": f"{accuracy_without_kb:.2f}%"
        },
        "improvement": f"{improvement:.2f}%"
    }

    # Save accuracy and scores in a separate file
    scores_filename = f"scores_eval_{llm_name}.json"

    with open(scores_filename, 'w', encoding='utf-8') as f:
        json.dump(evaluation_results, f, indent=4)

    print(f"Evaluation complete. Results saved to {result_filename}\n")
    print("LLM Evaluation Results:")
    print(f"LLM with KB Accuracy: {accuracy_with_kb:.2f}% ({scores['llm_with_kb']} correct out of {total_questions})")
    print(f"LLM without KB Accuracy: {accuracy_without_kb:.2f}% ({scores['llm_without_kb']} correct out of {total_questions})")
    print(f"Accuracy improvement with KB: {improvement:.2f}%")

# if __name__ == "__main__": 
#     # Check command-line arguments
#     model_paths = ["models/Qwen2.5-7B-Instruct-Q4_K_M.gguf"]
    
#     for model_path in model_paths:
#         questions_path = "questions.json"
#         run_evaluation(model_path, questions_path)
    
    # model_path = "models/Llama-3.2-3B-Instruct-Q4_K_M.gguf"
    # questions_path = "questions.json"
    # run_evaluation(model_path, questions_path)