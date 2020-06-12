import socketserver
import time
import pickle
import datetime

# 170401028 - Emir Kıvrak

class Handler_TCP_NTP_SERVER(socketserver.BaseRequestHandler):
    TIMEZONE = "UTC+2"
    def handle(self):
        T1 = datetime.datetime.now() # sunucu isteği aldığı gibi isteği aldığı zamanı kaydetti
        # self.request - TCP socketi cliente bağlı
        self.data = self.request.recv(1024).strip().decode()

        

        print("{} adresinden yollanan mesaj:".format(self.client_address[0]))

        if self.data == "TIMEREQUEST":
            self.SEND_TIME_INFORMATION(T1)

    def SEND_TIME_INFORMATION(self,T1):
        time_data = {
            "TIMEZONE": self.TIMEZONE,
            "TIME": int(round(time.time() * 1000)),
            "T1" : T1,
            "T2" : datetime.datetime.now()
        }
        self.request.sendall(pickle.dumps(time_data))


if __name__ == "__main__":
    server_ip = input("Lütfen sunucunun oluşturulacağı ip adresini giriniz")
    HOST, PORT = server_ip, 127
    

    # tcp sunucu nesnesini oluştur, ip port bind et
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCP_NTP_SERVER)
    print("Sunucu şu an ayakta ve dinliyor")
    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()
