
#-----------İSTEMCİ---------------------
#160401024 Adem Çelik
import socket


def putt(filenaem):
    global s
    f = open(filename, "rb")
    data = f.read()

    while data:
        s.send(data)
        data = f.read()

    f.close()
    print("Dosya gönderildi.")


def gett(filename):
    global s
    data = s.recv(1024)[1:]
    print(type(data))
    print(len(data))
    dosya = open(filename, "wb")
    dosya.write(data)
    dosya.close()

def listele(filename):
    global s
    filenames = open(filename, "rb")
    dosya = filenames.read()

    for satir in dosya():
        print(satir, "\n")
    print("\n")



host =input("Sunucu IP'si 127.0.0.1\nIp giriniz : ")
port = 42

s = socket.socket()

try:
    # Bağlantıyı yap
    s.connect((host, port))

    # serverden yanıtı al
    yanit = s.recv(1024)
    print(yanit.decode("utf-8"))
    yanit=yanit.decode("utf-8")
    # bağlantıyı kapat
    s.close()
except socket.error as msg:
    print("[Server aktif değil.] Mesaj:", msg)
while True:
    komut = input(str("ftp@ ") + str(yanit) + " > ")
    s.send(str.encode(komut))
    komut_ayir = komut.split(" ")
    cm = komut_ayir[0]

    try:
        filename = komut_ayir[1]
    except:
        filename = ""

    if (cm == "get"):
        get_fonk(filename)

    elif (cm == "put"):
        put_fonk(filename)
    elif (cm == "ls"):
        listele(filename)
    else:
        print()
        s.close()



