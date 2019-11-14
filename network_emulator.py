#!/usr/bin/python

"""
File transfer TCP Client: send or receive
netstat -anp --ip   -> checking udp is running or not

"""

import socket
import select

# This should come from user input.
error_rate = 10

TRANS_IP = '192.168.0.3'
TRANS_PORT = 7005

def emulate_network():
    sobj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      # Create a UDP socket object
    sobj.bind(('', TRANS_PORT))
    packet = ''

    while True:
        readable, writable, exceptional = select.select([sobj], [sobj], [])

        if readable:
            packet, address = sobj.recvfrom(1024)   # buffer size is 1024 bytes from transmitter

        if writable:
            # if address is from transmitter
                # randomly discard per error rate
                # sobj.sendto(packet, receiver_address)
            # else if address is from receiver
                # sobj.sendto(packet, transmitter_address)

    sobj.close()

if __name__ == '__main__':
    emulate_network()
