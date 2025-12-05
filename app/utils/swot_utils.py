import streamlit as st
import requests
from utils.gemini_utils import answer_online
from utils.gpt_utils import answer_online_gpt
from utils.qdrant_utils import get_qdrant_context
import os
import json

qdrant_url = os.environ.get("qdrant_url","http://localhost:7000")
# collections = ['BCG_energy_transition', 'Towards_sustainable_development_McKinsey', 'McKinsey_report2', 'srccl_ch7_ipcc', 'siemens_sustainability_report'  ]
siemens_collections = ["Siemens_Report_FY2023", "sustainability-report-fy2023"]
outer_world_reports = [
    "BCGreport_energy_transition",
    "SRCCL_Chapter_7_ipcc",
    "toward-a-sustainable-inclusive-growing-future-the-role-of-business_McKinsey",
    "56297_373_mckinsey_esg_report-2022_aw6_v10_final"
]
global_single_collection = "Chanakya" #"strategic_intelligence_test"
user_prompts = {
    "Managing Board": """I am the Chief People and sustainability officer at Siemens AG. I am a member of the board of Siemens.
                        I came across this topic and want strategic insights for it. 
                        My purpose is to create strategies to cater to Siemens Sustainability goals and provide sustainable solutions from Siemens.""",
    "Technology Manager DAI": """I am the head of a research group in Data analytics and AI at Siemens Technology. I came across this topic and want strategic insights for it. 
                        My purpose is to create a technology roadmap for the topic for research specifically in the field of AI in industry 4.0.""",
    "Research Engineer DAI": """I am a research engineer in Data analytics and AI at Siemens Technology. I came across this topic and want strategic insights for it. 
                        My purpose is to generate new ideas and create new AI driven solution prototypes for the topic."""
}

@st.cache_data
def get_mckinsey_opp(topic):
    prompts = [
        f"Key findings in the environmental sector for {topic}",
        f"Governance factors related to {topic}",
        f"Social factors related to {topic}",
        f"Emerging trends in the {topic}",
        f"Opportunities in {topic}",
        f"Real world examples of {topic}",
        f"Challenges associated with the {topic}"
    ]
    context = ""
    for prompt in prompts:
        data = {
            "queryText": prompt,
            "collectionName": "Towards_sustainable_development_McKinsey",
            "payloadKeys":["Document"]
        }
        context_from_qdrant = requests.post(f"{qdrant_url}/qdrant/answer", #TODO: qdrant host and port in config
                                            json=data, 
                                            headers={"customer-id":"strategic_intelligence"})
        if not context_from_qdrant.status_code==200:
            continue
        context += f"{context_from_qdrant.json()['context']}. "
    if context=="":
        return ""
    gpt_prompt = f"I want to identify opportunities in the {topic} market to achieve some of my sustainable development goals. "
    gpt_prompt += f"Doing a vector search through a mckinsey report the dump around the {topic} is given in the context"
    gpt_prompt += f"Summarize the opportunities for the {topic}"
    return answer_online(gpt_prompt, context)
    # return gpt_prompt

@st.cache_data
def get_mckinsey2_opp(topic):
    prompts = [
        f"Key findings in the environmental sector for {topic}",
        f"Market growth related to {topic}",
        f"Social factors related to {topic}",
        f"Emerging trends in the {topic}",
        f"Opportunities in {topic}",
        f"Real world examples of {topic}"
    ]
    context = ""
    for prompt in prompts:
        data = {
            "queryText": prompt,
            "collectionName": "McKinsey_report2"
        }
        context_from_qdrant = requests.post(f"{qdrant_url}/qdrant/answer",
                                            json=data,
                                            headers={"customer-id":"strategic_intelligence"})
        if not context_from_qdrant.status_code==200:
            continue
        context += f"{context_from_qdrant.json()['context']}. "
    if context=="":
        return ""
    gpt_prompt = f"I want to identify opportunities in the {topic} market to achieve some of my sustainable development goals. "
    gpt_prompt += f"Doing a vector search through a mckinsey report the dump around the {topic} is given in the context"
    gpt_prompt += f"Summarize the opportunities for the {topic}"
    return answer_online(gpt_prompt, context)
    # return gpt_prompt

