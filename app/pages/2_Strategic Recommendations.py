import streamlit as st
import streamlit_scrollable_textbox as stx
from utils.swot_utils import maxi_maxi_strategy, maxi_mini_strategy, mini_maxi_strategy, mini_mini_strategy

def elaborate_strenghts(topic):
    pass

def elaborate_weaknesses(topic):
    pass

def elaborate_opportunities(topic):
    pass

def elaborate_threats(topic):
    pass

def detailed_analysis(topic):
    tabs = st.tabs(["Strenghts","Weaknesses","Opportunities","Threats"])
    with tabs[0]:
        elaborate_strenghts(topic)
    with tabs[1]:
        elaborate_weaknesses(topic)
    with tabs[2]:
        elaborate_opportunities(topic)
    with tabs[3]:
        elaborate_threats(topic)

if __name__=="__main__":
    with st.form("Enter topic for streategic recommendations"):
        topic = st.text_input("Enter topic")
        st.form_submit_button("Submit")
    user = st.sidebar.selectbox("Select User",options=["Managing Board","Technology Manager DAI","Research Engineer DAI"])
    st.session_state["topic"] = topic
    st.session_state["user"] = user
    if topic=="":
        st.info("Please enter topic")
        st.stop()
    # if topic not in ["Clean energy", "Green hydrogen", "Agri tech", "Water irrigation systems"]:
    #     st.stop()
    st.write(f"# Strategic Recommendations for {topic}")
    st.write("### TOWS Matrix")
    cols = st.columns(2)
    maxi_maxi = maxi_maxi_strategy(topic)
    with cols[0]:
        st.write("# Maxi-Maxi strategy - S + O")
        stx.scrollableTextbox(maxi_maxi, key="maxi_maxi", height = 500)
    
    maxi_mini = maxi_mini_strategy(topic)
    with cols[0]:
        st.write("# Maxi-Mini strategy - S + T")
        stx.scrollableTextbox(maxi_mini, key="maxi_mini", height = 500)
    
    mini_maxi = mini_maxi_strategy(topic)
    with cols[1]:
        st.write("# Mini-Maxi strategy - W + O")
        stx.scrollableTextbox(mini_maxi, key="mini_maxi", height = 500)
    
    mini_mini = mini_mini_strategy(topic)
    with cols[1]:
        st.write("# Mini-Mini strategy - W + T")
        stx.scrollableTextbox(mini_mini, key="mini_mini", height = 500)
    
    # if st.checkbox("Detailed analysis"):
    #     detailed_analysis()
    url = "https://getlucidity.com/strategy-resources/an-introduction-to-tows-analysis/"
    st.markdown("For more details on TOWS matrix click [here](%s)" % url)
    