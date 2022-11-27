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
        #conn.setblocking(False)
        print(f"Connected by {addr}")
        while True:
            data_len = conn.recv(1024)
            if data_len == b"/q":
                break
            # code to convert from byte to int adapted from: https://www.geeksforgeeks.org/how-to-convert-bytes-to-int-in-python/
            data_len = int.from_bytes(data_len, "big")
            #print("!!!SERVER!!! length of msg rec: ", data_len)

            chunks = []
            bytes_rec = 0
            # Start receiving data in a loop

            while bytes_rec < data_len:
                chunk = conn.recv(min(data_len - bytes_rec, 2048))
                if chunk == b"":
                    raise RuntimeError("sockey broken")
                chunks.append(chunk)
                bytes_rec += len(chunk)
            if chunks[0] == b"/q":
                break
            print(b''.join(chunks).decode("utf-8"))

            # Get input to send back to client
            send_data = input(">")
            send_len = len(send_data)
            total_sent = 0

            # Send message length
            conn.send(send_len.to_bytes(3, 'big'))
            #print("server msg len: ", send_len)
            #conn.sendall(data)

            # Start sending data in a loop
            while total_sent < send_len:
                sent = conn.send(send_data[total_sent:].encode())
                if sent == 0:
                    raise RuntimeError("!!!SERVER!!! Connection broken.")
                total_sent = total_sent + sent
            if send_data == "/q":
                break