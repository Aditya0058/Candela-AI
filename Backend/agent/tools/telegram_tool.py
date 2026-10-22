
def send_message_on_telegram(message: str, **kwargs):
     import os
     from dotenv import load_dotenv
     import requests
     load_dotenv()
     bot_token = kwargs.get("telegram_bot_token") or os.environ.get("TELEGRAM_BOT_TOKEN")
     chat_id = kwargs.get("telegram_chat_id") or os.environ.get("TELEGRAM_CHAT_ID")

     if not chat_id:
          raise ValueError("chat id missing! please check your .env file")
     if not bot_token:
          raise ValueError("bot token missing! please check your .env file")
     

     url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

     payload = {
          "chat_id": chat_id,
          "text": message
     }
     try:
          response = requests.post(url, json=payload)
          response.raise_for_status() # Raises an error for bad responses (4xx, 5xx)
        
          return response.json()
        
     except requests.exceptions.RequestException as e:
          print(f"An error occurred: {e}")
          return None


TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "send_message_on_telegram",
        "description": "Send a message to the user's Telegram.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "The content of the message to send."
                }
            },
            "required": ["message"] 
        }
    }
}