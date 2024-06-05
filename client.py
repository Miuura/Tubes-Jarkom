import socket
import sys

def send_request(host, port, filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    while True: 
        request_line = f"GET {filename} HTTP/1.1\r\n"
        headers = f"Host: {host}\r\nConnection: keep-alive\r\n\r\n"
        request = request_line + headers
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(4096)
        print(response.decode('utf-8'))
        filename = '/'
        filename += input("Masukkan nama file: ")
        if filename == '/stop':
            break

    client_socket.sendall('CLOSE'.encode('utf-8'))
    client_socket.close()

if len(sys.argv) != 4:
    print("Usage: python client.py <server host> <server port> <file name>")
    sys.exit(1)
host = sys.argv[1]
port = int(sys.argv[2])
filename = "/" + sys.argv[3]
send_request(host, port, filename)
