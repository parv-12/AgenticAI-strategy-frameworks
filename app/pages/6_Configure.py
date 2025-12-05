import streamlit as st
import os
from utils.upload_docs_utils import extract_and_concatenate_by_heading, convert_to_desired_format, upload_data_to_qdrant

if "topic" not in st.session_state:
    st.session_state["topic"] = ""


def main():
    st.title('Upload PDF Document')

    UPLOAD_FOLDER = './utils/temp'
    # ALLOWED_EXTENSIONS = {'pdf'}
    # File upload
    with st.form("Upload file"):
        uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
        cols = st.columns(3)
        with cols[0]:
            report_name = st.text_input("Enter report name")
        with cols[1]:
            report_date = st.text_input("Enter date of report")
        with cols[2]:
            start_page = st.number_input("Enter starting page", 0, 10, 3)
        st.form_submit_button("Submit")

    if uploaded_file is not None and report_name != "" and report_date !=  "":
        # Save uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.read())

        # Extract and concatenate text by headings
        pages_data = extract_and_concatenate_by_heading(file_path)

        # Convert extracted text to the desired format
        final_kb = convert_to_desired_format(pages_data, report_name, report_date, start_page)

        # Display the resulting knowledge base
        # st.write("Knowledge Base:")
        # st.json(final_kb)

        #Uploading the KB to qdrant
        response = upload_data_to_qdrant(final_kb)
        st.write(response)
    else:
        st.info('Please upload a PDF file and enter all details.')

if __name__ == "__main__":
    main()
