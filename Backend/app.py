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
    if "tool_calls" in message_obj and message_obj["tool_calls"]:
        tool_call = message_obj["tool_calls"][0]
        function_name = tool_call["function"]["name"]
        
        # OpenAI sends arguments as a JSON string. Ollama sends them as a dict.
        args = tool_call["function"]["arguments"]
        if isinstance(args, str):
            arguments = json.loads(args)
        else:
            arguments = args
            
        print(f" AI requested tool: {function_name} with args: {arguments}")
        
        if function_name in TOOL_FUNCTIONS:
            tool_result = TOOL_FUNCTIONS[function_name](**arguments)
            print(f"Tool execution result: {tool_result}")
            return f"I used the {function_name} tool and got: {tool_result}"
        else:
            return f"Error: Tool '{function_name}' not found in registry."
            
    # If no tool was called, return the normal text content
    return message_obj.get("content", "")

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
                error_msg = error_msg.get("message", str(error_msg)) # OpenAI style
            bot_answer = f"API Error: {error_msg}"
            
        elif "choices" in result:
            message_obj = result["choices"][0]["message"]
            bot_answer = process_tool_calls(message_obj)
            
        elif "message" in result:
            message_obj = result["message"]
            bot_answer = process_tool_calls(message_obj)
            

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