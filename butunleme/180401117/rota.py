#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Onur ETLİOĞLU (180401117)


import os
import sys
import time
import socket
import struct

ICMP_ECHO_REQUEST = 8  # ICMP message type
DUMP_DATA = "bbHHh"

def header_checksum(string):
    string = bytearray(string)
    chksum = 0
    limit = (len(string) // 2) * 2
    for i in range(limit,2):
        val = string[i] + (string[i+1]*256)
        chksum += val
        chksum = chksum & 0xffffffff

    if limit < len(string):
        chksum += string[-1]
        chksum = chksum & 0xffffffff

    chksum = (chksum >> 16) + (chksum & 0xffff)
    chksum = chksum + (chksum >> 16)

    chksum = ~chksum
    chksum = chksum & 0xffff
    chksum = chksum >> 8 | (chksum << 8 & 0xff00)

    return chksum

def build_icmp_packet():
    checksum = 0
    id_ = os.getpid() & 0xFFFF
    header = struct.pack(DUMP_DATA, ICMP_ECHO_REQUEST, 0, checksum, id_, 1)
    data = struct.pack("d", time.time())
    packet = header + data
    checksum = header_checksum(packet)
    checksum = socket.htons(checksum)

    header = struct.pack(DUMP_DATA, ICMP_ECHO_REQUEST, 0, checksum, id_, 1)
    packet = header + data

    return packet


def trace_route(hostname):
    try:
        dest_ip_addr = socket.gethostbyname(hostname)
        icmp = socket.getprotobyname("icmp")
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,icmp)
        rsock = socket.socket(socket.AF_INET,socket.SOCK_RAW,icmp)
        rsock.bind(('',0))
        rsock.settimeout(2)
        print("rota: ICMP Traceroute")
        print("dest = [{} ({})], MAX_HOPS = 30".format(hostname,dest_ip_addr))
        dosya = open('rota.txt','w')
        for ttl in range(1,31): # hops = 30:
            packet = build_icmp_packet()
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, struct.pack('I', ttl))
            sock.sendto(packet, (dest_ip_addr, 0))
            try:
                recv_pack, src_addr = rsock.recvfrom(1024)
                dosya.write("ttl={:<3}=> {}\n".format(ttl,src_addr[0]))
                print("ttl={:<3}=> {}".format(ttl,src_addr[0]))
                if src_addr[0] == dest_ip_addr:
                    break
            except socket.timeout:
                dosya.write("ttl={:<3}=> *\n".format(ttl))
                print('ttl={:<3}=> *'.format(ttl))
                continue
    except Exception() as e:
        print(str(e))
        raise SystemExit()
    finally:
        sock.close()
        rsock.close()
        dosya.close()

if __name__ =="__main__":
    if len(sys.argv)>1:
        trace_route(sys.argv[1])
    else:
        print("Hata hedef makine adı lazımdır.")