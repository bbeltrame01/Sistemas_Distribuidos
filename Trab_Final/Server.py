#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import collections
import math
import requests
import serial
import time

respClients = []
totalClients = 2
operacao = ""
arduino = serial.Serial('COM6', 9600)


def postApi(data):
    API_ENDPOINT = "http://localhost:3000/evento/create"
    r = requests.post(url=API_ENDPOINT, json=data)


def accept_incoming_connections():
    global operacao
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()

        print("%s has connected." % client_address[0])
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,client_address[0],)).start()
        if len(addresses) == totalClients:
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
        arduinoLed()
    else:
        print("Sem consenso, nenhuma operação será executada")

def mandaMsg():  # prefix is for name identification.
    global valorAntigo
    global operacao
    """Broadcasts a message to all the clients."""
    entrada = input("Entre com a operação ( 0 = desligar / 1 = ligar )")
    operacao = entrada
    for sock in clients:
        traidor = 0
        ip = (sock.getpeername()[0])
        msg = input("Entre com o valor para o "+ip+" ")

        if valorAntigo == "":
            valorAntigo = msg;
        elif valorAntigo != msg:
            traidor = 1

        postApi({'origem': 'server', 'destino': ip, 'valor': msg, 'traidor': traidor})
        sock.send(bytes("Servidor:" +msg, "utf8"))


def arduinoLed():
    arduino.write(bytes(operacao, "utf8"))

valorAntigo = ""
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
