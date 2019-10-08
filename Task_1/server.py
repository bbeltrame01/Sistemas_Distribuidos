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
            msgOper = input("Entre com a operação matemática");

            if(msgOper):
                broadcast(msgOper);


def handle_client(client, name):  # Takes client socket as argument.
    """Handles a single client connection."""

    clients[client] = client

    while True:
        global bTrue
        msg = client.recv(BUFSIZ)
        if  bTrue:
            print(name, msg)
            bTrue = False


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(msg, "utf8"))


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
