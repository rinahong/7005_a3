#!/usr/bin/python

"""
File transfer TCP Client: send or receive
netstat -anp --ip   -> checking udp is running or not

"""

import socket, select, log_helper
import address_config as addr

PORT_NUMBER = addr.receiver['port']

def udp_receiver():
    sobj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      # Create a UDP socket object
    sobj.bind(('', PORT_NUMBER))
    log_helper.init_log_file('receiver_log.html')
    file_name = 'test'

    expected_seq = 1
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
                    log_helper.log("FIN IS RECIVED FROM THE TRANSMITTER --- TERMINATE THE PROGRAM", False, 'pink')
                    f.close()
                    break
                else:
                    # Save data only if packet has a expected SEQ num
                    if packet[1] == expected_seq:
                        log_helper.log("YAY~~~ XD Expected packet is received: " + expected_seq, False, '')
                        data_to_save = ''.join(packet[2:len(packet)])
                        f.write(data_to_save.encode())
                        expected_seq = packet[1] + 1
                    else:
                        log_helper.log("Discard :( " + expected_seq, True, '')

            if writable:
                # Always sends ACK back to transmitter
                if(packet):
                    print('------wrtiable=========', packet[0].encode())
                    sobj.sendto(b'ACK;' + packet[1].encode(), address)
                    log_helper.log("ACK: " + packet[1], False, '')

    sobj.close()

if __name__ == '__main__':
    udp_receiver()
