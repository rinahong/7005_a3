
#!/usr/bin/python3

"""
Transmitter with UDP:

TODO print out ongoing session with better message, wireshark

"""

import socket, select, time, datetime, log_helper
import address_config as addr
from collections import defaultdict


TRANS_IP = addr.network_emulator['ip']
TRANS_PORT = addr.network_emulator['port']
WINDOW_SIZE = 5
MAX_RETRANSMISSION = 5
timer_starts_at = None
rtt = 0.5
packets = {}

sobj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # Create a UDP socket object

def transfer_file():
    seq_num = 1
    file_name = 'test'
    log_helper.init_log_file('transmitter_log.html')
    retransmit_count = defaultdict(int)

    file = open(file_name,'rb')
    data = file.read(20)

    print ("===============START===============")

    while (sobj):
        readable, writable, exceptional = select.select([sobj],[sobj],[])
        received_ack = ''
        if readable:
            recv_packet = receive_packet()
            if recv_packet:
                received_ack = recv_packet.decode().split(';')
                if received_ack[1] == 'fin':
                    log_helper.log("FIN IS RETURNED FROM THE RECIEVER --- TERMINATE THE PROGRAM", False, 'pink')
                    break

        if writable:
            if received_ack:
                #Slide window when expected ACK is returned
                if list(packets)[0] == int(received_ack[1]):
                    log_helper.log("YAY~~~ XD ACK is returned! -> " + received_ack[1], False, '')
                    packets.pop(int(received_ack[1]))
                    reset_timer('Yellow')
                else:
                    log_helper.log("Duplicate ACK...." + received_ack[1], True, '')
                    if retransmit_count[int(received_ack[1])] > MAX_RETRANSMISSION:
                        # When retransmit the same packet more than maximum retransmission count..
                        # worthless to continue...
                        break

            #Normal behaviour upon received expected ACK
            while(data and len(packets) < WINDOW_SIZE): #Wait for ACKs from receiver when sending maximum packets
                if len(packets) == 0:
                    reset_timer('Yellow')

                packet = b'SEQ;' + str(seq_num).encode() + b';' + data
                packets[seq_num] = packet
                send_packet(packet)
                log_helper.log("DATA: " + packet.decode(), False, '')
                data = file.read(20)
                seq_num += 1


            #On timeout, retransmit packets
            if timer_starts_at and timeout():
                # if timeout for missing ack:
                reset_timer('pink')
                for seq, packet_data in packets.items():
                    print(seq, packet_data)
                    # retransmission
                    send_packet(packet_data)
                    log_helper.log("Retransmit: " + packet_data.decode(), False, 'grey')
                    retransmit_count[seq] += 1

            #No more data to send
            if not data and len(packets) == 0:
                send_packet(b'SEQ;fin')

    print ("---------------DONE----------------")
    file.close()
    log_helper.terminate_log_file()
    sobj.close()


def reset_timer(highlight):
    global timer_starts_at
    timer_starts_at = time.time()
    log_helper.log("Set timer starts at " + str(timer_starts_at), False, highlight)

def timeout():
    return (time.time() - timer_starts_at) > rtt

def send_packet(packet):
    sobj.sendto(packet, (TRANS_IP, TRANS_PORT))

def receive_packet():
    return sobj.recv(300)

if __name__ == '__main__':
    transfer_file()
