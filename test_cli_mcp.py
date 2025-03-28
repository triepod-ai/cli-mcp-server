import os
import subprocess
import sys

# Set necessary environment variables
os.environ["ALLOWED_DIR"] = "L:\\"
os.environ["ALLOWED_COMMANDS"] = "ls,cat,pwd,Get-ChildItem,Get-Content"
os.environ["ALLOWED_FLAGS"] = "-l,-a,--help"
os.environ["MAX_COMMAND_LENGTH"] = "1024"
os.environ["COMMAND_TIMEOUT"] = "30"

# Get the path to the cli-mcp-server executable
cli_mcp_server_path = "cli-mcp-server"

# Run the CLI MCP server
print(f"Running {cli_mcp_server_path}")
try:
    process = subprocess.run([cli_mcp_server_path], check=True)
    print(f"Process exited with code {process.returncode}")
except subprocess.CalledProcessError as e:
    print(f"Error running cli-mcp-server: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
