from scapy.all import sr1,IP,UDP
import os,sys


# Ahmet Orbay 100401053


def control(hostname):
    if(os.path.exists("rota.txt")):
            os.remove("rota.txt")
    with open("rota.txt", "a") as rota:
        for ttlNumber in range(1, 31):
            dportDefault=33433+ttlNumber 
            counter=0
            while counter<3:
                package = IP(dst=hostname, ttl=ttlNumber)/UDP(dport=dportDefault)
                response = sr1(package, verbose=0,timeout=1)
                counter+=1
            if response is None:
                continue
            
            elif response.type == 3:
                print ("Hedef Adres!", response.src)
                break
            else:
                rota.write(str(response.src)+"\n")
                print ("ttl=%d " % ttlNumber , response.src)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Lutfen python3 rota.py makineAdi seklinde giris yapiniz.")
    else:
        control(sys.argv[1])
