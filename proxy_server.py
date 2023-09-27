import socket
from threading import Thread

BYTES_TO_READ = 4096
PROXY_SERVER_HOST = "127.0.0.1"  # IP, localhost
PROXY_SERVER_POST = 8080


def send_request(host, port, request):
    """
    send some data(request) to host:port
    :return: None
    """
    # Create a new socket in with block to ensure it's closed once we're done
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:  # initialize the socket
        client_socket.connect((host, port))  # connect the socket to host:port
        client_socket.send(request)  # send the request through the connected socket
        client_socket.shutdown(socket.SHUT_WR)  # shut the socket to further writes, tells server we're done sending

        # Assemble response, but be careful, recv(bytes) blocks until it receives data
        data = client_socket.recv(BYTES_TO_READ)
        result = b"" + data

        while len(data) > 0:  # keep reading data until connection terminates
            data = client_socket.recv(BYTES_TO_READ)
            result += data

        return result  # return response


def handle_connection(conn, addr):
    """
    Handles an incoming connection that has been accepted by the server
    :param conn: socket referring to the client
    :param addr: address of the client [IP, Port]
    :return: None
    """
    with conn:
        print(f"Connected by {addr}")

        request = b""

        while True:  # while the client is keeping the socket open
            data = conn.recv(BYTES_TO_READ)  # read some data from the socket

            if not data:  # if the socket has been closed to further writes, break
                break

            print(data)  # otherwise, print the data to the screen
            request += data

            response = send_request("www.google.com", 80, request)  # and send it as a request to www.google.com
            conn.sendall(response)  # returns the response from www.google.com


def start_server():
    """
    a single-threaded echo server
    :return: None
    """
    # Creating the socket in the with block to ensure it gets auto-close once it's done
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:  # initialize the socket
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_POST))  # bind to the IP and port
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # set reuseaddr to 1
        server_socket.listen(2)  # listen for incoming connections

        # waiting for an incoming connection, when one arrives, accept it
        # create a new socket called conn to interact with it
        conn, addr = server_socket.accept()
        handle_connection(conn, addr)  # pass conn off to handle_connection to do some logic


def start_threaded_server():
    """
    a multithreaded echo server
    :return: None
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:  # initialize the socket
        server_socket.bind((PROXY_SERVER_HOST, PROXY_SERVER_HOST))  # bind to the IP and port
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # set reuseaddr to 1
        server_socket.listen(2)  # Allow backlog of up to 2 connections => queue [ waiting conn1, waiting conn 2]

        while True:
            conn, addr = server_socket.accept()  # conn = socket referring to the client, addr = address of the client [IP, Port]
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()


start_server()
# start_threaded_server()