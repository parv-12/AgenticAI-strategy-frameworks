import google.generativeai as genai
import os
import json


# Generic prompts for SWOT Analysis
SWOT_prompts = {
    "Strengths": [
        "Key findings in the environmental sector for {topic}",
        "Governance factors related to {topic}",
        "Social factors related to {topic}",
        "Emerging trends in the {topic}"
    ],
    "Weaknesses": [
        "Cultural or structural barriers that impede our responsiveness to change for {topic}",
        "Areas of improvement for {topic}",
        "{topic} performance against industry standards"
    ],
    "Opportunities": [
        "Market dynamics and technological levers for {topic}",
        "Potential growth areas for the {topic}",
        "Technologies related to {topic}",
        "Emerging trends in the {topic}",
        "Opportunities in {topic}"
    ],
    "Threats": [
        "Roadblocks for growth of {topic}",
        "Current and emerging trends in the market that could pose a threat to {topic}",
        "Regulations or compliance requirements to {topic}",
        "Technological advancements could render {topic} obsolete or less competitive",
        "Impact of environmental concerns or regulations on {topic}",
        "Financial risks that could pose a threat to the financial stability of {topic}"
    ]
}

# Generic prompts for Six-Pager
six_pager_prompts = {
    "first-page": [
        "An overview of the {topic} and its significance",
        "Concept and importance of {topic}",
        "A brief introduction to the {topic}"
    ],
    "second-page": [
        "Historical background of the {topic}, highlighting key milestones and developments",
        "The various types or categories within the realm of {topic}, outlining their characteristics and distinctions",
        "Practical guidelines or best practices for navigating {topic}, offering insights and recommendations for effective implementation",
        "The diversity of {topic} by delineating its various types, variants, or subcategories"
    ],
    "third-page": [
        "The major challenges hindering the development of {topic}, considering both internal and external factors",
        "The complexity of {topic} development by examining the interplay of various factors such as technological, socio-economic, and regulatory issues",
        "The evolving landscape of challenges faced by stakeholders in the field of {topic}, considering new threats, opportunities, and uncertainties"
    ],
    "fourth-page": [
        "An overview of existing solutions and innovative approaches aimed at mitigating challenges and overcoming obstacles in the field of {topic}",
        "The potential of emerging technologies in addressing specific challenges and enhancing efficiency in the {topic} sector",
        "The role of policy frameworks, regulations, and governance mechanisms in facilitating solutions to challenges in {topic} development, emphasizing the need for supportive policy environments and regulatory incentives"
    ],
    "fifth-page": [
        "Policy recommendations and strategic interventions aimed at advancing the development of {topic}, taking into account current challenges, emerging trends, and long-term sustainability objectives",
        "Priority areas for technological advancement and investment to address critical challenges and unlock new opportunities in {topic} development",
        "Initiatives and programs for capacity building, skills development, and knowledge transfer to strengthen human capital and institutional capacity in the {topic} sector"
    ],
    "sixth-page": [
        "A strategic action plan outlining key steps and initiatives needed to advance the development of {topic} in the coming years",
        "Strategies for scenario planning, risk assessment, and adaptive management related to the {topic}",
        "A call to action or next steps for {topic}"
    ]
}

# Combine SWOT and six-pager prompts into one dictionary
# generic_prompts = {**SWOT_prompts, **six_pager_prompts}



# The function to generate prompts for vector search.
def generate_vector_search_prompts(stm, interaction_id):

    # Retrieve the interaction details
    interaction = stm.get_interaction(interaction_id)
    if not interaction:
        raise ValueError(f"No interaction found with ID {interaction_id}")


    recommended_tool_str = interaction['strategy_model_decision'].replace("```json\n", "").replace("\n```", "")

    # Convert single quotes to double quotes to make it valid JSON
    recommended_tool_str = recommended_tool_str.replace("'", '"')

    # Now, parse the JSON string into a Python dictionary

    data = json.loads(recommended_tool_str)
    strategy_model_decision = data['strategy_model']
    # print("Strategy Model:", strategy_model)


    # Debug: Print the decision to check its exact value
    print(f"Strategy model decision from STM: {strategy_model_decision}")

    topic = interaction['user_request']  # Assuming this is a specific topic or keyword

    if strategy_model_decision == "SWOT Analysis":
        prompts = SWOT_prompts
    elif strategy_model_decision == "Six Pager":
        prompts = six_pager_prompts
    else:
        raise ValueError(f"Unknown strategy model decision: {strategy_model_decision}")

    # Build the API prompt
    api_prompt = f"For the strategy model '{strategy_model_decision}' related to '{topic}', create specific search queries to find relevant PDFs in a vector database. Here are some generic prompts:\n\n"
    for category, prompt_list in prompts.items():
        api_prompt += f"{category}:\n"
        for p in prompt_list:
            api_prompt += f"- {p.format(topic=topic)}\n"
    api_prompt += "\nGenerate specific prompts to use for a vector search:"
    # Add this line within the function generate_vector_search_prompts before calling the API
    api_prompt += "\nPlease return the search prompts in JSON format that can be parsed by Python json.loads. For example: {\"search_prompts\": [\"prompt 1\", \"prompt 2\"]}"


    # Call the OpenAI API
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(api_prompt)

    # The API response returns a string, which may need to be parsed or formatted
    try:
        vector_search_prompts = response.text
    except json.JSONDecodeError as e:
        raise ValueError("Failed to parse response as JSON: " + str(e))

    stm.update_rag_queries_decision(interaction_id, vector_search_prompts)

    return vector_search_prompts
