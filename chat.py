import socket
from _thread import *

def chat_server(iface:str, port:int, use_udp:bool) -> None:
    print("Hello, I am a server")
    n = 0
    if use_udp:
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host, port = socket.getaddrinfo(iface, port)[0][4]
        udp.bind((host, port))
        while True:
            msg, addr = udp.recvfrom(1024)
            msg = format(msg.decode().replace("\n", ""))
            if not msg:
                break
            elif msg == "hello":
                print(f"got message from ('{addr[0]}', {port})")
                udp.sendto(str.encode("world\n"), addr)
            elif msg == "goodbye":
                print(f"got message from ('{addr[0]}', {port})")
                udp.sendto(str.encode("farewell\n"), addr)
            elif msg == "exit":
                print(f"got message from ('{addr[0]}', {port})")
                udp.sendto(str.encode("ok\n"), addr)
                udp.close()
                return
            else:
                print(f"got message from ('{addr[0]}', {port})")
                udp.sendto(str.encode(msg+"\n"), addr)
    else:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host, port = socket.getaddrinfo(iface, port)[0][4]
        tcp.bind((host, port))
        while True:
            try:
                tcp.listen()   
                conn, addr = tcp.accept()
                n += 1
                print(f"Connection {n} from ('{addr[0]}', {port})")
                start_new_thread(multiThread, (tcp, conn, addr, port))
            except KeyboardInterrupt:
                tcp.close()
                break
            except:
                tcp.close()
                break

                    

def multiThread(tcp, conn, addr, port):
    exit_server = False

    while True:
        data = conn.recv(1024)
        data = data.decode().replace("\n", "")
        if not data:
            break
        elif data == "hello":
            print(f"got message from ('{addr[0]}', {port})")
            conn.sendall("world\n".encode())
        elif data == "goodbye":
            print(f"got message from ('{addr[0]}', {port})")
            conn.sendall("farewell\n".encode())
            conn.close()
            break
        elif data == "exit":
            print(f"got message from ('{addr[0]}', {port})")
            conn.sendall("ok\n".encode())
            exit_server = True
            break
        else:
            print(f"got message from ('{addr[0]}', {port})")
            data = data + "\n"
            conn.sendall(data.encode())
    if exit_server:
        tcp.shutdown(socket.SHUT_RDWR)


def chat_client(host:str, port:int, use_udp:bool) -> None:
    print("Hello, I am a client")
    if use_udp:
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host, port = socket.getaddrinfo(host, port)[0][4]
        while True:
            msg = input()
            udp.sendto(str.encode(msg), (host, port))
            msg, addr = udp.recvfrom(1024)
            msg = format(msg.decode().replace("\n", ""))
            print(msg)
            if not msg:
                udp.close()
                return
            elif msg == "goodbye" or msg == "exit":
                udp.close()
                return
                
    else:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host, port = socket.getaddrinfo(host, port)[0][4]
        tcp.connect((host, port))
        msg = input()  
        tcp.sendall((msg).encode())
        while True:
            try:
                data = tcp.recv(1024)
                data = data.decode().replace("\n", "")
                print(data)
                if not data:
                    tcp.close()
                    return
                elif msg == "goodbye" or msg == "exit":
                    tcp.close()
                    return
                msg = input()
                tcp.sendall((msg).encode())
            except KeyboardInterrupt:
                tcp.close()
                return

