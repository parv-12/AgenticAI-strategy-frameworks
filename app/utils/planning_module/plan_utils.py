import google.generativeai as genai
import os
import json


def generate_execution_plan(api_key, stm, interaction_id):
    # Set the API key for OpenAI
    api_key = "AIzaSyBQum-LHBsrq5DIKaEPKhkD5bizYR1eQr4"

    # Retrieve the stored interaction
    interaction = stm.get_interaction(interaction_id)
    if interaction is None:
        raise ValueError("No interaction found for the given ID")

    # Create the prompt for the foundation model
    prompt = f"Given the following details from a strategic session, please create a step-by-step plan of action by deciding the order of tools to be used and how to go about them.\n"
    prompt += f"User Request: {interaction['user_request']}\n"
    prompt += f"Strategy Model Decision: {interaction['strategy_model_decision']}\n"
    prompt += f"PDF Collections Decision: {interaction['pdf_collections_decision']}\n"
    prompt += f"RAG Queries: {interaction['rag_queries']}\n\n"
    prompt += "The available tools are:\n"
    prompt += "- Data Crawler: Crawl internal and external strategic sources.\n"
    prompt += "- Vector Search: Perform vector search with the list of collections based on a strategic model.\n"
    prompt += "- Strategy Model Creators: Use knowledge from vector search/crawler and additional prompts to create models.\n"
    prompt += "- Summarizer: Summarize the findings from the LLM hits.\n\n"
    prompt += "Please create a prioritized list of actions detailing which tool to use first, second, third and last. Provide reasons for the chosen order.\n"


    # Call the OpenAI API to generate the plan
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)

    # Extract the plan from the response
    plan_of_action_text = response.text

    print(plan_of_action_text)

    # try:
    #     plan_of_action = json.loads(plan_of_action_text)
    # except json.JSONDecodeError:
    #     raise ValueError("Failed to parse the plan of action response as JSON")

    # Add payload information to the plan
    # You will need to define how you want to structure this information
    # For example, you may include input data sources or parameters for each tool
    plan_with_payload = {
        "plan_of_action": plan_of_action_text,
        "tool_payloads": {
            "Data Crawler": {
                "input_sources": interaction['pdf_collections_decision'],
                "additional_info": interaction['rag_queries']
            },
            "Vector Search": {
                "query_prompts": interaction['rag_queries'],
                "database": "Vector DB containing PDF collections",
                # Add any other relevant info for Vector Search
            },
            "Strategy Model Creators": {
                "input_data": "Output from Data Crawler and Vector Search",
                # Include other necessary parameters for Strategy Model Creators
            },
            "Summarizer": {
                "input_data": "All collected and processed information",
                # Include other necessary parameters for Summarizer
            }
        }
    }

    # Convert the result to a JSON string if needed
    result_json = json.dumps(plan_with_payload)

    return result_json

    # # Construct the result dictionary
    # result = {
    #     "stm_interaction_id": interaction_id,
    #     "plan_of_action": plan_of_action_text
    # }

    # # Convert the result to a JSON string
    # # result_json = json.dumps(result)

    # return result

