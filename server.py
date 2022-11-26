# Author: Tyler Harwood
# Class: CS 372
# Program: Server for the server-client chat program
# Citation: Server code is adapted from the examples on https://realpython.com/python-sockets/ that was provided
# in the assignment specs.

import socket

HOST = "localhost"
PORT = 51055


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data_len = conn.recv(1024)
            if not data_len or data_len == b"/q":
                break
            # code to convert from byte to int adapted from: https://www.geeksforgeeks.org/how-to-convert-bytes-to-int-in-python/
            data_len = int.from_bytes(data_len, "big")
            print("!!!SERVER!!! length of msg rec: ", data_len)
            data = conn.recv(2048)
            if not data or data == b"/q":
                break
            print("SERVER received: ", data)
            conn.send(data_len.to_bytes(3, 'big'))
            print("echo length: ", data_len)
            conn.sendall(data)