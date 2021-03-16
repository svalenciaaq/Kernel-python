#!/usr/bin/python
from tkinter import Tk, Frame, Scrollbar, Label, END, Entry, Text, VERTICAL, Button
import socket
import threading
import gui as Gui
import file as File
from tkinter import messagebox


class GUI:
    client_socket = None
    last_received_message = None

    def __init__(self, master):
        self.root = master
        self.chat_transcript_area = None
        self.name_widget = None
        self.name_widget2 = None
        self.enter_text_widget = None
        self.join_button = None
        self.initialize_socket()
        self.initialize_gui()
        self.listen_for_incoming_messages_in_a_thread()
        print("Gui ready")

    def initialize_socket(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_ip = "127.0.0.1"
        remote_port = 10319
        self.client_socket.connect((remote_ip, remote_port))

    def initialize_gui(self):
        self.root.title("Socket Chat")
        self.root.geometry("1500x200")
        self.root.resizable(0, 0)
        self.display_name_section()

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
            if "joined" in message:
                user = message.split(":")[1]
                message = user + " has joined"
                self.chat_transcript_area.insert("end", message + "\n")
                self.chat_transcript_area.yview(END)
            else:
                self.chat_transcript_area.insert("end", message + "\n")
                self.chat_transcript_area.yview(END)

        so.close()

    def display_name_section(self):
        frame = Frame()
        Label(frame, text="Enter name directory:", font=("Helvetica", 16)).pack(
            side="left", padx=10
        )
        self.name_widget = Entry(frame, width=50, borderwidth=2)
        self.name_widget.pack(side="left", anchor="e")
        self.join_button = Button(
            frame, text="Create", width=10, command=self.create_file
        ).pack(side="left")
        frame.pack(side="top", anchor="nw")
        Label(frame, text="Enter name directory:", font=("Helvetica", 16)).pack(
            side="left", padx=10
        )
        self.name_widget2 = Entry(frame, width=50, borderwidth=2)
        self.name_widget2.pack(side="left", anchor="e")
        self.join_button3 = Button(
            frame, text="Delete", width=10, command=self.delete_file
        ).pack(side="left")

        self.join_button = Button(
            frame, text="Delete", width=10, command=self.start_app
        ).pack(side="left")

    def create_file(self):
        if len(self.name_widget.get()) == 0:
            messagebox.showerror("Enter your name", "Enter name directory")
            return

        self.client_socket.send(("create," + self.name_widget.get()).encode("utf-8"))

    def delete_file(self):
        if len(self.name_widget2.get()) == 0:
            messagebox.showerror("Enter the name", "Enter name directory")
            return
        self.client_socket.send(("delete," + self.name_widget2.get()).encode("utf-8"))

    def start_app(self):
        self.client_socket.send(("startapp").encode("utf-8"))

    def on_close_window(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            self.client_socket.close()
            exit(0)


def Main():
    root = Tk()
    gui = GUI(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_close_window)
    root.mainloop()