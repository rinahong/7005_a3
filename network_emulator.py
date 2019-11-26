#!/usr/bin/python

"""
Network Emulator with UDP
- When a packet is received, check the packet type.
- When the packet type is "Data", forward the packet to receiver.
- When the packet type is "ACK", forward the packet to transmitter.
- Per given error rate from user, Network Emulator has abililty drop the packet randomly.

"""

import socket, select, random, argparse, pickle
import address_config as addr

error_rate = None

RECV_ADDRESS = (addr.receiver['ip'], addr.receiver['port'])
PORT_NUMBER = addr.network_emulator['port']

def emulate_network():
    sobj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      # Create a UDP socket object
    sobj.bind(('', PORT_NUMBER))

    print("Bind to", sobj)

    transmitter_EOT = False
    receiver_EOT = False

    while not transmitter_EOT or not receiver_EOT :
        readable, writable, exceptional = select.select([sobj], [sobj], [])
        packet_type = ''
        recv_packet = ''
        loaded_packet = ''
        send_to_address = ''

        if readable:
            recv_packet, address = sobj.recvfrom(1024)   # buffer size is 1024 bytes from transmitter

            if recv_packet:
                loaded_packet = pickle.loads(recv_packet)
                print("recv_packet", pickle.loads(recv_packet))

                if discard_packet():
                    print("---DISCARD---", loaded_packet)
                    continue


                packet_type = loaded_packet['packet_type']

                if packet_type == 'DATA':
                    transmitter_address = address
                    if loaded_packet['seq'] == 'fin':
                        print("Received FIN ACK from Transmitter")
                        transmitter_EOT = True
                elif packet_type == 'ACK':
                    if loaded_packet['ack'] == 'fin':
                        print("Received FIN ACK from Receiver")
                        receiver_EOT = True

        if writable and loaded_packet:
            send_to_address = RECV_ADDRESS if packet_type == 'DATA' else transmitter_address
            sobj.sendto(recv_packet, send_to_address)

        if transmitter_EOT and receiver_EOT:
            print("Both transmitter and receiver sent FIN ACK successfully. Terminate the program")

    sobj.close()

def discard_packet():
    return random.randrange(100) < error_rate

def get_arguments():
    global error_rate
    parser = argparse.ArgumentParser()
    parser.add_argument("error_rate", help="Error Rate")
    error_rate = int(parser.parse_args().error_rate)

if __name__ == '__main__':
    get_arguments()
    emulate_network()
 
