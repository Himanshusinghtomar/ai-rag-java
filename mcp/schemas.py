# mcp/schemas.py

ASK_CODEBASE_SCHEMA = {
    "name": "ask_codebase",
    "description": "Answer questions using the project codebase",
    "input_schema": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "Developer question about the codebase"
            }
        },
        "required": ["question"]
    }
}
