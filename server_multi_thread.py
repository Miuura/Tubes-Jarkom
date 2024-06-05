import socket
import threading
import os

def handle_client(client_socket):
    while True:
        request = client_socket.recv(1024).decode('utf-8')
        print(f"Received request:\n{request}")
        if request == 'CLOSE':
            break
        headers = request.split('\n')
        try:
            filename = headers[0].split()[1]
        except IndexError:
            filename = 'error'
        if filename == '/':
            filename = '/index.html'
        filepath = '.' + filename
        try:
            with open(filepath, 'rb') as file:
                response_body = file.read()
            response_header = 'HTTP/1.1 200 OK\r\n'
            response_header += 'Content-Type: text/html\r\n'
            response_header += 'Content-Length: ' + str(len(response_body)) + '\r\n'
            response_header += '\r\n'
            client_socket.send(response_header.encode('utf-8') + response_body)
        except FileNotFoundError:
            response_header = 'HTTP/1.1 404 Not Found\r\n'
            response_body = '<html><body><h1>404 Not Found</h1></body></html>'
            response_header += 'Content-Type: text/html\r\n'
            response_header += 'Content-Length: ' + str(len(response_body)) + '\r\n'
            response_header += '\r\n'
            client_socket.send(response_header.encode('utf-8') + response_body.encode('utf-8'))
    client_socket.close()

serverAddress = '127.0.0.1'
serverPort = 8000
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((serverAddress, serverPort))
serverSocket.listen(0)
print("Server is listening on port 8000...")

while True:
    client_socket, addr = serverSocket.accept()
    print(f"Accepted connection from {addr}")
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    client_handler.start()
    print(f'[ACTIVE CONNECTIONS] {threading.active_count() -1}')

