import streamlit as st
import streamlit_scrollable_textbox as stx
import time
from PIL import Image
from utils.crawler_utils import crawl_web
from utils.gemini_utils import answer_online
from utils.gpt_utils import answer_online_gpt
from utils.web_crawler_utils import web_crawler, get_links

st.set_page_config(page_title="Strategic Intelligence", page_icon="🧠", layout="wide")
image = Image.open("./images/siemens.png")
st.image(image, width=175)
st.header("Strategic Intelligence")
st.write("***Get strategic insights on any topic, company, technology***")

if "topic" not in st.session_state:
    st.session_state["topic"] = ""

def display_news(topic:str):
    # search_results = crawl_web(topic)
    search_results = {
        f"About {topic}":web_crawler(f"https://en.wikipedia.org/wiki/{topic.replace(' ','_')}"),
        "Latest_news":web_crawler(f"https://energynews.biz/?s={topic.replace(' ','+')}")
    }
    extra_links = {
        f"About {topic}":get_links(f"https://en.wikipedia.org/wiki/{topic.replace(' ','_')}"),
        "Latest_news":get_links(f"https://energynews.biz/?s={topic.replace(' ','+')}")
    }
    tabs = st.tabs([key for key in search_results.keys()])
    for i, key in enumerate(search_results.keys()):
        with tabs[i]:
            columns = st.columns([5,2])
            # with columns[1]:
            #     st.write("# Extra information:")
            
            #     # st.write(f"### {key}")
            #     stx.scrollableTextbox(extra_links[key], key=f"{key}", height=500)
            # with columns[0]:
            st.write(f"# {key}")
            prompt = "You are a strategy manager at a big B2B conglomerate which sells industrial products and services. "
            prompt += f"You come across some snippets on the {topic} as given in the context. "
            prompt += f"Generate some key strategic insights for the {topic} based on the context."
            ans = answer_online(prompt, f"{key} - {search_results[key]}")
            # st.write(f"### Insights on {key}")
            time.sleep(5)
            stx.scrollableTextbox(ans, key=f"{key} Insights", height=500)

def url_insights(urls:list, topic:str):
    tabs = st.tabs(urls)
    for i, url in enumerate(urls):
        content = web_crawler(url)

        prompt = "You are a strategy manager at a big B2B conglomerate which sells industrial products and services. "
        prompt += f"You come across some latest news snippets on the {topic} as given in the context. "
        prompt += f"Generate some key strategic insights for the {topic} based on the recent news."
        ans = answer_online(prompt, content)
        with tabs[i]:
            st.write(f"### Insights on {url}")
            stx.scrollableTextbox(ans, key=f"{url} Insights", height=500)
            time.sleep(5)


if __name__=="__main__":
    with st.form("Enter topic"):
        topic = st.text_input("Enter topic")
        st.form_submit_button("Submit")
    st.session_state["topic"] = topic
    if topic=="":
        st.stop()
    # if topic not in ["Clean energy", "Green hydrogen", "Agri tech", "Water irrigation systems"]:
    #     st.stop()
    display_news(topic)
    with st.form("Enter URLs"):
        urls = st.text_input("Enter URLs:")
        st.form_submit_button("Submit")
    if urls=="": st.stop()
    try:
        urls = eval(urls)
    except:
        st.info("Enter URLs in a the format: ['www.example1.com', 'www.example2.com']")
        st.stop()

    if len(urls) == 0:
        st.stop()
    
    url_insights(urls, topic)

    

    # folder_location = r'C:\Users\Dell\Downloads\Strategic_planning_siemens\strategic_intelligence\app\utils\pdf_web' 
    # pdf_from_web(urls, folder_location)

    # st.success("PDFs downloaded successfully!")
    
    