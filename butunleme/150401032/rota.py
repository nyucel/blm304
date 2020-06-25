# 150401032 Enes TEKİN

import socket
import struct
import sys

name = sys.argv[1]
addr = socket.gethostbyname(name)

f = open("rota.txt", 'w')

max_hops = 30

port = 33434

icmp = socket.getprotobyname('icmp')
udp = socket.getprotobyname('udp')
ttl = 1

while True:

    receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
    sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

    timeout = struct.pack("ll", 3, 0)

    receiver.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)
    receiver.bind(('', port))

    sender.sendto(b'', (name, port))

    curr_addr = None
    kontrol = False
    sayac = 1


    while not kontrol and sayac > 0:
        try:
            _, curr_addr = receiver.recvfrom(512)
            kontrol = True
            curr_addr = curr_addr[0]
        except socket.error:
            sayac = sayac - 1

    sender.close()
    receiver.close()

    if not kontrol:
        pass

    if curr_addr is not None:
        f.write(str(curr_addr) + '\n')

    ttl += 1
    if curr_addr == addr or ttl > max_hops:
        break
