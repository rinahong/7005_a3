
#!/usr/bin/python3

"""
Transmitter with UDP:
"""

import socket, select, pickle
import Packet from Packet

TRANS_IP = '192.168.0.15'
TRANS_PORT = 7005
WINDOW_SIZE = 5

timeout = 10
packets = {}

sobj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # Create a UDP socket object

def transfer_file():
    seq_num = 1
    file_name = 'test'

    file = open(file_name,'rb')
    data = file.read(20)

    print ("===============start===============")

    while (sobj):
        readable, writable, exceptional = select.select([sobj],[sobj],[], timeout)
        received_ack = ''
        if readable:
            # TODO: tracking ACKs and timeout

            #if expected ACK returend
            recv_packet = receive_packet()
            if recv_packet:
                received_ack = recv_packet.decode().split(';')
                if received_ack[1] == 'fin':
                    break

        if writable:
            if received_ack:
                packets.pop(int(received_ack[1]))

            while(data and len(packets) < WINDOW_SIZE): #Wait for ACKs from receiver when sending maximum packets
                packet = Packet('DATA', seq_num) b'SEQ;' + str(seq_num).encode() + b';' + data
                packets[seq_num] = packet
                send_packet(packet)
                data = file.read(20)
                seq_num = seq_num + 1

                #timeout for ACK

            if not data and len(packets) == 0:
                packet = Packet('EOT', 'fin')
                send_packet(pickle.dumps(current_packet)b'SEQ;fin')

    print("------DONE------")
    file.close()
    sobj.close()

def check_timeout(packet):
    sobj.sendto(packet, (TRANS_IP, TRANS_PORT))
    print ("Packet sent: " + packet.decode())

def send_packet(packet):
    sobj.sendto(packet, (TRANS_IP, TRANS_PORT))
    #print ("Packet sent: " + packet.decode())

def receive_packet(): #for receiving a pkt from server
    return sobj.recv(300)

if __name__ == '__main__':
    transfer_file()
