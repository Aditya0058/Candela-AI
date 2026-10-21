# add here more tools if three
from .time_tool import TOOL_SCHEMA as time_schema, get_current_time
from .calc_tool import TOOL_SCHEMA as calc_schema, calculate
from .web_search import TOOL_SCHEMA as web_search_schema, web_search

ALL_TOOLS = [
    time_schema,
    calc_schema,
    web_search_schema,
    # more tools here
]

# 2. A dictionary mapping tool names to their actual Python functions
TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    "calculate": calculate,
    "web_search": web_search,
    # tool funcitons here
}