@st.cache_data
def get_bcg_opp(topic):
    prompts = [
        f"Market dynamics and technological levers for {topic}",
        f"Potential growth areas for the {topic}",
        f"Technologies related to {topic}",
        f"Emerging trends in the {topic}",
        f"Opportunities in {topic}",
        f"Real world examples of {topic}",
        f"Challenges associated with the {topic}"
    ]
    context = ""
    for prompt in prompts:
        data = {
            "queryText": prompt,
            "collectionName": "BCG_energy_transition"
        }
        context_from_qdrant = requests.post(f"{qdrant_url}/qdrant/answer", 
                                            json=data, 
                                            headers={"customer-id":"strategic_intelligence"})
        if not context_from_qdrant.status_code==200:
            continue
        context += f"{context_from_qdrant.json()['context']}. "
    if context=="":
        return ""
    gpt_prompt = f"I want to identify opportunities in the {topic} market to achieve some of my sustainable development goals. "
    gpt_prompt += f"Doing a vector search through a BCG report the dump around the {topic} is given in the context"
    gpt_prompt += f"Summarize the opportunities for the {topic}. If no opportunities are extacted in the vector search return 'No opportunities identified.'"
    return answer_online(gpt_prompt, context)
    # return gpt_prompt

@st.cache_data
def get_ipcc_opp(topic):
    prompts = [
        f"Climate change and {topic}",
        f"Decision making associated with {topic}",
        f"Potential growth areas for the {topic}",
        f"Technologies related to {topic}",
        f"Emerging trends in the {topic}",
        f"Opportunities in {topic}",
        f"Real world examples of {topic}",
        f"Challenges associated with the {topic}"
    ]
    context = ""
    for prompt in prompts:
        data = {
            "queryText": prompt,
            "collectionName": "srccl_ch7_ipcc"
        }
        context_from_qdrant = requests.post(f"{qdrant_url}/qdrant/answer", 
                                            json=data, 
                                            headers={"customer-id":"strategic_intelligence"})
        if not context_from_qdrant.status_code==200:
            continue
        context += f"{context_from_qdrant.json()['context']}. "
    if context=="":
        return ""
    gpt_prompt = f"I want to identify opportunities in the {topic} market to achieve some of my sustainable development goals. "
    gpt_prompt += f"Doing a vector search through a IPCC report the dump around the {topic} is given in the context"
    gpt_prompt += f"Summarize the opportunities for the {topic}. If no opportunities identified or clearly visible from the context return 'No opportunities identified.'"
    return answer_online(gpt_prompt, context)
    # return gpt_prompt

@st.cache_data
def get_siemens_opp(topic):
    prompts = [
        f"Climate change and {topic}",
        f"Decision making associated with {topic}",
        f"Potential growth areas for the {topic}",
        f"Technologies related to {topic}",
        f"Emerging trends in the {topic}",
        f"Opportunities in {topic}",
        f"Real world examples of {topic}",
        f"Challenges associated with the {topic}"
    ]
    context = ""
    for prompt in prompts:
        data = {
            "queryText": prompt,
            "collectionName": "siemens_sustainability_report"
        }
        context_from_qdrant = requests.post(f"{qdrant_url}/qdrant/answer", 
                                            json=data, 
                                            headers={"customer-id":"strategic_intelligence"})
        if not context_from_qdrant.status_code==200:
            continue
        context += f"{context_from_qdrant.json()['context']}. "
    if context=="":
        return ""
    gpt_prompt = f"I want to identify opportunities in the {topic} market to achieve some of my sustainable development goals. "
    gpt_prompt += f"Doing a vector search through a Siemens report the dump around the {topic} is given in the context"
    gpt_prompt += f"Summarize the opportunities for the {topic}. If no opportunities identified or clearly visible from the context return 'No opportunities identified.'"
    return answer_online(gpt_prompt, context)

