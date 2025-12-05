import google.generativeai as genai
import os
import json

class ShortTermMemory:
    def __init__(self):
        self.memory = {}

    def add_interaction(self, user_request, strategy_model_decision, pdf_collections_decision, rag_queries):
        interaction_id = len(self.memory) + 1
        self.memory[interaction_id] = {
            "user_request": user_request,
            "strategy_model_decision": strategy_model_decision,
            "pdf_collections_decision": pdf_collections_decision,
            "rag_queries": rag_queries
        }
        return interaction_id

    def get_interaction(self, interaction_id):
        return self.memory.get(interaction_id)

    def update_strategy_model_decision(self, interaction_id, strategy_model_decision):
        if interaction_id in self.memory:
            self.memory[interaction_id]['strategy_model_decision'] = strategy_model_decision
        else:
            raise ValueError(f"No interaction found with ID {interaction_id}")

    def update_pdf_collections_decision(self, interaction_id, pdf_collections_decision):
        if interaction_id in self.memory:
            self.memory[interaction_id]['pdf_collections_decision'] = pdf_collections_decision
        else:
            raise ValueError(f"No interaction found with ID {interaction_id}")

    def update_rag_queries_decision(self, interaction_id, rag_queries):
        if interaction_id in self.memory:
            self.memory[interaction_id]['rag_queries'] = rag_queries
        else:
            raise ValueError(f"No interaction found with ID {interaction_id}")