#!/usr/bin/python

"""
File transfer TCP Client: send or receive
netstat -anp --ip   -> checking udp is running or not

"""

import socket
import select

track_seq = 0

PORT_NUMBER = 7006

def udp_receiver():
    sobj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      # Create a UDP socket object
    sobj.bind(('', PORT_NUMBER))
    file_name = 'test'

    seq_array = []
    with open(file_name, 'wb') as f:
        while True:
            packet = ''
            readable, writable, exceptional = select.select([sobj], [sobj], [])

            if readable:
                packet, address = sobj.recvfrom(1024)   # buffer size is 1024 bytes from transmitter
                print('!!!!!!!!!!!!readable!!!!!!!', packet.decode())

                packet = packet.decode().split(';')

                if packet[1] == "fin":
                    sobj.sendto(b'ACK;' + packet[1].encode(), address)
                    f.close()
                    break
                else:
                    # Check if expected SEQ is returned.
                    # TODO: save data only if packet[1] == expected_seq:
                        data_to_save = ''.join(packet[2:len(packet)])
                        f.write(data_to_save.encode())

            if writable:
                # RETRUN ACK to network_emulator
                if(packet):
                    print('------wrtiable=========', packet[0].encode())
                    sobj.sendto(b'ACK;' + packet[1].encode(), address)

    sobj.close()

if __name__ == '__main__':
    udp_receiver()
