
#!/usr/bin/python3

"""
TCP server:
1. Listen for a client connectin
2. Responsd to a file transfer request form the client [1 (Client sends a file)  or 2 (Server sends a file)]

"""

from socket import *
from datetime import datetime

myHost = ''                                 # '' to set the default IP to localhost
port7005  = 7005                            # Initial port
port7006  = 7006                            # File transfer port

sobj1 = socket(AF_INET, SOCK_STREAM)        # Create a TCP socket object for initial connection
sobj1.bind((myHost, port7005))              # bind it to server port number for initial connection
sobj1.listen(5)

sobj2 = socket(AF_INET, SOCK_STREAM)        # Create a TCP socket object for file transfer
sobj2.bind((myHost, port7006))              # bind it to server port number for file transfer

def file_transfer():
    while True:
        connection1.send("--7006--".encode())
        connection2, address2 = sobj2.accept()
        print('Second client connection: ', address2)

        if(address2 != ""):
            if option.decode() == "1":
                #file_name = input("Please enter file name to save\n")
                file_name = "client_" + datetime.now().strftime("%Y%m%d_%H:%M:%S")
                print("File from the client is saved as " + file_name)
                with open(file_name, 'wb') as f:
                    while True:
                        data = connection2.recv(1024)
                        f.write(data)

                        if not data:
                            break
                    f.close()
            else:
                while True:
                    file_name = connection2.recv(1024)
                    if(file_name != ""):
                        f = open(file_name,'rb')
                        l = f.read(1024)
                        while (l):
                            connection2.send(l)
                            l = f.read(1024)
                        break

        if(connection2):
            break

    connection2.close()
    sobj2.close()


while True:                                 # listen until process killed
    connection1, address1 = sobj1.accept()
    option = ""
    print('Client Connection:', address1)    # Print the connected client address

    if(address1 != ""):
        option = connection1.recv(1024)
        sobj2.listen(5)
        print('option :', option.decode())
        if(option.decode() != ""):
            file_transfer()


    if(connection1):
        break

connection1.close()
sobj1.close()

print("------Both connection is closed---------")
