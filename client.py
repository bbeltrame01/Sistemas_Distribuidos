#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def receive():
   while True:
       try:
           msg = client_socket.recv(BUFSIZ).decode("utf8")
           if msg:
               result = str(eval(msg))
               print("Result= ",result)
               client_socket.send(bytes(result, "utf8"))


       except OSError:  # Possibly client has left the chat.
           break
def send(mensagem):  # event is passed by binders.

   client_socket.send(bytes(mensagem, "utf8"))
   if mensagem == "{quit}":
       client_socket.close()

BUFSIZ = 1024
ADDR = ('192.168.1.157', 33000)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()

