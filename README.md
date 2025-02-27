# CAKE: Context-Aware Knowledge Extraction

## Improving the Performance of LLMs with Knowledge Extraction

### Author: Antonio A.C. van Dijck  
**Student Number:** 12717673  
**Bachelor Thesis**  
**Bachelor Information Sciences**  
**University of Amsterdam**  
**Faculty of Science**  

### Supervisor  
**Dr. J. Helmus**  
**Dr. S. van Splunter**  
**Informatics Institute**  
**Faculty of Science**  
**University of Amsterdam**  

## Overview
CAKE (Context-Aware Knowledge Extraction) is a research project focused on improving the performance of Large Language Models (LLMs) by extracting and utilizing contextual knowledge from multiple modalities, such as video, audio, and text. The project aims to bridge the gap between structured knowledge management and AI-driven decision support.

## Problem Statement
Traditional knowledge management systems rely on structured databases and predefined taxonomies, but they struggle to capture nuanced and context-dependent knowledge. This project proposes a novel AI-driven framework to extract, structure, and store tacit knowledge for effective retrieval and application in real-world scenarios.

## Research Question
**Can Large Language Models utilize and extract crucial knowledge from different modalities to improve the accuracy and quality of generated responses?**

### Sub-Questions
- What methodologies exist for knowledge extraction, and how can they be adapted for LLMs?
- What are the challenges in extracting knowledge from multi-modal data?
- What role does knowledge have in enhancing the performance of Large Language Models over time?
- What role do LLMs play in creating a flexible and scalable knowledge framework?
- What are the computational and ethical considerations in deploying such a framework?

## Approach
This research introduces an Context-Aware Knowledge Extraction pipeline that automatically processes multi-modal (video, audio or text) data to extract, structure, and retrieve valuable knowledge. The framework includes:

1. **Semantic Context Transcription Pipeline**
   - Audio data processing using Whisper and TensorFlow LLama.ccp.
   - Text chunking using Semantic Double-Pass Merging for improved context preservation chunking.

2. **Semantic Knowledge Extraction Pipeline**
   - Local AI processing for efficient knowledge extraction.
   - Contextual embeddings for improved knowledge representation.

3. **Integration of Pipelines**
   - Combining extracted knowledge with Large Language Model to improve accuracy of generated responses.
   - Implementing FAISS for fast similarity search for extracted knowledge in the vector database.

## Technologies Used
- **LLMs**: Llama3.2-11B, Qwen2.5-7B
- **Speech-to-Text**: Whisper
- **Chunking & Segmentation**: Chonkie, SAM-2 (Segment Anything Model)
- **Knowledge Retrieval & Vector Database**: FAISS (Facebook AI Similarity Search)
- **Frameworks & Libraries**: TensorFlow, PyTorch, Hugging Face, React, Flask, LLama_cpp

## Key Contributions
- Development of a structured knowledge extraction framework.
- Integration of multi-modal data for improved LLM context-awareness.
- Implementation of a FAISS-based vector database retrieval mechanism.
- Exploration of knowledge graphs and their role for Large Language Models.

## Results & Findings
The framework successfully extracts and structures critical knowledge, leading to improved accuracy in LLM-generated responses. The FAISS-based retrieval system enhances real-time knowledge access for technical support applications, reducing dependency on static documentation or Retrieval Augmented Generation (RAG).

## Future Work
- Further optimization of retrieval mechanisms.
- Further optimization of knowledge graph construction algorithms and ontology.
- Exploring the impact of real-time knowledge updates.
- Exploring methods of knowledge management.
- Exploring the impact of the top-k parameter of the retrieved knowledge on the quality of generated responses.
- Implementing SAM-2 and Visual Question Answering Model (VQA) for multi-modal knowledge extraction.


## References
For a comprehensive list of related research and citations, please refer to the **Bibliography** section in the thesis document.

## Acknowledgements
I would like to express my sincere gratitude to my supervisors, **Dr. S. van Splunter** and **Dr. J. Helmus** , for their invaluable guidance and support throughout this research. Also a special thanks to Jesse for their insights and collaboration.