from flask import Flask, request
import requests

app = Flask(__name__)

AI_URL = "http://127.0.0.1:2026/api/chat"
AI_MODEL = "gemma4:31b-cloud"

@app.post("/chat")
def chat():
    # recive message
    data = request.get_json()
    message = data["message"]
    
    # prepare message to send to ai 
    payload = {
        "model" : AI_MODEL,
        "messages": [
            {"role": "user", "content": message}
        ], 
        "stream": False
    }
    # send prepared message's json to ai and store it into response
    received = requests.post(AI_URL, json=payload, timeout=30)

    # if upstream failed return error
    if received.status_code != 200:
        return {"error": "ai upstream failed", "upstream_status": received.status_code}, 502

    # parsing json and finding actual response
    body = received.json()
    actual_response = body["message"]["content"]

    return {"reply": actual_response}


if __name__ == "__main__":
    app.run(debug=True)