import socket

import threading

def handle_client_request(client_socket):

    print("Received request:\n")

    # read the data sent by the client in the request

    request = b''

    client_socket.setblocking(False)

    while True:

        try:

            # receive data from web server

            data = client_socket.recv(1024)

            request = request + data

            # Receive data from the original destination server

            print(f"{data.decode('utf-8')}")

        except:

            break

    # extract the webserver's host and port from the request

    host, port = extract_host_port_from_request(request)

    # create a socket to connect to the original destination server

    destination_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to the destination server

    destination_socket.connect((host, port))

    # send the original request

    destination_socket.sendall(request)

    # read the data received from the server

    # once chunk at a time and send it to the client

    print("Received response:\n")

    while True:

        # receive data from web server

        data = destination_socket.recv(1024)

        # Receive data from the original destination server

        print(f"{data.decode('utf-8')}")

        # no more data to send

        if len(data) > 0:

            # send back to the client

            client_socket.sendall(data)

        else:

            break

    # close the sockets

    destination_socket.close()

    client_socket.close()

def extract_host_port_from_request(request):

    # get the value after the "Host:" string

    host_string_start = request.find(b'Host: ') + len(b'Host: ')

    host_string_end = request.find(b'\r\n', host_string_start)

    host_string = request[host_string_start:host_string_end].decode('utf-8')

    webserver_pos = host_string.find("/")

    if webserver_pos == -1:

        webserver_pos = len(host_string)

    # if there is a specific port

    port_pos = host_string.find(":")

    # no port specified

    if port_pos == -1 or webserver_pos < port_pos:

        # default port

        port = 80

        host = host_string[:webserver_pos]

    else:

        # extract the specific port from the host string

        port = int((host_string[(port_pos + 1):])[:webserver_pos - port_pos - 1])

        host = host_string[:port_pos]

    return host, port

def start_proxy_server():

    port = 8888

    # bind the proxy server to a specific address and port

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind(('127.0.0.3', port))

    # accept up to 10 simultaneous connections

    server.listen(10)

    print(f"Proxy server listening on port {port}...")

    # listen for incoming requests

    while True:

        client_socket, addr = server.accept()

        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        # create a thread to handle the client request

        client_handler = threading.Thread(target=handle_client_request, args=(client_socket,))

        client_handler.start()

if __name__ == "__main__":

    start_proxy_server()
