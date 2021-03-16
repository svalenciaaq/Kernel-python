#!/usr/bin/python
import os
import socket
import threading
import lexer as Lexer


class App:
    client_socket = None
    last_received_message = None

    def __init__(self):
        self.initialize_socket()
        self.listen_for_incoming_messages_in_a_thread()
        print("App Ready ready")

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = "127.0.0.1"
        remote_port = 10319
        self.client_socket.connect((remote_ip, remote_port))

    def listen_for_incoming_messages_in_a_thread(self):
        thread = threading.Thread(
            target=self.receive_message_from_server, args=(self.client_socket,)
        )
        thread.start()

    def receive_message_from_server(self, so):
        while True:
            buffer = so.recv(256)
            if not buffer:
                break
            message = buffer.decode("utf-8")
            # self.chat_transcript_area.insert('end', message + '\n')
            # self.chat_transcript_area.yview(END)
            inpu = Lexer.Lexer.checkGrammar(message)
            if inpu == "starapp":
                self.start_app()

        so.close()

    def start_app(self):
        count1 = 0
        for count1 in range(10):
            print("Hilo 1: " + str(count1))
