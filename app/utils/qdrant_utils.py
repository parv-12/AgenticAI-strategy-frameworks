import requests
import base64
import streamlit as st
from io import BytesIO
import os

def base64_to_bytesio(base64_string):
    try:
        # Decode base64 string to bytes
        image_data = base64.b64decode(base64_string)
        
        # Create BytesIO object
        bytesio_object = BytesIO(image_data)
        
        return bytesio_object
    except Exception as e:
        print(f"Error converting base64 to BytesIO: {e}")
        return None

def get_images(meta_data):
    images = []
    # print(meta_data)
    for data in meta_data:
        if "type" in data.keys():
            if data["type"] == "image":
                images.append(base64_to_bytesio(data["original_content"]))
                # print(f"Image name: {data['img_file_name']}")
    return images

@st.cache_data
def get_qdrant_context(index_name, query_text, queryVectorName="page_content"):
    # try:
    qdrant_url = os.environ["qdrant_url"] # "http://localhost:7000"
    customerId = "strategic_intelligence"
    # Build the payload
    data = {"queryText":str(query_text), "collectionName":index_name, "queryVectorName":queryVectorName,
            "payloadKeys": ["type","original_content","page_number","img_file_name"]}

    # RAG endpoint
    response = requests.post(f"{qdrant_url}/qdrant/answer",json=data, headers={"customer-id":customerId})
    if not response.status_code==200:
        return "", []
    context = response.json()["context"]
    meta_data = response.json()["meta_data"]
    images = get_images(meta_data) #TODO: Try except block
    return context, images
    # except:
    #     return None, None
