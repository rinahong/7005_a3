#!/usr/bin/python3

"""
Author: Rina Hong (A00964022)
Transmitter with UDP
- Sliding window is implemented with timeout feature
- Upon receiving expected ACK, reset timer and send next data if exists
- Upon receiving undesirable ACK and on timeout, retransmit all packets in the window.

"""

import socket, select, time, datetime, pickle, log_helper
import address_config as addr
from collections import defaultdict

TRANS_IP = addr.network_emulator['ip']
TRANS_PORT = addr.network_emulator['port']
WINDOW_SIZE = 5
MAX_RETRANSMISSION = 5
BYTES_SIZE_TO_READ = 20

timer_starts_at = None
rtt = 0.5
packets = {}

sobj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # Create a UDP socket object

def transfer_file():
    seq_num = 1
    fin_sent = False
    file_name = 'test'
    log_helper.init_log_file('transmitter_log.html')
    retransmit_count = defaultdict(int)

    file = open(file_name,'rb')
    data = file.read(BYTES_SIZE_TO_READ)

    print ("===============START===============")

    while (sobj):
        readable, writable, exceptional = select.select([sobj],[sobj],[])
        recv_packet = ''
        if readable:
            recv_packet = receive_packet()
            if recv_packet:
                recv_packet = pickle.loads(recv_packet)
                #Termiate the program gracefully upon receiving fin
                if recv_packet['ack'] == 'fin':
                    log_helper.log("FIN IS RETURNED FROM THE RECIEVER --- TERMINATE THE PROGRAM", False, 'pink')
                    break

        if writable:
            if recv_packet:
                #Initiate sliding window by removing a packet from window when expected ACK is returned.
                if list(packets)[0] == recv_packet['ack']:
                    log_helper.log("YAY~~~ XD ACK is returned! -> " + str(recv_packet['ack']), False, '')
                    packets.pop(recv_packet['ack'])
                    reset_timer('Yellow')
                else:
                    log_helper.log("Expected: " + str(list(packets)[0]) + ", but received: " + str(recv_packet['ack']), True, '')


            #Normal behaviour upon received expected ACK
            while(data and len(packets) < WINDOW_SIZE): #Wait for ACKs from receiver when sending maximum packets
                if len(packets) == 0:
                    reset_timer('Yellow')

                packet = construct_packet('DATA', seq_num, None, data)
                packets[seq_num] = packet
                send_packet(pickle.dumps(packet))
                print("Transmit : ", seq_num, packet['data'])
                log_helper.log("DATA: " + str(packet['seq']) + ";" + packet['data'].decode(), False, '')
                data = file.read(BYTES_SIZE_TO_READ)
                seq_num += 1


            #On timeout, retransmit packets
            if len(packets) > 0 and timer_starts_at and timeout():
                # if timeout for missing ack:
                reset_timer('pink')

                #Track a packet timeout.
                retransmit_count[list(packets)[0]] += 1
                if retransmit_count[list(packets)[0]] > MAX_RETRANSMISSION:
                    print("Something is seriously wrong... maximum retransmission is reached... EXIT THE PROGRAM")
                    log_helper.log("Something is seriously wrong... maximum retransmission is reached... EXIT THE PROGRAM", False, 'red')
                    # When retransmit the same packet more than maximum retransmission count..
                    # worthless to continue...
                    break
                for seq, packet_obj in packets.items():
                    print("Retransmit: ", seq, packet_obj['data'])
                    # retransmission
                    send_packet(pickle.dumps(packet_obj))
                    log_helper.log("Retransmit: " + str(packet_obj['seq']) + ";" + packet_obj['data'].decode(), False, 'grey')

            #No more data to send
            if not data:
                if(len(packets) == 0 and not fin_sent) or (fin_sent and timeout()):
                    print("Transmitting FIN ACK to receiver")
                    log_helper.log("Transmitting FIN ACK to receiver", False, '')
                    fin_sent = True
                    packet = construct_packet('DATA', "fin", None, None)
                    send_packet(pickle.dumps(packet))
                    reset_timer('aqua')

    print ("---------------DONE----------------")
    file.close()
    log_helper.terminate_log_file()
    sobj.close()


#Reset timer on timeout
def reset_timer(highlight):
    global timer_starts_at
    timer_starts_at = time.time()
    log_helper.log("Set timer starts at " + str(timer_starts_at), False, highlight)

#Check timeout
def timeout():
    return (time.time() - timer_starts_at) > rtt

def send_packet(packet):
    sobj.sendto(packet, (TRANS_IP, TRANS_PORT))

def receive_packet():
    return sobj.recv(1024)

#Construct packet as a dictionary
def construct_packet(packet_type, seq, ack, data):
    return {
        'packet_type': packet_type,
        'seq': seq,
        'ack': ack,
        'data': data
    }


if __name__ == '__main__':
    transfer_file()
