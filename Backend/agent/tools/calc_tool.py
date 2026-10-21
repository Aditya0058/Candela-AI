def calculate(expression: str):
    try:
        result = eval(expression, {"__builtins__": None}, {})
        
        # 2. Return the result as a string (LLMs prefer strings)
        return str(result)
    except Exception as e:
        # 3. If they type bad math (like 2 + ), catch the error
        return f"Error calculating: {str(e)}"

TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Evaluates a mathematical expression. Use this for any math.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate, e.g., '2 + 2 * 5'"
                }
            },
            "required": ["expression"] 
        }
    }
}