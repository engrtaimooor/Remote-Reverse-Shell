# Remote Reverse Shell Project

> ⚠️ **Authorized Use Only:** This project is intended strictly for educational purposes and controlled laboratory environments where you own or have explicit permission to access all systems involved.

## Overview

This project demonstrates a Python-based client-server architecture for remote communication and command execution in an authorized testing environment.

The project consists of three main components:

* **`c2_server.py`** — Handles incoming client connections.
* **`payload.py`** — Client-side application that connects to the server.
* **`client.py`** — Interface used to interact with connected clients.

---

## Requirements

Before running the project, make sure Python is installed on your system.

The following Python packages are required:

* `requests`
* `flask`
* `prompt_toolkit`

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/engrtaimooor/Remote-Reverse-Shell
cd Remote-Reverse-Shell
```

### 2. Create a Virtual Environment

Create a virtual environment:

```bash
python3 -m venv c2_env
```

### 3. Activate the Virtual Environment

**Linux/macOS:**

```bash
source c2_env/bin/activate
```

**Windows:**

```cmd
c2_env\Scripts\activate
```

### 4. Install Required Packages

```bash
pip install -r requirements.txt
```

---

## Running the Project

### Step 1: Start the Server

Open the first terminal and run:

```bash
python c2_server.py
```

The server listens for incoming connections on port `4444`.

---

### Step 2: Create a Tunnel

Open a second terminal and run:

```bash
ngrok http 4444
```

Ngrok will generate a public forwarding address.

Copy the generated address and update the connection configuration in:

* `payload.py`
* `client.py`

Use only systems and networks where you have explicit authorization.

---

### Step 3: Start the Client Interface

Open a third terminal and run:

```bash
python client.py
```

Once an authorized client connects to the server, the connection will appear in the server terminal.

The client interface can then be used to interact with the connected system within the scope of the authorized lab environment.

---

## Building a Windows Executable

The Python application can optionally be packaged as a Windows executable for deployment in an authorized testing environment.

### Option 1: Using Auto Py to Exe

Install the tool:

```bash
pip install auto-py-to-exe
```

Run:

```bash
auto-py-to-exe
```

This provides a graphical interface for converting Python applications into executable files.

---

### Option 2: Using PyInstaller

Install PyInstaller:

```bash
pip install pyinstaller
```

Build the executable:

```bash
pyinstaller --onefile --noconsole payload.py
```

The generated executable will be available in the `dist` directory. Rename it from payload.exe to something else like accountdetails.txt

---

## Project Structure

```text
.
├── c2_server.py
├── payload.py
├── client.py
├── requirements.txt
└── README.md
```

---

## Disclaimer

This project is created for educational purposes and authorized security testing only.

Do not use this software to access computers, networks, or systems without explicit permission from their owners. Unauthorized access to computer systems may be illegal and unethical.

The developer assumes no responsibility for misuse of this project.
