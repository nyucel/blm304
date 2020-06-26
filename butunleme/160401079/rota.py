import socket
import struct
import sys

###  Muhammed Yasir KAYA
###  160401079


def main():
    file = open("rota.txt", "w")
    dest_name = sys.argv[1]
    dest_addr = socket.gethostbyname(dest_name)
    port = 33434
    max_hops = 30
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    timeout_second = 1
    while True:
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

        timeout = struct.pack("ll", timeout_second, 0)

        recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)

        recv_socket.bind(("", port))

        data = bytes("hello", "utf-8")
        send_socket.sendto(data, (dest_name, port))
        curr_addr = None

        try:
            _, curr_addr = recv_socket.recvfrom(1024)
            curr_addr = curr_addr[0]
            
        except socket.error:
            file.write("*\n")
            print("*\n")

        send_socket.close()
        recv_socket.close()

        if curr_addr is not None:
            file.write(curr_addr + "\n")
            print("%s\n" % (curr_addr))

        ttl += 1
        if curr_addr == dest_addr or ttl > max_hops:
            break

    file.close()


if __name__ == "__main__":
    main()
