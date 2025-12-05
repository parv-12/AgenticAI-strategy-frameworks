import streamlit as st
import os
import copy as cp
import requests
import time
from utils.gemini_utils import answer_online
from utils.gpt_utils import answer_online_gpt
from utils.qdrant_utils import get_qdrant_context

collections = ["Siemens_Report_FY2023", "sustainability-report-fy2023",
    "BCGreport_energy_transition",
    "SRCCL_Chapter_7_ipcc",
    "toward-a-sustainable-inclusive-growing-future-the-role-of-business_McKinsey",
    "56297_373_mckinsey_esg_report-2022_aw6_v10_final"
]

if "topic" not in st.session_state:
    st.session_state["topic"] = ""
st.title("Strategy Planning assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system",
                                  "content": "You are an AI assistant designed to help strategy managers to understand and evaluate reports."}]

for index, message in enumerate(st.session_state.messages):
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def context_qna():
    if prompt := st.chat_input("Please enter your query here"):

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            context = ""
            meta_data = []
            for collection in collections_to_answer_from:
                context_from_qdrant, images = get_qdrant_context(collection, prompt)
                context += context_from_qdrant
                # if not context_from_qdrant=="No information available" and len(context_from_qdrant["context"])>0:
                #     context+=context_from_qdrant["context"]
                #     context_meta_data = context_from_qdrant["meta_data"]
                #     # if len(context_meta_data)>3:
                #     #     context_meta_data = context_meta_data[:3]
                #     for data in context_meta_data:
                #         del data["Document"]
                #     meta_data.extend(context_meta_data)
            gemini_prompt = "You are a strategy manager assistant at a big B2B conglomerate which sells industrial products and services. "
            gemini_prompt += f"Someone asks you a question: {prompt}."
            gemini_prompt += f"Answer the question as a strategy manager based on the context retrieved from various strategic reports."
            gemini_prompt += f"Make sure to stick to the context."
            print(context)
            if len(context)>24000: #TODO: Reranking outputs from qdrant
                for i in range(24000,len(context),24000):
                    iteration_context = context[:i] #Try few shot answering here.
                    response = answer_online_gpt(gemini_prompt,iteration_context)
                    message_placeholder.markdown(response)
                    message_placeholder.image
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    time.sleep(2)
            else:
                response = answer_online_gpt(gemini_prompt, context)
                message_placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            if len(meta_data)>0:
                for data in meta_data:
                    st.sidebar.write(data)
            for image in images[:4]: st.image(image)
            meta_data = []

if __name__=="__main__":
    # collections = os.listdir("./utils/temp")
    if len(collections)==0:
        st.info("No PDFs to answer from")
        st.stop()
    # collections = [collection[:-4] for collection in collections]
    options = cp.copy(collections)
    options.append("all")
    # with st.form("Select collections"):
    selected_collections = st.sidebar.multiselect("Select PDFs to answer from. (Select all to answer from all)", options)
        # st.form_submit_button("Submit")
    if len(selected_collections)==0:
        st.info("Select PDFs to continue")
        st.stop()
    if "all" in selected_collections:
        collections_to_answer_from = collections
    else:
        collections_to_answer_from = selected_collections
    context_qna()