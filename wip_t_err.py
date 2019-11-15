
#!/usr/bin/python3

"""
Transmitter with UDP:

TODO log file, tracking ACKs and timeout, wireshark

"""

import socket
import select
from collections import defaultdict

TRANS_IP = '192.168.0.15'
TRANS_PORT = 7005
WINDOW_SIZE = 5
MAX_DUPLICATE = 3

timeout = 1
packets = {}

sobj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # Create a UDP socket object

def transfer_file():
    seq_num = 1
    file_name = 'test'
    dupe_count = defaultdict(int)

    file = open(file_name,'rb')
    data = file.read(20)

    print ("===============start===============")

    while (sobj):
        readable, writable, exceptional = select.select([sobj],[sobj],[], timeout)
        received_ack = ''
        if readable:
            recv_packet = receive_packet()
            if recv_packet:
                received_ack = recv_packet.decode().split(';')
                if received_ack[1] == 'fin':
                    break

        if writable:
            if received_ack:
                # print('all packets', packets)
                # print('received_ack', received_ack)

                #WIP - NOT YET TESTED: Checking expected ACK is returned #Only remove from packet if expected ACK is returned
                if list(packets)[0] = int(received_ack[1]):
                    packets.pop(int(received_ack[1]))
                else:
                      dupe_count[received_ack[1]] += 1
                    if dupe_count[received_ack[1]] > MAX_DUPLICATE:
                        # When the same ACK is returned more than maximum duplicate count..
                        # worthless to continue...
                        break
                    elif dupe_count[received_ack[1]] == MAX_DUPLICATE or timeout:
                        #WIP: On timeout, loop through packets and retransmit
                        # if timeout for missing ack:
                        for seq, packet_data in packets:
                            # retransmission
                            send_packet(packet_data)


            #elif normal behaviour upon received expected ACK
            while(data and len(packets) < WINDOW_SIZE): #Wait for ACKs from receiver when sending maximum packets
                packet = b'SEQ;' + str(seq_num).encode() + b';' + data
                packets[seq_num] = packet
                send_packet(packet)
                data = file.read(20)
                seq_num += 1

            if not data and len(packets) == 0:
                send_packet(b'SEQ;fin')


    print("------DONE------")
    file.close()
    sobj.close()

def check_timeout(packet):
    sobj.sendto(packet, (TRANS_IP, TRANS_PORT))
    print ("Packet sent: " + packet.decode())

def send_packet(packet):
    sobj.sendto(packet, (TRANS_IP, TRANS_PORT))

def receive_packet():
    return sobj.recv(300)

if __name__ == '__main__':
    transfer_file()
