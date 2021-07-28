#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(msg)
        except OSError:
            print("erreur")
            break


def send():
    while True :
        msg=input()    
        client_socket.send(bytes(msg, "utf8"))





HOST= '127.0.0.1'
PORT = 30000


BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM) #le type du socket : SOCK_STREAM pour le protocole TCP
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

receive_thread = Thread(target=send)
receive_thread.start()
