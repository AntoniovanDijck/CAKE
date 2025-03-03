"""
Antonio van Dijck
studentnumber: 12717673
Email: antonio.van.dijck@student.uva.nl

The class CAKE is the CAKE pipeline that runs the ContextAware_Knowledge_Extraction_Pipeline and the Knowledge_Extraction_Pipeline as a whole.
"""

from .Semantic_Context_Transcription_Pipeline.SCT_pipeline import *
from .Knowledge_Extraction_Pipeline.CAKE_pipeline import *
from .Knowledge_Extraction_Pipeline.chat import *
from .Knowledge_Extraction_Pipeline.evaluate import *
import sys
import os

class CAKE:
    def __init__(self):
        pass    

    def ContextAware_Knowledge_Extraction_Pipeline(self, video_url):
        Semantic_Context_Transcription_Pipeline(video_url)
        Knowledge_Extraction_Pipeline()

    def run_pipeline(self, video_url):
        self.ContextAware_Knowledge_Extraction_Pipeline(video_url)

    def chat(self):
        chatbot = Chatbot()
        chatbot.chat()

    # Evaluate the pipeline but the questions are only for this video; 
    # https://www.youtube.com/watch?v=g4lHxSAyf7M" #How the EVAP System Works (car engine)
    # You need to change the questions.json to evaluate other videos
    
    def evaluate(self):
        #model_paths = ["models/Qwen2.5-7B-Instruct-Q4_K_M.gguf"]
        model_dir = "pipelines/Knowledge_Extraction_Pipeline/data/models"
        questions_path = "pipelines/Knowledge_Extraction_Pipeline/data/questions.json"

        for file in os.listdir(model_dir):
            if file.endswith(".gguf"):
                model_path = os.path.join(model_dir, file)
                run_evaluation(model_path, questions_path)


        # for model_path in model_paths:
        #     questions_path = "questions.json"
        #     run_evaluation(model_path, questions_path)


#example usage
#video_url1 = "https://www.youtube.com/watch?v=g4lHxSAyf7M" #How the EVAP System Works (car engine)
#CAKE().run(video_url2)

