#Kadir Çolak 160401037
import socket
from datetime import datetime

print('ip :', end =" ")
HOST = input()
PORT = 142
UTC = 3.0
UTCDif = 3600.0 * UTC

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        with conn:
            while True:
                data = conn.recv(32)
                if not data:
                    break
                conn.sendall(str(datetime.utcnow().timestamp() + UTCDif).encode())
        conn.close()