import uuid
import spire_client
import json
from chatgpt_parser import parse_query, continue_conversation_with_tool_result
from function_definitions import get_function_names

conversation_state = {
    "last_response_id": None
}

# Dispatch OpenAI tool call to actual Python function
def run_tool_function(name: str, arguments: dict):
    if not hasattr(spire_client, name):
        raise Exception(f"Unknown tool: {name}")
    fn = getattr(spire_client, name)
    return fn(**arguments)

def agent_loop(user_input: str):
    print(f"User: {user_input}")
    
    # Initial parse
    response_data = parse_query(user_input, previous_response_id=conversation_state["last_response_id"])
    outputs = response_data.get("output", [])
    conversation_state["last_response_id"] = response_data.get("id")

    while True:
        tool_outputs = []
        messages = []

        for output in outputs:
            if output["type"] == "function_call":
                tool_name = output["name"]
                tool_args = json.loads(output["arguments"])
                tool_call_id = output["call_id"]

                print(f"Calling tool: {tool_name} with args: {tool_args}")
                result = run_tool_function(tool_name, tool_args)
                #print(f"Tool result: {result}")

                tool_outputs.append({
                    "type": "function_call_output",
                    "call_id": tool_call_id,
                    "output": json.dumps(result)
                })

            elif output["type"] == "message":
                for content in output.get("content", []):
                    if content["type"] == "output_text":
                        print(f"Assistant: {content['text']}")
                        messages.append(content["text"])

        # If there are tool outputs, send them together and continue loop
        if tool_outputs:
            response_data = continue_conversation_with_tool_result(
                previous_response_id=conversation_state["last_response_id"],
                tool_outputs=tool_outputs
            )
            outputs = response_data.get("output", [])
            conversation_state["last_response_id"] = response_data.get("id")
            continue

        # Otherwise, we assume we're done and print collected messages
        if messages:
            return messages[-1]  # Return the last one (if needed)

        print("No further response from model.")
        return None
