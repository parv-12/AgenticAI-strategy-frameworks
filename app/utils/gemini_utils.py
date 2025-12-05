import google.generativeai as genai
import streamlit as st
import os

api_key = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

def answer_online(query, context):
    print(len(query), len(context))
    # query = query[:500]
    context = context[:100000]
    final_prompt = f"prompt: {query}" + " " + f"context: {context}. If no information found in context give back an empty string."
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(final_prompt)
    return response.text

