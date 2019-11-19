#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import collections
import math

respClients = []
totalClients = 3
operacao = ""
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()

        print("%s has connected." % client_address[0])
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,client_address[0],)).start()
        if len(addresses) == totalClients:
            entrada = input("Entre com a operação ( 1 = ligar/ 2 = desligar)")
            operacao = entrada
            mandaMsg();


def handle_client(client, name):  # Takes client socket as argument.
    """Handles a single client connection."""

    clients[client] = client

    while True:
        msg = client.recv(BUFSIZ)
        if msg:
            respClients.append(msg)
            print(name, msg)
            if len(respClients) == totalClients:
                consenso()


def consenso():
    respostas = collections.Counter(respClients)
    result = False
    for item in respostas.most_common():
        # 0 valor
        # 1 qtd

        if (math.trunc(len(respClients) / 3) + 1) < item[1]:
            result = item[0].decode("utf-8")

    if bool(result) and result != "False":
        print("A operação será executada")
    else:
        print("Sem consenso, nenhuma operação será executada")

def mandaMsg():  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        ip = (sock.getpeername()[0])
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
