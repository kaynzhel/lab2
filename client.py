import socket

BYTES_TO_READ = 4096


def get(host, port):
    request = b"GET / HTTP/1.1\nHost: " + host.encode("utf-8") + b"\n\n"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # initializes a socket
    s.connect((host, port))  # connects to the host and port, e.g. connecting to google
    s.send(request)  # sending the request, e.g. requesting the google homepage
    s.shutdown(socket.SHUT_WR)  # done sending the request
    result = s.recv(BYTES_TO_READ)  # continuously receive the response

    while len(result) > 0:
        print(result)
        result = s.recv(BYTES_TO_READ)

    s.close()  # needed to close the socket


# get("www.google.com", 80)  # first part where we request google homepage
get("localhost", 8080)
