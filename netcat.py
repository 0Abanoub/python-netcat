import argparse   # to create a command-line interface for the script
import socket
import shlex      # to split the command string into a list of arguments
import subprocess # This library provides a powerful process-creation interface that gives you a number of ways to interact with client programs
import sys
import textwrap   # to format the help text for the command-line interface
import threading  # to handle multiple client connections concurrently

def execute(cmd):
    cmd = cmd.strip() # Remove leading/trailing whitespace
    if not cmd :
        return # If the command is empty, return nothing
    output = subprocess.check_output(shlex.split(cmd),
                                     stderr= subprocess.STDOUT) # Execute the command and capture the output 
    return output.decode()

class NetCat:
    def __init__(self, args, buffer=None): # Initialize the NetCat class with command-line arguments and an optional buffer
        self.args = args     # Store the command-line arguments
        self.buffer = buffer # Store the buffer, which may contain data to send
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP socket 
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Set socket options to allow reuse of the address 

    def run(self): # Main method to run the NetCat functionality
        if self.args.listen: # If the listen flag is set, start listening for incoming connections 
            self.listen() 
        else: 
            self.send()

    def send(self): # Method to send data to a target server
        self.socket.connect((self.args.target, self.args.port)) # Connect to the target server
        if self.buffer: # If there is data in the buffer, send it
            self.socket.send(self.buffer)

        try:
            while True: # start a loop to receive data from target 
                recv_len = 1
                response = ''
                while recv_len: 
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode() 
                    if recv_len < 4096: # If there is no more data break out of the loop
                        break
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode()) # If there is a response, print it and prompt for more input
        except KeyboardInterrupt: # the loop will continue until the user interrupts it (CTRL+C)
            print('User terminated.')
            self.socket.close()
            sys.exit()

    def listen(self): # Method to listen for incoming connections
        self.socket.bind((self.args.target, self.args.port)) # Bind the socket to the specified target and port
        self.socket.listen(5)

        while True: # start listening in a loop
            client_socket, _ = self.socket.accept() # Accept incoming connections
            client_thread = threading.Thread(target=self.handle , args=(client_socket,)) # passing the connected socket to a new thread (the handle method)
            client_thread.start() # Start a new thread to handle the client connection

    def handle(self, client_socket): # logic to perform file upload, command execution, or command shell
        if self.args.execute: 
           output = execute(self.args.execute) # Execute the specified command
           client_socket.send(output.encode()) # Send the output of the command to the client


        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096) # Receive data from the client
                if data: 
                    file_buffer += data
                else:
                    break
            
            with open(self.args.upload, 'wb') as f: # Open the specified file in binary write mode
                f.write(file_buffer) # Write the received data to the file
            message = f'Successfully saved file to {self.args.upload}' 
            client_socket.send(message.encode())


        elif self.args.command:
           cmd_buffer = b''
           while True:
                try:
                    client_socket.send(b'BHP: #> ') # Prompt the client for a command

                    while '\n' not in cmd_buffer.decode(): # Wait for a newline character to indicate the end of the command
                        cmd_buffer += client_socket.recv(64) # Receive data from the client
                    response = execute(cmd_buffer.decode()) # Execute the command and get the response
                    
                    if response:
                        client_socket.send(response.encode()) # Send the response back to the client
                    cmd_buffer = b'' # Reset the command buffer for the next command
                
                except Exception as e:
                    print(f'Server killed: {e}')
                    client_socket.close()
                    sys.exit()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='BHP Net Tool',
                                        formatter_class=argparse.RawDescriptionHelpFormatter,
                                        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.108 -p 5555 -l -c                     #command shell\n
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt          #upload file\n
            netcat.py -t 192.168.1.108 -p 5555 -l -e=\"cat /etc/passwd\"   #execute command\n
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135             #echo text to server port 135\n
            netcat.py -t 192.168.1.108 -p 5555                           #connect to server
                                                               '''))
parser.add_argument('-c', '--command', action='store_true', help='command shell')
parser.add_argument('-e', '--execute', help='execute specified command')
parser.add_argument('-l', '--listen', action='store_true', help='listen')
parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
parser.add_argument('-u', '--upload', help='upload file')
args = parser.parse_args()

if args.listen:
    buffer = '' # Initialize an empty buffer for listening mode
else:
    buffer = sys.stdin.read() # Read from standard input if not in listen mode

nc = NetCat(args, buffer.encode()) 
nc.run()