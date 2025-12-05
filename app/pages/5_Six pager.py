import streamlit as st
import streamlit.components.v1 as components
from utils.six_pager_utils import generate_six_pager, get_binary_file_downloader_html

if "topic" not in st.session_state:
    st.session_state["topic"] = ""

if __name__=="__main__":
    with st.form("Enter topic for Six Pager"):
        topic = st.text_input("Enter topic")
        st.form_submit_button("Submit")
    
    user = st.sidebar.selectbox("Select User", options=["Managing Board", "Technology Manager DAI", "Research Engineer DAI"])
    st.session_state["topic"] = topic
    st.session_state["user"] = user
    
    if topic == "":
        st.info("Please enter a topic")
        st.stop()
    
    st.write(f"Generating six-pager document for topic: **{topic}**")
    
    # Generate six-pager content
    # six_pager_content = generate_six_pager(topic)
    first_page_content, second_page_content, third_page_content, fourth_page_content, fifth_page_content, sixth_page_content, first_page_images, second_page_images, third_page_images, fourth_page_images, fifth_page_images, sixth_page_images = generate_six_pager(topic)
    tabs = st.tabs(["First page", "Second Page","Third Page", "Fourth Page", "Fifth Page", "Sixth Page"])
    for i, page in enumerate(["First page", "Second Page","Third Page", "Fourth Page", "Fifth Page", "Sixth Page"]):
        with tabs[i]:
            if page.startswith("First"):
                st.write(first_page_content)
                for image in first_page_images[:2]:
                    st.image(image)
            if page.startswith("Second"):
                st.write(second_page_content)
                for image in second_page_images[:2]:
                    st.image(image)
            if page.startswith("Third"):
                st.write(third_page_content)
                for image in third_page_images[:2]:
                    st.image(image)
            if page.startswith("Fourth"):
                st.write(fourth_page_content)
                for image in fourth_page_images[:2]:
                    st.image(image)
            if page.startswith("Fifth"):
                st.write(fifth_page_content)
                for image in fifth_page_images[:2]:
                    st.image(image)
            if page.startswith("Sixth"):
                st.write(sixth_page_content)
                for image in sixth_page_images[:2]:
                    st.image(image)


    # with open(f'{topic}_six_pager.docx', "rb") as file:
    #     file_contents = file.read()
    # st.download_button("Download 6 pager",data=file_contents,file_name="six_pager.docx",mime="application/docx")
    # Provide a download link for the generated document
    # st.markdown(get_bimnary_file_downloader_html(six_pager_content, file_label="Download Six Pager", file_name="six_pager.docx"), unsafe_allow_html=True)
