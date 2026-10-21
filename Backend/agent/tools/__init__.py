# add here more tools if three
from .time_tool import TOOL_SCHEMA as time_schema, get_current_time

ALL_TOOLS = [
    time_schema,
    # more tools here
]

# 2. A dictionary mapping tool names to their actual Python functions
TOOL_FUNCTIONS = {
    "get_current_time": get_current_time,
    # tool funcitons here
}