@st.cache_data
def get_mckinsey_threats(topic):
    prompts = [
        f"Roadblocks for growth of {topic}",
        f"Current and emerging trends in the market that could pose a threat to {topic}",
        f"Regulations or compliance requirements to {topic}",
        f"Technological advancements could render {topic} obsolete or less competitive",
        f"Impact of environmental concerns or regulations on {topic}",
        f"Financial risks that could pose a threat to the financial stability of {topic}",
        f"Leading market players for {topic} in the industry",
        f"current market share for {topic} among the leading competitors"
    ]
    context = ""
    for prompt in prompts:
        data = {
            "queryText": prompt,
            "collectionName": "Towards_sustainable_development_McKinsey",
            "payloadKeys":["Document"]
        }
        context_from_qdrant = requests.post(f"{qdrant_url}/qdrant/answer",
                                            json=data,
                                            headers={"customer-id":"strategic_intelligence"})
        if not context_from_qdrant.status_code==200:
            continue
        context += f"{context_from_qdrant.json()['context']}. "
    if context=="":
        return ""
    gpt_prompt = f"I want to identify threats in the {topic} market to achieve some of my sustainable development goals. "
    gpt_prompt += f"Doing a vector search through a Mckinsey report the dump around the {topic} is given in the context"
    gpt_prompt += f"Summarize the threats for the {topic}. If no threats are extacted in the vector search return 'No threats identified.'"
    return answer_online(gpt_prompt, context)
    # return gpt_prompt

@st.cache_data
def get_mckinsey2_threats(topic):
    prompts = [
        f"Roadblocks for growth of {topic}",
        f"Current and emerging trends in the market that could pose a threat to {topic}",
        f"Regulations or compliance requirements to {topic}",
        f"Technological advancements could render {topic} obsolete or less competitive",
        f"Impact of environmental concerns or regulations on {topic}",
        f"Financial risks that could pose a threat to the financial stability of {topic}",
        f"Leading market players for {topic} in the industry",
        f"current market share for {topic} among the leading competitors"
    ]
    context = ""
    for prompt in prompts:
        data = {
            "queryText": prompt,
            "collectionName": "McKinsey_report2"
        }
        context_from_qdrant = requests.post(f"{qdrant_url}/qdrant/answer",
                                            json=data,
                                            headers={"customer-id":"strategic_intelligence"})
        if not context_from_qdrant.status_code==200:
            continue
        context += f"{context_from_qdrant.json()['context']}. "
    if context=="":
        return ""
    gpt_prompt = f"I want to identify threats in the {topic} market to achieve some of my sustainable development goals. "
    gpt_prompt += f"Doing a vector search through a Mckinsey report the dump around the {topic} is given in the context"
    gpt_prompt += f"Summarize the threats for the {topic}. If no threats are extacted in the vector search return 'No threats identified.'"
    return answer_online(gpt_prompt, context)
    # return gpt_prompt

