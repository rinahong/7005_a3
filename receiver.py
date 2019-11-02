#!/usr/bin/python

"""
File transfer TCP Client: send or receive

"""

import sys
import socket

def udp_receiver():
    GETTER_IP = ''                                # '' to set the default IP to localhost
    GETTER_PORT = 700

    sockobj = socket(AF_INET, SOCK_STREAM)      # Create a TCP socket object
    sockobj.connect((serverHost, serverPort))   # connect to server IP + port

    newSockobj = socket(AF_INET, SOCK_STREAM)      # Create a TCP socket object

    user_request = ask_user_input()
    sockobj.send(user_request.encode())

    while True:
        data = sockobj.recv(1024)
        print("new port is created from server for file transfer:", data.decode())
        if(data.decode() == "--7006--"):
            newSockobj.connect((serverHost, 7006))   # connect to server IP + port
            if(user_request == "1"):
                send(newSockobj)
                break
            else:
                get(newSockobj)
                break


    sockobj.close()

def get(sockobj):
    file_name = input("Please enter file name to transfer\n")
    sockobj.send(file_name.encode())
    with open(file_name, 'wb') as f:
        while True:
            data = sockobj.recv(1024)
            f.write(data)
            if not data:
                break

if __name__ == '__main__':
    udp_receiver()
