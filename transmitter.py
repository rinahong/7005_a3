
#!/usr/bin/python3

"""
Transmitter with UDP:
"""

import socket

TRANS_IP = ''                                # '' to set the default IP to localhost
TRANS_PORT = 7005                            # Initial port

sobj = socket.socket(AF_INET, SOCK_STREAM)   # Create a UDP socket object

def file_transfer():
    print "Transmitter ip: ", TRANS_IP
    print "Transmitter port: ", TRANS_PORT
    file = open(file_name,'rb')
    data = file.read(1024)
    while (data):
        data = file.read(1024)
        sobj.sendto(data, (TRANS_IP, TRANS_PORT))
        # TODO: tracking SEQ and ACKs

    # necessary??
    file.close()
    sobj.close()

print("------DONE------")