@st.cache_data
def get_bcg_threats(topic):
    prompts = [
        f"Roadblocks for growth of {topic}",
        f"Current and emerging trends in the market that could pose a threat to {topic}",
        f"Regulations or compliance requirements to {topic}",
        f"Technological advancements could render {topic} obsolete or less competitive",
        f"Impact of environmental concerns or regulations on {topic}",
        f"Financial risks that could pose a threat to the financial stability of {topic}",
        f"Challenges associated with the {topic}",
        f"Leading market players for {topic} in the industry",
        f"current market share for {topic} among the leading competitors"
    ]
    context = ""
    for prompt in prompts:
        data = {
            "queryText": prompt,
            "collectionName": "BCG_energy_transition"
        }
        context_from_qdrant = requests.post(f"{qdrant_url}/qdrant/answer",
                                            json=data,
                                            headers={"customer-id":"strategic_intelligence"})
        if not context_from_qdrant.status_code==200:
            continue
        context += f"{context_from_qdrant.json()['context']}. "
    if context=="":
        return ""
    gpt_prompt = f"I want to identify threats in the {topic} market to achieve some of my sustainable development goals. "
    gpt_prompt += f"Doing a vector search through a BCG report the dump around the {topic} is given in the context"
    gpt_prompt += f"Summarize the threats for the {topic}. If no threats are extacted in the vector search return 'No threats identified.'"
    return answer_online(gpt_prompt, context)
    # return gpt_prompt

@st.cache_data
def get_ipcc_threats(topic):
    prompts = [
        f"Roadblocks for growth of {topic}",
        f"Current and emerging trends in the market that could pose a threat to {topic}",
        f"Regulations or compliance requirements to {topic}",
        f"Technological advancements could render {topic} obsolete or less competitive",
        f"Impact of environmental concerns or regulations on {topic}",
        f"Financial risks that could pose a threat to the financial stability of {topic}",
        f"Leading market players for {topic} in the industry",
        f"current market share for {topic} among the leading competitors"
    ]
    context = ""
    for prompt in prompts:
        data = {
            "queryText": prompt,
            "collectionName": "srccl_ch7_ipcc"
        }
        context_from_qdrant = requests.post(f"{qdrant_url}/qdrant/answer",
                                            json=data,
                                            headers={"customer-id":"strategic_intelligence"})
        if not context_from_qdrant.status_code==200:
            continue
        context += f"{context_from_qdrant.json()['context']}. "
    if context=="":
        return ""
    gpt_prompt = f"I want to identify threats in the {topic} market to achieve some of my sustainable development goals. "
    gpt_prompt += f"Doing a vector search through a IPCC report the dump around the {topic} is given in the context"
    gpt_prompt += f"Summarize the threats for the {topic}. If no threats are extacted in the vector search return 'No threats identified.'"
    return answer_online(gpt_prompt, context)
    # return gpt_prompt

@st.cache_data
def get_siemens_threats(topic):
    prompts = [
        f"Roadblocks for growth of {topic}",
        f"Current and emerging trends in the market that could pose a threat to {topic}",
        f"Regulations or compliance requirements to {topic}",
        f"Technological advancements could render {topic} obsolete or less competitive",
        f"Impact of environmental concerns or regulations on {topic}",
        f"Financial risks that could pose a threat to the financial stability of {topic}",
        f"Leading market players for {topic} in the industry",
        f"current market share for {topic} among the leading competitors"
    ]
    context = ""
    for prompt in prompts:
        data = {
            "queryText": prompt,
            "collectionName": "siemens_sustainability_report"
        }
        context_from_qdrant = requests.post(f"{qdrant_url}/qdrant/answer",
                                            json=data,
                                            headers={"customer-id":"strategic_intelligence"})
        if not context_from_qdrant.status_code==200:
            continue
        context += f"{context_from_qdrant.json()['context']}. "
    if context=="":
        return ""
    gpt_prompt = f"I want to identify threats in the {topic} market to achieve some of my sustainable development goals. "
    gpt_prompt += f"Doing a vector search through a Siemens report the dump around the {topic} is given in the context"
    gpt_prompt += f"Summarize the threats for the {topic}. If no threats are extacted in the vector search return 'No threats identified.'"
    return answer_online(gpt_prompt, context)
    # return gpt_prompt

