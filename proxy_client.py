import socket

BYTES_TO_READ = 4096


def get(host, port):
    request = b"GET / HTTP/1.1\nHost: www.google.com\n\n"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))  # connects to the host and port, e.g. connecting to google
        s.send(request)  # sending the request, e.g. requesting the google homepage
        s.shutdown(socket.SHUT_WR)  # socket can read and write, we are shutting down the write side and then get
        chunk = s.recv(BYTES_TO_READ)  # continuously receive the response
        result = b"" + chunk

        while len(chunk) > 0:
            chunk = s.recv(BYTES_TO_READ)
            result += chunk

        s.close()  # the empty bytestring was sent
        return result


print(get("127.0.0.1", 8000))