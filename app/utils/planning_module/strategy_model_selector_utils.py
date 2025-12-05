import google.generativeai as genai
import os
import json
from .stm_utils import ShortTermMemory

stm = ShortTermMemory()
interaction_id = stm.add_interaction(
    user_request="",
    strategy_model_decision="",
    pdf_collections_decision=[""],
    rag_queries=[""]
)


strategy_tools = {
    "swot_analysis": "SWOT analysis is a strategic planning technique used to identify Strengths, Weaknesses, Opportunities, and Threats related to a project or business.",
    "six_pager": "A Six Pager is a concise document that includes Introduction, Goals, Tenets, State of the Business, Lessons Learned, and Strategic Priorities. It provides a short overview of a project or business.",
    "strategic_recommendations": "Strategic Recommendations include various strategies such as maxi-maxi, maxi-mini, mini-maxi, and mini-mini strategies, which are used to make decisions based on maximizing benefits or minimizing risks."
}

def select_strategy_tool(stm, interaction_id):

    interaction = stm.get_interaction(interaction_id)
    if interaction is None:
        raise ValueError("No interaction found for the given ID")

    user_request = interaction['user_request']


    # Prompt the model with user input and descriptions of the strategy tools
    prompt = f"I need help selecting a strategy tool for the following: {user_request}.\n\n"
    prompt += "1. SWOT Analysis: SWOT analysis is a strategic planning technique used to identify Strengths, Weaknesses, Opportunities, and Threats related to a project or business.\n"
    prompt += "2. Six Pager: A Six Pager is a concise document that includes Introduction, Goals, Tenets, State of the Business, Lessons Learned, and Strategic Priorities. It provides a short overview of a project or business.\n"
    prompt += "3. Strategic Recommendations: Strategic Recommendations include various strategies such as maxi-maxi, maxi-mini, mini-maxi, and mini-mini strategies, which are used to make decisions based on maximizing benefits or minimizing risks.\n\n"
    prompt += "Based on the provided information, recommend the best strategy tool.\n"
    prompt += "Return the response in The form of a json as follows {'strategy_model' : 'recommended_tool'}. Ensure the response can be parsed by Python json.loads"

    # Call the model to generate a response
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    # Parse the model's response
    recommended_tool = response.text

    stm.update_strategy_model_decision(interaction_id, recommended_tool)

    # recommended_tool = json.loads(recommended_tool)['strategy_model']

    return recommended_tool
