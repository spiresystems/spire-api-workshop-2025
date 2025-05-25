import os
import json
import requests
from function_definitions import get_function_schemas
import os

OPENAI_API_KEY = ""

SYSTEM_PROMPT = (
    "You are an assistant for a sales order entry clerk using an accounting system called Spire. "
)

def parse_query(user_input: str, previous_response_id: str) -> dict:
    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    tools = get_function_schemas()

    body = {
        "model": "gpt-4.1",
        "input": user_input,
        "instructions": SYSTEM_PROMPT,
        "temperature": 0.2,
        "tool_choice": "auto",
        "tools": tools,
        "previous_response_id": previous_response_id
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code != 200:
        raise ValueError(f"OpenAI API error {response.status_code}: {response.text}")
    
    try:
        data = response.json()
        return data  

    except Exception as e:
        raise ValueError(f"Failed to parse response: {e}")

def continue_conversation_with_tool_result(previous_response_id, tool_outputs):
    url = "https://api.openai.com/v1/responses"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "gpt-4.1",
        "input": tool_outputs,
        "previous_response_id": previous_response_id
    }

    response = requests.post(url, headers=headers, json=body)
    if response.status_code != 200:
        raise ValueError(f"OpenAI API error: {response.status_code} - {response.text}")
    
    return response.json()

