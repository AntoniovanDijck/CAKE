# CAKE: Context-Aware Knowledge Extraction
#### Improving the Performance of LLMs with Knowledge Extraction

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
This research introduces a Context-Aware Knowledge Extraction pipeline that automatically processes multi-modal (video, audio, or text) data to extract, structure, and retrieve valuable knowledge. The framework includes:

1. **Semantic Context Transcription Pipeline**
   - Audio data processing using Whisper and TensorFlow LLama.cpp.
   - Text chunking using Semantic Double-Pass Merging for improved context preservation.

2. **Semantic Knowledge Extraction Pipeline**
   - Local AI processing for efficient knowledge extraction.
   - Contextual embeddings for improved knowledge representation.

3. **Integration of Pipelines**
   - Combining extracted knowledge with Large Language Models to improve the accuracy of generated responses.
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

## Usage
### Clone the Repository
```bash
git clone https://github.com/AntoniovanDijck/CAKE.git
cd CAKE
```



### Running the CAKE Pipeline
The CAKE pipeline provides flexibility to execute different components as needed. You can run the **knowledge extraction pipeline**, **evaluate the pipeline**, and **test extracted knowledge via chatbot** using command-line arguments.

#### Install Dependencies
Before running the pipeline, install the required dependencies:

```bash
pip install -r requirements.txt
```

#### Running Specific Components
Use the following command-line arguments to run specific components:

- `-run` → Run the **knowledge extraction pipeline**.
- `-eval` → Run the **evaluation process**.
- `-chat` → Test the extracted knowledge with a **chatbot interface**.
- `-run_all` → Run **all components** (pipeline, evaluation, and chat).

#### Example Commands:
```bash
# Run the full pipeline
python main.py -run

# Evaluate the pipeline
python main.py -eval

# Test extracted knowledge via chatbot
python main.py -chat

# Run all components (pipeline, evaluation, and chatbot)
python main.py -run_all
```

#### Changing the data
```bash
# Change video_url in main.py to the desired video link
video_url = "https://www.youtube.com/watch?v=example"

```

### Evaluating Additional Models
To evaluate more additional **LLM models**, place their **GGUF** files inside the \`models/\` directory. The evaluation script will automatically detect and include them in the evaluation.

```bash
# Place GGUF model files in the 'models/' directory
./pipelines/Knowledge_Extraction_Pipeline/data/models/

# Run the evaluation script
python main.py -eval
```

The script loads all available models in the `models/` folder and runs the evaluation process.

### Running the CAKE demo web application
The CAKE demo web application provides an interactive interface to test the knowledge extraction pipeline and chatbot functionality. The web application also has a visualizer for the extracted knowledge base, the web application is built using React and Flask.

#### Run install dependencies
```bash
cd CAKE_webapp
pip install -r requirements.txt
npm install
```

#### Run the web application and flask server
```bash
# Run the web application
# Don't forget to put a openAI API key in the backend/app.py file!
npm run dev & python backend/app.py
```

### Notebooks
The notebooks directory contains Jupyter notebooks for the different components of the CAKE pipeline. These notebooks give a detailed explanation of the code and the underlying concepts that were developed during the research.


## Results & Findings
The framework successfully extracts and structures critical knowledge, leading to improved accuracy in LLM-generated responses. The FAISS-based retrieval system enhances real-time knowledge access for technical support applications, reducing dependency on static documentation or Retrieval Augmented Generation (RAG).

## Future Work
- Further optimization of retrieval mechanisms.
- Further optimization of knowledge graph construction algorithms and ontology.
- Exploring the impact of real-time knowledge updates.
- Exploring methods of knowledge management.
- Investigating the impact of the top-k parameter of the retrieved knowledge on the quality of generated responses.
- Implementing SAM-2 and a Visual Question Answering Model (VQA) for multi-modal knowledge extraction.

## References
For a comprehensive list of related research and citations, please refer to the **Bibliography** section in the thesis document.

## Acknowledgements
I would like to express my gratitude to my supervisors, **Dr. Ir. J.R. Helmus** and **Dr. S. van Splunter**, for their invaluable guidance and support throughout this research. Also a special thanks to Jesse Jan van Schouten for his insights and collaboration.

### Author: Antonio Adrian Cornelis van Dijck  
**Student Number:** 12717673  
**Bachelor Thesis**  
**Bachelor Information Sciences**  
**University of Amsterdam**  
**Faculty of Science**  

### Supervisors  
**Dr. Ir. J.R. Helmus**  
**Dr. S. van Splunter**  
**Informatics Institute**  
**Faculty of Science**  
**University of Amsterdam**

## Contributors
**Antonio Adrian Cornelis van Dijck**: Context-Aware Knowledge Extraction Framework 

**Jesse Jan van Schouten**: Semantic Context Transcription Pipeline