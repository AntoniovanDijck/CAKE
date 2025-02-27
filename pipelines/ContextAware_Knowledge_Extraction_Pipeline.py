from .Semantic_Context_Transcription_Pipeline.SCT_pipeline import *
from .Knowledge_Extraction_Pipeline.CAKE_pipeline import *
import sys
import os

class CAKE:
    def __init__(self):
        pass    

    def ContextAware_Knowledge_Extraction_Pipeline(self, video_url):
        Semantic_Context_Transcription_Pipeline(video_url)
        Knowledge_Extraction_Pipeline()

    def run(self, video_url):
        self.ContextAware_Knowledge_Extraction_Pipeline(video_url)

    def evaluate(self):
        pass


#example usage
#video_url1 = "https://www.youtube.com/watch?v=g4lHxSAyf7M" #How the EVAP System Works (car engine)
#CAKE().run(video_url2)

