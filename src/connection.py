
import socket

def connect_back(**kwargs):
    address = (kwargs["ip"], kwargs["port"])
    print(address)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(address)
        data = s.recv(1024)
        print(data)
        while True:
            s.send(input().encode())
            data = s.recv(1024)
            print(data.decode())
            #while(len(data) > 0):
             #   print(data.decode())
              #  data = s.recv(1024)



connect_back(ip="127.0.0.1", port=5555)