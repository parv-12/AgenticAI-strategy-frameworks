# Strategic intelligence

This repo contains the work around the topic 'strategic intelligence'. The core idea is to develop LLM agents and RAG pipelines to create a framework which analysis a topic and outputs various strategic models for the topic. Some examples of strategic models are:
1. SWOT analysis
2. PR/FAQ document
3. 6 pager

# Components
1. RAG pipelines - IIL qdrant based RAG pipelines are used in the repo. https://code.siemens.com/indutrial-intelligence-layer/qdrant_service dev-cipla branch
2. Text extraction pipeline - Langchain PDF miner is used to extract text from the different strategic and business documents
3. Streamlit app - To query the databases and orchestrate workflows for creating different strategic model outputs. Also provide a user interface to explore different topics

# Setting the environment and running the app
1. Create a virtualenv and install requirements.txt
2. Add your openAI key as env variable: In powershell:
```
$env:OPENAI_API_KEY="your api key"
```
3. Running the streamlit app: In the same terminal:
```
cd app
streamlit run Home.py
```

# Dependencies:
1. Qdrant service is running on localhost:7000. Refer to qdrant repo to run the qdrant service
2. qdrant DB is running on 6333
3. OPENAI API KEY should be available

# Maintainers

- Abhinav Nirmal (abhinav.nirmal@siemens.com)
- Rohit Karanth (rohit.karanth@siemens.com)

# Contributers

- Rohit Karanth
- Abhinav Nirmal
- Parv Jain# stratergic-planning
