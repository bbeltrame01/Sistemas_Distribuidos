#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import collections
import math

bConectClient = True

messageArray = []


def receive(client_socket):
    global bConectClient
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if msg:
                result = str(msg)
                print("Valor recebido", result)
                result = result.split(':')
                messageArray.append(result[1])
                if bConectClient:
                    bConectClient = False
                    conectClients()

            if len(messageArray) == (len(clientsConnection) + 1):
                consenso()

        except OSError:  # Possibly client has left the chat.
            break


def consenso():
    global messageArray
    counter = collections.Counter(messageArray)
    resposta = False

    for item in counter.most_common():
        # 0 valor
        # 1 qtd
        if (math.trunc(len(messageArray) / 3) + 1) < item[1]:
            resposta = item[0]

    send(client_socket_server, resposta)


def send(client_socket, mensagem):  # event is passed by binders.

   client_socket.send(bytes(str(mensagem), "utf8"))
   if mensagem == "{quit}":
       client_socket.close()


def conectClients():
    for client in clientsConnection:
        ADDR = (client[0], client[1])

        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(ADDR)

        receive_thread = Thread(target=receive, args=(client_socket,))
        receive_thread.start()

#CONEXAO SERVIDOR
BUFSIZ = 1024
ADDR = ('192.168.43.34', 33000)

client_socket_server = socket(AF_INET, SOCK_STREAM)
client_socket_server.connect(ADDR)

receive_thread = Thread(target=receive, args=(client_socket_server,))
receive_thread.start()

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()

        print("%s has connected." % client_address[0])
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,client_address[0],)).start()
        if len(addresses) == len(clientsConnection):
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
        msg = input("Entre com o valor para o "+ip+" ")
        sock.send(bytes("Cliente:"+msg, "utf8"))


clients = {}
addresses = {}

#LIBERANDO CONEXAO VIA SOCKET
HOST = ''
PORT = 33001
BUFSIZ = 1024
ADDR = (HOST, PORT)
bTrue = True
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

clientsConnection = [
    ('192.168.43.34', 33002),
    #('192.168.43.34', 33003)
]


if __name__ == "__main__":
    SERVER.listen(5)
    print("Cliente 1 Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
