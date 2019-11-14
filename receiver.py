#!/usr/bin/python

"""
File transfer TCP Client: send or receive
netstat -anp --ip   -> checking udp is running or not

"""

import socket
import select

track_seq = 0

TRANS_IP = '192.168.0.3'
TRANS_PORT = 7005

def udp_receiver():
    sobj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      # Create a UDP socket object
    sobj.bind(('', TRANS_PORT))
    file_name = 'test'
    packet = ''
    with open(file_name, 'wb') as f:
        while True:
            readable, writable, exceptional = select.select([sobj], [sobj], [])
            #print('readable', readable)
            #print('writable', writable)
            if readable:
                packet, address = sobj.recvfrom(1024)   # buffer size is 1024 bytes from transmitter
                print('!!!!!!!!!!!!readable!!!!!!!', packet.decode())

                packet = packet.decode().split(';')

                if packet[0] == "fin":
                    sobj.sendto(packet[0].encode(), address)
                    f.close()
                    break
                else:
                    f.write(packet[1].encode())



            if writable:
                # if expected seq
                # write data into opened file and send ack back to transmitter
                # RETRUN ACK to network_emulator
                if(packet):
                    print('------wrtiable=========', packet[0].encode())
                    sobj.sendto(packet[0].encode(), address)
                    packet = ''

    sobj.close()

if __name__ == '__main__':
    udp_receiver()
