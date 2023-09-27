import socket
from threading import Thread

BYTES_TO_READ = 4096
HOST = "127.0.0.1"  # IP, localhost
PORT = 8080


def handle_connection(conn, addr):
    with conn:  # using with automatically closes the connection
        print(f"Connected by {addr}")

        while True:
            data = conn.recv(BYTES_TO_READ)  # waits for a request, when it gets a request, it receives it

            if not data:  # if data received is an empty byte string, break
                break
            print(data)

            conn.sendall(data)  # sends it back to the client


def start_server():
    """
    a single-threaded echo server
    :return: None
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # initialize the socket
        s.bind((HOST, PORT))  # bind to the IP and port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # set reuseaddr to 1
        s.listen()  # listen for incoming connections
        conn, addr = s.accept()  # conn = socket referring to the client, addr = address of the client [IP, Port]
        handle_connection(conn, addr)  # send it a response


def start_threaded_server():
    """
    a multithreaded echo server
    :return: None
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # initialize the socket
        s.bind((HOST, PORT))  # bind to the IP and port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # set reuseaddr to 1
        s.listen(2)  # Allow backlog of up to 2 connections => queue [ waiting conn1, waiting conn 2]

        while True:
            conn, addr = s.accept()  # conn = socket referring to the client, addr = address of the client [IP, Port]
            thread = Thread(target=handle_connection, args=(conn, addr))
            thread.run()


start_server()
# start_threaded_server()
