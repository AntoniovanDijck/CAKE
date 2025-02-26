from Semantic_Context_Transcription_Pipeline.SCT_pipeline import *
from Knowledge_Extraction_Pipeline.CAKE_pipeline import *
import sys
import os

video_url = "https://www.youtube.com/watch?v=g4lHxSAyf7M"

def ContextAware_Knowledge_Extraction_Pipeline(video_url = "https://www.youtube.com/watch?v=g4lHxSAyf7M"):
    
    Semantic_Context_Transcription_Pipeline(video_url)

    Knowledge_Extraction_Pipeline()

ContextAware_Knowledge_Extraction_Pipeline(video_url)
