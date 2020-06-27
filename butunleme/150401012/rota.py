#150401012 Yiğit Yüre

import socket
import sys

def trace(destinationname):
    destinationaddress = socket.gethostbyname(destinationname)
    port = 33434
    hops = 30
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    file = open("rota.txt","w")
    while True:
        receiver = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        sender.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        receiver.bind(("", port))
        sender.sendto("", (destinationname, port))
        currentaddress = None
        currentname = None
        try:
            _, currentaddress = receiver.recvfrom(512)
            currentaddress = currentaddress[0]
            try:
                currentname = socket.gethostbyaddr(currentaddress)[0]
            except socket.error:
                currentname = currentaddress
        except socket.error:
            pass
        finally:
            sender.close()
            receiver.close()

        if currentaddress is not None:
            currenthost = str(currentname), " ", str(currentaddress)
        else:
            currenthost = "*"
        print(ttl,"\t" currenthost"\n")
        file.write(str(currentaddress)"\n")

        ttl += 1
        if currentaddress == destinationaddress or ttl > hops:
            break
    file.close()

if __name__ =="__main__":
    trace(sys.argv[1])