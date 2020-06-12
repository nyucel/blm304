#Reber Ferhat Uluca - 170401053
import socket
import os


try:
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(("", 42))
    print("Server is running...")
except:
    print("Socket error!")

sep = os.sep
server_files = os.getcwd() + os.sep + "server_files"
buffer = 1024

def GET(filename):

    if not os.path.isfile(server_files + sep + filename):
        server.sendto("File doesn't exist!".encode("utf-8"), clientAddress)
        print("File doesn't exist message sent to", clientAddress)
        return
    else:
        file_size = os.path.getsize(server_files + sep + filename)
        server.sendto(str(file_size).encode("utf-8"), clientAddress)
        f = open(server_files + sep + filename, "rb")
        print("Sending packets...")

    packets = 0
    data = f.read(buffer)

    while data:
        try:
            server.settimeout(3)
            server.sendto(data, clientAddress)
            rec = int(server.recv(buffer).decode("utf-8"))
        except socket.timeout:
            print("Couldn't sent", filename)
            print("Only", packets, "packets sent")
            print("Couldn't sent", (file_size-(packets*buffer))//buffer + 1, "packets")
            return

        if rec != packets+1:
            continue

        data = f.read(buffer)
        packets += 1

    print(packets, "packets sent")
    f.close()

def PUT(filename):
    length = int(server.recv(buffer).decode("utf-8"))

    f = open(server_files + sep + filename, "wb")
    packets = 0

    print("Receiving data...")
    while length > 0:
        packets += 1
        try:
            server.settimeout(3)
            rec = server.recv(buffer)
            server.sendto(str(packets).encode("utf-8"), clientAddress)
        except socket.timeout:
            print("Couldn't get", filename)
            print("Only", packets-1, "packets received")
            f.close()
            os.remove(server_files + sep + filename)
            return

        f.write(rec)
        length -= buffer

    print(filename, "received")
    f.close()

def LIST():
    files = os.listdir(server_files)
    length = len(files)
    server.sendto(str(length).encode("utf-8"), clientAddress)

    packets = 0
    i = 0

    print("Sending packets...")
    while length > 0:
        file_size = str(os.path.getsize(server_files + sep + files[i]))

        try:
            server.settimeout(3)
            server.sendto((files[i] + ":" + file_size).encode("utf-8"), clientAddress)
            rec = int(server.recv(buffer).decode("utf-8"))
        except socket.timeout:
            print("Couldn't sent file list to", clientAddress)
            return

        if rec != packets + 1:
            continue

        packets += 1
        i += 1
        length -= 1

    print("File list sent")

while True:
    data, clientAddress = server.recvfrom(buffer)
    if data.decode("utf-8") == "HI!":
        server.sendto("Connected".encode("utf-8"), clientAddress)
        print(clientAddress, "connected the server!")
        continue

    command = data.decode("utf-8").split(" ")

    if command[0] == "GET":
        GET(command[1])
        server.settimeout(None)

    elif command[0] == "PUT":
        PUT(command[1])
        server.settimeout(None)

    elif command[0] == "LIST":
        LIST()
        server.settimeout(None)
