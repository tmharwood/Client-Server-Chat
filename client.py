# Author: Tyler Harwood
# Class: CS 372
# Program: Client for the server-client chat program
# Citation: Client code is adapted from the examples on https://realpython.com/python-sockets/ that was provided
# in the assignment specs.

import socket

HOST = "localhost"  # The server's hostname or IP address
PORT = 51055  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        msg = input(">")
        total_sent = 0
        # Code to convert int to bytes adapted from: https://www.geeksforgeeks.org/how-to-convert-int-to-bytes-in-python/
        msg_len = len(msg)
        s.send(msg_len.to_bytes(3, 'big'))
        # send message to server
        while total_sent < msg_len:
            sent = s.send(msg[total_sent:].encode())
            if sent == 0:
                raise RuntimeError("!!!CLIENT!!! Connection broken.")
            total_sent = total_sent + sent
        #print(msg)
        if msg == "/q":
            break
        # receive message from server
        chunks = []
        bytes_rec = 0
        data_len = s.recv(1024)
        data_len = int.from_bytes(data_len, "big")
        #print("!!!CLIENT!!! length of message from server: ", data_len)
        while bytes_rec < data_len:
            chunk = s.recv(min(data_len - bytes_rec, 2048))
            if chunk == b"":
                raise RuntimeError("socket broken")
            chunks.append(chunk)
            bytes_rec += len(chunk)
        if chunks[0] == b"/q":
            break
        print(b''.join(chunks).decode("utf-8"))



#print(f"Received {data!r}")