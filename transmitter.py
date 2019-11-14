
#!/usr/bin/python3

"""
Transmitter with UDP:
"""

import socket
import select

TRANS_IP = '192.168.0.4'
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
            #print("readable:=======================================  " )
            # TODO: tracking ACKs and timeout

            #if expected ACK returend
            recv_packet = receive_packet()
            if recv_packet:
                received_ack = recv_packet.decode()
                if received_ack == 'fin':
                    break

        if writable:
            if received_ack:
                # print('all packets', packets)
                # print('received_ack', received_ack)
                packets.pop(int(received_ack))

            while(data and len(packets) < WINDOW_SIZE): #Wait for ACKs from receiver when sending maximum packets
                packet = str(seq_num).encode() + b';' + data
                packets[seq_num] = packet
                send_packet(packet)
                data = file.read(20)
                seq_num = seq_num + 1

                #timeout for ACK

            if not data:
                send_packet('fin'.encode())



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
