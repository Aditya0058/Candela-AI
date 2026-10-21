from flask import Flask, request, jsonify
from flask_cors import CORS 
from agent.tools import ALL_TOOLS, TOOL_FUNCTIONS
import requests
import sqlite3
import uuid
import os
import json

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# database routes below
@app.route('/api/chats', methods=['GET'])
def get_chats():
    conn = sqlite3.connect('candela.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM chats ORDER BY created_at DESC")
    rows = cursor.fetchall()

    chats = [dict(row) for row in rows]

    conn.close()
    return jsonify(chats)

@app.route('/api/chats', methods=['POST'])
def create_chat():
    data = request.json
    chat_id = data.get('id')
    title = data.get('title')

    conn = sqlite3.connect('candela.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats (id, title) VALUES (?, ?)", 
        (chat_id, title)
    )
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "id": chat_id}), 201

@app.route('/api/chats/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    conn = sqlite3.connect('candela.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM chats WHERE id = ?', (chat_id,))

    conn.commit()
    conn.close()
    return jsonify({"status": "success"}), 200

# getting  data from datbase
@app.route('/api/chats/<chat_id>/messages', methods=['GET'])
def get_chat_messages(chat_id):
    conn = sqlite3.connect('candela.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM messages WHERE chat_id = ? ORDER BY created_at ASC", (chat_id,))
    rows = cursor.fetchall()

    messages = [dict(row) for row in rows]

    conn.close()
    return jsonify(messages)


# AI chatting routes below
def process_tool_calls(message_obj):
        # SAFETY CHECK: If the AI returned a plain string instead of a dict
    if isinstance(message_obj, str):
        return {"called": False, "content": message_obj}

    if "tool_calls" in message_obj and message_obj["tool_calls"]:
        tool_call = message_obj["tool_calls"][0]
        function_name = tool_call["function"]["name"]
        
        # OpenAI sends arguments as a JSON string. Ollama sends them as a dict.
        args = tool_call["function"]["arguments"]
        if isinstance(args, str):
            arguments = json.loads(args)
        else:
            arguments = args
            
        
        if function_name in TOOL_FUNCTIONS:
            tool_result = TOOL_FUNCTIONS[function_name](**arguments)
            return {
                "called": True,
                "name": function_name,
                "result": tool_result,
                "assistant_message": message_obj
            }    
        else:
            return {"called": False, "error": f"Tool '{function_name}' not found."}
            
    # If no tool was called, return the normal text content
    content = ""
    if isinstance(message_obj, dict):
        content = message_obj.get("content", "")
    else:
        content = str(message_obj)

    return {"called": False, "content": content}

@app.route('/chats', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages', [])
    chat_id = data.get('chat_id')
    proxy_url = data.get('proxy_url', 'http://127.0.0.1:2026/api/chat')
    model_name = data.get('model', 'gemma4:31b-cloud')
    api_key = data.get('api_key', '')   

    user_msg = messages[-1]

    conn = sqlite3.connect('candela.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (id, chat_id, role, content) VALUES (?, ?, ?, ?)",
        (user_msg['id'], chat_id, user_msg['role'], user_msg['content'])
    )

    conn.commit()
    conn.close()

    prompt_path = os.path.join(BASE_DIR, 'prompts', 'candela_system.txt')
    with open(prompt_path, 'r', encoding='utf-8') as file:
        system_prompt_text = file.read().strip()

    system_prompt = {
        "role": "system",
        "content": system_prompt_text
    }
    messages_with_system = [system_prompt] + messages

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model_name,
        "messages": messages_with_system,
        "stream": False,
        "tools": ALL_TOOLS
    }

    try:
        response = requests.post(proxy_url, json=payload, headers=headers)
        result = response.json()

        if "error" in result:
            error_msg = result["error"]
            if isinstance(error_msg, dict):
                error_msg = error_msg.get("message", str(error_msg))
            bot_answer = f"API Error: {error_msg}"
            
        elif "choices" in result:
            message_obj = result["choices"][0]["message"]
            tool_data = process_tool_calls(message_obj)
            
            if not isinstance(tool_data, dict):
                bot_answer = f"System Error: Expected dict, got {type(tool_data)}"
            
            elif tool_data.get("called"):
                # --- OPENAI AGENT LOOP ---
                clean_assistant_msg = {
                    "role": "assistant",
                    "content": tool_data["assistant_message"].get("content", ""),
                    "tool_calls": tool_data["assistant_message"].get("tool_calls")
                }
                messages_with_system.append(clean_assistant_msg)
                
                messages_with_system.append({
                    "role": "tool",
                    "content": str(tool_data["result"]),
                    "tool_call_id": tool_data["assistant_message"]["tool_calls"][0].get("id", "default_id")
                })
                
                print("Sending tool result back to AI...")
                second_payload = {
                    "model": model_name,
                    "messages": messages_with_system,
                    "stream": False,
                    "tools": ALL_TOOLS
                }
                second_response = requests.post(proxy_url, json=second_payload, headers=headers)
                second_result = second_response.json()
                
                print("RAW SECOND RESULT:", second_result)
                
                if "error" in second_result:
                    bot_answer = f"API Error on 2nd call: {second_result['error']}"
                elif "choices" in second_result:
                    bot_answer = second_result["choices"][0]["message"]["content"]
                elif "message" in second_result:
                    bot_answer = second_result["message"]["content"]
                else:
                    bot_answer = "Unknown error on second call."
            else:
                bot_answer = tool_data.get("content", "")
                
        elif "message" in result:
            # --- OLLAMA AGENT LOOP ---
            message_obj = result["message"]
            tool_data = process_tool_calls(message_obj)
            
            if isinstance(tool_data, dict) and tool_data.get("called"):
                clean_assistant_msg = {
                    "role": "assistant",
                    "content": tool_data["assistant_message"].get("content", ""),
                    "tool_calls": tool_data["assistant_message"].get("tool_calls")
                }
                messages_with_system.append(clean_assistant_msg)
                messages_with_system.append({
                    "role": "tool",
                    "content": str(tool_data["result"])
                })
                
                second_payload = {
                    "model": model_name, 
                    "messages": messages_with_system, 
                    "stream": False,
                    "tools": ALL_TOOLS
                }
                second_response = requests.post(proxy_url, json=second_payload, headers=headers)
                second_result = second_response.json()
                
                if "message" in second_result:
                    bot_answer = second_result["message"]["content"]
                elif "choices" in second_result:
                    bot_answer = second_result["choices"][0]["message"]["content"]
                else:
                    bot_answer = "Unknown error on second call."
            else:
                bot_answer = tool_data.get("content", "")
            
        else:
            bot_answer = f"Unexpected response format from proxy: {result}"
            
    except Exception as e:
        bot_answer = f"Connection Error: {str(e)}"

    ai_msg_id = str(uuid.uuid4())
    conn = sqlite3.connect('candela.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO messages (id, chat_id, role, content) VALUES (?, ?, ?, ?)",
        (ai_msg_id, chat_id, 'assistant', bot_answer)
    )
    conn.commit()
    conn.close()

    return jsonify({"response": bot_answer})
    

if __name__ == "__main__":
    app.run(debug=True, port=5000)