def get_strengths(topic):
    def get_strengths_from_source(collection_name):
        # prompts = [
        #     f"Key findings in the environmental sector for {topic}",
            # f"Governance factors related to {topic}",
            # f"Social factors related to {topic}",
        #     f"Emerging trends in the {topic}",
        #     f"opportunities in {topic}",
        #     f"Real-world examples of {topic}",
        #     f"Challenges associated with the {topic}"
        # ]  # Define prompts specific to the collection here
        prompts = [
            f"Position in the {topic} market",
            f"Major achievements for Siemens in the {topic}",
            f"Governance factors related to {topic}",
            f"Social factors related to {topic}",
            # f"Innovative technologies developed by Siemens in the {topic} market",
            f"in the research and development of the {topic}",
            # f"How is Siemens perceived by stakeholders in relation to its {topic} initiatives"
        ]

        context = ""
        images = []
        for prompt in prompts:
            context_from_qdrant, prompt_images = get_qdrant_context(collection_name, prompt)
            
            # print("Response status code:", context_from_qdrant.status_code)
            # print("Response text:", context_from_qdrant.json())

            if context_from_qdrant is not None :
                context += f"{context_from_qdrant}. "
                if len(prompt_images)>0:
                    images.extend(prompt_images[:2]) #Concatenating only first 2 images if they come

        return context, images

    total_context = ""
    images = []
    for collection_name in siemens_collections:
        context, collection_images = get_strengths_from_source(collection_name)
        if(len(collection_images)>0):
            images.extend(collection_images)
        total_context += f"{collection_name}: {context}"
    # collection_siemens = global_single_collection #"siemens_sustainability_report"
    # total_context, images = get_strengths_from_source(collection_siemens)
    user = st.session_state["user"]
    user_prompt = user_prompts[user]
    gpt_prompt = user_prompt + f" The context is a dump of information around the topic {topic}. Generate some strengths for the topic {topic}. This will help me create the strengths part of a SWOT analysis"
    gpt_prompt += "Answer in less than 200 words and in bullet points preferably"
    # st.write(len(total_context.split(" ")))
    # st.stop()
    # stx.scrollableTextbox(f"{user} + {gpt_prompt} + {total_context}",200,key="strengths_test")
<<<<<<< HEAD
    final_strengths = answer_online(gpt_prompt, total_context)
=======
    with open("./../strengths.json", "w") as f:
        json.dump({"Context":total_context},f,indent=4)
        f.close()
    
    final_strengths = answer_online_gpt(gpt_prompt, total_context)
>>>>>>> d133e39a54a7e5702bf800f7caf4f54679b3c274
    return final_strengths, images

def get_weaknesses(topic):
    def get_weaknesses_from_source(collection_name):
        # prompts = [
        # f"Key resource constraints, such as budget, manpower, or technology, that may hinder our effectiveness for {topic}",
        # f"Where are the bottlenecks or inefficiencies in our processes for {topic}",
        # f"Are there weaknesses in our quality control processes for {topic}",
        # f"cultural or structural barriers that impede our responsiveness to change for {topic}",
        # f"Areas of improvement for Siemens in {topic}",
        # f"Siemens performance in {topic} market against industry standards"
        #]  # Define prompts specific to the collection here
        prompts = [
            f"Main challenges ahead for {topic} market",
            f"Investments in the {topic} by Siemens businesses"
            f"Technological limitations in the {topic}",
            f"Research and development investments in {topic}",
            f"Areas of improvement for Siemens in {topic}",
            f"Future plans for {topic} market"
        ]
        context = ""
        images = []
        for prompt in prompts:
            context_from_qdrant, prompt_images = get_qdrant_context(collection_name, prompt)
            
            # print("Response status code:", context_from_qdrant.status_code)
            # print("Response text:", context_from_qdrant.json())

            if context_from_qdrant is not None :
                context += f"{context_from_qdrant}. "
                if len(prompt_images)>0:
                    images.extend(prompt_images[:2]) #Concatenating only first 2 images if they come

        return context, images

    total_context = ""
    images = []
    for collection_name in siemens_collections:
        context, collection_images = get_weaknesses_from_source(collection_name)
        if(len(collection_images)>0):
            images.extend(collection_images)
        total_context += f"{collection_name}: {context}"
    # total_context, images = get_weaknesses_from_source(global_single_collection)
    user = st.session_state["user"]
    user_prompt = user_prompts[user]
    gpt_prompt = user_prompt + f" The context is a dump of information around the topic {topic}. Generate some weaknesses for Siemens for the topic {topic}. This will help me create the weaknesses part of a SWOT analysis"
    gpt_prompt += "Answer in less than 200 words and in bullet points preferably"
    # stx.scrollableTextbox(f"{user} + {gpt_prompt} + {total_context}",200,key="weaknesses_test")
