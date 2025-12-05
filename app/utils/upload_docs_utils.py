import fitz  # PyMuPDF
from nltk import sent_tokenize
import requests
import os
qdrant_url = os.environ.get("qdrant_url","http://localhost:7000")

# Function to extract and concatenate text by headings from a PDF file
def extract_and_concatenate_by_heading(pdf_path):
    doc = fitz.open(pdf_path)
    pages_data = []

    for page_number in range(doc.page_count):
        page = doc[page_number]
        blocks = page.get_text("blocks")

        cur_heading = None
        cur_content = ''

        for block in blocks:
            text, font_size = block[4], block[5]

            # Assuming headings and subheadings are identified by their formatting
            if text.isupper():
                cur_heading = text
            elif text.istitle() and cur_heading:
                cur_content += text + ' '
            else:
                cur_content += text + ' '

        # Split content into sentences using NLTK
        sentences = sent_tokenize(cur_content.strip())

        # Append data for the current page
        pages_data.append({'page_number': page_number + 1, 'heading': cur_heading, 'content': cur_content.strip(), 'sentences': sentences})

    doc.close()
    return pages_data

# Function to convert extracted text to the desired format
def convert_to_desired_format(pages_data, pdf_name, pdf_date, start_page=3):
    final_kb = []
    for doc in pages_data[start_page:]:
        knowledge = doc["content"].replace("\n", "")
        if knowledge:
            final_kb.append({
                "knowledge": knowledge,
                'pdf_name': pdf_name,
                'page_number':doc['page_number'],
                'pdf_date': pdf_date
            })
    return final_kb

def upload_data_to_qdrant(knowledge):
    payload_keys = ["pdf_name","page_number","pdf_date"]
    collection_name = knowledge[0]['pdf_name']
    url = f'{qdrant_url}/qdrant/addKnowledge'
    data = {
        "knowledge": knowledge,
        "collectionName": collection_name,
        "payloadKeys": payload_keys
    }
    response = requests.post(url,json=data,headers={'customer-id':'strategic_intelligence'})
    return response.json()


# # Function to check if the file extension is allowed
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


