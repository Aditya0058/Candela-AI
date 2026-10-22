# add here more tools if three
from .time_tool import TOOL_SCHEMA as time_schema, get_current_time
from .calc_tool import TOOL_SCHEMA as calc_schema, calculate
from .web_search import TOOL_SCHEMA as web_search_schema, web_search
from .telegram_tool import TOOL_SCHEMA as telegram_send_message_schema, send_message_on_telegram
from .schedule_tool import TOOL_SCHEMA as schedule_tool_schema, schedule_action

ALL_TOOLS = [
    time_schema,
    calc_schema,
    web_search_schema,
    telegram_send_message_schema,
    schedule_tool_schema,
    # more tools here
]

TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "web_search": web_search,
    "send_message_on_telegram": send_message_on_telegram,
    "schedule_action": schedule_action,
    # tool funcitons here
}