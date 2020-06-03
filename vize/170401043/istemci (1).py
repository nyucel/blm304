import socket

#Merve Öztürk
#170401043

def get_fonk(filename):
    headerlar = {}
    dosya = open(filename, "rb")

    for satir in dosya.readlines():
        if not satir.strip():
            break
        if ":" not in satir:
            continue
        header, _, deger = satir.partition(":")
        headerlar[header.strip()] = deger.strip()

    for i in headerlar():
        print(headerlar[i])
    print("\n")
    dosya.close()
    print("\n")

def put_fonk(filenames):
    filename = open(filenames, "rb")
    data = filename.read()

    while data:
        sock.send(data)
        data = filename.read()

    filename.close()
    print("Dosya gönderildi.")
    print("\n")

def listele(filenames):
    filename = open(filenames, "rb")
    dosya=filename.read()

    for satir in dosya():
        print(satir,"\n")
    print("\n")


host = input("Ip giriniz:")
port = 42

sock = socket.socket()
sock.connect((host, port))
yanit = sock.recv(1024)
yanit=yanit.decode("utf-8")

while True:
    komut = input(str("ftp@ ") + str(yanit) + " > ")
    sock.send(str.encode(komut))
    komut_ayir = komut.split(" ")
    cm = komut_ayir[0]

    try:
        filename = komut_ayir[1]
    except:
        filename = ""


    if ( cm== "get"):
        get_fonk(filename)

    elif(cm=="put"):
        put_fonk(filename)
    elif(cm=="ls"):
        listele(filename)
    else:
        print()
        sock.close()

