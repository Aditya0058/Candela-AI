import threading
import json
import time

from .time_tool import TOOL_SCHEMA as time_schema, get_current_time
from .calc_tool import TOOL_SCHEMA as calc_schema, calculate
from .web_search import TOOL_SCHEMA as web_search_schema, web_search
from .telegram_tool import TOOL_SCHEMA as telegram_send_message_schema, send_message_on_telegram

def schedule_action.py(tool_name: str, arguments_json: str, delay_seconds: int):
    try:
        args = json.loads(arguments_json)

        def execute_later():
            from . import TOOL_FUNCTIONS
            if tool_name in TOOL_FUNCTIONS:
                print(f"executing scheduled tool {tool_name}")
            else:
                print(f"Tool not found {tool_name}")

        timer = threading.Timer(delay_seconds, execute_later)
        timer.start()

        return f"Successfully scheduled '{tool_name}' to run in {delay_seconds} seconds."

    except Exception as e:
        return f"Failed to schedule action: {str(e)}"