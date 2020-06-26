import sys
import socket
import struct

route = socket.gethostbyname(sys.argv[1])
rota = open("rota.txt","w")
rota.write(sys.argv[1])
rota.write("route IP:",str(route))
rota.write("\n")

MAX_HOPS = 30
port = 33434

icmp = socket.getprotobyname('icmp') 
udp = socket.getprotobyname('udp')
TTL = 1         

while True:
    icmp = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    SOCKETX = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
    SOCKETX.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL)
    TIMEOUT = struct.pack("ll", 3, 0)
    icmp.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, TIMEOUT)
    icmp.bind(("", port))
    SOCKETX.sendto(b"dummy", (sys.argv[1], port))
    ADDR = None
    adres = None
    BOOL = False
    TRIES = 3
    while not BOOL and TRIES > 0:
        try:
            _, ADDR = icmp.recvfrom(512)
            BOOL = True
            ADDR = ADDR[0]
            try:
                adres = socket.gethostbyaddr(ADDR)[0]
            except socket.error:
                adres = ADDR
        except socket.error:
            TRIES = TRIES - 1
    SOCKETX.close()
    icmp.close()

    if not BOOL:
        pass
    if ADDR is not None:
        print(TTL,str(ADDR))
        rota.write(str(ADDR))
        rota.write("\n")
    TTL += 1
    if ADDR == route or TTL > MAX_HOPS:
        break

rota.write("\n")
rota.close()
