import streamlit as st
import streamlit_scrollable_textbox as stx
from utils.swot_utils import *

if "topic" not in st.session_state:
    st.session_state["topic"] = ""

if __name__=="__main__":
    # topic = st.session_state["topic"]
    with st.form("Enter topic for SWOT"):
        topic = st.text_input("Enter topic")
        st.form_submit_button("Submit")
    user = st.sidebar.selectbox("Select User",options=["Managing Board","Technology Manager DAI","Research Engineer DAI"])
    st.session_state["topic"] = topic
    if topic=="":
        st.info("Please enter topic")
        st.stop()
    st.session_state["user"] = user
    # if topic not in ["Clean energy", "Green hydrogen", "Agri tech", "Water irrigation systems"]:
    #     st.stop()
    
    cols = st.columns(2)
    strenghts, images_strengths = get_strengths(topic)
    with cols[0]:
        st.write("# Strengths")
        stx.scrollableTextbox(strenghts, key="strenghts", height = 500)
    
    weaknesses, images_weaknesses = get_weaknesses(topic)
    with cols[1]:
        st.write("# Weaknesses")
        stx.scrollableTextbox(weaknesses, key="weaknesses", height = 500)
    
    opportunities, images_opportunities = get_opportunities(topic)
    with cols[0]:
        st.write("# Opportunities")
        stx.scrollableTextbox(opportunities, key="opportunities", height = 500)
    
    threats, images_threats = get_threats(topic)
    with cols[1]:
        st.write("# Threats")
        stx.scrollableTextbox(threats, key="threats", height = 500)
    
    if st.checkbox("Display images"):
        tabs = st.tabs(["Strengths","Weaknesses","Opportunities","Threats"])
        with tabs[0]:
            for image in images_strengths: st.image(image)
        with tabs[1]:
            for image in images_weaknesses: st.image(image)
        with tabs[2]:
            for image in images_opportunities: st.image(image)
        with tabs[3]:
            for image in images_threats: st.image(image)