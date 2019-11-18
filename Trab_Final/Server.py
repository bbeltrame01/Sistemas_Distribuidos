#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()

        print("%s has connected." % client_address[0])
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,client_address[0],)).start()
        if len(addresses) == 2:
            operacao = input("Entre com a operação ( 1 = ligar/ 2 = desligar)")

            mandaMsg();


def handle_client(client, name):  # Takes client socket as argument.
    """Handles a single client connection."""

    clients[client] = client

    while True:
        global bTrue
        msg = client.recv(BUFSIZ)
        if msg:
            print(name, msg)


def mandaMsg():  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        ip = (sock.getsockname()[0])
        msg = input("Entre com o valor para o "+ ip+" ")
        sock.send(bytes("Servidor:" +msg, "utf8"))


clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
bTrue = True
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
