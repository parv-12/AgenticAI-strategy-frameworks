import streamlit as st
import os
from openai import AzureOpenAI

# if "openai_model" not in st.session_state:
#     st.session_state["openai_model"] = "gpt-4-32k"

@st.cache_data
def answer_online_gpt(query:str, context:str=""):
    client = AzureOpenAI(
    azure_endpoint = "https://openai-aittack-msa-001506-swedencentral-hackethon-chatbot-00.openai.azure.com/",
    api_key=os.environ["OPENAI_API_KEY"],
    api_version="2023-07-01-preview"
    )
    print(len(context))
    context = context[:100000]
    messages = []
    if not context=="":
        messages.append({"role": "user",
                            "content": f"Context: {context}"})
    messages.append({"role": "user",
                            "content": query})
    messages.append({"role":"system","content":"You are an AI assistant that acts as the person mentioned in the prompt."})

    completion = client.chat.completions.create(
    model="gpt-4-32k", # model = "deployment_name"
    messages = messages,
    temperature=0.7,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
    )

    print(completion)
    return completion.choices[0].message.content