<<<<<<< HEAD
    final_weaknesses = answer_online(gpt_prompt, total_context)
=======
    with open("./../weaknesses.json", "w") as f:
        json.dumps({"Context":total_context})
    final_weaknesses = answer_online_gpt(gpt_prompt, total_context)
>>>>>>> d133e39a54a7e5702bf800f7caf4f54679b3c274
    return final_weaknesses, images

def get_opportunities(topic):
    def get_opportunities_from_source(collection_name):
        prompts = [
            f"Opportunities in the {topic} market",
            f"Latest developments in the {topic}",
            f"Funding in the areas of {topic}",
            # f"Areas of improvement for Siemens in {topic}",
            # f"Decision making associated with {topic}",
            f"Potential growth areas for the {topic}",
            f"Technologies related to {topic}",
            f"Emerging trends in the {topic}",
            f"Startups working on technologies related to the {topic}"
        ]
        context = ""
        images = []
        for prompt in prompts:
            context_from_qdrant, prompt_images = get_qdrant_context(collection_name, prompt)
            
            # print("Response status code:", context_from_qdrant.status_code)
            # print("Response text:", context_from_qdrant.json())

            if context_from_qdrant is not None :
                context += f"{context_from_qdrant}. "
                if len(prompt_images)>0:
                    images.extend(prompt_images[:2]) #Concatenating only first 2 images if they come

        return context, images

    total_context = ""
    images = []
    for collection_name in outer_world_reports:
        context, collection_images = get_opportunities_from_source(collection_name)
        if(len(collection_images)>0):
            images.extend(collection_images)
        total_context += f"{collection_name}: {context}"
    # total_context, images = get_opportunities_from_source(global_single_collection)
    user = st.session_state["user"]
    user_prompt = user_prompts[user]
    gpt_prompt = user_prompt + f" The context is a dump of information around the topic {topic}. Generate some Opportunities for Siemens for the topic {topic}. This will help me create the opportunities part of a SWOT analysis"
    gpt_prompt += "Answer in less than 200 words and in bullet points preferably"
    # stx.scrollableTextbox(f"{user} + {gpt_prompt} + {total_context}",200,key="weaknesses_test")
    # final_opportunities = ""
    # if len(total_context)>100000:
    #     for i in range(len(total_context),100000):
    #         final_opportunities += answer_online(gpt_prompt,total_context[:i])
    # else:
<<<<<<< HEAD
    final_opportunities = answer_online(gpt_prompt, total_context)
=======
    with open("./../opp.json", "w") as f:
        json.dumps({"Context":total_context})
    final_opportunities = answer_online_gpt(gpt_prompt, total_context)
>>>>>>> d133e39a54a7e5702bf800f7caf4f54679b3c274
    return final_opportunities, images

