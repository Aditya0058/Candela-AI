from datetime import datetime

def get_current_time():
    """Returns the current time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "Get the current date and time",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}