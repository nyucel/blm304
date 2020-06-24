#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ad: Ufuk
Soyad: KORKMAZ

Öğrenci No: 190401109
Tarih: Salı Haz 23 03:47:08 2020
"""


import socket
import sys
import time
import random

HOPS_MAX = 30  # maksimum 30 yönlendiriciye kadar deneme yapılcaktır.

def get_rand_port():
    return random.choice(range(33434,33535))  # rastgele olarak 33434-33535 arasında bir port numarası seçilir

class Rota(object):
    def __init__(self,dest,hops):
        self.TTL = 1
        self.hops = hops
        self.dest = dest
        self.port = get_rand_port()
        self.payload = bytes("Big Bang Boommmmmmmmmmmmm!!!","utf-8")
        self.send_sock = socket.socket(
                         family=socket.AF_INET,
                         type=socket.SOCK_DGRAM,
                         proto=socket.IPPROTO_UDP)

        self.recv_sock = socket.socket(family=socket.AF_INET,
                                       type=socket.SOCK_RAW,
                                       proto=socket.IPPROTO_ICMP)
        self.recv_sock.bind(('', self.port))
        self.recv_sock.settimeout(1)

    def traceroute(self):
        try:
            dest_ip = socket.gethostbyname(self.dest)
            print("route packets trace to {} ({}), {} hops max, {} byte packets".format(self.dest,dest_ip,self.hops,len(self.payload)))
            control = True
            with self.send_sock, self.recv_sock, open("rota.txt","w") as rota_file:
                while control:
                    self.send_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, self.TTL)
                    start_t = time.time()
                    self.send_sock.sendto(self.payload,(self.dest,self.port))
                    try:
                        icmp_msg, addr = self.recv_sock.recvfrom(1024)
                        end_t = time.time()
                        rtt = end_t - start_t # Round Trip Time (RTT) hesaplanması
                        rtt = "%.4f" % (rtt*1000)
                        if addr:
                            rota_file.write("TTL = {:<4} {} ({}) rtt = {} ms\n".format(self.TTL,socket.gethostbyaddr(addr[0])[0],addr[0],rtt))
                            print("TTL = {:<3} {} ({}) rtt = {} ms".format(self.TTL,socket.gethostbyaddr(addr[0])[0],addr[0],rtt))
                            #print(icmp_msg.decode('utf-8','replace'))
                        else:
                            rota_file.write("TTL={:<4} ***".format(self.TTL))
                            print("TTL={:<3} ***".format(self.TTL))
                    except socket.herror as error:
                        if error.errno == 1:  # Unknown Host hatası olduğunda
                            rota_file.write("TTL = {:<4} {} ({}) rtt = {} ms\n".format(self.TTL,addr[0],addr[0],rtt))
                            print("TTL = {:<3} {} ({}) rtt = {} ms".format(self.TTL,addr[0],addr[0],rtt))
                        else:
                            print(str(error))
                            sys.exit(1)
                    except socket.timeout:
                        rota_file.write("TTL = {:<4} ***\n".format(self.TTL))
                        print("TTL = {:<3} ***".format(self.TTL))
                    self.TTL += 1
                    if addr[0] == dest_ip or self.TTL > self.hops:
                        control = False
            print("\ntrace completed, rota.py output >> rota.txt")
        except Exception as ex:
            print(str(ex))
            sys.exit(1)



def run(argv):
    if len(argv) > 0:
        rota = Rota(argv[0], HOPS_MAX)
        rota.traceroute()
    else:
        print("Kullanım: rota.py HOSTNAME")
        print("Örnek: rota.py www.comu.edu.tr")

if __name__ == "__main__":
    run(sys.argv[1:])
