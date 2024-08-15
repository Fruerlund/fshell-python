import socket
from shell import command_handler, threadObject
from local_utils import splitdata

def create_socket(**kwargs):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock


def handleconnection(shell, connection, address): #connection, address):
    print("Got connection from: ", address)
    connection.send(b"Connection established!")
    while True:
        try:
            data = connection.recv(1024).decode("utf-8")
            if len(data) == 0:
                break
            output = command_handler(shell=shell, arguments=splitdata(data))
            if output is not None and len(output) > 0:
                if isinstance(output, bytes) is True:
                    connection.sendall(output)
                else:
                    connection.sendall(output.encode("utf-8"))
            else:
                connection.send(b" ")
        except Exception as e:
            print(e)
            connection.close()
            break
    print("Connection closed!")


def create_server(**kwargs):
    port = kwargs["port"]
    ip = kwargs["ip"]
    address = (ip, int(port))
    shell = kwargs["shell"]
    with create_socket() as s:
        s.bind(address)
        s.listen(5)
        while True:
            connection, addr = s.accept()
            shell.clients.append(shell.executor.submit(handleconnection, shell, connection, address))


def connect_back(**kwargs):
    address = (kwargs["ip"], kwargs["port"])
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(address)
        data = s.recv(1024)
        print(data)
        while True:
            s.send(input().encode())

