#170401011 Berfin Okuducu
import socket
import sys

adres=sys.argv[1]
hedef_adres=socket.gethostbyname(adres)
max_yonlendirici=30
ttl=1
proto_icmp = socket.getprotobyname('icmp')
proto_udp = socket.getprotobyname('udp')
port = 33434
block_size=512
f=open("rota.txt",'w')
timeout=0.2

while True:
    received_socket=socket.socket(socket.AF_INET, socket.SOCK_RAW, proto_icmp)
    send_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM, proto_udp)
    send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    received_socket.settimeout(timeout)
    received_socket.bind(('', port))
    send_socket.sendto(b'', (adres, port))

    try:
        veri,simdiki_adres=received_socket.recvfrom(block_size)
        simdiki_adres=simdiki_adres[0]

    except socket.error:
        simdiki_adres=None
    send_socket.close()
    received_socket.close()
    if(simdiki_adres is not None):
        simdiki_adres=str(simdiki_adres)
        f.write(simdiki_adres+"\n")
    ttl+=1
    if(simdiki_adres==hedef_adres or ttl>max_yonlendirici):
        break

f.close()


