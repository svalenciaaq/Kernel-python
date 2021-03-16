#!/usr/bin/python
import threading
import os
import socket
import gui as Gui
import file as File
import lexer as Lexer
import app as App


class Kernel:
    clients_list = []
    last_received_message = ""

    def __init__(self):
        self.server_socket = None
        listening = threading.Thread(target=self.create_listening_server)
        modules = threading.Thread(target=self.Start_modules)
        listening.start()
        modules.start()

    def create_listening_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        local_ip = "127.0.0.1"
        local_port = 10319
        # this will allow you to immediately restart a TCP server
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # this makes the server listen to requests coming from other computers on the network
        self.server_socket.bind((local_ip, local_port))
        print("Listening for incoming messages..")
        self.server_socket.listen(5)
        self.receive_messages_in_a_new_thread()

    def receive_messages(self, so):
        while True:
            incoming_buffer = so.recv(256)
            if not incoming_buffer:
                break
            self.last_received_message = incoming_buffer.decode("utf-8")
            self.broadcast_to_all_clients(so)  # send to all clients
        so.close()

    def broadcast_to_all_clients(self, senders_socket):
        for client in self.clients_list:
            socket, (ip, port) = client
            if socket is not senders_socket:
                socket.sendall(self.last_received_message.encode("utf-8"))

    def receive_messages_in_a_new_thread(self):
        while True:
            client = so, (ip, port) = self.server_socket.accept()
            self.add_to_clients_list(client)
            print("Connected to ", ip, ":", str(port))
            t = threading.Thread(target=self.receive_messages, args=(so,))
            t.start()

    def add_to_clients_list(self, client):
        if client not in self.clients_list:
            self.clients_list.append(client)

    def Start_modules(self):
        h4 = threading.Thread(target=Gui.Main)
        h4.start()
        h5 = threading.Thread(target=File.File)
        h5.start()
        h6 = threading.Thread(target=App.App)
        h6.start()