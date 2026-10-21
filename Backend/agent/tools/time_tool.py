def current_time():
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


TOOL_SCHEMA = {
    "type": function,
    "function": {
        "name": "get_current_time",
        "description": "Get the current date and time",
        "parameters": {"type": "object", "properties": {}}
    }
}