def get_threats(topic):
    def get_threats_from_source(collection_name):
        prompts = [
            f"Roadblocks for growth of {topic}",
            f"Current and emerging trends in the market that could pose a threat to {topic}",
            f"Regulations or compliance challenges for {topic}",
            f"Financial risks that could pose a threat to the financial stability of {topic}",
            f"Risks related to the {topic} market"
        ]
        context = ""
        images = []
        for prompt in prompts:
            context_from_qdrant, prompt_images = get_qdrant_context(collection_name, prompt)
            
            # print("Response status code:", context_from_qdrant.status_code)
            # print("Response text:", context_from_qdrant.json())

            if context_from_qdrant is not None :
                context += f"{context_from_qdrant}. "
                if len(prompt_images)>0:
                    images.extend(prompt_images[:2]) #Concatenating only first 2 images if they come

        return context, images

    total_context = ""
    images = []
    for collection_name in outer_world_reports:
        context, collection_images = get_threats_from_source(collection_name)
        if(len(collection_images)>0):
            images.extend(collection_images)
        total_context += f"{collection_name}: {context}"
    # total_context, images = get_threats_from_source(global_single_collection)
    user = st.session_state["user"]
    user_prompt = user_prompts[user]
    gpt_prompt = user_prompt + f" The context is a dump of information around the topic {topic}. Generate some threats for Siemens for the topic {topic}. This will help me create the threats part of a SWOT analysis"
    gpt_prompt += "Answer in less than 200 words and in bullet points preferably"
    # stx.scrollableTextbox(f"{user} + {gpt_prompt} + {total_context}",200,key="weaknesses_test")
<<<<<<< HEAD
    final_threats = answer_online(gpt_prompt, total_context)
=======
    with open("./../threats.json", "w") as f:
        json.dumps({"Context":total_context})
    final_threats = answer_online_gpt(gpt_prompt, total_context)
>>>>>>> d133e39a54a7e5702bf800f7caf4f54679b3c274
    return final_threats, images

def maxi_maxi_strategy(topic):
    strenghts, images = get_strengths(topic)
    opportunities, images = get_opportunities(topic)
    user = st.session_state["user"]
    user_prompt = user_prompts[user]
    prompt = user_prompt + f" Generate a comprehensive strategy for a maxi-maxi approach based on the identified strengths and opportunities. "
    prompt += "Consider how the strengths can be leveraged to maximize positive outcomes, and explore potential opportunities for achieving optimal results. "
    prompt += "Provide actionable insights, innovative ideas, and potential collaborative efforts that align with the maxi-maxi strategy. "
    prompt += "The goal is to formulate a strategic plan that capitalizes on internal strengths and external opportunities to achieve the maximum positive impact."

    context = f"Strengths: {strenghts}, opportunities: {opportunities}"

    return answer_online(prompt, context)

def maxi_mini_strategy(topic):
    strenghts, images = get_strengths(topic)
    threats, images = get_threats(topic)
    user = st.session_state["user"]
    user_prompt = user_prompts[user]
    prompt = user_prompt + f" Generate a strategic plan for a maxi-mini approach by leveraging the identified strengths and mitigating potential threats. "
    prompt += "Explore how the inherent strengths can be maximized to achieve positive outcomes while addressing and minimizing the impact of potential threats. "
    prompt += "Provide insights into innovative risk mitigation strategies, resource optimization, and collaborative efforts that align with the maxi-mini strategy. "
    prompt += "The objective is to formulate a balanced approach that capitalizes on internal strengths while effectively managing external threats."

    context = f"Strengths: {strenghts}, Threats: {threats}"

    return answer_online(prompt, context)

def mini_maxi_strategy(topic):
    weaknesses, images = get_weaknesses(topic)
    opportunities, images = get_opportunities(topic)
    
    user = st.session_state["user"]
    user_prompt = user_prompts[user]
    prompt = user_prompt + f" Formulate a strategic plan for a mini-maxi approach by addressing the identified weaknesses and capitalizing on available opportunities. "
    prompt += "Explore how weaknesses can be mitigated or turned into strengths to minimize negative impacts, while simultaneously leveraging opportunities to achieve maximum positive outcomes. "
    prompt += "Provide actionable insights into innovative approaches, resource optimization, and collaborative efforts that align with the mini-maxi strategy. "
    prompt += "The goal is to create a balanced approach that addresses internal weaknesses while maximizing the potential offered by external opportunities."

    context = f"Weaknesses: {weaknesses}, opportunities: {opportunities}"

    return answer_online(prompt, context)

