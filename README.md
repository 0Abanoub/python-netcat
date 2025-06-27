# BHP Netcat Clone (Educational)

This is a Python-based Netcat-like tool built while studying *Black Hat Python* book.  
It supports:
- Reverse shell
- Command execution
- File upload
- Listening for incoming connections

⚠️ This project is for **educational purposes only**. Do not use it on systems you don't own or have permission to test.

## Usage

Examples:

```bash
# Listen for a reverse shell
python netcat.py -t 0.0.0.0 -p 5555 -l -c

# Upload a file
python netcat.py -t 0.0.0.0 -p 5555 -l -u=output.txt

# Execute a command
python netcat.py -t 0.0.0.0 -p 5555 -l -e="ls -la"

# Send input to a server
echo "hello" | python netcat.py -t 192.168.1.10 -p 5555
