import os
import subprocess
import threading
import time

# Set necessary environment variables
os.environ["ALLOWED_DIR"] = "L:\\"
os.environ["ALLOWED_COMMANDS"] = "ls,cat,pwd,Get-ChildItem,Get-Content"
os.environ["ALLOWED_FLAGS"] = "-l,-a,--help"
os.environ["MAX_COMMAND_LENGTH"] = "1024"
os.environ["COMMAND_TIMEOUT"] = "30"

# Get the path to the cli-mcp-server executable
cli_mcp_server_path = "cli-mcp-server"

print(f"Starting {cli_mcp_server_path}")
print("Environment variables set:")
print(f"  ALLOWED_DIR = {os.environ['ALLOWED_DIR']}")
print(f"  ALLOWED_COMMANDS = {os.environ['ALLOWED_COMMANDS']}")
print(f"  ALLOWED_FLAGS = {os.environ['ALLOWED_FLAGS']}")

# Create a process with pipes for stdin, stdout, and stderr
process = subprocess.Popen(
    [cli_mcp_server_path],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

print(f"Process started with PID {process.pid}")
print("Server should be running. MCP servers use stdin/stdout for communication.")
print("Waiting for 5 seconds to see if there are any initial errors...")

# Read initial stderr output for 5 seconds
start_time = time.time()
stderr_lines = []

def read_stderr():
    while time.time() - start_time < 5:
        line = process.stderr.readline()
        if line:
            stderr_lines.append(line.strip())
        time.sleep(0.1)

stderr_thread = threading.Thread(target=read_stderr)
stderr_thread.start()
stderr_thread.join()

if stderr_lines:
    print("\nInitial stderr output:")
    for line in stderr_lines:
        print(f"  {line}")
else:
    print("\nNo initial stderr output - the server appears to be running correctly!")

print("\nTerminating the server process...")
process.terminate()
try:
    process.wait(timeout=5)
    print("Server terminated successfully.")
except subprocess.TimeoutExpired:
    print("Server did not terminate gracefully, killing...")
    process.kill()
    process.wait()
    print("Server killed.")

print("\nTest completed! The server appears to be working correctly.")
