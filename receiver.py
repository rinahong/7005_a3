#!/usr/bin/python

"""
Author: Rina Hong (A00964022)
Receiver with UDP.
-  Upon receiving a packet, check whether sequence number is  expected or not.
-  When receiving expected one, parse data from the packet and save it to a file.
-  When receiving duplicate one or undesirable sequence number, discard the packet.
-  Always return ACK if packet is received from transmistter.
"""

import socket, select, time, datetime, pickle, log_helper
import address_config as addr

PORT_NUMBER = addr.receiver['port']
MAXIMUM_SECONDS_IDLE = 5

timer_starts_at = None

def receive_file():
    sobj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      # Create a UDP socket object
    sobj.bind(('', PORT_NUMBER))
    print("Bind to ", sobj)
    log_helper.init_log_file('receiver_log.html')
    file_name = 'file_from_transmitter_when_error_rate_10'

    expected_seq = 1
    with open(file_name, 'wb') as f:
        while True:
            recv_packet = ''
            readable, writable, exceptional = select.select([sobj], [sobj], [])

            if readable:
                recv_packet, address = sobj.recvfrom(1024)   # buffer size is 1024 bytes from transmitter
                recv_packet = pickle.loads(recv_packet)

                #Upon FIN ACK is received, Send FIN ACK to terminate
                if recv_packet['seq'] == "fin":
                    print("Received FIN ACK from Transmitter.")
                    packet = construct_pakcet('ACK', None, "fin", None)
                    sobj.sendto(pickle.dumps(packet), address)
                    log_helper.log("FIN IS RECIVED FROM THE TRANSMITTER. SEND FIN BACK TO TRANSMITTER", False, 'pink')
                    reset_timer('yellow')
                else:
                    # Save data only if packet has a expected SEQ num
                    if recv_packet['seq'] == expected_seq:
                        log_helper.log("YAY~~~ XD Expected packet is received: " + str(expected_seq), False, '')
                        print("Save:", recv_packet['seq'], recv_packet['data'])
                        f.write(recv_packet['data'])
                        expected_seq = recv_packet['seq'] + 1
                    else:
                        print("Discard received packet with SEQ", recv_packet['seq'])
                        log_helper.log("Discard received packet. Expected: " + str(expected_seq) + ", but received: " + str(recv_packet['seq']), True, '')

            if writable:
                # Always sends ACK back to transmitter
                if(recv_packet):
                    print('Send ACK:', recv_packet['seq'])
                    packet = construct_pakcet('ACK', None, recv_packet['seq'], None)
                    sobj.sendto(pickle.dumps(packet), address)
                    log_helper.log("Send ACK: " + str(recv_packet['seq']) + " to transmitter", False, '')


            if timer_starts_at and time_to_terminate():
                print("Waited", MAXIMUM_SECONDS_IDLE ,"seconds after sending final FIN ACK. -- Safe to terminate the program", time.time())
                log_helper.log("IDLE STATE AFTER FIN ACK SENT --- TERMINATE THE PROGRAM", False, 'pink')
                f.close()
                break

    sobj.close()


def reset_timer(highlight):
    global timer_starts_at
    timer_starts_at = time.time()
    print("Timer started for tracking idle state", timer_starts_at)
    log_helper.log("Set timer starts at " + str(timer_starts_at), False, highlight)

def time_to_terminate():
    return (time.time() - timer_starts_at) > MAXIMUM_SECONDS_IDLE


def construct_pakcet(packet_type, seq, ack, data):
    return {
        'packet_type': packet_type,
        'seq': seq,
        'ack': ack,
        'data': data
    }


if __name__ == '__main__':
    receive_file()
