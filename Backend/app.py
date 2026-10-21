from flask import Flask, request
import requests

app = Flask(__name__)

@app.post("/chat")
def chat():
    # recive message
    data = request.get_json()
    message = data["message"]
    
    # prepare message to send to ai 
    payload = {
        "model" : "gemma4:31b-cloud",
        "messages": [
            {"role": "user", "content": message}
        ], 
        "stream": False
    }
    # send prepared message's json to ai and store it into response
    response_received = requests.post('http://127.0.0.1:2026/api/chat', json=payload)

    print("STATUS:", response_received.status_code)
    print("RAW BODY:", response_received.text)
    return {"debug": "look at your terminal, not the browser"}

    # extract the actual response from response recieved
    # actual_response = response_recieved["message"]

    # # returning ai response to frontend (from where the endpoint was called)
    # return {"recieved" : message}


if __name__ == "__main__":
    app.run(debug=True)