def mini_mini_strategy(topic):
    weaknesses, images = get_weaknesses(topic)
    threats, images = get_threats(topic)
    
    user = st.session_state["user"]
    user_prompt = user_prompts[user]
    prompt = user_prompt + f" Develop a strategic plan for a mini-mini approach, focusing on mitigating the identified weaknesses and addressing potential threats. "
    prompt += "Explore how weaknesses can be minimized to reduce negative impacts, and strategize ways to proactively manage and mitigate potential threats. "
    prompt += "Provide actionable insights into innovative risk mitigation strategies, resource optimization, and collaborative efforts that align with the mini-mini strategy. "
    prompt += "The objective is to formulate a balanced approach that addresses internal weaknesses while effectively managing external threats."

    context = f"Weaknesses: {weaknesses}, Threats: {threats}"

    return answer_online(prompt, context)

# def get_threats(topic):
#     threats_mckinsey = get_mckinsey_threats(topic),
#     threats_mckinsey2 = get_mckinsey2_threats(topic)
#     threats_bcg = get_bcg_threats(topic)
#     threats_ipcc = get_ipcc_threats(topic)
#     threats_siemens = get_siemens_threats(topic)
#     total_context = f"""Mckinsey: {threats_mckinsey}\n{threats_mckinsey2}, 
#                         BCG: {threats_bcg}
#                     """
#     user = st.session_state["user"]
#     user_prompt = user_prompts[user]
#     gpt_prompt = user_prompt + f" The context is a dump of information around the topic {topic}. Generate some threats for the topic {topic}. This will help me create the threats part of a SWOT analysis"
#     gpt_prompt += "Answer in less than 200 words and in bullet points preferably"
#     # stx.scrollableTextbox(f"{user} + {gpt_prompt} + {total_context}",200,key="threats_test")
#     final_threats = answer_online(gpt_prompt, total_context)

#     total_context = f"""IPCC: {threats_ipcc}
#                     """
#     # stx.scrollableTextbox(f"{user} + {gpt_prompt} + {total_context}",200,key="threats_test2")
#     final_threats += answer_online(gpt_prompt, total_context)
    # return final_threats

# def get_opportunities(topic):
#     opp_mckinsey = get_mckinsey_opp(topic)
#     opp_mckinsey2 = get_mckinsey2_opp(topic)
#     opp_bcg = get_bcg_opp(topic)
#     opp_ipcc = get_ipcc_opp(topic)
#     total_context = f"""Mckinsey: {opp_mckinsey},
#                         Mckinsey2: {opp_mckinsey2}, 
#                         BCG: {opp_bcg}
#                     """
#     user = st.session_state["user"]
#     user_prompt = user_prompts[user]
#     gpt_prompt = user_prompt + f" The context is a dump of information around the topic {topic}. Generate some opportunities for the topic {topic}. This will help me create the opportunities part of a SWOT analysis"
#     gpt_prompt += "Answer in less than 200 words and in bullet points preferably"
#     # stx.scrollableTextbox(f"{user} + {gpt_prompt} + {total_context}",200,key="opp_test1")
#     final_opp = answer_online(gpt_prompt, total_context)
    
#     total_context = f"""Mckinsey: {opp_mckinsey}
#                     """
#     # st.write(total_context)
#     # stx.scrollableTextbox(f"{user} + {gpt_prompt} + {total_context}",200,key="opp_test2")
#     final_opp = answer_online(gpt_prompt, total_context)

#     total_context = f"""ipcc: {opp_ipcc}
#                     """
#     # stx.scrollableTextbox(f"{user} + {gpt_prompt} + {total_context}",200,key="opp_test3")
#     final_opp += "\n"+answer_online(gpt_prompt, total_context)
#     return final_opp