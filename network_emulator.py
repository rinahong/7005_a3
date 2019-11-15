#!/usr/bin/python

"""
File transfer TCP Client: send or receive
netstat -anp --ip   -> checking udp is running or not

"""

import socket
import select

# This should come from user input.
error_rate = 10

RECV_ADDRESS = ('192.168.0.16', 7006)
PORT_NUMBER = 7005

def emulate_network():
    sobj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      # Create a UDP socket object
    sobj.bind(('', PORT_NUMBER))

    transmitter_EOT = False
    receiver_EOT = False

    while not transmitter_EOT or not receiver_EOT :
        readable, writable, exceptional = select.select([sobj], [sobj], [])
        packet_type = ''
        packet = ''

        if readable:
            packet, address = sobj.recvfrom(1024)   # buffer size is 1024 bytes from transmitter
            packet_type = packet.decode().split(';')[0]
            print("readable address", address)

            #TODO refactor this....
            if packet_type == 'SEQ':
                transmitter_address = address
                if packet.decode().split(';')[1] == 'fin':
                    transmitter_EOT = True
            elif packet_type == 'ACK':
                if packet.decode().split(';')[1] == 'fin':
                    receiver_EOT = True

        if writable:
            if packet_type == 'SEQ':
                # TODO randomly discard per error rate
                sobj.sendto(packet, RECV_ADDRESS)
            elif packet_type == 'ACK':
                sobj.sendto(packet, transmitter_address)

    sobj.close()

if __name__ == '__main__':
    emulate_network()
