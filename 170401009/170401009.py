from scapy.all import *
import time

""" sniff(filter="port 6969",prn=lambda x:x.sprintf("{IP:%IP.src% -> %IP.dst%\n}{Raw:%Raw.load%\n}"))
    //Ağı dinlemek için kullanıyorum
    
    Önemli Notlar.
    
    The maximum safe UDP payload is 508 bytes. This is a packet size of 576, minus the maximum 60-byte IP header and the 8-byte UDP header. Any UDP payload this size or smaller is guaranteed to be deliverable over IP (though not guaranteed to be delivered). Anything larger is allowed to be outright dropped by any router for any reason. Except on an IPv6-only route, where the maximum payload is 1,212 bytes. As others have mentioned, additional protocol headers could be added in some circumstances. A more conservative value of around 300-400 bytes may be preferred instead.

    Any UDP packet may be fragmented. But this isn't too important, because losing a fragment has the same effect as losing an unfragmented packet: the entire packet is dropped. With UDP, this is going to happen either way.

    Interestingly, the maximum theoretical packet size is around 30 MB (1,500 ethernet MTU - 60 IP header x 65,536 maximum number of fragments), though the likelihood of it getting through would be infinitesimal.

    Sources: RFC 791, RFC 2460
    
        
"""

t = AsyncSniffer(filter="udp and (port 6969 or 3131)")
t.start()

for i in range(1,122):
    binary_file=open("cache/part"+str(i).zfill(4),"rb")
    a = IP(dst="192.168.1.1")/UDP(dport=6969,sport=3131)/binary_file.read()
    send(a)
    print("cache/part"+str(i).zfill(4))

time.sleep(3) #Eğer bunu koymazsam paket kaybı yaşanıyor.
t.stop()

dizi=[]
print(t.results)

print("DOSYA UZUNLUĞU = > ",len(t.results))
for i in range(121):
    dizi.append(t.results.res[i].getlayer(Raw).load)




fileobj  = open("test.xd", 'wb+')

for bit in dizi:
    fileobj.write(bit)
fileobj.close()

# print(dizi)

#t.results.show(raw)

# t.results.res[1]
#t = AsyncSniffer(filter="udp and (port 6969 or 3131)")
#t.results.res[0].getlayer(Raw).load

