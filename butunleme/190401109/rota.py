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
    unused_ports = range(33434,33535)
    return random.choice(unused_ports)  # rastgele olarak 33434-33535 arasında bir port numarası seçilir

class Rota(object):
    def __init__(self,dest,hops):
        self.TTL = 1
        self.hops = hops
        self.dest = dest
        self.port = get_rand_port()
        self.payload = bytes("Bigggggggggg Banggggggggg Boommmmmmmmmmmmm!!!","utf-8") # Karşıya gönderilecek dump verisi
        self.dgram_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP) # UDP packeti gödermek için
        self.raw_sock = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket.IPPROTO_ICMP) # Hedef makineden ICMP mesajları almak için
        self.raw_sock.bind(('', self.port))
        self.raw_sock.settimeout(1.5)

    def get_route_packets_trace(self):
        try:
            dest_ip = socket.gethostbyname(self.dest)
            print("route packets trace to {} ({}), {} hops max, {} byte packets".format(self.dest,dest_ip,self.hops,len(self.payload)))
            control = True
            with self.dgram_sock, self.raw_sock, open("rota.txt","w") as rota_file:
                while control:
                    self.dgram_sock.setsockopt(socket.SOL_IP, socket.IP_TTL, self.TTL)
                    start_t = time.time()
                    self.dgram_sock.sendto(self.payload,(self.dest,self.port))
                    try:
                        icmp_msg, addr = self.raw_sock.recvfrom(1024)
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
                        if error.errno == 1 or error.errno == 2:  # Unknown Host hatası olduğunda
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
            print("\ntrace completed successfully, rota.py output >> rota.txt")
        except Exception as ex:
            print(str(ex))
            sys.exit(1)


def run_rota_tracer(argv):
    if len(argv) > 0:
        rota = Rota(argv[0], HOPS_MAX)
        rota.get_route_packets_trace()
    else:
        print("kullanım: rota.py HOSTNAME")
        print("orn: rota.py www.comu.edu.tr")

if __name__ == "__main__":
    run_rota_tracer(sys.argv[1:])
