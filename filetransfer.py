from typing import BinaryIO
import socket

def file_server(iface:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
    print("Hello, I am a server")
    if use_udp:
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host_addr, port_number = socket.getaddrinfo(iface, port)[0][4]
        server.bind((host_addr, port_number))
        fileval = open(fp.name, "wb")
        dataval, addr = server.recvfrom(256)
        while dataval:
            fileval.write(dataval)
            dataval, addr = server.recvfrom(256)
        fileval.close()
        server.close()
    else:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host_addr, port_number = socket.getaddrinfo(iface, port)[0][4]
        server.bind((host_addr, port_number))
        fileval = open(fp.name, "wb")
        server.listen()
        c, addr = server.accept()
        data = c.recv(256)
        while data:
            fileval.write(data)
            data = c.recv(256)
        fileval.close()
        c.close()
            
def file_client(host:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
    print("Hello, I am a client")
    if use_udp:
        fileval = open(fp.name, "rb")   
        data = fileval.read(256)
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        host_addr, port_number = socket.getaddrinfo(host, port)[0][4]
        while data:
            client.sendto(data,(host_addr,port_number))
            data = fileval.read(256)
        client.sendto("".encode(),  (host, port))
        fileval.close()
        client.close()
    else:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_addr, port_number = socket.getaddrinfo(host, port)[0][4]
        client.connect((host_addr, port_number))
        fileval = open(fp.name, "rb")
        data = fileval.read(256)
        while data: 
            client.send(data) 
            data = fileval.read(256)
        client.send(data)     
        fileval.close()
        client.close()
