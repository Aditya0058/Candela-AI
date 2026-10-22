
def web_search(query_text):
    import os
    from dotenv import load_dotenv
    import requests
    load_dotenv()
    my_api_key = os.environ.get("WEB_SEARCH_API_KEY")

    if not my_api_key:
            raise ValueError("API key missing! Please check your .env file.")
    
    url = "https://ollama.com/api/web_search"
    headers = {
        "Authorization": f"Bearer {my_api_key}"
    }
    payload = {
        "query": query_text
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status() # Raises an error for bad responses (4xx, 5xx)
        
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Stop guessing If u don't have knowledge about something or you find something unfamiliar then use this",
        "parameters": {
            "type": "object",
            "properties": {
                "query_text": {
                    "type": "string",
                    "description": "query to search on web, e.g., 'Jev Ai decision model'"
                }
            },
            "required": ["query_text"] 
        }
    }
}