import subprocess
import socket
import psutil

import threading
from contextlib import closing

def simple_server(port):
    def run_server():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            #binds the socket to all available network interfaces (using the IP address '0.0.0.0') and port 23.
            server.bind(('0.0.0.0', port)) 
            
            #sets the socket to listen for incoming connections. The server can have at most 1 pending connection in the queue.
            server.listen(1)

            #blocks and waits for an incoming connection
            conn, addr = server.accept() 
            with conn:
                print(f"\nConnection from: {addr}")

    #creates a new Thread object, setting its target function to run_server. The daemon=True parameter ensures that the thread will exit when the main program terminates.
    server_thread = threading.Thread(target=run_server, daemon=True)

    #starts the server thread
    server_thread.start() 

def open_port(port):
    rule_name = f"Allow_Port_{port}"
    #Create a new Firewall rule with a new rule name, apply it to inbound  traffic,  Sets the local port 23 for the rule, specify TCP, and allow it
    command = f'powershell New-NetFirewallRule -DisplayName "{rule_name}" -Direction Inbound -LocalPort {port} -Protocol TCP -Action Allow'
    subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def close_port(port):
    rule_name = f"Block_Port_{port}"
    command = f'powershell New-NetFirewallRule -DisplayName "{rule_name}" -Direction Inbound -LocalPort {port} -Protocol TCP -Action Block'
    subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def is_port_open(port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(1)
        try:
            sock.connect(('127.0.0.1', port))
            return True
        except socket.error:
            return False
        
def is_port_in_use(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port and conn.status == psutil.CONN_ESTABLISHED:
            return True
    return False

        
def main():
    port = 23
    simple_server(port)
    print(f"Opening port {port}.")
    #open_port(port)
    #if is_port_open(port):
        #print(f"Port {port} is open.")
    #else:
        #print(f"Port {port} is closed.")
    if not is_port_in_use(port):
        print(f"Port {port} is not being used. Closing port.")
        close_port(port)
    else:
        print(f"Port {port} is being used.")
    if is_port_open(port):
        print(f"Port {port} is open.")
    else:
        print(f"Port {port} is closed.")

if __name__ == "__main__":
    main()
