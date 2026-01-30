# mcp/stdio_server.py
import sys
import json
import logging
from mcp.tools import ask_codebase
from mcp.schemas import ASK_CODEBASE_SCHEMA

# Set up logging to a file for debugging
logging.basicConfig(
    filename='/tmp/mcp_stdio_server.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def handle_message(message):
    """Handle incoming MCP protocol messages"""
    method = message.get("method")
    logging.debug(f"Received method: {method}")
    logging.debug(f"Full message: {json.dumps(message)}")
    
    if method == "initialize":
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "java-rag-mcp",
                "version": "1.0.0"
            }
        }
    
    elif method == "tools/list":
        return {
            "tools": [ASK_CODEBASE_SCHEMA]
        }
    
    elif method == "tools/call":
        tool_name = message.get("params", {}).get("name")
        arguments = message.get("params", {}).get("arguments", {})
        
        if tool_name == "ask_codebase":
            question = arguments.get("question")
            logging.debug(f"Calling ask_codebase with question: {question}")
            result = ask_codebase(question)
            logging.debug(f"Got result: {result}")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": result["answer"]
                    }
                ]
            }
    
    logging.warning(f"Unknown method: {method}")
    return {"error": f"Unknown method: {method}"}

def main():
    """Main stdio loop"""
    logging.info("MCP stdio server starting...")
    
    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
                
            logging.debug(f"Received line: {line}")
            
            try:
                message = json.loads(line)
                response = handle_message(message)
                
                # Build proper JSON-RPC response
                json_rpc_response = {
                    "jsonrpc": "2.0",
                    "id": message.get("id")
                }
                
                if "error" in response:
                    json_rpc_response["error"] = response["error"]
                else:
                    json_rpc_response["result"] = response
                
                # Write response
                response_str = json.dumps(json_rpc_response)
                logging.debug(f"Sending response: {response_str}")
                print(response_str, flush=True)
                
            except json.JSONDecodeError as e:
                logging.error(f"JSON decode error: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)
                
            except Exception as e:
                logging.error(f"Error handling message: {e}", exc_info=True)
                error_response = {
                    "jsonrpc": "2.0",
                    "id": message.get("id") if 'message' in locals() else None,
                    "error": {
                        "code": -32603,
                        "message": str(e)
                    }
                }
                print(json.dumps(error_response), flush=True)
    
    except Exception as e:
        logging.error(f"Fatal error in main loop: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()