import google.generativeai as genai
import os
import json

# Dictionary containing PDF titles and their definitions
pdfs = {
    "Siemens_report_fy2023": "It is a combined management report of Siemens for the fiscal year 2023 which includes financial performance system, segment information for all industries Siemens work in, results of operation, Financial position and report on expected developments and associated material opportunities and risks",
    "McKinsey_report for creating a more sustainable, inclusive and growing future for all": "The McKinsey report on sustainable development which provides a comprehensive overview of the firm's efforts to accelerate sustainable growth and combat global challenges through collaborative initiatives with clients, highlighting achievements in decarbonization and inclusive economic development.",
    "McKinsey_report on the role of business towards a sustainable future": "The McKinsey report on sustainable development emphasizes the urgent need for collaborative partnerships to address global challenges, especially in the wake of the COVID-19 pandemic. It advocates for international cooperation to achieve sustainable and inclusive growth, highlighting the importance of cross-border collaboration in areas such as fair trade, climate transitions, and humanitarian relief to foster global economic resilience.",
    "BCG report on energy transition": "The BCG report on sustainable development emphasizes the urgent need for a net zero energy transition to mitigate environmental and economic risks. It outlines key actions for stakeholders and aims to provide clarity and guidance, fostering collaboration and informed decision-making. Designed as a living document, the report invites feedback and updates to address challenges and promote prosperity through collective action.",
    "SRCCL_ipcc_report": "The SRCCL IPCC report on risk management and decision-making underscores the projected impacts of global temperature rise, including permafrost and coastal degradation, increased wildfires, and diminished crop yields and food stability. It highlights the urgency for action based on high-confidence evidence of these outcomes, emphasizing the need for robust risk management strategies to address these challenges and foster sustainable development.",
    "55 tech leaders to watch i 2024": "The report by ABI Research offers actionable insights into the dynamic technology landscape. Through comprehensive Competitive Rankings, it identifies top companies based on implementation and innovation strategies, providing valuable guidance for businesses navigating the complex tech environment.",
    "82 tech trends that will and will not shape 2024": "ABI Research's report provides a comprehensive analysis of the evolving technology landscape amid global challenges. It identifies key trends, such as AI advancements and emerging solutions like RedCap and PQC, while addressing factors like inflation and supply chain disruptions. With 45 predictions of anticipated developments and 37 predictions of stagnation, the report offers valuable insights for navigating technology markets in the year ahead.",
    "Cybersecurity Opportunities": "The report by ABI Research delves into the current landscape of industrial cybersecurity, exploring key topics such as technology and market trends, cybersecurity spending in critical infrastructure, and the maturity and demand for cybersecurity in industrial operations. With a focus on Siemens as a case study, the report identifies pain points and offers insights on how ABI Research can assist stakeholders in addressing cybersecurity challenges within industrial settings",
    "Gen AI PC arms race": "The report examines the rapid evolution of on-device generative Artificial Intelligence (AI) inferencing capabilities, particularly within the realm of Personal Computers (PCs). Enabled by advancements in compression techniques and hardware performance, including the integration of AI accelerators, AI inferencing is transitioning from cloud environments to resource-constrained devices like PCs and smartphones. This report highlights the significant progress made by major Original Equipment Manufacturers (OEMs) and chip vendors in developing solutions capable of handling AI inference workloads on-device.",
    "Key Takeaways from CES 2024": "The report provides concise insights into the trends and innovations showcased at the Consumer Electronics Show. Organized into sections such as first impressions, standout innovations, missed opportunities, and final thoughts, the report covers key areas like Augmented & Virtual Reality, IoT, Smart Home & Buildings, Smart Mobility & Automotive, and Supply Chain Management & Logistics. With expert analysis from our team, this report offers valuable perspectives on the evolving consumer electronics landscape in 2024",
    "Supply chain management and logistics": "The report provides insights into key industry aspects, including ecosystem activity, market opportunities, disruptive threats, and strategic guidance for end users and technology vendors. It covers areas such as freight transport, last-mile delivery, retail, e-commerce, warehouse operations, supply chain software, multimodal transportation, global supply chain dynamics, government regulations, and commercial telematics connections. This comprehensive resource offers valuable insights for understanding current trends and future developments in supply chain management and logistics.",
    "Supply Chain Control Towers": "The report introduces SCCTs, centralized dashboards aggregating supply chain data for real-time insights. They enhance collaboration and efficiency by providing essential metrics and visibility across different functions, with advanced versions leveraging AI for comprehensive End-to-End (E2E) visibility and alignment."
    # Add more PDF titles and descriptions as needed
}

def select_pdf(stm, interaction_id):

    interaction = stm.get_interaction(interaction_id)
    if interaction is None:
        raise ValueError("No interaction found for the given ID")

    user_request = interaction['user_request']
    strategy_tool = interaction['strategy_model_decision']

    # Prompt the model with user query and PDF titles with descriptions
    prompt = f"I need help selecting a PDF relevant to the following query: {user_request} and also relevant to the following strategic model: {strategy_tool}.\n\n"
    for title, definition in pdfs.items():
        prompt += f"{title}: {definition}\n"
    prompt += "\nBased on the provided information, recommend the most relevant PDF.\n"
    prompt += "Return the response in the form of a JSON as follows: {'selected_pdf': pdf_title}. Ensure the response can be parsed by Python json.loads."

    # Call the model to generate a response
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    # Parse the model's response
    selected_pdf = response.text
    # selected_pdf = json.loads(selected_pdf)['selected_pdf']

    stm.update_pdf_collections_decision(interaction_id, selected_pdf)

    return selected_pdf

