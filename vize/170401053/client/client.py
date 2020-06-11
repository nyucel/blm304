#Reber Ferhat Uluca - 170401053
import socket
import os

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print("Socket error!")

sep = os.sep
client_files = os.getcwd() + os.sep + "client_files"
buffer = 1024

host = input("Enter the host ip address: ")
port = int(input("Enter the port number: "))

try:
    client.settimeout(1)
    client.sendto("HI!".encode("utf-8"), (host, port))
    msg = client.recv(buffer)
    print(msg.decode("utf-8") + " to the server!")
    client.settimeout(None)
except:
    print("Invalid host name or port or server is not responding!")
    quit()

def GET(filename):
    try:
        client.sendto(("GET " + filename).encode("utf-8"), (host, 42))
    except:
        return 1

    length = client.recv(buffer).decode("utf-8")

    if length == "File doesn't exist!":
        print("File doesn't exist on server!")
        return 0

    length = int(length)
    f = open(client_files + sep + filename, "wb")
    packets = 0

    print("receiving data...")
    while length > 0:
        packets += 1
        try:
            client.settimeout(3)
            rec = client.recv(buffer)
            client.sendto(str(packets).encode("utf-8"), (host, 42))
        except socket.timeout:
            f.close()
            os.remove(client_files + sep + filename)
            print("Connection to the server has been lost!")
            print("Couldn't get", filename)
            print("Only", packets-1, "packets received")
            return 1

        f.write(rec)
        length -= buffer

    print(filename, "received")
    f.close()
    return 0

def PUT(filename):

    if not os.path.isfile(client_files + sep + filename):
        print("File doesn't exist in client_files folder")
        return 0
    else:
        try:
            client.sendto(("PUT " + filename).encode("utf-8"), (host, 42))
        except:
            return 1
        file_size = os.path.getsize(client_files + sep + filename)
        client.sendto(str(file_size).encode("utf-8"), (host, 42))
        f = open(client_files + sep + filename, "rb")
        print("Sending packets..")

    packets = 0
    data = f.read(buffer)
    while data:
        try:
            client.settimeout(3)
            client.sendto(data, (host, 42))
            rec = int(client.recv(buffer).decode("utf-8"))
        except socket.timeout:
            print("Connection to the server has been lost!")
            print("Couldn't sent", filename)
            print("Only", packets, "packets sent")
            print("Couldn't sent", (file_size - (packets * buffer)) // buffer + 1, "packets")
            return 1

        if rec != packets+1:
            continue

        data = f.read(buffer)
        packets += 1

    print(filename, "sent to the server")
    f.close()
    return 0

def LIST():
    try:
        client.sendto("LIST".encode("utf-8"), (host, 42))
    except:
        return 1

    length = int(client.recv(buffer).decode("utf-8"))
    files = []
    packets = 0

    while length > 0:
        packets += 1
        try:
            client.settimeout(3)
            rec = client.recv(buffer)
            client.sendto(str(packets).encode("utf-8"), (host, 42))
        except socket.timeout:
            print("Connection to the server has been lost!")
            return 1

        files.append(rec.decode("utf-8"))
        length -= 1

    print("   Name\t\t\t\t\t   Size")
    for file in files:
        sp = file.split(":")
        file_size = int(sp[1])
        print("{:<25}{}".format(sp[0], convert_bytes(file_size)))

    return 0

def convert_bytes(size):
   for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
       if size < 1024.0:
           return "%3.1f %s" % (size, x)
       size /= 1024.0
   return size

def main():
    print("Available commands are listed below:\n  1-)GET -file_name- \n  2-)PUT -file_name-\n  3-)LIST")
    while True:
        command = input("-> ")
        com = command.split(" ")

        if com[0] == "GET":
            if GET(com[1]):
                return
            client.settimeout(None)

        elif com[0] == "PUT":
            if PUT(com[1]):
                return
            client.settimeout(None)

        elif com[0] == "LIST":
            if LIST():

                return
            client.settimeout(None)

        else:
            print("invalid command!")

if __name__ == "__main__":
    main()
