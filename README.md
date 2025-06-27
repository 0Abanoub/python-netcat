# Python Netcat Clone (Educational Tool)

This is a custom implementation of Netcat built using raw sockets in Python.  
Created while studying *Black Hat Python*, it replicates core Netcat features including:

- Reverse Shell
- Remote Command Execution
- File Upload
- Listening for connections

⚠️ **Disclaimer:**  
This tool is created purely for **educational purposes**.  
Do not use it on systems you do not own or have explicit permission to test.

---

## 🧪 Usage Examples

```bash
# Start a listener with command shell
python netcat.py -t 0.0.0.0 -p 5555 -l -c

# Upload a file
python netcat.py -t 0.0.0.0 -p 5555 -l -u=output.txt

# Execute a command automatically upon connect
python netcat.py -t 0.0.0.0 -p 5555 -l -e="ls -la"

# Send a message to server
echo "hello" | python netcat.py -t 192.168.1.10 -p 5555

---

## 🛠 Tech Stack

- Python 3
- Sockets
- Subprocess
- Threading
- argparse

---

### 📚 Based on
📘 Black Hat Python, 2nd Edition
Author: Justin Seitz
