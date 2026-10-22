import threading
import json
from datetime import datetime
import time

from .time_tool import TOOL_SCHEMA as time_schema, get_current_time
from .calc_tool import TOOL_SCHEMA as calc_schema, calculate
from .web_search import TOOL_SCHEMA as web_search_schema, web_search
from .telegram_tool import TOOL_SCHEMA as telegram_send_message_schema, send_message_on_telegram

def schedule_action.py(tool_name: str, arguments_json: str, scheduled_time: str):
    """
    scheduled_time should be a string in the format: "YYYY-MM-DD HH:MM:SS"
    Example: "2026-10-22 17:30:00"
    """
    try:
        args = json.loads(arguments_json)

        target_time = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M:%S")

        now = datetime.now()
        delay_seconds = (target_time - now).total_seconds()

        if delay_seconds < 0:
            return f"Error: The scheduled time {scheduled_time} is in the past."

        def execute_later():
            from . import TOOL_FUNCTIONS
            if tool_name in TOOL_FUNCTIONS:
                print(f"executing scheduled tool {tool_name}")
            else:
                print(f"Tool not found {tool_name}")

        timer = threading.Timer(delay_seconds, execute_later)
        timer.start()

        return f"Successfully scheduled '{tool_name}' to run in {delay_seconds} seconds."

    except ValueError as e:
        return f"Format error. Ensure time is 'YYYY-MM-DD HH:MM:SS'. Details: {str(e)}"
    except Exception as e:
        return f"Failed to schedule action: {str(e)}"


TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "schedule_action",
        "description": "Schedule a tool to run at an exact date and time in the future. ALWAYS use the get_current_time tool FIRST to find the current date before calculating the schedule.",
        "parameters": {
            "type": "object",
            "properties": {
                "tool_name": {
                    "type": "string",
                    "description": "The exact name of the tool to run (e.g., 'send_message_on_telegram')."
                },
                "arguments_json": {
                    "type": "string",
                    "description": "A valid JSON string of arguments for the tool. E.g., '{\"message\": \"Hello\"}'"
                },
                "scheduled_time": {
                    "type": "string",
                    "description": "The exact future date and time. MUST be in the format: 'YYYY-MM-DD HH:MM:SS'."
                }
            },
            "required": ["tool_name", "arguments_json", "scheduled_time"]
        }
    }
}