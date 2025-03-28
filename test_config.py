import sys
import json
import os
from pathlib import Path

# Function to validate configuration paths
def validate_paths(config_path):
    print(f"Testing configuration file: {config_path}")
    
    try:
        # Check if file exists
        if not os.path.isfile(config_path):
            print(f"ERROR: Configuration file does not exist: {config_path}")
            return False
        
        # Load configuration
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        print("Configuration loaded successfully.")
        
        # Check allowed directory
        allowed_dir = config.get("allowedDir", "")
        if not allowed_dir:
            print("ERROR: allowedDir is empty or not specified.")
            return False
        
        if not os.path.isdir(allowed_dir):
            print(f"ERROR: allowedDir '{allowed_dir}' is not a valid directory.")
            return False
            
        print(f"allowedDir '{allowed_dir}' exists and is valid.")
        
        # Check other fields
        commands = config.get("allowedCommands", "").split(',')
        flags = config.get("allowedFlags", "").split(',')
        timeout = config.get("commandTimeout", 0)
        max_length = config.get("maxCommandLength", 0)
        
        print(f"Configuration specifies {len(commands)} commands and {len(flags)} flags")
        print(f"Command timeout: {timeout} seconds")
        print(f"Max command length: {max_length} characters")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON format in configuration file: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error while validating configuration: {e}")
        return False

def validate_mcp_config(config_path):
    print(f"\nTesting MCP configuration file: {config_path}")
    
    try:
        # Check if file exists
        if not os.path.isfile(config_path):
            print(f"ERROR: Configuration file does not exist: {config_path}")
            return False
        
        # Load configuration
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        print("MCP configuration loaded successfully.")
        
        # Check if cli-mcp-server is in the config
        if "mcpServers" not in config:
            print("ERROR: 'mcpServers' object not found in MCP configuration.")
            return False
            
        if "cli-mcp-server" not in config["mcpServers"]:
            print("ERROR: 'cli-mcp-server' not found in mcpServers configuration.")
            return False
            
        server_config = config["mcpServers"]["cli-mcp-server"]
        
        # Check command and args
        command = server_config.get("command", "")
        args = server_config.get("args", [])
        
        if not command:
            print("ERROR: 'command' is empty or not specified.")
            return False
            
        print(f"Command: {command}")
        print(f"Args: {args}")
        
        # Check environment variables
        env = server_config.get("env", {})
        allowed_dir = env.get("ALLOWED_DIR", "")
        
        if not allowed_dir:
            print("ERROR: ALLOWED_DIR environment variable is empty or not specified.")
            return False
            
        if not os.path.isdir(allowed_dir):
            print(f"ERROR: ALLOWED_DIR '{allowed_dir}' is not a valid directory.")
            return False
            
        print(f"ALLOWED_DIR '{allowed_dir}' exists and is valid.")
        
        # Check other environment variables
        print(f"ALLOWED_COMMANDS: {env.get('ALLOWED_COMMANDS', '')[:50]}...")
        print(f"ALLOWED_FLAGS: {env.get('ALLOWED_FLAGS', '')[:50]}...")
        print(f"MAX_COMMAND_LENGTH: {env.get('MAX_COMMAND_LENGTH', '')}")
        print(f"COMMAND_TIMEOUT: {env.get('COMMAND_TIMEOUT', '')}")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON format in MCP configuration file: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error while validating MCP configuration: {e}")
        return False

if __name__ == "__main__":
    current_dir = Path(__file__).parent.absolute()
    
    # Test the local config.json
    validate_paths(os.path.join(current_dir, "config.json"))
    
    # Test the recommended MCP configurations
    validate_mcp_config(os.path.join(current_dir, "recommended_mcp_config.json"))
    validate_mcp_config(os.path.join(current_dir, "recommended_dev_mcp_config.json"))
